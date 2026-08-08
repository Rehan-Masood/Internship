# Cyber-Typer 2070

Developer terminal-style typing game with reactive security-breach events and synthesized audio.

## Demo Video
<video src="https://github.com/user-attachments/assets/123f8f46-55fd-4a96-8aa7-91ecc8378649" controls width="600"></video>

## Features
- Stylized terminal UI using `pygame`
- Timed typing challenges with scoring, streaks and WPM calculation
- Reactive "breach" events that require rapid override typing
- Procedural synthesized sound effects (no external audio files)

## Files
- [main.py](main.py) — main game implementation and entrypoint
- [requirements.txt](requirements.txt) — Python dependencies

## Prerequisites
- Python 3.10+ (recommended)
- `pip` available on your PATH

## Install
Install dependencies from `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Or on Unix/macOS:

```bash
python3 -m pip install -r requirements.txt
```

## Run
Start the game with:

```powershell
python main.py
```

## Controls
- `SPACE`: Start / Restart
- `F11` or `f`: Toggle fullscreen
- Type displayed target text to score points
- During breach events, type the override command exactly and press Enter

## Notes
- The game uses `pygame` audio mixer and a small synthesized sound engine; audio may behave differently across platforms.
- If you encounter issues with sound initialization, try updating your drivers or run without audio by modifying `pygame.mixer.init` in `main.py`.

## Contributing
Feel free to open issues or submit pull requests. Suggested improvements:
- Add configurable difficulty and levels
- Persist high scores
- Add localization and accessibility options

## License
Specify a license for your project here (e.g., MIT). If unsure, add a `LICENSE` file.
