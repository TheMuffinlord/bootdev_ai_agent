import os

def write_file(working_directory, file_path, content):
    fullpath = os.path.join(working_directory, file_path)
    wd_paths = os.listdir(working_directory)
    file_alone = os.path.split(file_path)[1]
    if os.path.split(file_path)[0] not in wd_paths and os.path.dirname(file_path) != "":
        raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.')
    if os.path.exists(fullpath) != True:
        open_switch = "x"
    else:
        open_switch = "w"
    try:
        with open(fullpath, open_switch) as f:
            f.write(content)
    except Exception as e:
        return f"ERROR: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
