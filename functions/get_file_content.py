import os
from functions.config import MAX_CHARS
from functions.get_absolute_path import get_absolute_path

def get_file_content(working_directory, file_path):
    try:
        # Get aboslute path
        work_dir, file_dir = get_absolute_path(working_directory, file_path)

        # Check if file is in wokring dir and if it is a file
        if not file_dir.startswith(work_dir):
            return f'Error: Cannot read "{file_dir}" as it is outside the permitted working directory'

        if not os.path.isfile(file_dir):
            return f'Error: File not found or is not a regular file: "{file_dir}"'

        # Read the file and return contents as a string
        with open(file_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= 10000:
                file_content_string = f"{file_content_string[:10000]} [...File \"{file_dir}\" truncated to 10000 characters]"
    except Exception as e:
        return f"Error: {str(e)}"

    return file_content_string
