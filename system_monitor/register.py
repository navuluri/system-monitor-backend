"""
Database Registration Agent

Continuously monitors and registers system metrics to a PostgreSQL database.
This allows centralized tracking of multiple system monitors.
"""

import time
import socket
import platform
import sys
from typing import Optional

import psycopg2
from psycopg2 import OperationalError, DatabaseError

import system_monitor.config as config
import psutil

# Prime the CPU measurement
psutil.cpu_percent(interval=1)

# Database connection variables
conn: Optional[psycopg2.extensions.connection] = None
cursor: Optional[psycopg2.extensions.cursor] = None

# SQL query for inserting/updating server information
sql_insert = """
             INSERT INTO server_info(ip, hostname, access_port, cpu_percent, cpu_count, memory_percent, memory_total,
                                     disk_usage, updated_on)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
             ON CONFLICT(ip) DO UPDATE SET 
                                           hostname=%s,
                                           access_port=%s,
                                           cpu_percent=%s,
                                           cpu_count=%s,
                                           memory_percent=%s,
                                           memory_total=%s,
                                           disk_usage=%s,
                                           updated_on=%s
             """

register_flag = False


def get_ip_address() -> str:
    """
    Get the local IP address of the machine.

    Returns:
        IP address as a string
    """
    try:
        # Works on Linux/Unix
        if platform.system() != "Windows":
            import subprocess
            result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
            ip_address = result.stdout.strip().split()[0]
            return ip_address
    except Exception:
        pass

    # Fallback method that works on all platforms
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "127.0.0.1"


def get_hostname() -> str:
    """
    Get the hostname of the machine.

    Returns:
        Hostname as a string
    """
    return socket.gethostname()


def connect_to_database():
    """
    Establish connection to PostgreSQL database.

    Returns:
        True if connection successful, False otherwise
    """
    global conn, cursor

    try:
        host = config.get("database", "host")
        port = config.get("database", "port")
        username = config.get("database", "username")
        password = config.get("database", "password")
        database = config.get("database", "db")

        conn = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=host,
            port=int(port)
        )
        cursor = conn.cursor()
        print(f"Successfully connected to database at {host}:{port}")
        return True
    except (OperationalError, DatabaseError, ValueError) as e:
        print(f"Error connecting to database: {e}")
        print("Please check your database configuration in config.ini")
        return False
    except Exception as e:
        print(f"Unexpected error connecting to database: {e}")
        return False


def total_disk_usage_percent() -> float:
    """
    Calculate the total disk usage percentage across all partitions.

    Returns:
        Total disk usage percentage as a float
    """
    total = used = free = 0
    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue  # skip restricted partitions

        total += usage.total
        used += usage.used
        free += usage.free

    return (used / total) * 100 if total else 0.00


def register():
    """
    Main registration loop that continuously updates system metrics to the database.
    """
    global register_flag, conn, cursor

    if not connect_to_database():
        print("Failed to connect to database. Exiting.")
        sys.exit(1)

    ip_address = get_ip_address()
    host_name = get_hostname()
    access_port = config.get("api", "port", "8000")

    print(f"Starting registration agent for {ip_address}:{access_port}")
    print(f"Hostname: {host_name}")

    # Prime CPU measurement
    psutil.cpu_percent(interval=1)

    while True:
        try:
            virtual_memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            disk_percent = round(total_disk_usage_percent(), 2)
            timestamp = int(time.time() * 1000)

            cursor.execute(sql_insert,
                           (ip_address,
                            host_name,
                            access_port,
                            cpu_percent,
                            psutil.cpu_count(logical=False),
                            virtual_memory.percent,
                            virtual_memory.total / 1024 ** 3,
                            disk_percent,
                            timestamp,
                            host_name,
                            access_port,
                            cpu_percent,
                            psutil.cpu_count(logical=False),
                            virtual_memory.percent,
                            virtual_memory.total / 1024 ** 3,
                            disk_percent,
                            timestamp
                            ))
            conn.commit()

            if not register_flag:
                print(f"Successfully registered {ip_address}:{access_port} to database")
                register_flag = True

            time.sleep(1)

        except (OperationalError, DatabaseError) as e:
            print(f"Database error: {e}")
            print("Attempting to reconnect...")
            if connect_to_database():
                print("Reconnected successfully")
            else:
                print("Reconnection failed. Retrying in 5 seconds...")
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nShutting down registration agent...")
            if conn:
                conn.close()
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    register()

