import os
from functions.get_absolute_path import get_absolute_path

def write_file(working_directory, file_path, content):
    try:
        # Get aboslute path
        work_dir, file_dir = get_absolute_path(working_directory, file_path)

        # Check if file is in wokring dir and if it is a file
        if not file_dir.startswith(work_dir):
            return f'Error: Cannot read "{file_dir}" as it is outside the permitted working directory'

        if not os.path.isfile(file_dir):
            return f'Error: File not found or is not a regular file: "{file_dir}"'
    except Exception as e:
        return f"Error: {str(e)}"
