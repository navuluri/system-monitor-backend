"""Memory monitoring endpoints"""

import psutil
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/memory",
    tags=["Memory"],
)


@router.get("/")
async def get_memory_usage():
    """
    Get comprehensive virtual memory usage statistics.
    
    Returns detailed memory information including total, available, used, free,
    and platform-specific metrics like active, inactive, buffers, cached, etc.
    """
    memory = psutil.virtual_memory()
    return {
        "total": f"{memory.total / (1024 ** 3):.2f} GB",
        "available": f"{memory.available / (1024 ** 3):.2f} GB",
        "used": f"{memory.used / (1024 ** 3):.2f} GB",
        "free": f"{memory.free / (1024 ** 3):.2f} GB",
        "percent": f"{memory.percent}%",
        "active": f"{memory.active / (1024 ** 3):.2f} GB" if hasattr(memory, "active") else "NA",
        "inactive": f"{memory.inactive / (1024 ** 3):.2f} GB" if hasattr(memory, "inactive") else "NA",
        "buffers": f"{memory.buffers / (1024 ** 3):.2f} GB" if hasattr(memory, "buffers") else "NA",
        "cached": f"{memory.cached / (1024 ** 3):.2f} GB" if hasattr(memory, "cached") else "NA",
        "shared": f"{memory.shared / (1024 ** 3):.2f} GB" if hasattr(memory, "shared") else "NA",
        "slab": f"{memory.slab / (1024 ** 3):.2f} GB" if hasattr(memory, "slab") else "NA"
    }
