from dataclasses import dataclass, field
from typing import Any


@dataclass
class Place:
    id: str = ""
    name: str = ""
    type: str = ""
    geolocation: dict | None = None
    geolocation_box: tuple[float, float, float, float] = field(default_factory=tuple)
    parent_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_doc(cls, doc: dict[str, Any]) -> "Place":
        return cls(
            id=str(doc["_id"]),
            name=doc.get("name", ""),
            type=doc.get("type", ""),
            geolocation=doc.get("geolocation"),
            geolocation_box=tuple(doc["geolocation_box"]),
            parent_ids=doc.get("parent_ids", []),
        )
