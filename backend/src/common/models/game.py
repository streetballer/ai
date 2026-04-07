from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, ClassVar


@dataclass
class Game:
    FIELDS_PROJECTION: ClassVar[dict] = {"_id": 1, "timestamp": 1, "court_id": 1, "player_ids": 1}

    id: str = ""
    timestamp: datetime | None = None
    court_id: str = ""
    player_ids: list[str] = field(default_factory=list)

    @classmethod
    def floor_to_hour(cls, dt: datetime) -> datetime:
        return dt.replace(minute=0, second=0, microsecond=0)

    @classmethod
    def from_doc(cls, doc: dict[str, Any]) -> "Game":
        return cls(
            id=str(doc["_id"]),
            timestamp=doc.get("timestamp"),
            court_id=doc.get("court_id", ""),
            player_ids=doc.get("player_ids", []),
        )

    def to_doc(self) -> dict[str, Any]:
        return {
            "court_id": self.court_id,
            "timestamp": self.timestamp,
            "player_ids": self.player_ids,
        }
