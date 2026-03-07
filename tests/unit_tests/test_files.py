import pytest
from gct.lib import files
from gct.lib.utils import ERROR, SUCCESS


@pytest.fixture
def dir_path(tmp_path):
    src_path = tmp_path / "source"
    src_path.mkdir()
    return src_path


@pytest.fixture
def fake_path(tmp_path):
    fake_path = tmp_path / "not_created"
    return fake_path


@pytest.fixture
def txt_file_1(dir_path):
    f_path = dir_path / "test_1.txt"
    f_path.write_text(
        "This is a test text file.\n"
        "This is the second sentence.\n"
        "This is the third sencentce.\n"
    )
    return f_path


@pytest.fixture
def txt_file_2(dir_path):
    f_path = dir_path / "test_1.txt"
    f_path.write_text(
        "This is a test text file 2.\n"
        "Hello World.\n"
        "This should work or I will be sad\n"
    )
    return f_path


@pytest.fixture
def json_file(dir_path):
    f_path = dir_path / "test.json"
    f_path.write_text("This is DEFINITELY a json file.")
    return f_path


@pytest.fixture
def json_file_2(dir_path):
    f_path = dir_path / "test_2.json"
    f_path.write_text("This is DEFINITELY a json file.")
    return f_path


@pytest.fixture
def csv_file(dir_path):
    f_path = dir_path / "test.csv"
    f_path.write_text("one,two,three,four")
    return f_path


@pytest.fixture
def fake_file(dir_path):
    f_path = dir_path / "fake_file.txt"
    return f_path


@pytest.fixture
def dst_path(tmp_path):
    dst_path = tmp_path / "destination"
    dst_path.mkdir()
    return dst_path


def test_handle_src_file_1(txt_file_1):
    """
    This tests that handle_src_file returns true when it
    is given an existing src file.
    """
    result = files.handle_src_file(txt_file_1)
    assert result is True


def test_handle_src_file_2(dir_path):
    """
    Testing that handle_src_file return false when given just
    a directory path.
    """
    result = files.handle_src_file(dir_path)
    assert result is False


def test_handle_src_file_3(fake_path):
    """
    Testing that handle_src_file returns false when given a
    directory path that doesn't exist.
    """
    result = files.handle_src_file(fake_path)
    assert result is False


def test_handle_dst_file_1(dir_path):
    """
    This tests that handle_dts_file returns true when it is given
    an existing destination folder
    """

    result = files.handle_dst_file(dir_path)
    assert result is True


def test_handle_dst_file_2(txt_file_1, capsys):
    """
    This tests that handle_dst_file() returns false and outputs the
    correct text when a file path is provided to the function.
    """
    result = files.handle_dst_file(txt_file_1)
    output = capsys.readouterr().out.strip()
    expected_output = (
        f"{ERROR}: The destination path provided: {txt_file_1} is an already existing file. "
        "Please provide a path to a directory."
    )
    assert result is False
    assert output == expected_output


def test_handle_dst_file_3(fake_path, monkeypatch):
    """
    This tests that handle_dst_file() returns True and produces the correct
    output when a directory that doesn't exist is give to it.
    """
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    result = files.handle_dst_file(fake_path)
    assert result is True


def test_handle_dst_file_4(fake_path, monkeypatch, capsys):
    """
    his tests that handle_dst_file() returns False and produces the correct
    output when a directory that doesn't exist is given to it and user responds
    with 'no' to the user input prompt.
    """
    monkeypatch.setattr("builtins.input", lambda _: "no")
    result = files.handle_dst_file(fake_path)
    expected_output = (
        f"{ERROR}: Path doesn't exist and user does not want to create path."
    )

    output = capsys.readouterr().out.strip()
    assert result is False
    assert output == expected_output


def test_check_overwrite_file_1(txt_file_1, monkeypatch):
    """
    This tests check_overwrite_file() returns True when provided an already existing
    file and the user responds with yes.
    """
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    result = files.check_overwrite_file(txt_file_1)
    assert result is True


def test_check_overwrite_file_2(txt_file_1, monkeypatch):
    """
    This tests check_overwrite_file() returns False when provided an already existing
    file and the user responds with No.
    """
    monkeypatch.setattr("builtins.input", lambda _: "no")
    result = files.check_overwrite_file(txt_file_1)
    assert result is False


def test_check_overwrite_file_3(dir_path, capsys):
    """
    This tests check_overwrite_file() returns False when provided with a directory
    """
    result = files.check_overwrite_file(dir_path)
    output = capsys.readouterr().out.strip()
    expected_output = (
        f"{ERROR}: The path provided: {dir_path} is a directory, not a file."
    )
    assert result is False
    assert output == expected_output


def test_check_overwrite_file_4(fake_file):
    """
    This tests check_overwrite_file() returns True when provided a file path
    to a file that doesn't exist.
    """
    result = files.check_overwrite_file(fake_file)
    assert result is True


def test_exe_file_copy_1(txt_file_1, dst_path, capsys):
    """
    This tests exe_file_copy() produces the correct output when
    it successfully copies a file.
    """
    files.exe_file_copy(txt_file_1, dst_path)
    output = capsys.readouterr().out.strip()
    expected_output = (
        f"{SUCCESS}: File {txt_file_1.name} was successfully copied to {dst_path}"
    )

    assert output == expected_output


def test_merge_files_1_nominal_check(txt_file_1, txt_file_2, capsys, monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _: "yes")
    files.merge_files(False, txt_file_1, txt_file_2)
    out = capsys.readouterr().out.strip()
    exp_out = f"{SUCCESS}: The files were merged. The merged file is located here: "
    assert exp_out in out


def test_compare_file_exts_1_correct_input(txt_file_1, txt_file_2, capsys):
    """This function tests that compare_file_exts()

    It tests that the function prints a success message when the function
    is provided the correct input via the command line and returns True
    """
    ret_val: bool = files.compare_file_exts(txt_file_1, txt_file_2)
    out = capsys.readouterr().out.strip()
    exp_out = f"{SUCCESS}: Both files to be combined are valid and the same"

    assert ret_val is True
    assert exp_out in out


def test_compare_file_exts_2_diff_file_types(csv_file, txt_file_2, capsys):
    """This function tests that compare_file_exts()

    It tests that the function prints an error message when the function
    is provided two files with different file extensions via the command
    line and returns False
    """
    ret_val: bool = files.compare_file_exts(csv_file, txt_file_2)
    out = capsys.readouterr().out.strip()
    exp_out = (
        f"{ERROR}: The files provided are not of the same file type. Please try again"
    )

    assert ret_val is False
    assert exp_out in out


def test_compare_file_exts_3_invalid_file_type(json_file, json_file_2, capsys):
    """This function tests that compare_file_exts()

    It tests that the function prints an error message when the function
    is provided a file with an invalid file type.
    """
    ret_val: bool = files.compare_file_exts(json_file, json_file_2)
    out = capsys.readouterr().out.strip()
    exp_out = (
        f"{ERROR}: One of the files provided is not of the accepted file types. "
        f"These are the accepted file types:"
    )

    assert ret_val is False
    assert exp_out in out


def test_w_to_file_1_correct_input(txt_file_1):
    """This function tests the w_to_file() function.

    This is testing that the function returns True when provided with the
    correct inputs.
    """
    data = ["hello", "this is another line", "this is the final one"]
    ret_val = files.w_to_file(txt_file_1, data)
    assert ret_val is True


def test_check_file_ext_1_correct_input(txt_file_1):
    """This function tests the check_file_ext() function

    This is testing that the function returns true when provided
    correct inputs.
    """
    valid_exts = [".txt"]
    ret_val = files.check_file_ext(txt_file_1, valid_exts)
    assert ret_val is True


def test_check_file_ext_2_invalid_input(csv_file):
    """This function tests the check_file_ext() function

    This is testing that the function returns false when provided
    a file with an invalid file type.
    """
    valid_exts = [".txt"]
    ret_val = files.check_file_ext(csv_file, valid_exts)
    assert ret_val is False
