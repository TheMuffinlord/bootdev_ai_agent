import os

def get_files_info(working_directory, directory=None):
    fullpath = os.path.join(working_directory, directory)
    wd_paths = os.listdir(working_directory)
    if os.path.isfile(fullpath):
        raise Exception(f'Error: "{directory}" is not a directory')
    elif directory not in wd_paths and directory != ".":
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

        

    

#i will write this tomorrow. fuck you