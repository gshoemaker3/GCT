import time
import sys

from cli_tool.lib import display

def get_input(options: list[str]) -> int:
    """ This function gets input from the user in response from 
        the options displayed to the user.

        Args:
            - options: selections presented to the user to pick from.
        
        Return:
            - The number that corresponds the option the user has selected.
    """
    options.append("Exit")
    display(options)
    user_input: int = handle_user_input(len(options))
    return user_input


def handle_user_input(max: int) -> bool:
    """ This method insures the input from the user is valid.
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
    RED = "\033[31m"
    END = "\033[0m"
    while True:
        raw_input = input("Select one of the following options above: ")

        if not raw_input.isdigit():
            print(f"{RED}ERROR{END}: The input provided: {raw_input} is not a positive integer. Please provide a valid input")
            continue

        int_input = int(raw_input)
        if int_input == max:
            print("Exiting app now...")
            time.sleep(1)
            sys.exit()
        elif 0 < int_input < max:
            return int_input
        else:
            print(f"{RED}ERROR{END}:  The value provided: {int_input} is outside of acceptable range."
                  f"Please provide an answer is within the range of 1 - {max}")
