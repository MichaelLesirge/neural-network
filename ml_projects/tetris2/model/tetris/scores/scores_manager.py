from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from typing import Optional
import heapq
import json


@dataclass(slots=True, frozen=True, order=True)
class Score:
    score: int = field(compare=True)
    time: str = field(compare=False)
    playerName: str = field(compare=False)


class HighScoreManager(ABC):

    @abstractmethod
    def save_score(self, score: Score) -> None:
        pass

    @abstractmethod
    def get_top_scores(self, n: int) -> list[Score]:
        pass

    @abstractmethod
    def get_top_score(self) -> Optional[Score]:
        pass


class JSONFileHighScoreStorage(HighScoreManager):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.scores: list[Score] = [] 
        self._load_scores()

    def save_score(self, score: Score) -> None:
        heapq.heappush(self.scores, score)
        self._save_scores()

    def get_top_scores(self, n: int) -> list[Score]:
        if len(self.scores) < 1:
            return None
        return heapq.nlargest(n, self.scores)

    def get_top_score(self) -> Optional[Score]:
        if len(self.scores) < 1:
            return None
        return heapq.nlargest(1, self.scores)[0]

    def _load_scores(self) -> list[Score]:
        try:
            with open(self.file_path, "r") as file:
                scores_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            scores_data = []

        self.scores = [Score(**score) for score in scores_data]
        heapq.heapify(self.scores)

    def _save_scores(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump([asdict(score) for score in self.scores], file, indent=4)
