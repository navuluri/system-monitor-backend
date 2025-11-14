-- Database schema for System Monitor registration agent
-- This creates the necessary table for tracking multiple system monitors

CREATE TABLE IF NOT EXISTS server_info (
    ip VARCHAR(15) PRIMARY KEY,
    hostname VARCHAR(255) NOT NULL,
    access_port INTEGER NOT NULL,
    cpu_percent FLOAT,
    cpu_count INTEGER,
    memory_percent FLOAT,
    memory_total FLOAT,
    disk_usage FLOAT,
    updated_on BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_cpu_percent CHECK (cpu_percent >= 0 AND cpu_percent <= 100),
    CONSTRAINT valid_memory_percent CHECK (memory_percent >= 0 AND memory_percent <= 100),
    CONSTRAINT valid_disk_usage CHECK (disk_usage >= 0 AND disk_usage <= 100)
);

-- Create an index on updated_on for faster queries
CREATE INDEX IF NOT EXISTS idx_server_info_updated_on ON server_info(updated_on);

-- Create an index on hostname for faster lookups
CREATE INDEX IF NOT EXISTS idx_server_info_hostname ON server_info(hostname);

-- Example query to get all servers updated in the last 5 minutes
-- SELECT * FROM server_info WHERE updated_on > (EXTRACT(EPOCH FROM NOW()) * 1000) - 300000;

-- Example query to get servers with high CPU usage
-- SELECT * FROM server_info WHERE cpu_percent > 80 ORDER BY cpu_percent DESC;

