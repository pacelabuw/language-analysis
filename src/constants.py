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
CODE_SWITCH = "@s"
OTOMATOPEIA = "@o"
MADEUP_WORD = "@c"
PHRASE_START = "<"
PHRASE_END = ">"
IGNORE_STARTS_WITH = ["&=", "&-", "["] + PUNCTUATION
TOKEN_REPLACE = [PHRASE_START, PHRASE_END, "(", ")"] + PUNCTUATION
