from django.core.files.storage import default_storage
import os
# Function to save or overwrite the file
def save_or_overwrite_file(file, path):
    if os.path.exists(path):
        os.remove(path)  # Remove the existing file
    with default_storage.open(path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
