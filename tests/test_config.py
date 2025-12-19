"""Tests for configuration management."""

import pytest
from pathlib import Path
import tempfile
import yaml

from sound_notify.config import Config, load_config, get_default_sound, create_default_config


class TestConfig:
    """Test Config model."""
    
    def test_default_config(self):
        config = Config()
        assert config.min_duration == 5
        assert config.success_sound.exists()
        assert config.failure_sound.exists()
    
    def test_custom_config(self, tmp_path):
        sound_file = tmp_path / "custom.wav"
        sound_file.touch()
        config = Config(success_sound=sound_file, min_duration=10)
        assert config.success_sound == sound_file
        assert config.min_duration == 10
    
    def test_negative_duration_fails(self):
        with pytest.raises(ValueError):
            Config(min_duration=-1)


class TestGetDefaultSound:
    """Test default sound retrieval."""
    
    def test_success_sound(self):
        sound = get_default_sound("success")
        assert sound.name == "success.wav" or sound.name == "default.wav"
    
    def test_failure_sound(self):
        sound = get_default_sound("failure")
        assert sound.name == "failure.wav" or sound.name == "default.wav"
    
    def test_unknown_sound_type(self):
        sound = get_default_sound("unknown")
        assert sound.name == "default.wav"


class TestLoadConfig:
    """Test configuration loading."""
    
    def test_load_nonexistent_returns_default(self):
        config = load_config("/nonexistent/path.yml")
        assert config.min_duration == 5
    
    def test_load_valid_config(self, tmp_path):
        config_file = tmp_path / "config.yml"
        sound_file = tmp_path / "test.wav"
        sound_file.touch()
        
        data = {
            "success_sound": str(sound_file),
            "failure_sound": str(sound_file),
            "min_duration": 15
        }
        with open(config_file, "w") as f:
            yaml.dump(data, f)
        
        config = load_config(str(config_file))
        assert config.min_duration == 15
        assert config.success_sound == sound_file
    
    def test_load_invalid_yaml_raises(self, tmp_path):
        config_file = tmp_path / "bad.yml"
        config_file.write_text("invalid: yaml: content: [")
        
        with pytest.raises(ValueError, match="Failed to load config"):
            load_config(str(config_file))
    
    def test_load_with_expanduser(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path))
        config_file = tmp_path / "config.yml"
        sound_file = tmp_path / "sound.wav"
        sound_file.touch()
        
        data = {"success_sound": "~/sound.wav"}
        with open(config_file, "w") as f:
            yaml.dump(data, f)
        
        config = load_config(str(config_file))
        assert config.success_sound == sound_file


class TestCreateDefaultConfig:
    """Test config file creation."""
    
    def test_create_config_file(self, tmp_path):
        config_path = tmp_path / "test-config.yml"
        create_default_config(config_path)
        
        assert config_path.exists()
        with open(config_path) as f:
            data = yaml.safe_load(f)
        assert "min_duration" in data
        assert data["min_duration"] == 5
