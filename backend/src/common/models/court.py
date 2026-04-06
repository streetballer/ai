from dataclasses import dataclass, field
from typing import Any


@dataclass
class Court:
    id: str = ""
    name: str = ""
    geolocation: dict | None = None
    place_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_doc(cls, doc: dict[str, Any]) -> "Court":
        return cls(
            id=str(doc["_id"]),
            name=doc.get("name", ""),
            geolocation=doc.get("geolocation"),
            place_ids=doc.get("place_ids", []),
        )

    def to_doc(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "geolocation": self.geolocation,
            "place_ids": self.place_ids,
        }
