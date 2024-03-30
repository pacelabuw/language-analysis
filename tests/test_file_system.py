import os
import pytest

from pathlib import Path
from src import file_system
from src.constants import INPUT_DIR


@pytest.mark.unit
def test_input_dir_created_no_input_dir(tmp_path: Path):
    result = file_system.input_dir_was_created(tmp_path)
    assert result == True
    assert (tmp_path / INPUT_DIR).exists()


@pytest.mark.unit
def test_input_dir_created_with_input_dir(tmp_path: Path):
    os.mkdir(tmp_path / INPUT_DIR)
    result = file_system.input_dir_was_created(tmp_path)
    assert result == False


@pytest.mark.unit
def test_get_cha_files_no_files(tmp_path: Path):
    # Make the input dir but no files
    os.mkdir(tmp_path / INPUT_DIR)
    result = file_system.get_cha_files(tmp_path)
    assert result == []

@pytest.mark.unit
def test_get_cha_files_with_files(tmp_path: Path):
    input_dir = tmp_path / INPUT_DIR
    cha_files = ["file1.cha", "file2.cha", "file3.cha"]
    other_files = ["file4.png", "file5.chat", "file6.txt"]

    # Make the input dir and files
    os.mkdir(input_dir)
    for f in cha_files:
        (input_dir / f).touch()
    for f in other_files:
        (input_dir / f).touch()

    result = file_system.get_cha_files(tmp_path)

    assert len(result) == 3
    assert set(cha_files) == set(result)
