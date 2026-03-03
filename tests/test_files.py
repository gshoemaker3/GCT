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
def txt_file(dir_path):
    f_path = dir_path / "test.txt"
    f_path.write_text("This is a test text file.")
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


def test_handle_src_file_1(txt_file):
    """
    This tests that handle_src_file returns true when it
    is given an existing src file.
    """
    result = files.handle_src_file(txt_file)
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


def test_handle_dst_file_2(txt_file, capsys):
    """
    This tests that handle_dst_file() returns false and outputs the
    correct text when a file path is provided to the function.
    """
    result = files.handle_dst_file(txt_file)
    output = capsys.readouterr().out.strip()
    expected_output = (
        f"{ERROR}: The destination path provided: {txt_file} is an already existing file. "
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


def test_check_overwrite_file_1(txt_file, monkeypatch):
    """
    This tests check_overwrite_file() returns True when provided an already existing
    file and the user responds with yes.
    """
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    result = files.check_overwrite_file(txt_file)
    assert result is True


def test_check_overwrite_file_2(txt_file, monkeypatch):
    """
    This tests check_overwrite_file() returns False when provided an already existing
    file and the user responds with No.
    """
    monkeypatch.setattr("builtins.input", lambda _: "no")
    result = files.check_overwrite_file(txt_file)
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


def test_exe_file_copy_1(txt_file, dst_path, capsys):
    """
    This tests exe_file_copy() produces the correct output when
    it successfully copies a file.
    """
    files.exe_file_copy(txt_file, dst_path)
    output = capsys.readouterr().out.strip()
    expected_output = (
        f"{SUCCESS}: File {txt_file.name} was successfully copied to {dst_path}"
    )

    assert output == expected_output
