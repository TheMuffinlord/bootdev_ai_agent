import os

from google import genai
from google.genai import types

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and outputs the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read and output, relative to the working directory. If not a file, the function returns an error.",
            ),
        },
    ),
)        