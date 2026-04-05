# Controllers Documentation

## API Properties

| Property                  | Value                                                                        |
| ------------------------- | ---------------------------------------------------------------------------- |
| Architecture              | RESTful API                                                                  |
| Base URL (Development)    | [http://localhost:3000](http://localhost:3000)                               |
| Base URL (Production)     | [https://api.streetballer.app](https://api.streetballer.app)                 |
| Authentication Mechanism  | Bearer Token (Access Token with TTL = 1h / Refresh Token with TTL = 28 Days) |
| Default Success HTTP Code | 200                                                                          |
| Default Error HTTP Code   | 500                                                                          |

## Response Format

All requests to the server, without exception and regardless of errors or success status, must return a response in JSON format and adhere to the following schema:

```json
{
  "type": "object",
  "description": "Response Object",
  "properties": {
    "message": { "type": "string", "default": "" },
    "data": { "type": "object", "default": {} }
  }
}
```

## Endpoints

| Endpoint                       | Task                   | Request Data Schema (GET Query or POST Body)             | Response Data Schema                              | Possible HTTP Codes |
| ------------------------------ | ---------------------- | -------------------------------------------------------- | ------------------------------------------------- | ------------------- |
| GET /health-check              | Check availability     |                                                          |                                                   |                     |
| POST /auth/log-in              | Log in                 | { username, password } OR { email, password }            | { access_token, refresh_token }                   | 401, 422            |
| POST /auth/sign-up             | Sign up                | { username, email, password }                            | { access_token, refresh_token }                   | 409, 422            |
| POST /auth/google              | Sign in with Google    | { token }                                                | { access_token, refresh_token }                   | 422, 498            |
| POST /auth/apple               | Sign in with Apple     | { token }                                                | { access_token, refresh_token }                   | 422, 498            |
| POST /auth/facebook            | Sign in with Facebook  | { token }                                                | { access_token, refresh_token }                   | 422, 498            |
| POST /auth/password            | Request password reset | { username } OR { email }                                |                                                   | 422                 |
| POST /auth/password/:token     | Reset password         | { password }                                             |                                                   | 422, 498            |
| POST /auth/verification/:token | Verify account         |                                                          |                                                   | 498                 |
| POST /auth/refresh/:token      | Rotate tokens          |                                                          | { access_token, refresh_token }                   | 498                 |
| GET /players                   | Search players         | { lon, lat } OR { text }                                 | { players }                                       | 422                 |
| GET /players/player            | Get own player data    |                                                          | { player }                                        | 401, 404            |
| GET /players/:player_id        | Get player             |                                                          | { player }                                        | 404                 |
| GET /players/:player_id/record | Get record with player |                                                          | { team: { won, lost }, opponents: { won, lost } } | 401, 404            |
| GET /places                    | Search places          | { text, lon, lat } OR { lon, lat } OR { text }           | { places }                                        | 422                 |
| GET /courts                    | Search courts          | { lon, lat } OR { lon, lat, radius }                     | { courts }                                        | 422                 |
| POST /courts                   | Add court              | { lon, lat, name }                                       | { court }                                         | 401, 409, 422       |
| GET /courts/:court_id          | Get court              |                                                          | { court }                                         | 404                 |
| GET /games                     | Search games           | { court_id } OR { lon, lat }                             | { games, courts }                                 | 422                 |
| POST /games                    | Create game            | { court_id, timestamp }                                  |                                                   | 401, 422            |
| POST /games/:game_id/join      | Join game              |                                                          |                                                   | 401, 403, 404       |
| GET /teams                     | Search teams           | { court_id } OR { lon, lat }                             | { teams }                                         | 422                 |
| POST /teams                    | Create team            | { player_id }                                            | { team }                                          | 401, 404, 409, 422  |
| GET /teams/team                | Get own team data      |                                                          | { team, players }                                 | 401, 404            |
| POST /teams/team               | Edit own team          | { color } OR { add_player_ids } OR { remove_player_ids } |                                                   | 401, 404, 422       |
| GET /teams/standings           | Get current standings  |                                                          | { teams, players, scores }                        | 401, 404            |
| GET /teams/:team_id            | Get team               |                                                          | { team, players }                                 | 401, 404            |
| GET /scores                    | Get scores with player | { player_id, confirmed }                                 | { scores }                                        | 401, 422            |
| POST /scores                   | Submit score           | { score_1, score_2, opponent_id }                        | { score }                                         | 401, 422            |
| GET /scores/:score_id          | Get score              |                                                          | { score, players }                                | 404                 |
| POST /scores/:score_id/confirm | Confirm score          |                                                          |                                                   | 401, 403, 404       |
| POST /scores/:score_id/reject  | Reject score           |                                                          |                                                   | 401, 403, 404       |
| GET /league                    | Get league standings   | { place_id, team_size } OR { court_id, team_size }       | { standings: [{ players, points }] }              | 404, 422            |
| POST /settings/username        | Edit username          | { username }                                             |                                                   | 401, 422, 409       |
| POST /settings/email           | Edit email             | { email }                                                |                                                   | 401, 422, 409       |
| POST /settings/password        | Edit password          | { old_password, new_password }                           |                                                   | 401, 422            |
| POST /settings/language        | Edit language          | { language }                                             |                                                   | 401, 422            |
| POST /settings/geolocation     | Edit geolocation       | { lon, lat }                                             |                                                   | 401, 422            |
| POST /settings/delete-account  | Delete account         | { password }                                             |                                                   | 401, 422            |
