from src import file_system

def run() -> None:
    """The whole enchilada."""
    if file_system.input_dir_was_created():
        # We don't have anything to do
        return
    
    ## Do all the other cool stuff here
