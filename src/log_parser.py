import os
import re

class LogParser:
    """Parses system log files for critical error keywords and status patterns."""

    def __init__(self, log_path):
        self.log_path = log_path

    def parse_log_summary(self):
        if not os.path.exists(self.log_path):
            return {"error": f"Log file not found: {self.log_path}"}

        counts = {"ERROR": 0, "WARNING": 0, "CRITICAL": 0, "FAILED": 0, "INFO": 0}
        recent_matches = []

        try:
            with open(self.log_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line_str = line.strip()
                    matched_keys = set()
                    for key in counts:
                        if re.search(r'\b' + key + r'\b', line_str, re.IGNORECASE):
                            counts[key] += 1
                            matched_keys.add(key)
                    if matched_keys.intersection({"ERROR", "CRITICAL", "FAILED"}) and len(recent_matches) < 5:
                        recent_matches.append(line_str)
            return {
                "file": self.log_path,
                "counts": counts,
                "critical_sample": recent_matches
            }
        except Exception as e:
            return {"error": f"Failed to read log file: {str(e)}"}
