import json

class Reporter:
    """Formats system metrics into ASCII tables or JSON reports."""

    def __init__(self, metrics_data):
        self.data = metrics_data

    def generate(self, format_type="table"):
        if format_type == "json":
            return json.dumps(self.data, indent=2)

        lines = [
            "==================================================================",
            "        LINUX SYSTEM MONITORING & HEALTH OBSERVABILITY REPORT     ",
            "=================================================================="
        ]

        if "system_info" in self.data:
            s = self.data["system_info"]
            lines.append(f"Host OS: {s.get('os')} ({s.get('architecture')}) | Kernel: {s.get('os_release')} | Python: {s.get('python_version')}")
            lines.append(f"Report Generated: {s.get('timestamp')}")
            lines.append("------------------------------------------------------------------")

        if "anomalies" in self.data and self.data["anomalies"]:
            lines.append("\n[!] INFRASTRUCTURE ALERTS DETECTED:")
            for alert in self.data["anomalies"]:
                lines.append(f"  * [{alert['severity']}] {alert['component']}: {alert['message']}")
            lines.append("------------------------------------------------------------------")

        if "cpu" in self.data:
            c = self.data["cpu"]
            lines.append(f"CPU Utilization: {c.get('cpu_utilization_percent')}%  (Cores: {c.get('physical_cores')} Physical, {c.get('logical_cores')} Logical)")

        if "memory" in self.data:
            m = self.data["memory"]
            lines.append(f"Memory (RAM):    {m.get('used_mb')} MB used / {m.get('total_mb')} MB total ({m.get('percent_used')}%) | Free: {m.get('available_mb')} MB")

        if "load_average" in self.data:
            l = self.data["load_average"]
            lines.append(f"Load Average:    1m={l.get('1min')}, 5m={l.get('5min')}, 15m={l.get('15min')}")

        if "network" in self.data:
            net = self.data["network"]
            lines.append(f"Network I/O:     Sent: {net.get('bytes_sent_mb')} MB ({net.get('packets_sent')} pkts) | Recv: {net.get('bytes_recv_mb')} MB ({net.get('packets_recv')} pkts)")
            if "total_open_sockets" in net:
                states_summary = ", ".join([f"{k}: {v}" for k, v in net.get("socket_states", {}).items()])
                lines.append(f"Active Sockets:  Total: {net.get('total_open_sockets')} [{states_summary}]")

        if "disk" in self.data:
            lines.append("\nMounted Partitions:")
            for d in self.data["disk"]:
                lines.append(f"  - {d.get('mountpoint')} ({d.get('fstype')}): {d.get('used_gb')} GB / {d.get('total_gb')} GB ({d.get('percent')}%) [Free: {d.get('free_gb')} GB]")

        if "top_processes" in self.data and self.data["top_processes"]:
            lines.append("\nTop Active Processes:")
            lines.append(f"  {'PID':<8} {'NAME':<24} {'STATUS':<12} {'CPU%':<8} {'MEM%'}")
            lines.append("  " + "-" * 58)
            for p in self.data["top_processes"]:
                lines.append(f"  {p['pid']:<8} {p['name'][:22]:<24} {p['status'][:10]:<12} {p['cpu_percent']:<8} {p['memory_percent']}%")

        if "log_summary" in self.data:
            ls = self.data["log_summary"]
            lines.append("\nLog Stream Diagnostics:")
            if "counts" in ls:
                counts_str = ", ".join([f"{k}:{v}" for k, v in ls["counts"].items()])
                lines.append(f"  - Match Summary: {counts_str}")
            if "error" in ls:
                lines.append(f"  - Error Status: {ls['error']}")

        lines.append("==================================================================")
        return "\n".join(lines)
