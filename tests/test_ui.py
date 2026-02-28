from cli_tool.lib import ui

def test_get_input_1(monkeypatch):
    """Testing that a valid user input works."""
    monkeypatch.setattr('builtins.input', lambda _: "1")
    options = ["one", "two", "three"]
    answer = ui.get_input(options)
    assert answer == 1

def test_get_input_2(monkeypatch):
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
    answer = ui.get_input(options)

    # validating function return value
    assert answer == 1


def test_handle_user_input_1(monkeypatch, capsys):
    """Testing that entering a word or string results in an error output"""

    # simulating user input
    inputs = iter(["hello", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # establishing variables
    RED = "\033[31m"
    END = "\033[0m"
    options = ["one", "two", "three", "four"]
    expected_output = (f"{RED}ERROR{END}: The input provided: hello is not a positive integer. "
                         "Please provide a valid input")

    # capturing function console output 
    ui.handle_user_input(len(options))
    output = capsys.readouterr()

    # validating input.
    assert output.out.strip() == expected_output

def test_handle_user_input_2(monkeypatch, capsys):
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
    expected_output = (f"{RED}ERROR{END}:  The value provided: 14 is outside of acceptable range."
                       f"Please provide an answer is within the range of 1 - {len(options)}")

    # capturing console output
    ui.handle_user_input(len(options))
    output = capsys.readouterr()

    # validating
    assert output.out.strip() == expected_output