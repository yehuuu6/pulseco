import pytest
import os
from pulseco.loaders.config_loader import (
    load_config,
    use_default_config,
    DEFAULT_CONFIG,
)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Ensure the config directory and file do not exist before each test
    if os.path.exists("config/settings.json"):
        os.remove("config/settings.json")
    if os.path.exists("config"):
        os.rmdir("config")
    yield
    # Restore permissions if the directory exists and is read-only
    if os.path.exists("config"):
        os.chmod("config", 0o755)
    # Teardown: Clean up after each test
    if os.path.exists("config/settings.json"):
        os.remove("config/settings.json")
    if os.path.exists("config"):
        os.rmdir("config")


def test_use_default_config_creates_config_directory():
    config = use_default_config()
    assert os.path.exists("config")
    assert os.path.exists("config/settings.json")
    assert config == DEFAULT_CONFIG


def test_load_config_uses_default_when_no_config_file():
    config = load_config()
    assert config == DEFAULT_CONFIG
    assert os.path.exists("config/settings.json")


def test_load_config_loads_existing_config():
    os.makedirs("config", exist_ok=True)
    with open("config/settings.json", "w") as f:
        f.write(DEFAULT_CONFIG.model_dump_json(indent=4))
    config = load_config()
    assert config == DEFAULT_CONFIG


def test_load_config_invalid_json():
    os.makedirs("config", exist_ok=True)
    with open("config/settings.json", "w") as f:
        f.write("{invalid_json}")
    config = load_config()
    assert config == DEFAULT_CONFIG
