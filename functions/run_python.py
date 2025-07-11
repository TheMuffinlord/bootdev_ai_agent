import os, subprocess

from google import genai
from google.genai import types

def run_python_file(working_directory, file_path):
    fullpath = os.path.join(working_directory, file_path)
    #wd_paths = os.listdir(working_directory)
    abs_fullpath = os.path.abspath(fullpath)
    abs_workdir = os.path.abspath(working_directory)
    #abs_filepath = os.path.abspath(file_path)
    #file_alone = os.path.split(file_path)[1]
    if not abs_fullpath.startswith(abs_workdir):
        raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if os.path.exists(abs_fullpath) != True:
        raise Exception(f'Error: File "{file_path}" not found.')
    if os.path.splitext(file_path)[1] != ".py":
        raise Exception(f'Error: "{file_path}" is not a Python file.')
    try:
        result = subprocess.run(["python3", abs_fullpath], timeout=30, capture_output=True)
        #print(result)
        output = f"File output:\n"
        if result.stdout != None:
            output += f"STDOUT: {result.stdout}\n"
        else:
            return "No output produced."
        if result.stderr != None:
            output += f"STDERR: {result.stderr}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}.\n"
        return output
    except Exception as e:
        raise Exception(f"Error: executing Python file: {e}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and returns its output, constrained to the working directory.",
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