# Data directories
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Meta data header tags
LANGUAGE_TAG = "@Languages"
PARTICIPANTS_TAG = "@Participants"

# Things to ignore in file
PUNCTUATION = ["?", "!", "."]
REPEAT = "[/]"
FALSE_START = "[//]"
IGNORE_STARTS_WITH = ["&=", "["] + PUNCTUATION
