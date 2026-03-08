"""
The menu.py module contains the functions to create and display menus to the user
when the tool is in interactive mode.
"""

from __future__ import annotations


def display(options: list[str]) -> None:
    """
    This function is used to display all options stored
    in 'options' to the user to select from.

    Args:
        - options: A list of strings that will be displayed to the user.
    """
    try:
        if has_non_string(options):
            raise TypeError("Error: Options must be of type str")

        for idx, option in enumerate(options):
            print(f"{idx+1}.) {option}")

    except TypeError as e:
        print(e)


def has_non_string(target: list) -> bool:
    """
    This function checks if a list has any other types besides strings.

    Args:
        - target: the list that will be checked for types other than string.
    """
    return any(not isinstance(element, str) for element in target)
