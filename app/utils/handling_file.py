import uuid
import os
from datetime import datetime
from pathlib import Path
import shutil

def upload_file(data, folder, file_extension):
    if data:
        # Generate a new filename based on date now with random uuid and provided extension
        current_date = datetime.now().date()
        new_filename = f"{current_date}-{str(uuid.uuid4())}.{file_extension}"

        # Save the uploaded file to a directory
        file_path = Path(folder) / new_filename
        with open(file_path, "wb") as f_dest:
            shutil.copyfileobj(data.file, f_dest)

        # Return the filename
        return str(Path(new_filename))
    else:
        print('error to upload file')
        return None

def delete_file(file_path: str):
    try:
        # Check if the file exists before attempting to delete
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            return False  # File not found
    except Exception as e:
        print(e)
        return False  # Error occurred while deleting
