"""Setup configuration for System Monitor API"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="system-monitor-api",
    version="1.0.0",
    author="Your Name",
    author_email="bhaskara[dot]navuluri[at]gmail[dot]com",
    description="A comprehensive system monitoring API built with FastAPI and psutil",
    long_description_content_type="text/markdown",
    url="https://github.com/navuluri/system-monitor-backend",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.116.0",
        "uvicorn>=0.35.0",
        "psutil>=7.0.0",
        "psycopg2-binary>=2.9.10",
        "pydantic>=2.11.0",
    ],
    entry_points={
        "console_scripts": [
            "system-monitor=system_monitor.main:main",
            "system-monitor-register=system_monitor.register:register",
        ],
    },
    keywords="system monitoring api fastapi psutil metrics",
    project_urls={
        "Bug Reports": "https://github.com/navuluri/system-monitor-backend/issues",
        "Source": "https://github.com/navuluri/system-monitor-backend",
        "Documentation": "https://github.com/navuluri/system-monitor-backend#readme",
    },
)

