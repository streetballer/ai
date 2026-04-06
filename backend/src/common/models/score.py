from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Score:
    id: str = ""
    timestamp: datetime | None = None
    result: tuple[int, int] = (0, 0)
    points: tuple[int, int] = (0, 0)
    players: tuple[list[str], list[str]] = field(default_factory=lambda: ([], []))
    teams: tuple[str, str] = ("", "")
    colors: tuple[str, str] = ("", "")
    confirmations: list[str] = field(default_factory=list)
    rejections: list[str] = field(default_factory=list)
    confirmed: bool = False
    player_ids: list[str] = field(default_factory=list)
    geolocation: dict | None = None
    court_id: str = ""
    place_ids: list[str] = field(default_factory=list)

    def to_doc(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "result": list(self.result),
            "points": list(self.points),
            "players": [list(self.players[0]), list(self.players[1])],
            "teams": list(self.teams),
            "colors": list(self.colors),
            "confirmations": self.confirmations,
            "rejections": self.rejections,
            "confirmed": self.confirmed,
            "player_ids": self.player_ids,
            "geolocation": self.geolocation,
            "court_id": self.court_id,
            "place_ids": self.place_ids,
        }

    @classmethod
    def from_doc(cls, doc: dict[str, Any]) -> "Score":
        players_raw = doc.get("players", [[], []])
        players = (
            list(players_raw[0]) if len(players_raw) > 0 else [],
            list(players_raw[1]) if len(players_raw) > 1 else [],
        )
        points_raw = doc.get("points", [0, 0])
        points = (
            points_raw[0] if len(points_raw) > 0 else 0,
            points_raw[1] if len(points_raw) > 1 else 0,
        )
        return cls(
            id=str(doc["_id"]) if "_id" in doc else "",
            timestamp=doc.get("timestamp"),
            result=tuple(doc.get("result", [0, 0])),
            points=points,
            players=players,
            teams=tuple(doc.get("teams", ["", ""])),
            colors=tuple(doc.get("colors", ["", ""])),
            confirmations=doc.get("confirmations", []),
            rejections=doc.get("rejections", []),
            confirmed=doc.get("confirmed", False),
            player_ids=doc.get("player_ids", []),
            geolocation=doc.get("geolocation"),
            court_id=doc.get("court_id", ""),
            place_ids=doc.get("place_ids", []),
        )
