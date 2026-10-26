# Linux System Monitoring & Health Observability Toolkit

![Linux System Monitor CI](https://github.com/Abhijit0810/linux-system-monitor/workflows/Linux%20System%20Monitor%20CI/badge.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Ubuntu Compatible](https://img.shields.io/badge/Ubuntu-22.04%20LTS-orange.svg)
![Tests Passing](https://img.shields.io/badge/tests-11%2F11%20passing-brightgreen.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A modular, high-performance command-line system diagnostics utility engineered by **Abhijit Uday Naik**. Designed for Linux/Ubuntu servers and high-availability systems, it profiles CPU scheduling, memory pressure, I/O wait times, process states, and active TCP/UDP network sockets in real time. It also features regex-based log streaming and threshold-based anomaly detection engines with negligible runtime overhead.

---

## Key Features

- **Hardware & Kernel Introspection:** Real-time metrics for CPU utilization (physical vs logical cores), virtual memory allocation (`used`, `available`, `cached`), partition disk utilization, and load averages (`1m`, `5m`, `15m`).
- **Network I/O & Socket Diagnostics:** Tracks total bytes sent/received, packet drops, transmission errors, and active socket connection states (`ESTABLISHED`, `LISTEN`, `TIME_WAIT`, `CLOSE_WAIT`).
- **Process Profiling:** Scans active kernel processes and dynamically extracts top CPU and memory consumers.
- **Threshold-Based Anomaly Detection:** Configurable alerts flag critical system degradation (CPU spikes, memory exhaustion, disk filling) before system outages occur.
- **Log Stream Diagnostics:** High-speed regex parsing across Linux system logs (`/var/log/syslog`, `dpkg.log`) to surface error clusters (`ERROR`, `CRITICAL`, `FAILED`).
- **Dual Output Modes:** Structured ASCII tables for human operators and JSON formats for programmatic ingestion by observability platforms (e.g., Prometheus / Datadog).
- **Automated CI/CD:** GitHub Actions workflow executing automated linting (`flake8`) and unit tests (`pytest`) with 100% pass rate.

---

## Architecture & Directory Structure

```text
linux-system-monitor/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI automated pipeline
├── scripts/
│   └── health_check.sh        # Production Bash health check launcher
├── src/
│   ├── __init__.py
│   ├── cli.py                 # Argparse CLI interface
│   ├── collector.py           # Kernel & hardware metrics collector
│   ├── log_parser.py          # High-speed regex log parser
│   └── reporter.py            # ASCII table & JSON formatter
├── tests/
│   ├── __init__.py
│   ├── test_collector.py      # Unit tests for metrics & anomaly detection
│   └── test_log_parser.py     # Unit tests for log parsing
├── .gitignore
├── LICENSE                    # MIT License
├── README.md                  # Comprehensive Documentation
├── requirements.txt           # Production dependencies
└── setup.py                   # Packaging & installation metadata
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Abhijit0810/linux-system-monitor.git
cd linux-system-monitor

# Install production dependencies
pip install -r requirements.txt

# Or install locally in editable mode
pip install -e .
```

---

## Usage

### 1. Complete System Health Inspection (Table Format)
```bash
python -m src.cli --all
```

### 2. Network Sockets & Process Inspection
```bash
python -m src.cli --network --processes
```

### 3. Anomaly Alerting with Custom Thresholds
```bash
python -m src.cli --alert --cpu-threshold 80 --mem-threshold 85
```

### 4. Structured JSON Output (For Automation & Observability)
```bash
python -m src.cli --all --format json --output report.json
```

### 5. System Log Parsing
```bash
python -m src.cli --logs /var/log/syslog --format table
```

---

## Running the Automated Test Suite

```bash
# Run pytest with verbosity
pytest -v tests/
```

All 11 unit tests execute in under 15 seconds with a 100% pass rate.

---

## Author

**Abhijit Uday Naik**  
- **Email:** [naikabhi081004@gmail.com](mailto:naikabhi081004@gmail.com)  
- **LinkedIn:** [linkedin.com/in/abhijit-naik-20168b347](https://www.linkedin.com/in/abhijit-naik-20168b347/)  
- **GitHub:** [github.com/Abhijit0810](https://github.com/Abhijit0810)  
- **Portfolio:** [mellifluous-biscuit-b2608f.netlify.app](https://mellifluous-biscuit-b2608f.netlify.app/)

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
