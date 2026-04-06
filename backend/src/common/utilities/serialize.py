from typing import Any
from src.common.models.court import Court
from src.common.models.game import Game
from src.common.models.place import Place
from src.common.models.player import Player


def public_player(player: Player) -> dict[str, Any]:
    return {
        "id": player.id,
        "username": player.username,
        "language": player.language,
        "team_id": player.team_id,
    }


def private_player(player: Player) -> dict[str, Any]:
    return {
        "id": player.id,
        "username": player.username,
        "email": player.email,
        "email_verified": player.email_verified,
        "language": player.language,
        "team_id": player.team_id,
        "geolocation": player.geolocation,
        "google_id": player.google_id,
        "apple_id": player.apple_id,
        "facebook_id": player.facebook_id,
    }


def serialize_court(court: Court) -> dict[str, Any]:
    return {
        "id": court.id,
        "name": court.name,
        "geolocation": court.geolocation,
        "place_ids": court.place_ids,
    }


def serialize_game(game: Game) -> dict[str, Any]:
    return {
        "id": game.id,
        "timestamp": game.timestamp.isoformat() if game.timestamp else None,
        "court_id": game.court_id,
        "player_ids": game.player_ids,
    }


def serialize_place(place: Place) -> dict[str, Any]:
    return {
        "id": place.id,
        "geolocation": place.geolocation,
        "geolocation_box": place.geolocation_box,
        "address": place.address,
        "is_parent": place.is_parent,
        "parent_ids": place.parent_ids,
    }
