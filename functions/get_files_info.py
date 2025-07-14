import os

from google import genai
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory:
        fullpath = os.path.join(working_directory, directory)
    else:
        fullpath = working_directory
    #wd_paths = os.listdir(working_directory)
    abs_fullpath = os.path.abspath(fullpath)
    abs_workdir = os.path.abspath(working_directory)
    if os.path.isfile(abs_fullpath):
        raise Exception(f'Error: "{directory}" is not a directory')
    if not abs_fullpath.startswith(abs_workdir):
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    pathlist = os.listdir(fullpath)
    if directory == None or directory == ".":
        result_string = f"Result for current directory:\n"
    else:
        result_string = f"Result for '{directory}' directory:\n"
    for path in pathlist:
        onefullpath = os.path.join(fullpath, path)
        ofp_size = os.path.getsize(onefullpath)
        ofp_isdir = os.path.isdir(onefullpath)
        result_string += f"- {path}: file_size={ofp_size} bytes, is_dir={ofp_isdir}\n"
    return result_string

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)        

