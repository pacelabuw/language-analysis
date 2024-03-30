# Data directories
INPUT_DIR = "input"
RESULT_FILE = "results.csv"

# Meta data header tags
LANGUAGE_TAG = "@Languages"
PARTICIPANTS_TAG = "@Participants"

# Things to ignore in file
PUNCTUATION = ["?", "!", "."]
REPEAT = "[/]"
FALSE_START = "[//]"
IGNORE_STARTS_WITH = ["&=", "["] + PUNCTUATION
