from src.constants import CODE_SWITCH, PHRASE_START, PHRASE_END
from src.models import Utterance

class ParticipantResult:
    languages: list[str]
    language_utterance_counts: dict[str, int] = {}
    language_mlu_counts: dict[str, float] = {}
    language_type_counts: dict[str, int] = {}
    language_token_counts: dict[str, int] = {}
    total_utterance_count: int = 0
    mixed_utterance_count: int = 0
    total_mlu: float = 0
    utterances: list[Utterance]

    def __init__(self, languages: list[str], utterances: list[str]):
        self.languages = languages
        self.language_utterance_counts = {}
        self.language_mlu_counts = {}
        self.language_type_counts = {}
        self.language_token_counts = {}
        self.total_utterance_count = len(utterances)
        self.mixed_utterance_count = 0
        self.total_mlu = 0
        self.utterances = [
            Utterance(u, primary_language=languages[0], secondary_language=languages[1])
            for u in utterances
        ]
        total_mlu_words = 0

        for utterance in self.utterances:
            if utterance.is_mixed:
                self.mixed_utterance_count += 1

        for language in languages:
            self._count_language_utterances(language)
            total_mlu_words += self._calculate_language_mlu(language)
            self._count_tokens_and_types(language)

        self.total_mlu = total_mlu_words / self.total_utterance_count

    def _count_language_utterances(self, language: str) -> None:
        """Count utterances by language, assume first language is primary."""
        count = 0
        for utterance in self.utterances:
            if utterance.language == language and not utterance.is_mixed:
                count += 1

        self.language_utterance_counts[language] = count

    def _calculate_language_mlu(self, language) -> int:
        """Find mean number of words per utterance for each language.

        Returns the total words used for language specific mlu, need for finding total mlu.
        """
        word_count = 0
        for utterance in self.utterances:
            word_count += utterance.get_mlu_word_count(language)

        utterance_count = self.mixed_utterance_count + self.language_utterance_counts[language]
        self.language_mlu_counts[language] = word_count / utterance_count
        return word_count
    
    def _count_tokens_and_types(self, language: str) -> None:
        """Find tokens (cleaned words) and types (unique words) in all utterances by language."""
        tokens = []
        for utterance in self.utterances:
            tokens += utterance.get_tokens(language)

        self.language_token_counts[language] = len(tokens)
        self.language_type_counts[language] = len(set(tokens))
