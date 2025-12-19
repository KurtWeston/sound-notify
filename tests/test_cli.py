"""Tests for CLI interface."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from pathlib import Path

from sound_notify.cli import main


class TestCLI:
    """Test CLI command."""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_no_command_fails(self):
        result = self.runner.invoke(main, [])
        assert result.exit_code != 0
    
    @patch('sound_notify.cli.subprocess.run')
    @patch('sound_notify.cli.time.time', side_effect=[0, 10])
    @patch('sound_notify.cli.AudioPlayer')
    def test_successful_command_plays_sound(self, mock_player, mock_time, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        mock_player_instance = MagicMock()
        mock_player.return_value = mock_player_instance
        
        result = self.runner.invoke(main, ['echo', 'test'])
        
        assert result.exit_code == 0
        mock_player_instance.play.assert_called_once()
    
    @patch('sound_notify.cli.subprocess.run')
    @patch('sound_notify.cli.time.time', side_effect=[0, 10])
    @patch('sound_notify.cli.AudioPlayer')
    def test_failed_command_plays_failure_sound(self, mock_player, mock_time, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        mock_player_instance = MagicMock()
        mock_player.return_value = mock_player_instance
        
        result = self.runner.invoke(main, ['false'])
        
        assert result.exit_code == 1
        mock_player_instance.play.assert_called_once()
    
    @patch('sound_notify.cli.subprocess.run')
    @patch('sound_notify.cli.time.time', side_effect=[0, 2])
    @patch('sound_notify.cli.AudioPlayer')
    def test_short_command_no_notification(self, mock_player, mock_time, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        mock_player_instance = MagicMock()
        mock_player.return_value = mock_player_instance
        
        result = self.runner.invoke(main, ['echo', 'quick'])
        
        mock_player_instance.play.assert_not_called()
    
    @patch('sound_notify.cli.subprocess.run')
    @patch('sound_notify.cli.time.time', side_effect=[0, 10])
    def test_dry_run_no_sound(self, mock_time, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        
        result = self.runner.invoke(main, ['--dry-run', 'echo', 'test'])
        
        assert result.exit_code == 0
    
    @patch('sound_notify.cli.subprocess.run')
    @patch('sound_notify.cli.time.time', side_effect=[0, 10])
    def test_verbose_mode(self, mock_time, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        
        result = self.runner.invoke(main, ['--verbose', 'echo', 'test'])
        
        assert 'Running:' in result.output
        assert 'completed' in result.output
    
    @patch('sound_notify.cli.subprocess.run', side_effect=FileNotFoundError)
    def test_command_not_found(self, mock_run):
        result = self.runner.invoke(main, ['nonexistent_command'])
        assert result.exit_code == 127
        assert 'Command not found' in result.output
    
    def test_custom_threshold(self, tmp_path):
        with patch('sound_notify.cli.subprocess.run') as mock_run:
            with patch('sound_notify.cli.time.time', side_effect=[0, 3]):
                mock_run.return_value = MagicMock(returncode=0)
                result = self.runner.invoke(main, ['--threshold', '2', 'echo', 'test'])
                assert result.exit_code == 0
