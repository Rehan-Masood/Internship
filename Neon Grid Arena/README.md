# Neon Grid Arena

Neon Grid Arena is a small, real-time multiplayer browser game built with Flask and Socket.IO. Players pilot neon cores around an arena, collect the Gold Power Core (coin), avoid procedurally generated neon barrier walls, level up, and compete on the live leaderboard.

## Demo Video
<video src="https://github.com/user-attachments/assets/55986a2f-3b61-496e-a56a-4c7a2d9d4fce" controls width="600"></video>

## Features
- Real-time multiplayer using WebSockets (Socket.IO)
- Neon-styled 2D arena rendered on an HTML5 Canvas
- Procedural neon barrier generation and level progression
- Live leaderboard and activity feed
- Respawn system and simple collision/game-over logic

## Tech stack
- Backend: Python, Flask, Flask-SocketIO
- Transport: python-socketio, eventlet
- Frontend: HTML/CSS, Canvas API, vanilla JavaScript, Socket.IO client

## Requirements
- Python 3.8+ recommended
- See [requirements.txt](requirements.txt) for runtime dependencies

## Quick start (development)
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the server:

```powershell
python app.py
```

4. Open your browser to `http://localhost:5000`.

## Project layout
- [app.py](app.py) — Flask + Socket.IO server (game state, player handling, level logic)
- [requirements.txt](requirements.txt) — Python dependencies
- [templates/index.html](templates/index.html) — Main HTML page
- [static/js/game.js](static/js/game.js) — Frontend game logic and Socket.IO client
- [static/css/style.css](static/css/style.css) — Visual styling and neon theme

## Notes / Development
- The server uses `eventlet` for async support with Flask-SocketIO — ensure it's installed.
- `app.py` sets a development `SECRET_KEY` string; replace it in production.
- The game spawns a coin and generates walls via `generate_walls` in `app.py`.

## Next steps / ideas
- Add player names / lobby UI and custom controls
- Persist scores and add a database-backed leaderboard
- Add tests and CI for the server

## License
No license specified. Add a `LICENSE` file if you wish to open-source this project.
