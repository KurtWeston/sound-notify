# sound-notify

Play customizable sound notifications when long-running CLI commands complete

## Features

- Wrap any CLI command and monitor its exit code
- Play different sounds for success (exit 0) vs failure (non-zero exit)
- Configurable minimum duration threshold to avoid notifications for quick commands
- Support custom sound files (WAV, MP3, OGG) via config file or CLI arguments
- Include default notification sounds bundled with the package
- Cross-platform audio playback (Windows, macOS, Linux)
- Pass through stdout/stderr in real-time while monitoring
- Configuration file support (~/.sound-notify.yml) for default settings
- Verbose mode to show timing and notification details
- Dry-run mode to test without playing sounds

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/sound-notify.git
cd sound-notify

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python

## Dependencies

- `click`
- `playsound3`
- `pydantic`
- `pyyaml`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
