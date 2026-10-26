import argparse
import sys
from src.collector import SystemCollector
from src.log_parser import LogParser
from src.reporter import Reporter

def build_parser():
    parser = argparse.ArgumentParser(
        description="Linux System Monitoring & Health Observability Utility - Abhijit Naik Portfolio"
    )
    parser.add_argument("--cpu", action="store_true", help="Collect CPU usage metrics")
    parser.add_argument("--memory", action="store_true", help="Collect RAM / memory metrics")
    parser.add_argument("--disk", action="store_true", help="Collect disk partition metrics")
    parser.add_argument("--load", action="store_true", help="Collect system load averages")
    parser.add_argument("--network", action="store_true", help="Collect network throughput and socket states")
    parser.add_argument("--processes", action="store_true", help="Collect top resource-consuming processes")
    parser.add_argument("--alert", action="store_true", help="Run anomaly checks against thresholds")
    parser.add_argument("--cpu-threshold", type=float, default=85.0, help="CPU alert threshold percent (default: 85)")
    parser.add_argument("--mem-threshold", type=float, default=90.0, help="Memory alert threshold percent (default: 90)")
    parser.add_argument("--logs", type=str, help="Path to system log file to parse (e.g. /var/log/syslog)")
    parser.add_argument("--all", action="store_true", help="Collect all system metrics and inspect health")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format (table or json)")
    parser.add_argument("--output", type=str, help="File path to save the generated report")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    collector = SystemCollector()
    metrics = {}

    has_specific_flag = (args.cpu or args.memory or args.disk or args.load or 
                          args.network or args.processes or args.alert or args.logs)

    if args.all or not has_specific_flag:
        metrics.update(collector.get_all_metrics())
    else:
        metrics["system_info"] = collector.get_system_info()
        if args.cpu:
            metrics["cpu"] = collector.get_cpu_metrics()
        if args.memory:
            metrics["memory"] = collector.get_memory_metrics()
        if args.disk:
            metrics["disk"] = collector.get_disk_metrics()
        if args.load:
            metrics["load_average"] = collector.get_load_average()
        if args.network:
            metrics["network"] = collector.get_network_metrics()
        if args.processes:
            metrics["top_processes"] = collector.get_top_processes(limit=5)
        if args.alert:
            metrics["anomalies"] = collector.check_anomalies(
                cpu_thresh=args.cpu_threshold,
                mem_thresh=args.mem_threshold
            )

    if args.logs:
        parser_obj = LogParser(args.logs)
        metrics["log_summary"] = parser_obj.parse_log_summary()

    reporter = Reporter(metrics)
    output_str = reporter.generate(format_type=args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"[+] System metrics report successfully written to {args.output}")
    else:
        print(output_str)

    sys.exit(0)

if __name__ == "__main__":
    main()
