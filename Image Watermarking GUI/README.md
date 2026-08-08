# Image Watermarking GUI

A small cross-platform GUI application to add text or image watermarks to photos.

## Demo Video
<video src="https://github.com/user-attachments/assets/cfcf8a40-0a33-4f68-8ae7-4692e2813488" controls width="600"></video>

## Image Watermarking GUI
   ![Image Watermarking GUI.](./Pic.jpg)

## Features
- Add text or image watermarks
- Adjust position, opacity, and scale
- Live preview and save watermarked images

## Requirements
- Python 3.8+
- See [requirements.txt](requirements.txt) for dependencies

## Installation
1. Create a virtual environment (recommended):

```bash
python -m venv .venv
```

2. Activate the virtual environment and install dependencies:

Windows:
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
Run the GUI:

```bash
python main.py
```

The app will open a window where you can load images, apply text or image watermarks, preview results, and save.

## Project files
- [main.py](main.py) — application entrypoint
- [requirements.txt](requirements.txt) — Python dependencies

## Contributing
Contributions and improvements are welcome. Open an issue or submit a pull request.

## License
Specify a license for your project (e.g., MIT). If unsure, add one later.
