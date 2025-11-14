# System Monitor API - Quick Start Guide

## Quick Installation

```bash
# Clone the repository
git clone https://github.com/navuluri/system-monitor-backend.git
cd system-monitor-backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create configuration
cp config.ini.example config.ini
# Edit config.ini with your settings

# Run the API
python -m system_monitor.main
```

Visit http://localhost:8000/docs for API documentation.

## Docker Quick Start

```bash
# Using Docker Compose (includes PostgreSQL)
docker-compose up -d

# Or build and run standalone
docker build -t system-monitor .
docker run -p 8000:8000 -v $(pwd)/config.ini:/app/config.ini system-monitor
```

## API Endpoints

- `/` - API information
- `/health` - Health check
- `/docs` - Interactive API documentation
- `/api/v1/cpu/` - CPU metrics
- `/api/v1/memory/` - Memory metrics
- `/api/v1/disk/` - Disk metrics
- `/api/v1/network/` - Network metrics
- `/api/v1/process/` - Process information
- `/api/v1/sensors/` - Sensor data
- `/api/v1/system/` - System information

## Configuration

Edit `config.ini`:

```ini
[api]
host = 0.0.0.0
port = 8000
log_level = info

[database]  # Optional, for registration agent
host = localhost
port = 5432
db = postgres
username = postgres
password = your_password
```

## Running the Registration Agent

```bash
# Setup database first
psql -U postgres -f schema.sql

# Run the agent
python -m system_monitor.register
```

For more details, see [README.md](README.md).

