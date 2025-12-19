"""Cross-platform audio playback handler."""

import platform
from pathlib import Path
from typing import Union


class AudioPlayer:
    """Handle audio playback across different platforms."""
    
    def __init__(self):
        self.system = platform.system()
    
    def play(self, sound_file: Union[str, Path]) -> None:
        """Play audio file using appropriate backend."""
        sound_path = Path(sound_file)
        
        if not sound_path.exists():
            raise FileNotFoundError(f"Sound file not found: {sound_path}")
        
        try:
            from playsound import playsound
            playsound(str(sound_path))
        except ImportError:
            self._fallback_play(sound_path)
        except Exception as e:
            raise RuntimeError(f"Failed to play sound: {e}")
    
    def _fallback_play(self, sound_path: Path) -> None:
        """Fallback to system-specific commands."""
        import subprocess
        
        if self.system == "Darwin":
            subprocess.run(["afplay", str(sound_path)], check=True)
        elif self.system == "Linux":
            for cmd in ["paplay", "aplay", "ffplay"]:
                try:
                    subprocess.run(
                        [cmd, str(sound_path)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=True
                    )
                    return
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
            raise RuntimeError("No audio player found on system")
        elif self.system == "Windows":
            import winsound
            winsound.PlaySound(str(sound_path), winsound.SND_FILENAME)
        else:
            raise RuntimeError(f"Unsupported platform: {self.system}")
