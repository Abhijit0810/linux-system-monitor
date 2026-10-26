import pytest
from src.collector import SystemCollector
from src.reporter import Reporter

def test_collector_system_info():
    collector = SystemCollector()
    info = collector.get_system_info()
    assert "os" in info
    assert "architecture" in info
    assert "timestamp" in info

def test_collector_cpu_metrics():
    collector = SystemCollector()
    cpu = collector.get_cpu_metrics()
    assert cpu["logical_cores"] >= 1
    assert cpu["physical_cores"] >= 1
    assert 0.0 <= cpu["cpu_utilization_percent"] <= 100.0

def test_collector_memory_metrics():
    collector = SystemCollector()
    mem = collector.get_memory_metrics()
    assert mem["total_mb"] > 0
    assert 0.0 <= mem["percent_used"] <= 100.0

def test_collector_disk_metrics():
    collector = SystemCollector()
    disk = collector.get_disk_metrics()
    assert isinstance(disk, list)

def test_collector_network_metrics():
    collector = SystemCollector()
    net = collector.get_network_metrics()
    assert "bytes_sent_mb" in net
    assert "bytes_recv_mb" in net
    assert "socket_states" in net

def test_collector_top_processes():
    collector = SystemCollector()
    procs = collector.get_top_processes(limit=3)
    assert isinstance(procs, list)
    if procs:
        p = procs[0]
        assert "pid" in p
        assert "name" in p

def test_collector_anomalies():
    collector = SystemCollector()
    alerts = collector.check_anomalies(cpu_thresh=0.0)  # guaranteed to trigger if CPU >= 0
    assert isinstance(alerts, list)
    assert len(alerts) >= 1
    assert alerts[0]["component"] == "CPU"

def test_collector_all_metrics():
    collector = SystemCollector()
    all_data = collector.get_all_metrics()
    assert "system_info" in all_data
    assert "cpu" in all_data
    assert "memory" in all_data
    assert "disk" in all_data
    assert "network" in all_data
    assert "top_processes" in all_data
    assert "anomalies" in all_data

def test_reporter_generation():
    collector = SystemCollector()
    data = collector.get_all_metrics()
    reporter = Reporter(data)
    table_out = reporter.generate("table")
    json_out = reporter.generate("json")
    assert "LINUX SYSTEM MONITORING" in table_out
    assert "system_info" in json_out
