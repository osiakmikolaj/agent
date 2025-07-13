import os
from functions.get_absolute_path import get_absolute_path

def write_file(working_directory, file_path, content):
    try:
        # Get aboslute path
        work_dir, file_dir = get_absolute_path(working_directory, file_path)

        # Check if file is in wokring dir and if it is a file
        if not file_dir.startswith(work_dir):
            return f'Error: Cannot read "{file_dir}" as it is outside the permitted working directory'

        # If parent directory doesn't exist, create it
        parent_dir = os.path.dirname(file_dir)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # Check if the target path is already a directory
        if os.path.isdir(file_dir):
            return f'Error: "{file_path}" is a directory, not a file'

        with open(file_dir, "w") as f:
            f.write(content)

    except Exception as e:
        return f"Error: {str(e)}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
