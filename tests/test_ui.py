from gct.lib import ui

def test_get_input_1(monkeypatch):
    """Testing that a valid user input works."""
    monkeypatch.setattr('builtins.input', lambda _: "1")
    options = ["one", "two", "three"]
    answer = ui.get_menu_input(options)
    assert answer == 1

def test_get_menu_input_2(monkeypatch):
    """ 
        Testing that a valid user input is returned even after multiple
        invalid responses are provided. The correct input is 1 while the
        other simulated responses are invalid responses.
    """

    # simulating inputs
    inputs = iter(["hello", "wrong", "34", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # establishing variables
    options = ["one", "two", "three"]
    answer = ui.get_menu_input(options)

    # validating function return value
    assert answer == 1


def test_handle_menu_input_1(monkeypatch, capsys):
    """Testing that entering a word or string results in an error output"""

    # simulating user input
    inputs = iter(["hello", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # establishing variables
    RED = "\033[31m"
    END = "\033[0m"
    options = ["one", "two", "three", "four"]
    expected_output = (f"{RED}ERROR{END}: The input provided: hello is not a positive integer. Please provide a valid input.")

    # capturing function console output 
    ui.handle_menu_input(len(options))
    output = capsys.readouterr()

    # validating input.
    assert output.out.strip() == expected_output

def test_handle_menu_input_2(monkeypatch, capsys):
    """ 
        Testing that entering a integer not within acceptable bounds
        results in an error output
    """

    # simulating input
    inputs = iter(["14", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # establishing variables
    RED = "\033[31m"
    END = "\033[0m"
    options = ["one", "two", "three", "four"]
    expected_output = (f"{RED}ERROR{END}: The value provided: 14 is outside of acceptable range."
                       f" Please provide an answer is within the range of 1 - {len(options)}")

    # capturing console output
    ui.handle_menu_input(len(options))
    output = capsys.readouterr()

    # validating
    assert output.out.strip() == expected_output

def test_yes_no_1(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'yes'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "yes")
    result = ui.yes_no(prompt)

    assert result is True


def test_yes_no_2(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'YES'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "YES")
    result = ui.yes_no(prompt)

    assert result is True


def test_yes_no_3(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'y'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "y")
    result = ui.yes_no(prompt)

    assert result is True


def test_yes_no_4(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'Y'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    result = ui.yes_no(prompt)

    assert result is True


def test_yes_no_5(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'yEs'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "yEs")
    result = ui.yes_no(prompt)

    assert result is True

def test_yes_no_6(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'no'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "no")
    result = ui.yes_no(prompt)

    assert result is False


def test_yes_no_7(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'NO'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "NO")
    result = ui.yes_no(prompt)

    assert result is False


def test_yes_no_8(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'No'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "No")
    result = ui.yes_no(prompt)

    assert result is False


def test_yes_no_9(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'n'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "n")
    result = ui.yes_no(prompt)

    assert result is False


def test_yes_no_10(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        'N'
    """
    prompt = "A statement asking the user a question"
    monkeypatch.setattr('builtins.input', lambda _: "N")
    result = ui.yes_no(prompt)

    assert result is False


def test_yes_no_11(monkeypatch):
    """
        Tests that yes_no() returns True with the user inputs
        an invalid response then a 'yes'
    """
    prompt = "A statement asking the user a question"
    inputs = iter(["hello", "yes"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = ui.yes_no(prompt)

    assert result is True