import json

import psutil
from fastapi import APIRouter
from psutil._common import bytes2human

router = APIRouter(
    prefix="/api/v1/network",  # all routes here start with /api/v1/network
    tags=["Network"],  # useful for docs grouping
)


def get_interfaces():
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    output_format = "%(value).2f%(symbol)s"
    nic_data = []
    for nic, addrs in psutil.net_if_addrs().items():
        nic_info = {"nic": nic, "bytes_sent": 0, "bytes_received": 0, "packets_sent": 0, "packets_received": 0}
        if nic in io_counters:
            io = io_counters[nic]
            nic_info["stats"] = stats[nic]._asdict() if nic in stats else {}
            nic_info["bytes_sent"] = bytes2human(io.bytes_sent, format=output_format)
            nic_info["bytes_received"] = bytes2human(io.bytes_recv, format=output_format)
            nic_info["packets_sent"] = io.packets_sent
            nic_info["packets_received"] = io.packets_recv
            nic_data.append(nic_info)
    return nic_data


@router.get("/details")
async def get_network_usage_details():
    net_io = psutil.net_io_counters(pernic=True)
    network_info = []
    for interface, stats in net_io.items():
        network_info.append({
            "interface": interface,
            "bytes_sent": f"{bytes2human(stats.bytes_sent)}",
            "bytes_recv": f"{bytes2human(stats.bytes_recv)}",
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv,
            "errin": net_io.errin,
            "errout": net_io.errout,
            "dropin": net_io.dropin,
            "dropout": net_io.dropout,
        })
    return network_info


@router.get("/")
async def get_network_usage():
    """
    Get comprehensive network usage statistics.
    
    Returns:
        - bytes_sent: Total bytes sent across all interfaces
        - bytes_recv: Total bytes received
        - packets_sent: Total packets sent
        - packets_recv: Total packets received
        - num_sockets: Number of active network connections
        - num_interfaces: Number of network interfaces
        - interfaces: Detailed per-interface statistics
    """
    net_io = psutil.net_io_counters(pernic=False)
    return {
        "bytes_sent": f"{bytes2human(net_io.bytes_sent)}",
        "bytes_recv": f"{bytes2human(net_io.bytes_recv)}",
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
        "num_sockets": len(psutil.net_connections()),
        "num_interfaces": len(psutil.net_if_addrs()),
        "errin": net_io.errin if hasattr(net_io, 'errin') else 0,
        "errout": net_io.errout if hasattr(net_io, 'errout') else 0,
        "interfaces": get_interfaces()
    }

