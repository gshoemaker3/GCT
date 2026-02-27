def display(options: list[str]) -> None:
    """
    This function is used to display all options stored
    in 'options' to the user to select from.
    
    :param options: A list of strings that will be displayed to the user.
    :type options: list
    """
    for idx, option in enumerate(options):
        print(f"{idx+1}.) {option}")