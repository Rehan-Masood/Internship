import os
import secrets
from PIL import Image
from flask import current_app


def save_image(form_picture, folder_config_key, output_size):
    """
    Saves an uploaded image to disk with a randomized filename, resized
    to fit within output_size (a (width, height) tuple). Returns the
    filename to store in the database.
    """
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext.lower()

    folder_path = current_app.config[folder_config_key]
    os.makedirs(folder_path, exist_ok=True)
    picture_path = os.path.join(folder_path, picture_filename)

    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_filename


def delete_image(filename, folder_config_key):
    """Deletes an image file from disk if it exists."""
    if not filename:
        return
    folder_path = current_app.config[folder_config_key]
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
