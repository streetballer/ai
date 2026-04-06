from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, ClassVar


@dataclass
class Team:
    ACTIVE_HOURS: ClassVar[int] = 4

    id: str = ""
    color: str = ""
    geolocation: dict | None = None
    court_id: str = ""
    last_activity: datetime | None = None

    def is_active(self) -> bool:
        if self.last_activity is None:
            return False
        last = self.last_activity
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        return last >= datetime.now(timezone.utc) - timedelta(hours=self.ACTIVE_HOURS)

    @classmethod
    def active_cutoff(cls) -> datetime:
        return datetime.now(timezone.utc) - timedelta(hours=cls.ACTIVE_HOURS)

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
