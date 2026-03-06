import subprocess
import pytest

TOOL_PATH = "dist/gct"


@pytest.fixture
def dir_path(tmp_path):
    src_path = tmp_path / "source"
    src_path.mkdir()
    return src_path


@pytest.fixture
def txt_file(dir_path):
    f_path = dir_path / "test.txt"
    f_path.write_text("This is a test text file.")
    return f_path


@pytest.fixture
def dst_path(tmp_path):
    dst_path = tmp_path / "destination"
    dst_path.mkdir()
    return dst_path


def test_tool_runs():
    result = subprocess.run([TOOL_PATH], capture_output=True, text=True)
    assert result.returncode == 0


def test_tool_expected_output(txt_file, dst_path):
    result = subprocess.run(
        [TOOL_PATH, "cp", "-s", txt_file, "-d", dst_path],
        capture_output=True,
        text=True,
    )
    assert "expected output" in result.stdout
