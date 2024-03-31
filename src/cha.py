from pathlib import Path
from src.constants import LANGUAGE_TAG, PARTICIPANTS_TAG

class ChaData:
    file_path: str
    languages: list[str]
    participant_id: str
    participants: dict[str, str]
    utterances: dict[str, list[str]]

    def __init__(self, file_path: str):
        self.languages = []
        self.file_path = file_path
        self.participants = {}
        self._get_participant_id()
        self.utterances = {}

        with open(file_path) as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith("@"):
                self._read_metadata(line)

        self._verify_required_metadata()

        for line in lines:
            self._read_utterance(line)

    def _read_metadata(self, line: str):
        """Pull any requried data from files metadata tags."""
        if line.startswith(LANGUAGE_TAG):
            # Separate tag from metadata
            language_data = line.split(":")[1].strip()
            self.languages = [l.strip() for l in language_data.split(",")]
        elif line.startswith(PARTICIPANTS_TAG):
            # Separate tag from metadata
            separated_participants = [p.strip() for p in line.split(":")[1].strip().split(",")]

            # Go through participant data and initialize fields
            for participant in separated_participants:
                key, description = [p.strip() for p in participant.split(" ")]
                self.participants[key.upper()] = description
                self.utterances[key.upper()] = []

    
    def _verify_required_metadata(self) -> None:
        """Check that the required metadata is available, raise ValueError if not."""
        if len(self.languages) == 0:
            raise ValueError(f"Could not read {self.file_path}, missing {LANGUAGE_TAG} metadata.")
        elif len(self.participants.keys()) == 0:
            raise ValueError(
                f"Could not read {self.file_path}, missing {PARTICIPANTS_TAG} metadata."
            )
        

    def _get_participant_id(self) -> None:
        """Pull participant ID from file path. Expect it to be the first two pieces of filename."""
        file = Path(self.file_path)
        split_filename = file.name.split("_")

        if len(split_filename) > 2:
            self.participant_id = f"{split_filename[0]}_{split_filename[1]}"
        else:
            self.participant_id = "unknown"


    def _read_utterance(self, line: str):
        """Determine which participant utterance belongs to, clean it and append to their utterance
        list.
        """
        split_line = line.split(":\t")
        if len(split_line) < 2:
            # nothing to do here
            return
        elif len(split_line) == 2:
            # The ideal case of, *participant:   utterance
            participant = split_line[0].lstrip("*").upper()
            utterance = split_line[1]
        elif len(split_line) > 2:
            # our utterance seems to have colons, we will just stitch it back together
            participant = split_line[0].lstrip("*").upper()
            utterance = ":".join(split_line[1:])
        
        if participant in self.participants:
            split_utterance = utterance.split(" ")
            split_utterance.pop() # This is a timestamp
            self.utterances[participant].append(" ".join(split_utterance))
