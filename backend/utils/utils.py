import os

def format_filename(filename: str) -> str:
    # Remove the extension
    name, _ = os.path.splitext(filename)
    # Replace spaces with underscores
    return name.replace(" ", "_")