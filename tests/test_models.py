import pytest
from unittest.mock import Mock

from src.models import Utterance, Word
from src import bother_user


def _assert_word(word: Word, language: str, is_code_switched: bool, is_mlu_ignored: bool):
    assert word.language == language
    assert word.is_code_switched == is_code_switched
    assert word.is_mlu_ignored == is_mlu_ignored

@pytest.mark.unit
def test_simple_spa_utterance() -> None:
    utterance = Utterance("a ver sácalo .", primary_language="spa", secondary_language="eng")
    assert utterance.language == "spa"
    assert utterance.is_mixed == False
    assert len(utterance.words) == 3

    for word in utterance.words:
        _assert_word(word, "spa", False, False)


@pytest.mark.unit
def test_spa_utterance_code_switch() -> None:
    utterance = Utterance("si butterfly@s .", primary_language="spa", secondary_language="eng")
    assert utterance.language == "spa"
    assert utterance.is_mixed == True
    assert len(utterance.words) == 2

    _assert_word(utterance.words[0], "spa", False, False)
    _assert_word(utterance.words[1], "eng", True, False)


@pytest.mark.unit
def test_simple_eng_utterance_with() -> None:
    utterance = Utterance(
        "[- eng] yes butterfly .", primary_language="spa", secondary_language="eng"
    )
    assert utterance.language == "eng"
    assert utterance.is_mixed == False
    assert len(utterance.words) == 2

    for word in utterance.words:
        _assert_word(word, "eng", False, False)


@pytest.mark.unit
def test_eng_utterance_code_switch() -> None:
    utterance = Utterance("[- eng] my patito@s ?", primary_language="spa", secondary_language="eng")
    assert utterance.language == "eng"
    assert utterance.is_mixed == True
    assert len(utterance.words) == 2

    _assert_word(utterance.words[0], "eng", False, False)
    _assert_word(utterance.words[1], "spa", True, False)


@pytest.mark.unit
def test_utterance_with_mlu_ignored_phrase() -> None:
    utterance = Utterance(
        "<esto no> [/] esto no .", primary_language="spa", secondary_language="eng"
    )
    assert utterance.language == "spa"
    assert utterance.is_mixed == False
    assert len(utterance.words) == 4

    _assert_word(utterance.words[0], "spa", False, True)
    _assert_word(utterance.words[1], "spa", False, True)
    _assert_word(utterance.words[2], "spa", False, False)
    _assert_word(utterance.words[3], "spa", False, False)


@pytest.mark.unit
def test_utterance_with_mlu_ignored_words() -> None:
    utterance = Utterance(
        "oh no[/] no [/] no !", primary_language="spa", secondary_language="eng"
    )
    assert utterance.language == "spa"
    assert utterance.is_mixed == False
    assert len(utterance.words) == 4

    _assert_word(utterance.words[0], "spa", False, False)
    _assert_word(utterance.words[1], "spa", False, True)
    _assert_word(utterance.words[2], "spa", False, True)
    _assert_word(utterance.words[3], "spa", False, False)


@pytest.mark.unit
def test_utterance_with_ignored_words() -> None:
    utterance = Utterance("&=gasps qué es ?", primary_language="spa", secondary_language="eng")
    assert utterance.language == "spa"
    assert utterance.is_mixed == False
    assert len(utterance.words) == 2

    _assert_word(utterance.words[0], "spa", False, False)
    _assert_word(utterance.words[1], "spa", False, False)


@pytest.mark.unit
@pytest.mark.parametrize("is_token", [True, False])
def test_utterance_with_ignored_words(is_token: bool, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bother_user, "is_this_a_token", Mock(return_value=is_token))
    utterance = Utterance(
        "[- eng] <but> [//] butterfly .", primary_language="spa", secondary_language="eng"
    )
    assert utterance.language == "eng"
    assert utterance.is_mixed == False
    assert len(utterance.words) == 2 if is_token else 1


    if is_token:
        assert utterance.words[0].cleaned_word == "but"
        _assert_word(utterance.words[0], "eng", False, True)
        _assert_word(utterance.words[1], "eng", False, False)
    else:
         assert utterance.words[0].cleaned_word == "butterfly"
         _assert_word(utterance.words[0], "eng", False, False)
