from dataclasses import dataclass
from typing import Any


@dataclass
class Record:
    team_won: int = 0
    team_lost: int = 0
    opponents_won: int = 0
    opponents_lost: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "team": {"won": self.team_won, "lost": self.team_lost},
            "opponents": {"won": self.opponents_won, "lost": self.opponents_lost},
        }
