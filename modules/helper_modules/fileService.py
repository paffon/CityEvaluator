import json
import os
import pandas as pd


def get_ancestor_path(ancestor):
    """
    Retrieves the path of the closest ancestor directory with the given name.

    Args:
        ancestor (str): The name of the ancestor directory to search for.

    Returns:
        str: The path of the closest ancestor directory.

    Raises:
        ValueError: If the ancestor directory is not found.

    Example:
        ancestor_name = "my_ancestor"
        ancestor_path = get_ancestor_path(ancestor_name)
        print(ancestor_path)
    """
    current_dir = os.getcwd()  # Get the current working directory

    # Move up the directory hierarchy until finding the ancestor directory
    while os.path.basename(current_dir) != ancestor:
        current_dir = os.path.dirname(current_dir)
        if current_dir == os.path.dirname(current_dir):
            raise ValueError(f"Directory '{ancestor}' not found.")

    return current_dir


def find_paths(ancestor, target, file_or_folder):
    """
    Recursively searches for files or folders with the given name within an ancestor directory.

    Args:
        ancestor (str): The name of the ancestor directory to start the search from.
        target (str): The name of the file or folder to search for.
        file_or_folder (str): Specify whether to search for 'file' or 'folder'.

    Returns:
        list: A list of full paths to the found files or folders.

    Raises:
        ValueError: If the ancestor directory is not found.

    Example:
        ancestor_name = "my_ancestor"
        target_name = "file.txt"
        file_or_folder = "file"
        found_paths = find_paths(ancestor_name, target_name, file_or_folder)
        print(found_paths)

    """
    project_dir = get_ancestor_path(ancestor)

    # Use os.walk to recursively search for files or folders with the given name
    found_paths = []
    for root, dirs, files in os.walk(project_dir):
        if file_or_folder == "file":
            for file in files:
                if file == target:
                    found_paths.append(os.path.join(root, file))
        elif file_or_folder == "folder":
            for folder in dirs:
                if folder == target:
                    found_paths.append(os.path.join(root, folder))
        else:
            raise ValueError(f"Unknown target type {file_or_folder}")

    return found_paths


def determine_path(ancestor, target, file_or_folder):
    found_files = find_paths(ancestor, target, file_or_folder)
    if len(found_files) == 0:
        raise FileNotFoundError(f"No file named {target} found under ancestor folder {ancestor}.")
    elif len(found_files) == 1:
        return found_files[0]
    else:
        printable_list = '\n\t'.join(found_files)
        error_message = f"Found {len(found_files)} {file_or_folder}s named {target}:\n\t{printable_list}"
        raise FileExistsError(error_message)


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def get_files_in_folder(folder_path, extension=None):
    """
    Retrieves a list of files with the specified extension in the specified folder.

    Args:
        folder_path (str): The path to the folder.
        extension (str, optional): The desired file extension. If None, all files will be retrieved. Defaults to None.

    Returns:
        list: A list of file names with the specified extension.

    Example:
        folder_path = '/path/to/folder'
        extension = 'txt'
        txt_files = get_files_in_folder(folder_path, extension)
        print(txt_files)

    """
    files = []
    for file_name in os.listdir(folder_path):
        if extension is None or file_name.endswith(extension):
            files.append(file_name)
    return files
