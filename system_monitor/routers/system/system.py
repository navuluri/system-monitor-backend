"""System information endpoints"""

import time
import platform

import psutil
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/system",
    tags=["System"],
)


@router.get("/")
async def get_system_info():
    """
    Get system information including uptime and logged-in users.
    
    Returns:
        - boot_time_timestamp: Unix timestamp of system boot time
        - uptime_days: Number of days since system boot
        - uptime_seconds: Number of seconds since system boot
        - platform: Operating system information
        - users: List of currently logged-in users
    """
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    uptime_days = round(uptime_seconds / 86400, 2)
    
    users = psutil.users()
    return {
        "boot_time_timestamp": int(boot_time),
        "uptime_days": uptime_days,
        "uptime_seconds": uptime_seconds,
        "platform": platform.system(),
        "platform_release": platform.release(),
        "users": [
            {
                "name": user.name,
                "terminal": user.terminal,
                "host": user.host,
                "started": user.started,
                "pid": user.pid
            }
            for user in users
        ]
    }

