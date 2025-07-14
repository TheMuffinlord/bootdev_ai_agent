import os

from google import genai
from google.genai import types

from functions.constants import FILE_LENGTH_LIMIT

def get_file_content(working_directory, file_path):
    
    abs_fullpath = os.path.abspath(os.path.join(working_directory, file_path))
    abs_workdir = os.path.abspath(working_directory)
    if not abs_fullpath.startswith(abs_workdir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
    
    if not os.path.isfile(abs_fullpath):
        return f'Error: File not found or is not a regular file: "{file_path}". debug full path: {abs_fullpath}'
    try:
        with open(abs_fullpath, "r") as f:
            file_string = f.read(FILE_LENGTH_LIMIT)
            if len(f.read()) > FILE_LENGTH_LIMIT:
                file_string += f'[...File "{file_path}" truncated at {FILE_LENGTH_LIMIT} characters]'
        return file_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
    

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