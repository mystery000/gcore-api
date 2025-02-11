from pathlib import Path
from typing import Dict, List

import yaml


class Config:
    """Handle configuration for Gcore CLI."""

    def __init__(self):
        """Initialize configuration."""
        self.config_dir = Path.home() / ".config" / "gcore"
        self.config_file = self.config_dir / "config.yaml"
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save_token(self, token: str):
        """Save API token to configuration file."""
        config = {"api_token": token}
        with open(self.config_file, "w") as f:
            yaml.dump(config, f)

    def load_token(self) -> Optional[str]:
        """Load API token from configuration file."""
        if not self.config_file.exists():
            return None

        with open(self.config_file) as f:
            config = yaml.safe_load(f)
            return config.get("api_token")
