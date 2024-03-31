import os

from pathlib import Path
from src.constants import INPUT_DIR


def input_dir_was_created(dir: Path = Path(os.getcwd())) -> bool:
    input_dir = dir / INPUT_DIR
    if input_dir.exists():
        return False
    
    os.mkdir(input_dir)
    print("Created directory `input`. Please put CHA files to analyze in it and run again.")
    return True

def get_cha_files(dir: Path = Path(os.getcwd())):
    """Collect all CHA files from input dir."""
    files = os.listdir(dir / INPUT_DIR)

    return [dir / INPUT_DIR / f for f in files if f.endswith(".cha")]
