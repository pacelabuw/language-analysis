from src import constants


class Word:
    cleaned_word: str
    language: str
    is_mlu_ignored: bool = False
    is_code_switched: bool = False

    def __init__(
        self,
        word: str,
        active_language: str,
        alternate_language: str,
        is_mlu_ignored: bool
    ):
        if constants.CODE_SWITCH in word:
            self.is_code_switched = True
            self.language = alternate_language
        else:
            self.language = active_language

        if constants.FALSE_START in word or constants.REPEAT in word:
            self.is_mlu_ignored = True
        else:
            self.is_mlu_ignored = is_mlu_ignored

        self._clean_word(word)

    def _clean_word(self, word: str) -> None:
        word = word.split("@")[0]  # Ignore end tags

        for p in constants.TOKEN_REPLACE:
            word = word.replace(p, "")

        self.cleaned_word =  word


class Utterance:
    language: str
    is_mixed: bool
    words: list[Word]

    def __init__(self, utterance: str, primary_language: str, secondary_language: str):
        self.is_mixed = False
        self.words = []
        words = utterance.split(" ")

        if words[0] == "[-":
            words = words [2:]  # Remove the tag
            self.language = secondary_language
            alternate_language = primary_language
        else:
            self.language = primary_language
            alternate_language = secondary_language

        in_phrase = False
        for i in range(len(words)):
            next_word = words[i+1] if i < len(words) - 1 else None
            should_mlu_ignore = next_word == constants.REPEAT or next_word == constants.FALSE_START
            if not in_phrase:
                in_phrase = words[i].startswith(constants.PHRASE_START)
            if in_phrase:
                in_phrase = not words[i].endswith(constants.PHRASE_END)

            if not self._starts_with_ignored_symbol(words[i]):
                new_word = Word(
                    words[i],
                    active_language=self.language,
                    alternate_language=alternate_language,
                    is_mlu_ignored=in_phrase or should_mlu_ignore
                )
                self.is_mixed = self.is_mixed or new_word.is_code_switched
                self.words.append(new_word)


    def _starts_with_ignored_symbol(self, word: str) -> None:
        for ignore_symbol in constants.IGNORE_STARTS_WITH:
            if word.startswith(ignore_symbol):
                return True
        return False


        
