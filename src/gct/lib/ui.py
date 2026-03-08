"""
The ui.py module contains all functions that
are used to interface with the user. This includes
prompting the user and also handling and validating
the input from the user to ensure the tool functions
properly.
"""

from __future__ import annotations
import time
import sys
import os
from pathlib import Path

from gct.lib import menu
from gct.lib import files
from gct.lib.utils import ERROR, GREEN, END, WARNING


def get_menu_input(options: list[str]) -> int:
    """This function gets input from the user in response from
    the menu options displayed to the user.

    Args:
        - options: selections presented to the user to pick from.

    Return:
        - The number that corresponds the option the user has selected.
    """
    all_options = options + ["Exit"]
    # options.append("Exit")
    menu.display(all_options)
    user_input: int = handle_menu_input(len(all_options))
    return user_input


def handle_menu_input(max: int) -> bool:
    """This method insures the input from the user is valid.
    The method is valid if:
        - It is a number
        - The number greater than 0
        - The number is less than or equal to the number of options which is
          is stored in 'max'

    Args:
        - input: The user input that is to be verified/validated.
        - max: The maximum size the input can be. This is number of options
               the user selected from.
    """

    while True:
        raw_input = input("Select one of the following options above: ")

        if not raw_input.isdigit():
            print(
                f"{ERROR}: The input provided: {raw_input} is not a positive integer. "
                "Please provide a valid input."
            )
            continue

        int_input = int(raw_input)
        if int_input == max:
            print("Exiting app now...")
            time.sleep(1)
            sys.exit()
        elif 0 < int_input < max:
            return int_input
        else:
            print(
                f"{ERROR}: The value provided: {int_input} is outside of acceptable range. "
                f"Please provide an answer is within the range of 1 - {max}"
            )


def yes_no(prompt: str) -> bool:
    """This method prompts the user with a yes or no question

    Args:
        - prompt: is the yes/no question that will be asked to the user.

    Return:
        - True if the user says yes and False if the user says no.
    """
    while True:
        usr_input = input(prompt + "(yes/no): ").lower()
        if usr_input in ["n", "no"]:
            return False
        elif usr_input in ["y", "yes"]:
            return True
        else:
            print(
                f"{ERROR}: Invalid input was provided. Please respond with either yes or no."
            )


def get_file_input(file_type: str) -> Path:
    """This function retrieves file path related input from the user.

    Args:
        - file_type: This is the filepath type. There are 3 accetable types:
            - src: which means the file should already exist and will be checked
                for that
            - dst: which means this location may not exists and will be created
                if it doesn't exist.
            - name: which means this should just be a file name.
    Return:
        - A validated file path as a Path object.
    """
    valid_types = ["src", "dst", "name"]

    try:
        if file_type.lower() not in valid_types:
            raise TypeError(
                f"The provide value ({file_type}) for input arguemnt 'type' is invalid."
                " Valid values for input agrument 'type' are: 'src', 'dst', or 'name' "
            )
        while True:
            # print(f"Please input the {file_type} of file.")
            raw_input = input(f"{file_type.upper()}: ")
            handled_input = handle_file_input(file_type, raw_input)
            if handled_input is not None:
                return handled_input
    except TypeError as e:
        print(e)
        print("Fix error and re-run tool. Exiting tool now...")
        time.sleep(1)
        sys.exit()


def handle_file_input(file_type: str, raw_input: str) -> Path:
    """This function validates that the user provided path.
    The existance of the path is dependant on the file type. This
    is handled later.

    Args:
        - file_type: This is the filepath type. There are two accetable types:

    Return:
        - A Path object containing the validated file path or None if there is an issue.
    """
    if not raw_input:
        if file_type == "dst":
            default = Path.cwd() / "files"
            print(
                f"{WARNING}: Since a destination file path was not provided, the default path: "
                f"{default} will be used instead.]"
            )
            raw_input = Path.cwd() / "files"
        else:
            print(f"{ERROR}: A source path was not provided. Please try again")
            return None
    else:
        raw_input = Path(raw_input)

    # Validating user input.
    if file_type == "src":
        if files.handle_src_file(raw_input):
            print(GREEN + "Source file found" + END)
            return raw_input
        return None
    elif file_type == "name":
        return raw_input
    else:
        if files.handle_dst_file(raw_input):
            return raw_input
        else:
            return None
