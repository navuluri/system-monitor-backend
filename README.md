# System Monitor API

A comprehensive, real-time system monitoring API built with FastAPI and psutil. This project provides RESTful endpoints to monitor CPU, memory, disk, network, processes, sensors, and system information on Linux/Unix systems.

## Features

- 🖥️ **CPU Monitoring**: Real-time CPU usage, per-core utilization, and load averages
- 💾 **Memory Tracking**: Virtual memory statistics including used, available, and cached memory
- 💿 **Disk Usage**: Storage information for all mounted partitions
- 🌐 **Network Stats**: Network interface statistics, bytes sent/received, and packet info
- 📊 **Process Information**: Detailed information about running processes
- 🌡️ **Sensor Data**: Temperature, fan speeds, and battery information (where available)
- ⚙️ **System Info**: Boot time, uptime, and logged-in users
- 📝 **PostgreSQL Integration**: Optional agent to register and update server metrics in a database

## Requirements

- Python 3.8+
- Linux/Unix-based OS (some features are platform-specific)
- PostgreSQL (optional, for the registration agent)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/navuluri/system-monitor-backend.git
   cd system-monitor-backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application:**
   ```bash
   cp config.ini.example config.ini
   ```
   
   Edit `config.ini` with your settings:
   ```ini
   [database]
   host = localhost
   port = 5432
   db = postgres
   username = your_username
   password = your_password

   [api]
   host = 0.0.0.0
   port = 8000
   log_level = info
   ```

## Usage

### Running the API Server

**Method 1: Direct Python execution**
```bash
python -m system_monitor.main
```

**Method 2: Using uvicorn directly**
```bash
uvicorn system_monitor.main:app --host 0.0.0.0 --port 8000
```

**Method 3: Using the start script (Linux/Unix)**
```bash
chmod +x start.sh
./start.sh
```

The API will be available at `http://localhost:8000`

### Running the Registration Agent (Optional)

The registration agent continuously updates server metrics to a PostgreSQL database:

```bash
python -m system_monitor.register
```

### API Documentation

Once the server is running, visit:
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### CPU
- `GET /api/v1/cpu/` - Get CPU usage statistics

### Memory
- `GET /api/v1/memory/` - Get memory usage information

### Disk
- `GET /api/v1/disk/` - Get disk usage for all partitions

### Network
- `GET /api/v1/network/` - Get network statistics summary
- `GET /api/v1/network/details` - Get detailed per-interface statistics

### Process
- `GET /api/v1/process/` - Get information about all running processes

### Sensors
- `GET /api/v1/sensors/` - Get temperature, fan, and battery information

### System
- `GET /api/v1/system/` - Get system uptime and user information

## Database Schema (Optional)

If using the registration agent, create this table in PostgreSQL:

```sql
CREATE TABLE server_info (
    ip VARCHAR(15) PRIMARY KEY,
    hostname VARCHAR(255),
    access_port INTEGER,
    cpu_percent FLOAT,
    cpu_count INTEGER,
    memory_percent FLOAT,
    memory_total FLOAT,
    disk_usage FLOAT,
    updated_on BIGINT
);
```

## Development

### Project Structure

```
system-monitor/
├── system_monitor/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration loader
│   ├── register.py          # Database registration agent
│   └── routers/
│       ├── cpu/
│       │   └── cpu.py       # CPU monitoring endpoints
│       ├── memory/
│       │   └── memory.py    # Memory monitoring endpoints
│       ├── disk/
│       │   └── disk.py      # Disk monitoring endpoints
│       ├── network/
│       │   └── network.py   # Network monitoring endpoints
│       ├── process/
│       │   └── process.py   # Process monitoring endpoints
│       ├── sensors/
│       │   └── sensors.py   # Sensor monitoring endpoints
│       └── system/
│           └── system.py    # System info endpoints
├── config.ini.example       # Example configuration file
├── requirements.txt         # Python dependencies
├── start.sh                 # Startup script for Linux/Unix
├── README.md
├── LICENSE
└── .gitignore
```

### Running Tests

```bash
pytest
```

## Platform Compatibility

- **Full Support**: Linux (Ubuntu, Debian, CentOS, RHEL, etc.)
- **Partial Support**: macOS (some sensor features may not be available)
- **Limited Support**: Windows (network and sensor features may be limited)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- System metrics powered by [psutil](https://github.com/giampaolo/psutil)

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/system-monitor/issues).

## Roadmap

- [ ] Add authentication/authorization
- [ ] WebSocket support for real-time streaming
- [ ] Docker containerization
- [ ] Prometheus metrics export
- [ ] Historical data storage and graphing
- [ ] Alert system for threshold violations
- [ ] Multi-server dashboard UI

---