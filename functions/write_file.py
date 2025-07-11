import os

from google import genai
from google.genai import types

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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Opens and writes to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be written, constrained to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file."
            )
        },
    ),
)        