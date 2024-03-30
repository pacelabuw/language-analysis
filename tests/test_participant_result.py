from unittest.mock import Mock
import pytest

from src.participant_result import ParticipantResult
from src import bother_user

UTTERANCES_1 = [
    "[- eng] <b> [//] butterfly .",
    "hay [?] una butterfly@s .",
    "pata [?] .",
    "no [/] no [/] no [/] no [/] no .",
    "[- eng] butterfly .",
]
UTTERANCES_2 = [
    "[- eng] butterfly .",
    "<bueno tecnicamente> [//] tal vez no si no sabes .",
    "cuántos son ?",
    "palo stick@s .",
    "<mira y aquí hay una> [//] quién esta acá ?",
    "ya casi acabamos con el libro xxx .",
    "okay .",
    "ya no quieres jugar [?] .",
    "uh uh .",
    "si butterfly@s .",
]
UTTERANCES_3 = [
    "a ver sácalo .",
    "sácalo .",
    "&=gasps qué es ?",
    "un libro!",
    "oh no[/] no[/] no[/] no !",
    "<esto no> [/] esto no .",
    "esto se queda aquí .",
    "está no .",
    "aquí dice .",
    "[- eng] have you seen my duckling ?",
    "has visto el patito ?",
    "xxx .",
]


def _assert_utterance_counts(
    result: ParticipantResult, total: int, mixed: int, spa: int, eng: int
) -> None:
    assert result.total_utterance_count == total
    assert result.mixed_utterance_count == mixed
    assert result.language_utterance_counts["spa"] == spa
    assert result.language_utterance_counts["eng"] == eng


def _assert_mlu_counts(result: ParticipantResult, total: float, spa: float, eng: float) -> None:
    assert round(result.total_mlu, 1) == total
    assert round(result.language_mlu_counts["spa"], 1) == spa
    assert round(result.language_mlu_counts["eng"], 1) == eng


def _assert_type_and_token_counts(
    result: ParticipantResult, type_spa: int, token_spa: int, type_eng: int, token_eng: int
) -> None:
    assert result.language_type_counts["spa"] == type_spa
    assert result.language_token_counts["spa"] == token_spa
    assert result.language_type_counts["eng"] == type_eng
    assert result.language_token_counts["eng"] == token_eng


@pytest.mark.unit
def test_utterance_1_result(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(bother_user, "is_this_a_token", Mock(return_value=False))
    result = ParticipantResult(["spa", "eng"], UTTERANCES_1)

    _assert_utterance_counts(result, 5, 1, 2, 2)
    _assert_mlu_counts(result, 1.4, 1.3, 1.0)
    _assert_type_and_token_counts(result, 4, 8, 1, 3)


@pytest.mark.unit
def test_utterance_2_result():
    result = ParticipantResult(["spa", "eng"], UTTERANCES_2)

    _assert_utterance_counts(result, 10, 2, 7, 1)
    _assert_mlu_counts(result, 3.0, 3.0, 1.0)
    _assert_type_and_token_counts(result, 29, 34, 2, 3)


@pytest.mark.unit
def test_utterance_3_result():
    result = ParticipantResult(["spa", "eng"], UTTERANCES_3)

    _assert_utterance_counts(result, 12, 0, 11, 1)
    _assert_mlu_counts(result, 2.5, 2.3, 5.0)
    _assert_type_and_token_counts(result, 21, 30, 5, 5)
