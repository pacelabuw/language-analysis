import pytest

from src.cha import ChaData


@pytest.mark.unit
def test_cha_file_1():
    test_file = "tests/data/BWL_2002_3Bags_iPad_reading.cha"
    data = ChaData(file_path=test_file)

    assert data.participant_id == "BWL_2002"
    assert data.languages == ["spa", "eng"]
    assert "CHI" in data.participants
    assert "MOT" in data.participants
    assert len(data.utterances["CHI"]) == 5
    assert len(data.utterances["MOT"]) == 10


@pytest.mark.unit
def test_cha_file_2():
    test_file = "tests/data/BWL_2003_3BagsTask_Camcorder_reading.cha"
    data = ChaData(file_path=test_file)

    assert data.participant_id == "BWL_2003"
    assert data.languages == ["spa", "eng"]
    assert "CHI" in data.participants
    assert "MOT" in data.participants
    assert len(data.utterances["CHI"]) == 0
    assert len(data.utterances["MOT"]) == 12


@pytest.mark.unit
def test_cha_file_3():
    test_file = "tests/data/BWL_2004_3BagsTask_iPad_reading.cha"
    data = ChaData(file_path=test_file)

    assert data.participant_id == "BWL_2004"
    assert data.languages == ["spa", "eng"]
    assert "CHI" in data.participants
    assert "MOT" in data.participants
    assert len(data.utterances["CHI"]) == 2
    assert len(data.utterances["MOT"]) == 5


@pytest.mark.unit
def test_cha_file_no_participant_id():
    test_file = "tests/data/no-participant-id.cha"
    data = ChaData(file_path=test_file)

    assert data.participant_id == "unknown"


@pytest.mark.unit
@pytest.mark.parametrize(
    "file_path",
    ["tests/data/no_languages.cha", "tests/data/no_participants.cha"]
)
def test_cha_file_missing_metadata(file_path: str):
    with pytest.raises(ValueError):
        data = ChaData(file_path=file_path)
