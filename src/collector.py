import os
import platform
import psutil
from datetime import datetime

class SystemCollector:
    """High-performance Linux & POSIX system metrics collector."""

    def get_system_info(self):
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def get_cpu_metrics(self):
        return {
            "physical_cores": psutil.cpu_count(logical=False) or 1,
            "logical_cores": psutil.cpu_count(logical=True) or 1,
            "cpu_utilization_percent": psutil.cpu_percent(interval=0.1)
        }

    def get_memory_metrics(self):
        mem = psutil.virtual_memory()
        return {
            "total_mb": round(mem.total / (1024 * 1024), 2),
            "available_mb": round(mem.available / (1024 * 1024), 2),
            "used_mb": round(mem.used / (1024 * 1024), 2),
            "percent_used": mem.percent
        }

    def get_disk_metrics(self):
        partitions = psutil.disk_partitions()
        disk_data = []
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                disk_data.append({
                    "device": p.device,
                    "mountpoint": p.mountpoint,
                    "fstype": p.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": usage.percent
                })
            except (PermissionError, FileNotFoundError):
                continue
        return disk_data

    def get_load_average(self):
        if hasattr(os, "getloadavg"):
            load1, load5, load15 = os.getloadavg()
            return {"1min": round(load1, 2), "5min": round(load5, 2), "15min": round(load15, 2)}
        return {"1min": 0.0, "5min": 0.0, "15min": 0.0}

    def get_network_metrics(self):
        """Collects network I/O throughput and socket state summaries."""
        net_io = psutil.net_io_counters()
        metrics = {
            "bytes_sent_mb": round(net_io.bytes_sent / (1024 * 1024), 2),
            "bytes_recv_mb": round(net_io.bytes_recv / (1024 * 1024), 2),
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "errin": net_io.errin,
            "errout": net_io.errout,
            "dropin": net_io.dropin,
            "dropout": net_io.dropout,
            "socket_states": {}
        }

        try:
            connections = psutil.net_connections(kind="inet")
            states = {}
            for conn in connections:
                status = conn.status
                states[status] = states.get(status, 0) + 1
            metrics["socket_states"] = states
            metrics["total_open_sockets"] = len(connections)
        except (psutil.AccessDenied, PermissionError):
            metrics["socket_states"] = {"ACCESS_DENIED": 1}
            metrics["total_open_sockets"] = 0

        return metrics

    def get_top_processes(self, limit=5):
        """Inspects running processes and returns the top resource consumers."""
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
            try:
                info = p.info
                procs.append({
                    "pid": info['pid'],
                    "name": info['name'] or "unknown",
                    "status": info['status'] or "unknown",
                    "cpu_percent": round(info['cpu_percent'] or 0.0, 1),
                    "memory_percent": round(info['memory_percent'] or 0.0, 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sort primarily by CPU and secondarily by Memory
        procs.sort(key=lambda x: (x["cpu_percent"], x["memory_percent"]), reverse=True)
        return procs[:limit]

    def check_anomalies(self, cpu_thresh=85.0, mem_thresh=90.0, disk_thresh=90.0):
        """Evaluates operational thresholds and flags infrastructure anomalies."""
        alerts = []
        cpu = self.get_cpu_metrics()["cpu_utilization_percent"]
        if cpu >= cpu_thresh:
            alerts.append({
                "component": "CPU",
                "severity": "WARNING",
                "value": cpu,
                "threshold": cpu_thresh,
                "message": f"High CPU utilization detected: {cpu}% >= {cpu_thresh}%"
            })

        mem = self.get_memory_metrics()["percent_used"]
        if mem >= mem_thresh:
            alerts.append({
                "component": "MEMORY",
                "severity": "CRITICAL",
                "value": mem,
                "threshold": mem_thresh,
                "message": f"High RAM consumption detected: {mem}% >= {mem_thresh}%"
            })

        for d in self.get_disk_metrics():
            if d["percent"] >= disk_thresh:
                alerts.append({
                    "component": f"DISK ({d['mountpoint']})",
                    "severity": "WARNING",
                    "value": d["percent"],
                    "threshold": disk_thresh,
                    "message": f"Partition {d['mountpoint']} space nearly exhausted: {d['percent']}% >= {disk_thresh}%"
                })

        return alerts

    def get_all_metrics(self):
        return {
            "system_info": self.get_system_info(),
            "cpu": self.get_cpu_metrics(),
            "memory": self.get_memory_metrics(),
            "disk": self.get_disk_metrics(),
            "load_average": self.get_load_average(),
            "network": self.get_network_metrics(),
            "top_processes": self.get_top_processes(limit=5),
            "anomalies": self.check_anomalies()
        }
