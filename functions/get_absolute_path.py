import os

def get_absolute_path(working_directory, file_path):
    return (os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, file_path)))
