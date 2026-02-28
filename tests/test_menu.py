import pytest

from cli_tool.lib import display, has_non_string

def test_display_1(capsys):
    display(["one", "two", "three"])
    captured = capsys.readouterr()
    assert captured.out == "1.) one\n2.) two\n3.) three\n"

def test_display_2(capsys):
    display(["one", "two", 3])
    captured = capsys.readouterr()
    assert captured.out.strip() == "Error: Options must be of type str"

def test_has_non_string_1():
    """test has_non_string() method for all strings list"""
    ret_val = has_non_string(["one", "hello", "strings"])
    assert ret_val is False


def test_has_non_string_2():
    """Test has_non_string() method with different types in list"""
    import logging
    ret_val = has_non_string(["hello", 4, 3.456, logging.getLogger(), "end"])
    assert ret_val is True