"""CLI entry point for sound-notify."""

import sys
import time
import subprocess
from pathlib import Path
from typing import Optional

import click

from sound_notify.player import AudioPlayer
from sound_notify.config import Config, load_config


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("command", nargs=-1, required=True, type=click.UNPROCESSED)
@click.option("-s", "--success-sound", type=click.Path(exists=True), help="Custom success sound file")
@click.option("-f", "--failure-sound", type=click.Path(exists=True), help="Custom failure sound file")
@click.option("-t", "--threshold", type=int, help="Minimum duration (seconds) to trigger notification")
@click.option("-v", "--verbose", is_flag=True, help="Show timing and notification details")
@click.option("-d", "--dry-run", is_flag=True, help="Test without playing sounds")
@click.option("-c", "--config", type=click.Path(exists=True), help="Custom config file path")
def main(
    command: tuple,
    success_sound: Optional[str],
    failure_sound: Optional[str],
    threshold: Optional[int],
    verbose: bool,
    dry_run: bool,
    config: Optional[str]
) -> None:
    """Wrap CLI commands with sound notifications on completion."""
    config_obj = load_config(config)
    
    if success_sound:
        config_obj.success_sound = Path(success_sound)
    if failure_sound:
        config_obj.failure_sound = Path(failure_sound)
    if threshold is not None:
        config_obj.min_duration = threshold
    
    cmd_str = " ".join(command)
    
    if verbose:
        click.echo(f"Running: {cmd_str}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            stdin=sys.stdin
        )
        exit_code = result.returncode
    except FileNotFoundError:
        click.echo(f"Error: Command not found: {command[0]}", err=True)
        sys.exit(127)
    except KeyboardInterrupt:
        click.echo("\nInterrupted by user", err=True)
        sys.exit(130)
    
    duration = time.time() - start_time
    
    if verbose:
        click.echo(f"\nCommand completed in {duration:.2f}s with exit code {exit_code}")
    
    if duration >= config_obj.min_duration:
        sound_file = config_obj.success_sound if exit_code == 0 else config_obj.failure_sound
        
        if verbose:
            status = "success" if exit_code == 0 else "failure"
            click.echo(f"Playing {status} notification: {sound_file}")
        
        if not dry_run:
            player = AudioPlayer()
            try:
                player.play(sound_file)
            except Exception as e:
                if verbose:
                    click.echo(f"Warning: Failed to play sound: {e}", err=True)
    elif verbose:
        click.echo(f"Duration {duration:.2f}s below threshold {config_obj.min_duration}s, skipping notification")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
