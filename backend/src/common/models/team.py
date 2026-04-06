from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Team:
    id: str = ""
    color: str = "#20DFBF"
    geolocation: dict | None = None
    court_id: str = ""
    last_activity: datetime | None = None

    @classmethod
    def from_doc(cls, doc: dict[str, Any]) -> "Team":
        return cls(
            id=str(doc["_id"]),
            color=doc.get("color", "#20DFBF"),
            geolocation=doc.get("geolocation"),
            court_id=doc.get("court_id", ""),
            last_activity=doc.get("last_activity"),
        )

    def to_doc(self) -> dict[str, Any]:
        return {
            "color": self.color,
            "geolocation": self.geolocation,
            "court_id": self.court_id,
            "last_activity": self.last_activity,
        }
