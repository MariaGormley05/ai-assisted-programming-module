"""Saving files that users upload: the subject of DIY 4.

save_upload(filename, data) stores the bytes a user uploaded, under the
name the user's browser sent, in UPLOAD_DIR.
"""
import os

UPLOAD_DIR = "uploads"


def save_upload(filename, data):
    """Save the uploaded bytes in UPLOAD_DIR and return the path written."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, filename)
    f = open(path, "wb")
    f.write(data)
    f.close()
    return path
