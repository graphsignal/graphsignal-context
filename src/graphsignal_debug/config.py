"""Load and save config at ~/.graphsignal/config.yml."""

import os
from pathlib import Path
from typing import Optional

import yaml

CONFIG_DIR = Path.home() / ".graphsignal"
CONFIG_FILE = CONFIG_DIR / "config.yml"

DEFAULT_API_BASE = "https://api.graphsignal.com"


def get_config_path() -> Path:
    return CONFIG_FILE


def ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load config from ~/.graphsignal/config.yml. Returns empty dict if missing."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE) as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_config(config: dict) -> None:
    """Write config to ~/.graphsignal/config.yml."""
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)


def get_api_key() -> Optional[str]:
    """Return stored API key or None if not logged in."""
    config = load_config()
    return config.get("api_key") or os.environ.get("GRAPHSIGNAL_API_KEY")


def set_api_key(api_key: str) -> None:
    """Store API key in config."""
    config = load_config()
    config["api_key"] = api_key
    save_config(config)
