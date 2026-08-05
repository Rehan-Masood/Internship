# Higher-Lower App

- **Description:** A tiny Flask web app that asks the user to guess a secret number between 0 and 9.
- **Main file:** [server.py](server.py#L1-L40)

## Demo Video
<video src="https://github.com/user-attachments/assets/8b9e9450-4807-4764-b623-6f3e73bbc755" controls width="600"></video>

**Requirements**

- **Python:** 3.8+
- **Packages:** Flask

**Install**

Run the following to install Flask:

```
pip install Flask
```

Optionally, create a virtual environment first:

```
python -m venv .venv
.
```

Activate it (Windows PowerShell):

```
.venv\Scripts\Activate.ps1
```

**Run**

Start the server with:

```
python server.py
```

By default the app runs in debug mode on `http://127.0.0.1:5000`.

**How to play**

- Visit the home page: `http://127.0.0.1:5000/` to see the prompt.
- Submit a guess by appending the number to the URL, for example:

```
http://127.0.0.1:5000/5
```

- The app will respond with hints: "Too low", "Too high", or "You found me!" and will show a GIF.

**Notes**

- The app prints the chosen secret number to the console for debugging when started (see server logs).
- The app currently selects a single random number at startup; restarting the server picks a new secret number.

**Contributing**

- Feel free to open issues or submit pull requests with improvements (examples: add a web form, persist high scores, add tests).

**License**

- MIT (use as you like)
