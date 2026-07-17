import os
import yaml
from pathlib import Path
from typing import Any, Dict

APP_NAME = "PCA Cognitive DNA Prototype"
VERSION = "0.2.0"
SPECIFICATION_VERSION = "PCA Specification v1.0 (Draft)"

# Default configuration
DEFAULT_CONFIG = {
    "llm": {
        "provider": "ollama",
        "model": "qwen3:4b",
        "temperature": 0.7,
        "max_tokens": 500
    }
}

def load_config() -> Dict[str, Any]:
    """Loads configuration from config.yaml or returns default."""
    config_path = Path(__file__).resolve().parents[1] / "config.yaml"
    
    if not config_path.exists():
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, "r") as f:
            user_config = yaml.safe_load(f)
            config = DEFAULT_CONFIG.copy()
            if user_config and "llm" in user_config:
                config["llm"].update(user_config["llm"])
            return config
    except Exception as e:
        print(f"Warning: Failed to load config.yaml ({e}). Using defaults.")
        return DEFAULT_CONFIG

# Global config object
settings = load_config()
