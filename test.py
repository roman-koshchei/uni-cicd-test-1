import os
import pytest
import tempfile
import argparse
import subprocess
import sys

# Import the functions from the original script
from main import read_unique_lines, write_unique_lines, validate_txt_file, main


# Fixture for creating temporary text files
@pytest.fixture
def temp_txt_file():
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as temp_file:
        yield temp_file.name
    # Clean up the file after the test
    os.unlink(temp_file.name)


# Fixture for creating multiple temporary text files
@pytest.fixture
def multiple_temp_txt_files():
    files = []
    for _ in range(2):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as temp_file:
            files.append(temp_file.name)
    yield files
    # Clean up the files after the test
    for file in files:
        os.unlink(file)


# Parametrized test for read_unique_lines function
@pytest.mark.parametrize(
    "file_content,expected",
    [
        (["hello", "world", "hello"], {"hello", "world"}),
        (["  hello  ", "world", "  hello"], {"hello", "world"}),
        ([], set()),
    ],
)
def test_read_unique_lines(temp_txt_file, file_content, expected):
    # Write test content to the temporary file
    with open(temp_txt_file, "w") as f:
        for line in file_content:
            f.write(line + "\n")

    # Test the function
    result = read_unique_lines(temp_txt_file)
    assert result == expected


# Test read_unique_lines error handling
def test_read_unique_lines_nonexistent_file():
    result = read_unique_lines("nonexistent_file.txt")
    assert result is None


# Parametrized test for write_unique_lines function
@pytest.mark.parametrize(
    "lines,expected_content",
    [
        ({"world", "hello"}, ["hello", "world"]),
        (set(), []),
        ({"  world  ", " hello"}, ["hello", "world"]),
    ],
)
def test_write_unique_lines(temp_txt_file, lines, expected_content):
    # Test writing unique lines
    result = write_unique_lines(temp_txt_file, lines)
    assert result is True

    # Verify file content
    with open(temp_txt_file, "r") as f:
        # Read lines, strip whitespace, and sort
        file_lines = [line.strip() for line in f.readlines()]

        # Sort both the file lines and expected content
        file_lines.sort()
        expected_content.sort()

        # Compare sorted lists
        assert file_lines == expected_content


# Test write_unique_lines with permission error (simulated)
def test_write_unique_lines_error(monkeypatch):
    def mock_open(*args, **kwargs):
        raise OSError("Simulated permission error")

    monkeypatch.setattr("builtins.open", mock_open)
    result = write_unique_lines("some_file.txt", {"test"})
    assert result is False


# Parametrized test for validate_txt_file function
@pytest.mark.parametrize(
    "filename,should_raise",
    [
        ("test.txt", False),
        ("test.TXT", False),
        ("test.doc", True),
        ("nonexistent.txt", True),
    ],
)
def test_validate_txt_file(temp_txt_file, filename, should_raise):
    if should_raise:
        with pytest.raises(argparse.ArgumentTypeError):
            validate_txt_file(filename)
    else:
        # Ensure the file exists for successful validation
        with open(temp_txt_file, "w") as f:
            f.write("test")
        result = validate_txt_file(temp_txt_file)
        assert result == temp_txt_file


# Integration test for main function
def test_main_integration(multiple_temp_txt_files):
    file1, file2 = multiple_temp_txt_files

    # Prepare test files
    with open(file1, "w") as f1:
        f1.write("hello\nworld\n")

    with open(file2, "w") as f2:
        f2.write("world\npython\n")

    # Simulate command-line arguments
    sys.argv = ["main.py", file1, file2, "--same", "same.txt", "--diff", "diff.txt"]

    # Capture stdout
    captured = subprocess.run(
        [sys.executable, "main.py", file1, file2], capture_output=True, text=True
    )

    # Verify output files are created
    assert os.path.exists("same.txt")
    assert os.path.exists("diff.txt")

    # Verify same.txt content
    with open("same.txt", "r") as f:
        assert f.read().strip() == "world"

    # Verify diff.txt content
    with open("diff.txt", "r") as f:
        assert set(f.read().strip().split("\n")) == {"hello", "python"}

    # Clean up
    os.unlink("same.txt")
    os.unlink("diff.txt")
