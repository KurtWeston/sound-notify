"""Tests for audio player."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import platform

from sound_notify.player import AudioPlayer


class TestAudioPlayer:
    """Test AudioPlayer class."""
    
    def test_init(self):
        player = AudioPlayer()
        assert player.system == platform.system()
    
    def test_play_nonexistent_file_raises(self):
        player = AudioPlayer()
        with pytest.raises(FileNotFoundError, match="Sound file not found"):
            player.play("/nonexistent/file.wav")
    
    @patch('sound_notify.player.playsound')
    def test_play_with_playsound(self, mock_playsound, tmp_path):
        sound_file = tmp_path / "test.wav"
        sound_file.touch()
        
        player = AudioPlayer()
        player.play(sound_file)
        
        mock_playsound.assert_called_once_with(str(sound_file))
    
    @patch('sound_notify.player.playsound', side_effect=ImportError)
    @patch('sound_notify.player.subprocess.run')
    def test_fallback_macos(self, mock_run, mock_playsound, tmp_path, monkeypatch):
        monkeypatch.setattr('sound_notify.player.platform.system', lambda: 'Darwin')
        sound_file = tmp_path / "test.wav"
        sound_file.touch()
        
        player = AudioPlayer()
        player.play(sound_file)
        
        mock_run.assert_called_once()
        assert mock_run.call_args[0][0][0] == "afplay"
    
    @patch('sound_notify.player.playsound', side_effect=ImportError)
    @patch('sound_notify.player.subprocess.run')
    def test_fallback_linux(self, mock_run, mock_playsound, tmp_path, monkeypatch):
        monkeypatch.setattr('sound_notify.player.platform.system', lambda: 'Linux')
        sound_file = tmp_path / "test.wav"
        sound_file.touch()
        
        player = AudioPlayer()
        player.play(sound_file)
        
        assert mock_run.called
    
    @patch('sound_notify.player.playsound', side_effect=Exception("Play failed"))
    def test_play_exception_raises(self, mock_playsound, tmp_path):
        sound_file = tmp_path / "test.wav"
        sound_file.touch()
        
        player = AudioPlayer()
        with pytest.raises(RuntimeError, match="Failed to play sound"):
            player.play(sound_file)
