from src.constants import (
    CODE_SWITCH, FALSE_START, IGNORE_STARTS_WITH, PHRASE_START, PHRASE_END, REPEAT, TOKEN_REPLACE
)
from src import bother_user

class ParticipantResult:
    languages: list[str]
    language_utterance_counts: dict[str, int] = {}
    language_mlu_counts: dict[str, float] = {}
    language_type_counts: dict[str, int] = {}
    language_token_counts: dict[str, int] = {}
    total_utterance_count: int = 0
    mixed_utterance_count: int = 0
    total_mlu: float = 0
    utterances: list[str]

    def __init__(self, languages: list[str], utterances: list[str]):
        self.languages = languages
        self.total_utterance_count = len(utterances)
        self.utterances = utterances
        total_mlu_words = 0

        for language in languages:
            self._count_language_utterances(language)
            total_mlu_words += self._calculate_language_mlu(language)
            self._count_tokens_and_types(language)

        self.total_mlu = total_mlu_words / self.total_utterance_count

    def _count_language_utterances(self, language: str) -> None:
        """Count utterances by language, assume first language is primary."""
        count = 0
        is_primary_language = language == self.languages[0]
        for utterance in self.utterances:
            is_utterance_nonprimary = utterance.startswith("[- ")
            is_utterance_mixed = CODE_SWITCH in utterance  # Code switching will always be in mixed

            if is_primary_language and is_utterance_mixed:
                # We only check mixed on primary to ensure no double counting
                self.mixed_utterance_count += 1
            elif is_primary_language and not is_utterance_nonprimary:
                count += 1
            elif not is_primary_language and is_utterance_nonprimary:
                count += 1

        self.language_utterance_counts[language] = count

    def _calculate_language_mlu(self, language) -> int:
        """Find mean number of words per utterance for each language.
        
        Follows a few rules:
          - Ignores words before [/] or [//]
          - Ignores phrases in <> before [/] or [//]
          - Ignores punctuation

        Returns the total words used for language specific mlu, need for finding total mlu.
        """
        word_count = 0
        for utterance in self.utterances:
            words = utterance.split(" ")
            utterance_language = self._get_utterance_language(words)  # Assume primary language

            if utterance_language != self.languages[0] and utterance_language != language:
                # This is not the utterance we are looking for
                continue

            is_ignored_phrase = False
            for i in range(len(words)):
                next_word = words[i+1] if i < len(words) - 1 else None
                if self._mlu_should_ignore_word(words[i], is_ignored_phrase, next_word):
                    if not is_ignored_phrase:
                        is_ignored_phrase = words[i].startswith(PHRASE_START)
                    if is_ignored_phrase:
                        is_ignored_phrase = not words[i].endswith(PHRASE_END)
                    continue

                if utterance_language == self.languages[0] and language == self.languages[0]:
                    if not words[i].endswith(CODE_SWITCH):
                        word_count += 1  # Count non code switched words when looking at primary
                elif utterance_language != language and language != self.languages[0]:
                    if words[i].endswith(CODE_SWITCH):
                        word_count += 1  # Count code switched words for non primary language
                elif utterance_language == language and language != self.languages[0]:
                    word_count += 1  # Gotta count em all

        utterance_count = self.mixed_utterance_count + self.language_utterance_counts[language]
        self.language_mlu_counts[language] = word_count / utterance_count
        return word_count
    
    def _count_tokens_and_types(self, language: str) -> None:
        """Find tokens (cleaned words) and types (unique words) in all utterances by language."""
        tokens = []
        for utterance in self.utterances:
            words = utterance.split(" ")
            utterance_language = self._get_utterance_language(words)  # Assume primary language

            if utterance_language != self.languages[0] and utterance_language != language:
                # This is not the utterance we are looking for
                continue

            for word in words:
                should_bother_user = word.startswith(PHRASE_START) and word.endswith(PHRASE_END)
                if should_bother_user and not bother_user.is_this_a_token(word):
                    continue
                elif self._starts_with_ignored_symbol(word):
                    continue
                elif utterance_language == language and language == self.languages[0]:
                    if not word.endswith(CODE_SWITCH):
                        tokens.append(self._clean_word(word))
                elif utterance_language == language and language != self.languages[0]:
                    tokens.append(self._clean_word(word))
                elif utterance_language != language and language != self.languages[0]:
                    if word.endswith(CODE_SWITCH):
                        tokens.append(self._clean_word(word))

        self.language_token_counts[language] = len(tokens)
        self.language_type_counts[language] = len(set(tokens))
    
    def _mlu_should_ignore_word(
        self, word: str, is_ignored_phrase: bool, next_word: str | None
    ) -> bool:
        if is_ignored_phrase:
            # Keep skipping a phrase until we hit the end
            return True
        elif word.startswith(PHRASE_START):
            return True
        elif self._includes_repeat_or_false_start(word):
            return True
        elif next_word is not None and self._startswith_repeat_or_false_start(next_word):
            return True
        elif self._starts_with_ignored_symbol(word):
            return True
        return False

    def _includes_repeat_or_false_start(self, word: str) -> bool:
        return FALSE_START in word or REPEAT in word
    
    def _startswith_repeat_or_false_start(self, word: str) -> bool:
        return word.startswith(FALSE_START) or word.startswith(REPEAT)
    
    def _starts_with_ignored_symbol(self, word: str) -> bool:
        for ignore_symbol in IGNORE_STARTS_WITH:
            if word.startswith(ignore_symbol):
                return True
        return False
    
    def _get_utterance_language(self, words: list[str]) -> str:
        """Check if utterance has a language tag, if it does get language or use primary."""
        utterance_language = self.languages[0]
        if words[0] == "[-":
            # There is a tag in front of the utterance, not the primary language
            words.pop(0)
            utterance_language = words.pop(0).rstrip("]")
        return utterance_language
    
    def _clean_word(self, word: str) -> str:
        word = word.split("@")[0]  # Ignore end tags

        for p in TOKEN_REPLACE:
            word = word.replace(p, "")

        return word
