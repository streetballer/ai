from typing import Any


def serialize_document(doc: dict[str, Any]) -> dict[str, Any]:
    result = {k: v for k, v in doc.items() if k != "_id"}
    result["id"] = str(doc["_id"])
    return result


def public_player(player: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(player["_id"]),
        "username": player.get("username"),
        "language": player.get("language"),
        "team_id": player.get("team_id"),
    }


def private_player(player: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(player["_id"]),
        "username": player.get("username"),
        "email": player.get("email"),
        "email_verified": player.get("email_verified"),
        "language": player.get("language"),
        "team_id": player.get("team_id"),
        "geolocation": player.get("geolocation"),
        "google_id": player.get("google_id"),
        "apple_id": player.get("apple_id"),
        "facebook_id": player.get("facebook_id"),
    }


def serialize_court(court: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(court["_id"]),
        "name": court.get("name"),
        "geolocation": court.get("geolocation"),
        "place_ids": court.get("place_ids", []),
    }


def serialize_game(game: dict[str, Any]) -> dict[str, Any]:
    timestamp = game.get("timestamp")
    return {
        "id": str(game["_id"]),
        "timestamp": timestamp.isoformat() if timestamp else None,
        "court_id": game.get("court_id"),
        "player_ids": game.get("player_ids", []),
    }


def serialize_place(place: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(place["_id"]),
        "geolocation": place.get("geolocation"),
        "geolocation_box": place.get("geolocation_box"),
        "address": place.get("address", []),
        "is_parent": place.get("is_parent", False),
        "parent_ids": place.get("parent_ids", []),
    }
