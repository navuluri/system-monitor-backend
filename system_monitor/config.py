"""Configuration management for System Monitor API"""

import configparser
import os
from pathlib import Path

# Get the project root directory (parent of system_monitor)
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / 'config.ini'

config_parser = configparser.ConfigParser()

# Load configuration file
if CONFIG_PATH.exists():
    config_parser.read(CONFIG_PATH)
else:
    print(f"Warning: Configuration file not found at {CONFIG_PATH}")
    print("Please create config.ini from config.ini.example")


def get(section: str, key: str, default: str = None) -> str:
    """
    Get a configuration value from the config file.
    
    Args:
        section: The configuration section name
        key: The configuration key name
        default: Default value if key is not found
        
    Returns:
        The configuration value as a string, or default if not found
    """
    try:
        return config_parser[section].get(key, default)
    except (KeyError, configparser.NoSectionError):
        if default is not None:
            return default
        raise ValueError(f"Configuration key '{key}' not found in section '{section}'")
