"""
System Monitor API - Main application entry point

A comprehensive FastAPI-based system monitoring solution providing real-time metrics
for CPU, memory, disk, network, processes, sensors, and system information.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from system_monitor.routers.cpu import cpu
from system_monitor.routers.memory import memory
from system_monitor.routers.disk import disk
from system_monitor.routers.network import network
from system_monitor.routers.sensors import sensors
from system_monitor.routers.system import system
from system_monitor.routers.process import process
import system_monitor.config as config
from system_monitor import __version__

app = FastAPI(
    title="System Monitor API",
    description="A comprehensive system monitoring API providing real-time metrics",
    version=__version__,
    contact={
        "name": "System Monitor Project",
        "url": "https://github.com/yourusername/system-monitor",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Register routers
app.include_router(cpu.router)
app.include_router(memory.router)
app.include_router(disk.router)
app.include_router(network.router)
app.include_router(sensors.router)
app.include_router(system.router)
app.include_router(process.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "System Monitor API",
        "version": __version__,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration with defaults
    host = config.get("api", "host", "0.0.0.0")
    port = int(config.get("api", "port", "8000"))
    log_level = config.get("api", "log_level", "info")
    
    print(f"Starting System Monitor API v{__version__}")
    print(f"Server running on http://{host}:{port}")
    print(f"Documentation available at http://{host}:{port}/docs")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=log_level
    )

