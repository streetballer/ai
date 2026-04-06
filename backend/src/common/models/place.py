from dataclasses import dataclass, field
from typing import Any


@dataclass
class Place:
    id: str = ""
    geolocation: dict | None = None
    geolocation_box: tuple[float, float, float, float] | None = None
    address: list[str] = field(default_factory=list)
    is_parent: bool = False
    parent_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_doc(cls, doc: dict[str, Any]) -> "Place":
        return cls(
            id=str(doc["_id"]),
            geolocation=doc.get("geolocation"),
            geolocation_box=doc.get("geolocation_box"),
            address=doc.get("address", []),
            is_parent=doc.get("is_parent", False),
            parent_ids=doc.get("parent_ids", []),
        )
