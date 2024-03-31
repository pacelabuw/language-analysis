import csv

from src.constants import ID_COLUMN, INITIAL_COLUMNS, LANGUAGE_COLUMNS, NO_DATA
from src.participant_result import ParticipantResult


def write_participant_results(
    results: dict[str, dict[str, list[ParticipantResult]]],
    participants: list[str],
    languages: list[str],
):
    participant_ids = sorted(results.keys())
    data = []

    columns = ID_COLUMN + _get_columns(participants, languages)
    participant_column_count = len(INITIAL_COLUMNS) + len(LANGUAGE_COLUMNS) * len(languages)

    for id in participant_ids:
        new_data = [id]
        for participant in participants:
            if participant in results[id]:
                new_data += _extract_participant_results(results[id][participant], languages)
            else:
                # This participant is not in data set, fill participant dolumns for this row
                new_data += [NO_DATA for _ in range(participant_column_count)]

        data.append(new_data)

    with open("./results.csv", mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)
        csv_writer.writerows(data)


def _get_columns(participants: list[str], languages: list[str]) -> list[str]:
    columns = []
    for participant in participants:
        columns += [f"{participant} {c}" for c in INITIAL_COLUMNS]
        _add_language_columns(participant, columns, languages)
    
    return columns


def _add_language_columns(participant: str, columns: list[str], languages: list[str]) -> None:
    for language in languages:
        columns += [f"{participant} {language} {c}" for c in LANGUAGE_COLUMNS]


def _extract_participant_results(data: ParticipantResult, languages: list[str]) -> list:
    result = [
        data.total_utterance_count, 
        round(data.total_mlu, 2),
        data.mixed_utterance_count,
    ]

    for lang in languages:
        if lang not in data.languages:
            result += [NO_DATA for _ in range(len(LANGUAGE_COLUMNS))]
        else:
            if data.language_token_counts[lang] != 0:
                ttr = float(data.language_type_counts[lang]) / data.language_token_counts[lang]
            else:
                ttr = 0
            result.append(data.language_utterance_counts[lang])
            result.append(round(data.language_mlu_counts[lang], 2))
            result.append(data.language_type_counts[lang])
            result.append(data.language_token_counts[lang])
            result.append(round(ttr, 2))

    return result
