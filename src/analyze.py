from src import file_system, csv_writer
from src.cha import ChaData
from src.participant_result import ParticipantResult


def run() -> None:
    """The whole enchilada."""
    if file_system.input_dir_was_created():
        # We don't have anything to do
        return
    
    ## Do all the other cool stuff here
    results = {}
    languages = []
    participants = []
    cha_files = file_system.get_cha_files()

    for file in cha_files:
        data = ChaData(file)
        for language in data.languages:
            if language not in languages:
                languages.append(language)

        for participant in data.participants:
            if participant not in participants:
                participants.append(participant)
            if data.participant_id not in results:
                results[data.participant_id] = {}
            
            results[data.participant_id][participant] = ParticipantResult(
                data.languages, data.utterances[participant]
            )

    
    csv_writer.write_participant_results(results, participants, languages)
