# Models Documentation

## Data Structures

```py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Tuple


@dataclass
class Geolocation:
    type: str = "Point" # GeoJSON Type, Constant Value "Point"
    coordinates: Tuple[float, float] = (0, 0) # Coordinates: [Longitude, Latitude]

@dataclass
class Player:
    id: str = Field() # Uniquer Player ID
    email: str # Account Email // private: only accessible for the user and system
    email_verified: bool # Account Email Verification Status // private: only accessible for the user and system
    username: str # Username
    password_hash: str # Hashed Password // secret: only accessible for the system
    refresh_token_hash: str  # Hashed Refresh Token // secret: only accessible for the system
    google_id: str # Linked Google ID // private: only accessible for the user and system
    apple_id: str # Linked Apple ID // private: only accessible for the user and system
    facebook_id: str # Linked Facebook ID (private: only accessible for the user and system)
    language: str # ISO 639 Two-Letter Language Code
    rating: int # Player Rating (Minimum: 1, Maximum: 9) // secret: only accessible for the system
    geolocation: Geolocation | None # Last Known Geolocation // private: only accessible for the user and system
    geolocation_timestamp: datetime | None # Last Known Geolocation Timestamp // secret: only accessible for the system
    team_id: str # Linked Team ID
    created: datetime # Creation Date // secret: only accessible for the system

@dataclass
class Place:
    id: str # Unique Place ID
    geolocation: Geolocation # Geographic Center
    geolocation_box: Tuple[float, float, float, float] | None # Geographic Area: [Min. Longitude, Min. Latitude, Max. Longitude, Max. Latitude]
    address: List[str] # Address Fields from Narrow (e.g. "Los Angeles") to Broad (e.g. "US")
    is_parent: bool # Whether Place is Parent to Other Places (e.g. "Los Angeles" = False, "US" = True)
    parent_ids: List[str] # Associated Parent Place IDs

@dataclass
class Court:
    id: str # Unique Court ID
    name: str # Common Court Name
    geolocation: Geolocation # Court Geolocation
    place_ids: List[str] # Associated Place IDs

@dataclass
class Game:
    id: str
    timestamp: datetime # Game Start Timestamp
    court_id: str # Associated Court ID
    player_ids: List[str] # Signed-up Player IDs

@dataclass
class Team:
    id: str # Unique Team ID
    color: str # Team Color Hex Code (e.g. #20DFBF)
    geolocation: Geolocation # Team Geolocation
    court_id: str # Associated Court ID
    last_activity: datetime # Timestamp of Last Activity (Team Created OR Player Added OR Score Recorded)

@dataclass
class Score:
    id: str # Unique Score ID
    timestamp: datetime # Score Submission Timestamp
    result: Tuple[int, int] # Score Result: [Score Side A, Score Side B] (Minimum: 0, Maximum: 99)
    points: Tuple[int, int] # Earned Points: [Earned Points Side A, Earned Points Side B] (Winner = Minimum: 1, Maximum: 9 / Loser = 0)
    players: Tuple[List[str], List[str]] # Team Player IDs [Player IDs Side A, Player IDs Side B]
    teams: Tuple[str, str] # Team IDs [Team ID Side A, Team ID Side B]
    colors: Tuple[str, str] # Team Colors [Hex Code Side A, Hex Code Side B]
    confirmations: List[str] # Confirmation Player IDs
    rejections: List[str] # Rejection Player IDs
    confirmed: bool # Confirmation Status
    player_ids: List[str] # Player IDs Flat List
    geolocation: Geolocation | None # Score Geolocation
    court_id: str # Associated Court ID
    place_ids: List[str] # Associated Place IDs
```

## Business Logic

### Player Ratings

Players have a rating that measures their skill level. The rating is continuously calibrated every time the player participates in a game as follows: When a score between two sides is submitted, the rating average across all players is calculated for each side. If the winning side has a lower or equal rating average than the losing side, all players on the winning side receive a rating increase of +1, whereas all players on the losing side receive a rating decrease of -1. Otherwise, no rating changes occur.

### Geolocation Tracking

Players' geolocation isn't actively tracked but instead silently updated based on their requests. Whenever a player invokes a feature on the client side that causes a geolocation detection, the detected geolocation is checked against the current value. If the difference exceeds 200 meters, the new geolocation is stored to achieve a semi-real-time geolocation tracking.

### Place Associations

The places collection is a supporting no-write database collection to facilitate search features and geographic relationships. Whenever an entity is associated to a place, it is first associated to the nearest place with the attribute "is_parent=False", and then associated to all corresponding parent places.

### Game Sign-ups

Games are not key events managed by players, but rather an informative indication of the players who have declared that they are playing on a certain court at a certain time, nothing else. Games have a start time and no end time because they always encompass a fixed duration of 1h, with the start time always being on the hour. A game with a start time pointing to 6pm means that the game covers the hour between 6pm and 7pm. If a player is going to play for two hours (e.g. from 6pm to 8pm), they effectively sign up for both the 6pm (6pm-7pm) and the 7pm (7pm-8pm) games.

### Team Management

Teams are the cornerstone of player interactions and are designed as ephemeral entities. A team is formed when one player scans the QR code of their first teammate, provided that both players are not currently associated to another active team. The team's court ID and geolocation are assigned automatically based on the nearest court. From there, all players on the team have admin rights and can change the team's color and add/remove players. A team is considered to be active when its last activity was less than 4h ago. When a team becomes inactive or when it is reduced to less than two players, the team is deleted as soon as possible. The team ID stored on a player may point to a team that no longer exists in some cases, which is fine and is simply corrected whenever that player tries any team-related operation.

### Score Points Calculation

Every time a score is submitted, the winning side earns points based on the rating average of both sides. By default, a win grants 5 points, with bonus or penalty points awarded based on the difference in rating averages. For example: If a 6-side and a 4-side play each other, the 6-side stands to win 3 points (5 default - 2 penalty due to weaker opponent) whereas the 4-side stands to win 7 points (5 default + 2 bonus due to stronger opponent). Points assigned are always calculated in decimals but rounded to the nearest integer at the end. A win grants a minimum of 1 and a maximum of 9 points. Tied scores are not allowed, there is always a winner and a loser.

### Score Confirmation & Rejection

When a score is submitted, the winning side's points only count towards league points if both sides have confirmed the score. A score counts as confirmed by a side when more than 50% of the players have confirmed the score (e.g. 3 out of 5 players). A score counts as rejected when more then 50% of any of the two sides rejects the score, in which case the game is deleted.
