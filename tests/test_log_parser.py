import os
import pytest
from src.log_parser import LogParser

def test_log_parser_nonexistent(tmp_path):
    parser = LogParser(str(tmp_path / "nonexistent.log"))
    res = parser.parse_log_summary()
    assert "error" in res

def test_log_parser_valid_log(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("INFO Service started\nERROR Failed to bind port 8080\nWARNING Memory high\nCRITICAL Out of disk space\n")
    
    parser = LogParser(str(log_file))
    res = parser.parse_log_summary()
    assert res["counts"]["ERROR"] == 1
    assert res["counts"]["WARNING"] == 1
    assert res["counts"]["CRITICAL"] == 1
    assert len(res["critical_sample"]) == 2
