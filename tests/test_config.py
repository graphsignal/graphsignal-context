"""Tests for graphsignal_debug.config."""

import tempfile
from pathlib import Path

import pytest


# Patch CONFIG_DIR/CONFIG_FILE to a temp dir so we don't touch ~/.graphsignal
@pytest.fixture(autouse=True)
def isolated_config(monkeypatch):
    tmp = tempfile.mkdtemp()
    config_dir = Path(tmp)
    config_file = config_dir / "config.yml"
    import graphsignal_debug.config as config_mod
    monkeypatch.setattr(config_mod, "CONFIG_DIR", config_dir)
    monkeypatch.setattr(config_mod, "CONFIG_FILE", config_file)
    yield config_file
    # cleanup
    if config_file.exists():
        config_file.unlink()
    config_dir.rmdir()


def test_load_config_missing_returns_empty_dict():
    from graphsignal_debug.config import load_config
    assert load_config() == {}


def test_save_and_load_config():
    from graphsignal_debug.config import save_config, load_config
    save_config({"api_key": "test-key", "other": "value"})
    assert load_config() == {"api_key": "test-key", "other": "value"}


def test_get_api_key_from_config():
    from graphsignal_debug.config import set_api_key, get_api_key
    set_api_key("stored-key")
    assert get_api_key() == "stored-key"


def test_get_api_key_from_env(monkeypatch):
    from graphsignal_debug.config import get_api_key
    monkeypatch.setenv("GRAPHSIGNAL_API_KEY", "env-key")
    # With empty config file, get_api_key falls back to env
    assert get_api_key() == "env-key"


def test_set_api_key_persists():
    from graphsignal_debug.config import set_api_key, get_api_key, load_config
    set_api_key("my-api-key")
    assert load_config().get("api_key") == "my-api-key"
    assert get_api_key() == "my-api-key"
