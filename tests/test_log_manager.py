import os
import pytest
from unittest.mock import patch, mock_open
from pulseco.log_manager import main_logger, log_files
from typing import Any


@pytest.fixture
def setup_logs_directory():
    # Setup: Create a temporary logs directory
    os.makedirs("logs", exist_ok=True)
    yield
    # Teardown: Remove the logs directory and its contents
    for log_file in log_files:
        try:
            os.remove(f"logs/{log_file}")
        except FileNotFoundError:
            pass
    os.rmdir("logs")


def test_logs_directory_creation():
    # Test if logs directory is created
    assert os.path.exists("logs")


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
