"""Configuration management for sound-notify."""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
import yaml


class Config(BaseModel):
    """Configuration model for sound notifications."""
    
    success_sound: Path = Field(default_factory=lambda: get_default_sound("success"))
    failure_sound: Path = Field(default_factory=lambda: get_default_sound("failure"))
    min_duration: int = Field(default=5, ge=0)


def get_default_sound(sound_type: str) -> Path:
    """Get path to bundled default sound."""
    package_dir = Path(__file__).parent
    sounds_dir = package_dir / "sounds"
    
    sound_map = {
        "success": sounds_dir / "success.wav",
        "failure": sounds_dir / "failure.wav"
    }
    
    sound_file = sound_map.get(sound_type)
    if sound_file and sound_file.exists():
        return sound_file
    
    return sounds_dir / "default.wav"


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or use defaults."""
    if config_path:
        path = Path(config_path)
    else:
        path = Path.home() / ".sound-notify.yml"
    
    if path.exists():
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    if "success_sound" in data:
                        data["success_sound"] = Path(data["success_sound"]).expanduser()
                    if "failure_sound" in data:
                        data["failure_sound"] = Path(data["failure_sound"]).expanduser()
                    return Config(**data)
        except Exception as e:
            raise ValueError(f"Failed to load config from {path}: {e}")
    
    return Config()


def create_default_config(path: Optional[Path] = None) -> None:
    """Create a default configuration file."""
    if path is None:
        path = Path.home() / ".sound-notify.yml"
    
    config = Config()
    config_dict = {
        "success_sound": str(config.success_sound),
        "failure_sound": str(config.failure_sound),
        "min_duration": config.min_duration
    }
    
    with open(path, "w") as f:
        yaml.dump(config_dict, f, default_flow_style=False)
