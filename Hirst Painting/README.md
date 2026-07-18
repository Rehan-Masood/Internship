# Hirst Painting

A simple Python project that generates a Damien Hirst style dot painting using the `turtle` module.

## Project Files

- `main.py`: Draws a 10x10 grid of colored dots (100 total) using a predefined palette.
- `extract_colors.py`: Extracts RGB colors from a source image using `colorgram` so you can build your own palette.
- `Hirst Painting.jpg`: Source image included in this project.

## Requirements

- Python 3.x
- `colorgram.py` (only needed for `extract_colors.py`)

Install dependency:

```bash
pip install colorgram.py
```

## How to Run

Run the painting generator:

```bash
python main.py
```

A turtle graphics window will open and draw the artwork. Click the window to close it.

## Extract a New Color Palette (Optional)

Run:

```bash
python extract_colors.py
```

This prints a list of RGB tuples you can paste into `main.py`.

Note: `extract_colors.py` currently uses:

```python
colorgram.extract('image.jpg', 10)
```

If your file is named `Hirst Painting.jpg`, either:

- rename the file to `image.jpg`, or
- update the filename in `extract_colors.py`.

## Customization Ideas

- Change `number_of_dots` for larger/smaller paintings.
- Change `dot_spacing` to adjust density.
- Change dot size in `tim.dot(20, ...)`.
- Replace `color_list` with your own extracted palette.
