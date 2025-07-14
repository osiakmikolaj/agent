import os
from functions.get_absolute_path import get_absolute_path
import subprocess

def run_python_file(working_directory, file_path):
    try:
        # Get the absolute path
        work_dir, file_dir = get_absolute_path(working_directory, file_path)

        # Check if file is in wokring dir, if it exists and if it ends with .py
        if not file_dir.startswith(work_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file_dir):
            return f'Error: File "{file_path}" not found.'

        if not file_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute python file
        output = subprocess.run(["python", file_dir], cwd=work_dir, timeout=30, capture_output=True, text=True)

        # Build the result
        result = f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\n"

        # Check if output was produced
        if not output.stdout and not output.stderr:
            result += "No output produced"

        if output.returncode != 0:
            result += f"Process exited with code {output.returncode}"

    except Exception as e:
        return f"Error: executing Python file: {e}"

    return result
