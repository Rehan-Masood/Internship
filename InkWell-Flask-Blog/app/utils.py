import os
import secrets
from urllib.parse import urlparse

import cloudinary
import cloudinary.uploader
from flask import current_app


def _cloudinary_folder(folder_config_key):
    if folder_config_key == "UPLOAD_FOLDER_PROFILE":
        return "inkwell/profile_pics"
    return "inkwell/post_covers"


def _public_id_from_url(image_url):
    if not image_url or not image_url.startswith("http"):
        return None

    try:
        path = urlparse(image_url).path
        segments = [segment for segment in path.split("/") if segment]
        if not segments:
            return None

        if "upload" in segments:
            upload_index = segments.index("upload")
            segments = segments[upload_index + 1:]

        if segments and segments[0].startswith("v"):
            segments = segments[1:]

        if not segments:
            return None

        filename = segments[-1]
        name, _ = os.path.splitext(filename)
        return "/".join(segments[:-1] + [name]) if len(segments) > 1 else name
    except Exception:
        return None


def save_image(form_picture, folder_config_key, output_size=None):
    """Upload an image to Cloudinary and store the CDN URL in the database."""
    if not form_picture:
        return None

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    )

    folder = _cloudinary_folder(folder_config_key)
    public_id = secrets.token_hex(8)
    upload_result = cloudinary.uploader.upload(
        form_picture,
        folder=folder,
        public_id=public_id,
        overwrite=False,
    )
    return upload_result.get("secure_url")


def delete_image(image_value, folder_config_key):
    """Delete the image from Cloudinary if it is a Cloudinary URL; fall back to local disk for legacy records."""
    if not image_value:
        return

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    )

    public_id = _public_id_from_url(image_value)
    if public_id:
        cloudinary.uploader.destroy(public_id, invalidate=True)
        return

    folder_path = current_app.config.get(folder_config_key)
    if folder_path:
        file_path = os.path.join(folder_path, image_value)
        if os.path.exists(file_path):
            os.remove(file_path)
