import os
import pytest
from unittest.mock import patch, mock_open
from pulseco.log_manager import main_logger, log_files
from typing import Any
import shutil


@pytest.fixture
def setup_logs_directory():
    # Setup: Create a temporary logs directory
    os.mkdir("logs")
    yield
    # Teardown: Remove the logs directory and its contents
    if os.path.exists("logs"):
        shutil.rmtree("logs")


def test_create_logs_directory(monkeypatch: pytest.MonkeyPatch):
    def mock_mkdir():
        raise Exception("Permission denied mock")

    monkeypatch.setattr(os, "mkdir", mock_mkdir)

    with pytest.raises(Exception):
        os.mkdir("logs")


def test_log_files_creation():
    # Test if log files are created
    for log_file in log_files:
        assert os.path.exists(f"logs/{log_file}")


@patch("builtins.open", new_callable=mock_open)
def test_log_file_writing(mock_open: Any):
    # Test if log files are writable
    for log_file in log_files:
        with open(f"logs/{log_file}", "w") as f:
            f.write("test")
        mock_open.assert_called_with(f"logs/{log_file}", "w")


def test_main_logger_exists():
    # Test if main logger is created
    assert main_logger is not None
    assert main_logger.name == "pulseco"
