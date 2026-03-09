from __future__ import annotations
import os
import shutil
from pathlib import Path

from gct.lib import ui
from gct.lib.utils import ERROR, WARNING, SUCCESS


def copy_file(is_interactive: bool, src: str = None, dst: str = None) -> None:
    """
    this function takes a two file paths in and
    copies the file stored in "source"

    Args:
        - is_interactive: This true if the tool is in interactive mode and false otherwise.
        - src: this is the source file path if provided from the command line.
        - dst: this is the destination for the copied file if provided from the command line.
    """

    BadVariableSyntax = 53

    if is_interactive:
        print("Please provide the source path for the file to be copied")
        src_path = ui.get_file_input("src")

        print("Please provide the destination the file will be copied to.")
        dst_path = ui.get_file_input("dst")
    else:
        src_path = ui.handle_file_input("src", src)
        dst_path = ui.handle_file_input("dst", dst)

    if check_overwrite_file(dst_path / src_path.name):
        exe_file_copy(src_path, dst_path)
    else:
        print(f"{WARNING}: The file copy was canceled.")


def create_file(is_interactive: bool, file_name: str = None, dst: str = None) -> None:
    """
    this function creates a file based on the filename provided by the user. destination
    path is optional.

    Args:
        - is_interactive: This true if the tool is in interactive mode and false otherwise.
        - file_name: The name of the file to be created if provided from the command line.
        - dst: this is the destination for the new file if provided from the command line.
    """
    if is_interactive:
        file = ui.get_file_input("name")
        dst_path = ui.get_file_input("dst")
    else:
        file = ui.handle_file_input("name", file_name)
        dst_path = ui.handle_file_input("dst", dst)

    # create file.
    new_file = dst_path / file
    new_file.parent.mkdir(parents=True, exist_ok=True)
    new_file.touch()

    # validate creation
    if new_file.exists():
        print(f"{SUCCESS}: file: {file.name} was created at: {dst_path}.")
    else:
        print(f"{ERROR}: The file creation was unsuccessful")


def merge_files(
    is_interactive: bool, src1: str = None, src2: str = None, file_dst: str = None
) -> None:
    """This function takes in two files and merges them into one

    Args:
        - is_interactive: This determines what mode the tool is in.
        - src1: This is one of the files to be combine with another.
        - src2: This is the other file that will be combined with another.
    """
    if is_interactive:
        while True:
            print("Please provide the source path for the first file to be merged.")
            file_1: Path = ui.get_file_input("src")

            print("Please provide the source path for the second file to be merged.")
            file_2: Path = ui.get_file_input("src")

            print("Please provide the destination to store the combined files.")
            dst_path: Path = ui.get_file_input("dst")
            if compare_file_exts(file_1, file_2):
                break
    else:
        file_1: Path = ui.handle_file_input("src", src1)
        file_2: Path = ui.handle_file_input("src", src2)
        dst_path = ui.handle_file_input("dst", file_dst)
        if not compare_file_exts(file_1, file_2):
            return

    merged_file: Path = dst_path / f"{file_1.stem}_{file_2.name}"
    data: list = file_1.read_text().splitlines() + file_2.read_text().splitlines()
    if w_to_file(merged_file, data):
        print(
            f"{SUCCESS}: The files were merged. The merged file is located here: {str(merged_file)}"
        )
    else:
        print(f"{ERROR}: The files could not be merged successfully.")


def compare_file_exts(file_1: Path, file_2: Path) -> bool:
    valid_exts = [".txt", ".csv"]
    if check_file_ext(file_1, valid_exts) and check_file_ext(file_2, valid_exts):
        if file_1.suffix == file_2.suffix:
            print(f"{SUCCESS}: Both files to be combined are valid and the same")
            return True
        else:
            print(
                f"{ERROR}: The files provided are not of the same file type. Please try again"
            )
            return False
    else:
        print(
            f"{ERROR}: One of the files provided is not of the accepted file types. "
            f"These are the accepted file types: {','.join(valid_exts)}"
        )
        return False


def w_to_file(file: Path, data: list[str]) -> bool:
    """This function writes data to a file.

    Args:
        - file: This is the file that will be written to.
        - data: This is the data that will be written to the file.

    Returns:
        - return True if the file was successfully written to and false otherwise.
    """
    try:
        if not file.exists():
            file.touch()

        with file.open(mode="w", encoding="utf-8") as f:
            for line in data:
                f.write(line + "\n")
        return True
    except Exception as e:
        print(f"{ERROR}: Encountered the following error: {e}")
        return False


def check_file_ext(file: Path, valid_exts: list[str]) -> bool:
    """This function checks whether the file has an accepted file type.
    All accepted file types are defined in 'valid_exts.

    Args:
        - file: The file that is having its file extension validated.
        - valid_exts: All acceptable file types.

    Returns:
        - True if the file has a valid file extension and False otherwise.
    """
    ext = file.suffix
    if ext in valid_exts:
        return True
    return False


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
