import os

from pathlib import Path
from src.constants import INPUT_DIR


def input_dir_was_created(dir: Path) -> bool:
    input_dir = dir / INPUT_DIR
    if input_dir.exists():
        return False
    
    os.mkdir(input_dir)
    print("Created directory `input`. Please put CHA files to analyze in it and run again.")
    return True

def get_cha_files(dir: Path):
    """Collect all CHA files from input dir."""
    files = os.listdir(dir / INPUT_DIR)

    return [f for f in files if f.endswith(".cha")]
