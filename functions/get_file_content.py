import os

from functions.constants import FILE_LENGTH_LIMIT

def get_file_content(working_directory, file_path):
    fullpath = os.path.join(working_directory, file_path)
    
    wd_paths = os.listdir(os.path.split(fullpath)[0])
    file_alone = os.path.split(file_path)[1]
    if file_alone not in wd_paths:
        raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory. Full path: {fullpath}')
    yes_file = os.path.isfile(os.path.abspath(fullpath))
    if yes_file != True:
        raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
    with open(fullpath, "r") as f:
        try:
            file_string = f.read(FILE_LENGTH_LIMIT)
            if len(f.read()) > FILE_LENGTH_LIMIT:
                file_string += f'[...File "{file_path}" truncated at {FILE_LENGTH_LIMIT} characters]'
        except Exception as e:
            return f'ERROR: {e}'
    return file_string