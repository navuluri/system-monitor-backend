"""Sensor monitoring endpoints"""

import psutil
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/sensors",
    tags=["Sensors"],
)


@router.get("/")
async def get_sensors_data():
    """
    Get sensor data including temperatures, fan speeds, and battery information.
    
    Note: Availability of sensor data depends on the platform and hardware.
    Some features may not be available on all systems.
    
    Returns:
        - temperatures: Temperature sensors by device
        - fans: Fan speed sensors by device
        - battery: Battery information (if available)
    """
    sensors_info = {}
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        sensors_info["temperatures"] = {
            k: [{"label": entry.label, "current": entry.current, "high": entry.high, "critical": entry.critical} for
                entry in v] for k, v in temps.items()}
    else:
        sensors_info["temperatures"] = "Not supported on this platform"

    if hasattr(psutil, "sensors_fans"):
        fans = psutil.sensors_fans()
        sensors_info["fans"] = {k: [{"label": entry.label, "current": entry.current} for entry in v] for k, v in
                                fans.items()}
    else:
        sensors_info["fans"] = "Not supported on this platform"

    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            sensors_info["battery"] = {
                "percent": battery.percent,
                "secsleft": battery.secsleft,
                "power_plugged": battery.power_plugged
            }
        else:
            sensors_info["battery"] = "No battery information available"
    else:
        sensors_info["battery"] = "Not supported on this platform"

    return sensors_info
