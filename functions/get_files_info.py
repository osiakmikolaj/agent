import os

def get_files_info(working_directory, directory=None):
    try:
        # Create absolute paths - work_dir and target_dir
        work_dir = os.path.abspath(working_directory)
        if directory is not None:
            target_dir = os.path.abspath(os.path.join(working_directory, directory))
        else:
            target_dir = os.path.abspath(working_directory)


        # Check if directories are correct and not outside of working directory
        if not target_dir.startswith(work_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Get dir contents
        items = os.listdir(target_dir)

        dir_con_string = ""
        for item in items:
            # item path
            item_path = os.path.abspath(os.path.join(target_dir, item))

            # Check if dir
            is_dir = os.path.isdir(item_path)

            # Get size
            if is_dir:
                item_size = get_size(item_path)
            else:
                item_size = os.path.getsize(item_path)

            dir_con_string += f"- {item}: file_size={item_size} bytes, is_dir={is_dir}\n"
    except Exception as e:
        return f"Error: {str(e)}"

    return dir_con_string.strip()

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size
