"""
This module contains the main execution loop when the
tool is in interactive mode as well as some of the basic
usage of each tool that is displayed to the user once
a function is selected from the menu.
"""

from gct.lib import files, ui


def run():
    """The main execution loop for interactive mode."""
    options = ["Copy File", "Combine Files", "Create File"]
    # title()
    while True:
        title()
        print("These are the available options to select from:")
        usr_input = ui.get_menu_input(options)
        if usr_input == 1:
            copy_file_usage()
            files.copy_file(True)
        elif usr_input == 2:
            merge_files_usage()
            files.merge_files(True)
        else:
            create_file_usage()
            files.create_file(True)


def title():
    """This prints the title and usage of the tool"""
    print("\n=================================================================")
    print("             Garrett's CLI Tool (GCT) Interactive Menu.         ")
    print("=================================================================\n")
    print(
        "- This mode allows the user to select the file operation they\n"
        "  want via an interactive menu instead of command line arguments.\n"
        "- Select an option by selecting the number that is to the left\n"
        "  of the text.\n"
        "- The 'Exit' option will allow you to exit the tool"
    )
    print("\n=================================================================")
    print("=================================================================\n")


def create_file_usage():
    """This prints off the usage of the create file function"""
    print(
        "\n================================================================================"
    )
    print(
        "                              FILE CREATION USAGE                               "
    )
    print(
        "================================================================================\n"
    )
    print(
        "This will allow you to create an empty file of any file type.\n\n"
        "REQUIREMENTS:\n"
        "  - A name must be provided for the file to be created.\n\n"
        "OPTIONALS:\n"
        "  - A destination path for the newly created file is not required. If a path is\n"
        "    not provided, the default path will be used."
    )
    print(
        "\n================================================================================"
    )
    print(
        "================================================================================\n"
    )


def copy_file_usage():
    """This prints out the usage of the file copy function"""
    print(
        "\n============================================================================"
    )
    print(
        "                               FILE COPY USAGE                                "
    )
    print(
        "============================================================================\n"
    )
    print(
        "Currently the copy file function has only been tested to support\n "
        "local-to-local file copies.\n"
        "It DOES NOT support:\n"
        "  - copying files from remote locations to local locations\n"
        "  - copying local files to remote locations\n"
        "  - copying remote files to other remote locations.\n\n"
        "REQUIREMENTS:\n"
        "  - A source path to a file must be provided.\n"
        "  - A destination path is optional. If one is not provided, a default\n "
        "    destination path will be used instead\n"
        "  - The destination path has to be to a directory/folder. it cannot be a file"
    )
    print(
        "\n============================================================================"
    )
    print(
        "============================================================================\n"
    )


def merge_files_usage():
    """This prints out the usage of the combine files function"""
    print(
        "\n============================================================================"
    )
    print("                            FILE COMBINE USAGE                            ")
    print(
        "============================================================================\n"
    )
    print(
        "Currently the combine file function can only combine .txt and .csv files.\n"
        "Additional file type support will be added in the future.\n\n"
        "REQUIREMENTS:\n"
        "  - A source path to both of the files to be combined.\n"
        "  - Both source files must be of the same file type.\n\n"
        "OPTIONALS:\n"
        "  - A destination path is not required. If one isn't provided,\n"
        "    the default path will be used instead."
    )
    print(
        "\n============================================================================"
    )
    print(
        "============================================================================\n"
    )
