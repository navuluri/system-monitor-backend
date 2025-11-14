"""Process monitoring endpoints"""

import psutil
from fastapi import APIRouter
from psutil._common import bytes2human

router = APIRouter(
    prefix="/api/v1/process",
    tags=["Process"],
)


@router.get("/")
async def get_system_info():
    """
    Get information about all running processes.
    
    Returns:
        List of process information including PID, name, CPU usage, memory usage,
        I/O statistics, and network connections
    """
    return get_all_processes()


def get_all_processes() -> list:
    """
    Retrieve detailed information for all running processes.
    
    Returns:
        List of dictionaries containing process information
    """
    process_list = []

    for proc in psutil.process_iter(attrs=[
        "pid", "name", "username", "status", "cpu_percent",
        "memory_percent", "memory_info", "create_time", "exe", "io_counters", "num_threads"
    ]):
        try:
            process_info = proc.info

            # Handle zombie process
            if process_info.get("status") == psutil.STATUS_ZOMBIE:
                process_info["is_zombie"] = True
                process_info["connections"] = []# zombies won’t have active sockets
                process_info["read"] = 0,
                process_info["write"] = 0
                process_list.append(process_info)
                continue

            # Convert memory_info to human-readable
            mem_info = process_info.pop("memory_info", None)
            if mem_info:
                process_info["rss"] = f"{bytes2human(mem_info.rss)}"
                process_info["vms"] = f"{bytes2human(mem_info.vms)}"

            # Convert io_info to human-readable
            io_info = process_info.pop("io_counters", None)
            if io_info:
                process_info["read"] = f"{bytes2human(io_info.read_bytes)}"
                process_info["write"] = f"{bytes2human(io_info.write_bytes)}"

            process_info["connections"] = len(proc.net_connections())
            process_info["is_zombie"] = False
            process_list.append(process_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        except psutil.ZombieProcess:  # fallback just in case
            process_list.append({
                "pid": proc.pid,
                "name": proc.name(),
                "status": "zombie",
                "is_zombie": True,
                "connections": [],
                "read":0,
                "write":0
            })

    return process_list
