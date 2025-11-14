"""CPU monitoring endpoints"""

import psutil
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/cpu",
    tags=["CPU"],
)


@router.get("/")
async def get_cpu_usage():
    """
    Get comprehensive CPU usage statistics.
    
    Returns:
        - physical_cpu_count: Number of physical CPU cores
        - cpu_utilization: Overall CPU usage percentage
        - per_cpu_utilization: Usage percentage for each CPU core
        - load_avg: System load average (1min, 5min, 15min) as percentages
    """
    try:
        cpu_avg = [round(x / psutil.cpu_count() * 100, 2) for x in psutil.getloadavg()]
    except (AttributeError, OSError):
        # getloadavg() not available on Windows
        cpu_avg = [0.0, 0.0, 0.0]
    
    return {
        "physical_cpu_count": psutil.cpu_count(logical=False),
        "cpu_utilization": psutil.cpu_percent(interval=1),
        "per_cpu_utilization": psutil.cpu_percent(interval=1, percpu=True),
        "load_avg": cpu_avg
    }
