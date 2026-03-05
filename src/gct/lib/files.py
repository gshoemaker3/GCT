from __future__ import annotations
import os
import shutil
from pathlib import Path

from gct.lib import ui
from gct.lib.utils import ERROR, WARNING, SUCCESS


def copy_files_usage() -> None:
    print("\n\n==============FILE COPY==================")
    print("================USAGE====================")
    print(
        "Currently the copy file function has only been tested to support "
        "local-to-local file copies.\n"
        "It DOES NOT support:\n"
        "  - copying files from remote locations to local locations\n"
        "  - copying local files to remote locations\n"
        "  - copying remote files to other remote locations."
        "REQUIREMENTS: "
        "  - A source path to a file must be provided.\n"
        "  - A destination path is optional. If one is not provided, "
        "a default destination path will be used instead\n"
        "  - The destination path has to be to a directory/folder. it cannot be a file"
    )
    print("================USAGE====================\n\n")


def copy_file(is_interactive: bool, src: str = None, dst: str = None) -> None:
    """
    this function takes a two file paths in and
    copies the file stored in "source"
    """

    copy_files_usage()
    if is_interactive:
        src_path = ui.get_file_input("src")
        dst_path = ui.get_file_input("dst")
    else:
        src_path = ui.handle_file_input("src", src)
        dst_path = ui.handle_file_input("dst", dst)

    if check_overwrite_file(dst_path / src_path.name):
        exe_file_copy(src_path, dst_path)
    else:
        print(f"{WARNING}: The file copy was canceled.")


def check_overwrite_file(file: Path) -> bool:
    """
    This function asks the user if they want to overwrite a file
    if that file already exists at a specific destination.

    Args:
        - file: The file that will be check for if it exists and if
            it will be overwritten.

    Return:
        - True if the file doesn't exist, or if the file does exist and the
            user ops to overwrite it and False if the file path stored in
            file is not a file or if the file exists and the user ops to
            NOT overwrite the file.
    """
    if file.is_dir():
        print(f"{ERROR}: The path provided: {file} is a directory, not a file.")
        return False
    elif file.exists():
        prompt = f"{WARNING}: The source file already exists at the destination. Would you like to overwrite it? "
        return ui.yes_no(prompt)
    else:
        return True


def exe_file_copy(src_path: Path, dst_path: Path):
    """
    This function executes the file copy and verfies that the copy
    was successfully completed.

    Args:
        - src_path: This is the file that will be copied
        - dst_path: This is the location to which the file will be copied to.
    """

    # Performing copy.
    try:
        shutil.copy2(src_path, dst_path)
    except PermissionError as e:
        print(
            f"{ERROR}: The file copy was unsuccessful. "
            f"Permission error has occurred. Received the following error:\n{e}"
        )
    except Exception as e:
        print(
            f"{ERROR}: The file copy was unsuccessful. "
            f"Received the following error:\n{e}"
        )

    copied_file = dst_path / src_path.name

    if copied_file.exists() and src_path.stat().st_size == copied_file.stat().st_size:
        print(f"{SUCCESS}: File {src_path.name} was successfully copied to {dst_path}")
    else:
        print(f"{ERROR}: File {src_path.name} failed to be copied to {dst_path}")


def handle_src_file(src: Path) -> bool:
    """
    This function takes in a file path and determines if it exists.

    Args:
        - src: The file path to be validated.

    Return:
        - True if the file exists and false otherwise.
    """
    if src.exists() and src.is_file():
        return True
    else:
        print(
            f"{ERROR}: The file path provide: {src} could not be found."
            " Ensure that the path is correct and the file exists then try again."
        )
        return False


def handle_dst_file(dst: Path) -> bool:
    """
    This function takes in a file path and determines if it exists.
    If the file path doesn't exists, it prompts the user if they want
    to create the path.

    Args:
        - dst: the file path to a desired destination.

    Return:
        - True if the destination exists and isn't a file and false if it doesn't
            exists or is a file.
    """

    if dst.exists() and not dst.is_file():
        return True
    elif dst.is_file():
        print(
            f"{ERROR}: The destination path provided: {dst} is an already existing file. "
            "Please provide a path to a directory."
        )
        return False
    else:
        # Not a file and path doesn't exist
        prompt = (
            f"{WARNING}: The provided file path, {dst} does not exist."
            " Would you like to create the file path?"
        )
        if ui.yes_no(prompt):
            dst.mkdir(parents=True, exist_ok=True)
            return True
        else:
            print(f"{ERROR}: Path doesn't exist and user does not want to create path.")
            return False
