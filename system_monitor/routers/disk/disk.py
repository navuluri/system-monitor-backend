import psutil
import os
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/disk",  # all routes here start with /api/v1/disk
    tags=["Disk"],  # useful for docs grouping
)


def get_size(bytes, suffix="B"):
    """Convert bytes to human-readable format (GB, MB, etc.)"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor


@router.get("/")
async def get_disk_usage():
    """
    Get disk usage statistics for all mounted partitions.
    
    Returns:
        - total: Total disk space across all partitions
        - used: Total used space
        - free: Total free space
        - used_percent: Percentage of disk space used
        - free_percent: Percentage of disk space free
        - partitions: Detailed information for each partition
    """
    total = used = free = 0
    partitions_info = []

    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue  # skip restricted partitions

        total += usage.total
        used += usage.used
        free += usage.free

        used_percent = (usage.used / usage.total) * 100
        free_percent = 100 - used_percent

        partitions_info.append({
            "device": partition.device,
            "total": get_size(usage.total),
            "used": get_size(usage.used),
            "free": get_size(usage.free),
            "used_percent": f"{used_percent:.2f}%",
            "free_percent": f"{free_percent:.2f}%",
            "fstype": partition.fstype,
            "mountpoint": partition.mountpoint
        })

    total = used = free = 0
    for partition in partitions_info:
        size = psutil.disk_usage(partition["mountpoint"])
        total += size.total
        used += size.used
        free += size.free

    return {
        "total": get_size(total),
        "used": get_size(used),
        "free": get_size(free),
        "used_percent": f"{(used / total * 100):.2f}%" if total else "0.00%",
        "free_percent": f"{(free / total * 100):.2f}%" if total else "0.00%",
        "partitions": partitions_info
    }