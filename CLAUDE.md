# CLAUDE.md - Streetballer

---

## Project Identity

### Details

- Name: Streetballer
- Description: Basketball community app to find courts, organize pick-up games, and gamify the playing experience
- Target Users: Amateur Basketball Players
- App Stores: iOS, Android

### Target Problem

Amateur basketball players usually quit the sport at some point due at least one of three reasons:

1. The local basketball community is generally poorly connected, making it very difficult to organize pick-up games, unless you are part of an already established and usually exclusive group.
2. Most people can't adhere to the rigid structure of a basketball club's training and playing schedules, discarding joining a club as a potential option to play regularly.
3. The quality of pick-up games is highly chance-dependent and unreliable in three key areas: number of players and teams, level of play, intensity of competition.

### Proposed Solution

Streetballer is a mobile app that aims to solve the problems listed above. The core of the app is defined by the following features:

1. Players can find courts to play on anywhere
2. Players can see when others a

### Product Philosophy

### Business Model

### Growth Engine

Streetballer's strategy is strongly based on a combination of viral and sticky growth engines (in reference to "Lean Startup" by Eric Ries)

- Viral Engine:

### Retention Loop

---

## Technical Stack

| Layer            | Choice                                  |
| ---------------- | --------------------------------------- |
| Framework        | Flutter                                 |
| Language         | Dart                                    |
| State Management | Riverpod                                |
| Navigation       | go_router                               |
| UI Components    | Material UI                             |
| Styling Approach | Guided by Figma Design Files            |
| HTTP Client      | http                                    |
| Local Storage    | flutter_secure_storage                  |
| Backend          | Python with FastAPI                     |
| Database         | Self-hosted MongoDB                     |
| Authentication   | User/Password, Google, Apple, Facebook  |
| Analytics        | PostHog                                 |
| Testing          | "test" on frontend, "vitest" on backend |
| CI/CD            | Jenkins                                 |
| Monorepo tooling | Bazel                                   |

---

## Architecture & Patterns

### App Architecture Patterns

All code should adhere to the best practices as specified in the following sources

- "Clean Architecture" Book by Robert C. Martin
- ["Flutter Architecture Recommendations" Documentation by Flutter](https://docs.flutter.dev/app-architecture/recommendations)
- ["Flutter Design Patterns" Documentation by Flutter](https://docs.flutter.dev/app-architecture/design-patterns)
- ["Flutter Performance Best Practices" Documentation by Flutter](https://docs.flutter.dev/perf/best-practices)
- ["FastAPI Best Practices" Documentation by Auth0](https://auth0.com/blog/fastapi-best-practices/)

### Folder Structure

Folder structure should prioritize long-term scalability, granular modularity, and ease of understanding. A logical structure by business logic (external) should be prioritized over a logical structure by technical purpose (internal).

The project should be managed as a mono-repo, with separate folders for frontend and backend.

### App Modules

| Module         | Priority | Features                                                                                           | Notes                                                       |
| -------------- | -------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Authentication | 1        | Log in, Sign up, Reset password, Verify account, Refresh authentication, Log out                   | Lazy Login Pattern                                          |
| Players        | 2        | Search players, See playing history with other players                                             | Minimalistic Player Profile                                 |
| Places         | 3        | Search places by text/geolocation                                                                  | Support Module for other Search Features                    |
| Courts         | 4        | Browse courts, Add courts, Edit court information                                                  | Actual Interface for Write Operations reg. Games Module     |
| Games          | 5        | Sign up to play on a certain court at a certain time, Find games by date/time/place/court          | Indication of Playing Opportunities, not a Key Parent Event |
| Teams          | 6        | Create team, Add/remove players, Change team color, View standings                                 | Temporary Purpose, not Permanent Association                |
| Scores         | 7        | Record scores of games played, View/confirm/reject score, Earn points based on team/player ratings | Core Gamification Mechanism, Heavily QR-code-based          |
| League         | 8        | View standings and points by court/locality/region/country/etc.                                    | Efficient Database Queries Essential in this Module         |
| Settings       | 9        | Change username/email/password/language, Log out, Request account deletion                         | Isolated Administration Section for the User                |

### Dependency Injection / Service Layer

Riverpod

### Error Handling Strategy

1. First Layer: Global error handling as a catch-all safety fallback
2. Second Layer: Local error handling as close to the source as possible

### Offline / Connectivity Strategy

Internet connection is generally required for all features, but users should still be able to open the app when offline and just be alerted about it.

---

## Data Models & API

### Core Data Models

```json
{
  "type": "object",
  "properties": {
    "player": {
      "type": "object",
      "properties": {
        "_id": { "type": "string" },
        "email": { "type": "string" },
        "email_verified": { "type": "boolean" },
        "username": { "type": "string" },
        "password_hash": { "type": "string" },
        "google_id": { "type": "string" },
        "apple_id": { "type": "string" },
        "facebook_id": { "type": "string" },
        "refresh_token_hash": { "type": "string" },
        "device_notification_ids": {
          "type": "array",
          "items": { "type": "string" }
        },
        "geolocation": {
          "type": "object",
          "description": "GeoJSON object",
          "properties": {
            "type": { "const": "Point" },
            "coordinates": {
              "type": "array",
              "prefixItems": [
                {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180,
                  "description": "Longitude"
                },
                {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90,
                  "description": "Latitude"
                }
              ]
            }
          }
        },
        "place_id": { "type": "string" },
        "team_id": { "type": "string" },
        "rating": { "type": "number", "minimum": 1, "maximum": 99 },
        "language": {
          "type": "string",
          "description": "Two-Letter Language Code according to ISO 639"
        },
        "active": { "type": "boolean" }
      }
    },
    "place": {
      "type": "object",
      "properties": {
        "_id": { "type": "string" },
        "geolocation": {
          "type": "object",
          "description": "GeoJSON object",
          "properties": {
            "type": { "const": "Point" },
            "coordinates": {
              "type": "array",
              "prefixItems": [
                {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180,
                  "description": "Longitude"
                },
                {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90,
                  "description": "Latitude"
                }
              ]
            }
          }
        },
        "address": {
          "type": "object",
          "description": "Address Fields (e.g. { country: US, state: California, city: Sacramento })",
          "additionalProperties": { "type": "string" }
        }
      }
    },
    "court": {
      "type": "object",
      "properties": {
        "_id": { "type": "string" },
        "name": { "type": "string" },
        "geolocation": {
          "type": "object",
          "description": "GeoJSON object",
          "properties": {
            "type": { "const": "Point" },
            "coordinates": {
              "type": "array",
              "prefixItems": [
                {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180,
                  "description": "Longitude"
                },
                {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90,
                  "description": "Latitude"
                }
              ]
            }
          }
        },
        "place_id": { "type": "string" }
      }
    },
    "game": {
      "type": "object",
      "properties": {
        "_id": { "type": "string" },
        "start": {
          "type": "number",
          "description": "Unix Timestamp in Milliseconds of the Game Start Time"
        },
        "geolocation": {
          "type": "object",
          "description": "GeoJSON object",
          "properties": {
            "type": { "const": "Point" },
            "coordinates": {
              "type": "array",
              "prefixItems": [
                {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180,
                  "description": "Longitude"
                },
                {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90,
                  "description": "Latitude"
                }
              ]
            }
          }
        },
        "player_ids": { "type": "array", "items": { "type": "string" } },
        "place_id": { "type": "string" },
        "court_id": { "type": "string" }
      }
    },
    "team": {
      "type": "object",
      "properties": {
        "_id": { "type": "string" },
        "color": {
          "type": "string",
          "description": "Hex Color Code (e.g. #20DFBF)"
        },
        "geolocation": {
          "type": "object",
          "description": "GeoJSON object",
          "properties": {
            "type": { "const": "Point" },
            "coordinates": {
              "type": "array",
              "prefixItems": [
                {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180,
                  "description": "Longitude"
                },
                {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90,
                  "description": "Latitude"
                }
              ]
            }
          }
        },
        "place_id": { "type": "string" },
        "court_id": { "type": "string" }
      }
    },
    "score": {
      "type": "object",
      "properties": {
        "_id": { "type": "string" },
        "timestamp": {
          "type": "number",
          "description": "Unix Timestamp in Milliseconds of the Score"
        },
        "result": {
          "type": "array",
          "prefixItems": [
            {
              "type": "number",
              "minimum": 0,
              "maximum": 999,
              "description": "Score of Side A"
            },
            {
              "type": "number",
              "minimum": 0,
              "maximum": 999,
              "description": "Score of Side B"
            }
          ]
        },
        "points": {
          "type": "array",
          "prefixItems": [
            {
              "type": "number",
              "minimum": 0,
              "maximum": 10,
              "description": "League Points for Side A"
            },
            {
              "type": "number",
              "minimum": 0,
              "maximum": 10,
              "description": "League Points for Side B"
            }
          ]
        },
        "players": {
          "type": "array",
          "prefixItems": [
            {
              "type": "array",
              "description": "Player IDs of Side A",
              "items": { "type": "string" }
            },
            {
              "type": "array",
              "description": "Player IDs of Side B",
              "items": { "type": "string" }
            }
          ]
        },
        "teams": {
          "type": "array",
          "prefixItems": [
            { "type": "string", "description": "Team ID of Side A" },
            { "type": "string", "description": "Team ID of Side B" }
          ]
        },
        "colors": {
          "type": "array",
          "prefixItems": [
            {
              "type": "string",
              "description": "Hex Color Code of Side A (e.g. #20DFBF)"
            },
            {
              "type": "string",
              "description": "Hex Color Code of Side B (e.g. #DF4020)"
            }
          ]
        },
        "confirmations": {
          "type": "array",
          "description": "Player IDs of Players who confirmed the Score",
          "items": { "type": "string" }
        },
        "rejections": {
          "type": "array",
          "description": "Player IDs of Players who rejected the Score",
          "items": { "type": "string" }
        },
        "confirmed": { "type": "boolean" },
        "player_ids": {
          "type": "array",
          "items": { "type": "string" }
        },
        "place_id": { "type": "string" },
        "court_id": { "type": "string" }
      }
    }
  }
}
```

### API Contract

- Protocol: REST
- Base URL (dev): [http://localhost:3000](http://localhost:3000)
- Base URL (prod): [https://api.streetballer.app](https://api.streetballer.app)
- Authentication Mechanism: Bearer Token (Access Token + Refresh Token), FastAPI OAuth2
- Pagination Strategy: Cursor
- Rate Limiting: 60 Requests per Minute per User

### Key API Endpoints

| Endpoint                              | Method | Description                        | Request Input                        | Response Output                    | Errors        |
| ------------------------------------- | ------ | ---------------------------------- | ------------------------------------ | ---------------------------------- | ------------- |
| /health-check                         | GET    | Check Backend Availability         |                                      |                                    |               |
| /authentication/log-in                | POST   | Log in                             | Login Credentials                    | Access + Refresh Token             | 400, 401      |
| /authentication/sign-up               | POST   | Sign up                            | Account Credentials                  | Access + Refresh Token             | 400, 409      |
| /authentication/reset-password        | POST   | Request Password Reset             | User Reference                       | Email with Reset Link              | 400           |
| /authentication/reset-password/:token | POST   | Reset Password                     | New Password                         |                                    | 400, 498      |
| /authentication/verify-account/:token | POST   | Verify Account                     |                                      |                                    | 498           |
| /authentication/refresh/:token        | POST   | Refresh Access and Refresh Tokens  |                                      | Access + Refresh Token             | 498           |
| /players                              | GET    | Search Players                     | Geolocation or Text Search           | List of Players                    | 400           |
| /players/:player_id                   | GET    | Get Player                         |                                      | Player                             | 404           |
| /players/:player_id/record            | GET    | Get Playing Record with Player     |                                      | Wins/Losses as Teammates/Opponents | 401, 404      |
| /places                               | GET    | Search Places                      | Geolocation or Text Search           | List of Places                     | 400           |
| /courts                               | GET    | Search Courts                      | Geolocation                          | List of Courts                     | 400           |
| /courts                               | POST   | Add Court                          | Geolocation + Court Name             | Court                              | 400, 401      |
| /courts/:court_id                     | GET    | Get Court                          |                                      | Court                              | 404           |
| /games                                | GET    | Search Games                       | Date Range + Geolocation or Court ID | List of Games                      | 400           |
| /games                                | POST   | Create Game                        | Court ID + Date & Time               | Game                               | 400, 401      |
| /games/:game_id/join                  | POST   | Join Game                          |                                      |                                    | 401           |
| /teams                                | GET    | Search Teams                       | Geolocation or Court ID              | List of Teams                      | 400           |
| /teams                                | POST   | Create Team                        | Player ID of First Teammate          | Team                               | 400, 401, 404 |
| /teams/team                           | GET    | Get Own Team                       |                                      | Team + List of Players             | 401, 404      |
| /teams/team                           | POST   | Edit Own Team                      | Color + Player IDs to add/remove     |                                    | 400, 401, 404 |
| /teams/standings                      | GET    | Get Team Standings of Current Game |                                      | List of Teams + List of Scores     | 401, 404      |
| /scores                               | GET    | Search Scores                      | Player ID (optional), Date Range     | List of Scores                     | 401           |
| /scores                               | POST   | Submit Score                       | Team IDs or Player IDs, Score Result | Score                              |               |
| /scores/pending                       | GET    | Get Scores awaiting Confirmation   |                                      | List of Scores                     | 401           |
| /scores/:score_id                     | GET    | Get Score                          |                                      | Score + List of Players            | 404           |
| /scores/:score_id/confirm             | POST   | Confirm Score                      |                                      |                                    | 401, 403, 404 |
| /scores/:score_id/reject              | POST   | Reject Score                       |                                      |                                    | 401, 403, 404 |
| /league                               | GET    | Get League Standings               | Place or Court, Team Size (1-5)      | List of Standings Items            | 404           |

---

## Authentication & Authorization

- Authentication Strategy: Self-managed with Passport.js
- Authentication Flows Supported: Email + Password, Username + Password, Sign-in with Google, Sign-in with Apple, Sign-in with Facebook
- Token Storage Strategy: flutter_secure_storage package
- Token Refresh Strategy: Short-lived Access Token (1 Hour) + Long-lived Refresh Token (14 Days)
- Role-based Access: General "user" Role for Everyone, No Differentiation
- "Lazy Login" Pattern: Authentication is only required for features that fall under one of two categories: A) requests that read data that is linked to the individual identity or features that write data

---

## Design System & UI

### Design Source of Truth

<!-- IMAGES -->

### Theming

- **Light mode:** `[ ] Yes` `[ ] No`
- **Dark mode:** `[ ] Yes` `[ ] No`
- **System-follow:** `[ ] Yes` `[ ] No`

### Core design tokens

> Fill in your actual values, or say "use sensible defaults" if you want Claude to choose.

```
Colors:
  primary:
  secondary:
  background:
  surface:
  error:
  text-primary:
  text-secondary:

Typography:
  font-family:
  heading sizes:
  body sizes:

Spacing scale:
  (e.g., 4, 8, 12, 16, 24, 32, 48)

Border radius:
  (e.g., small: 4, medium: 8, large: 16)

Shadows / Elevation: None, Flat Design
```

### Component Conventions

> How should shared components be built? List your expectations.

- Naming convention for components:
- Props pattern (e.g., destructured, single props object, typed interface):
- Accessibility requirements (WCAG level, screen reader support, min tap targets):
- Animation library / approach:
- Loading / skeleton states — describe pattern:
- Empty states — describe pattern:

---

## Navigation & Routing

### Navigation structure

> Describe your app's navigation hierarchy. Example:

```
Tab Bar
├── Home (stack)
│   ├── Dashboard
│   ├── Detail screen
│   └── ...
├── Search (stack)
│   └── ...
├── Profile (stack)
│   └── ...
└── Settings (stack)
    └── ...

Modal flows:
├── Create [entity]
├── Onboarding
└── ...

Auth flow (before main app):
├── Welcome
├── Login
├── Register
└── Forgot password
```

### Deep linking scheme

- **URL scheme:** (e.g., `myapp://`)
- **Universal links domain:** (e.g., `https://myapp.com`)
- **Routes that must be deep-linkable:**

---

## 🟡 State Management Details

> Go deeper than just naming the library. Describe the philosophy.

- **Global state — what lives here:**
- **Server/async state — how is remote data cached and invalidated:**
- **Local/ephemeral state — what stays in the widget/component:**
- **Persistence — what state survives app kill:**
- **State reset — when does state clear (logout, session expiry, etc.):**

---

## 🟡 Testing Strategy

- **Unit tests:** `[ ] Required` `[ ] Nice-to-have` `[ ] Skip`
  - Minimum coverage target:
  - What to test: (e.g., business logic, models, utils)
- **Widget / component tests:** `[ ] Required` `[ ] Nice-to-have` `[ ] Skip`
  - What to test:
- **Integration tests:** `[ ] Required` `[ ] Nice-to-have` `[ ] Skip`
  - What to test:
- **E2E tests:** `[ ] Required` `[ ] Nice-to-have` `[ ] Skip`
  - Tool:
- **Mocking strategy:** (e.g., manual mocks, MSW, Mockito, mocktail)
- **Test file location:** co-located / separate `__tests__` directory / `test/` mirror

---

## 🟡 Environment & Configuration

- **Environment tiers:** `dev` / `staging` / `prod` (list all)
- **How env variables are managed:** (e.g., `.env` files, build flavors, `--dart-define`, EAS secrets)
- **Feature flags:** (provider and approach, e.g., LaunchDarkly, Firebase Remote Config, hardcoded)
- **Sensitive keys:** (list which keys exist — NOT the values — and where they're stored)

---

## 🟡 Third-Party Integrations

| Service | Purpose | SDK / Package | Notes |
| ------- | ------- | ------------- | ----- |
|         |         |               |       |
|         |         |               |       |
|         |         |               |       |

---

## 🟡 Performance & Optimization

- **Target cold-start time:**
- **Target frame rate:**
- **Image handling:** (CDN, caching, lazy loading, progressive, format)
- **List virtualization:** (approach for long scrollable lists)
- **Bundle size concerns:**
- **Known performance hotspots from v1:**

---

## 🟢 Internationalization (i18n)

- **Supported locales:**
- **Default locale:**
- **i18n library:**
- **RTL support:** `[ ] Yes` `[ ] No`
- **Where do translations live:**
- **String key naming convention:**

---

## 🟢 Accessibility (a11y)

- **Target compliance level:** (e.g., WCAG 2.1 AA)
- **Screen reader testing:** `[ ] VoiceOver` `[ ] TalkBack` `[ ] Both`
- **Min tap target size:**
- **Dynamic text / font scaling:** `[ ] Supported` `[ ] Not supported`
- **Reduced motion support:** `[ ] Yes` `[ ] No`

---

## 🟢 Push Notifications

- **Provider:**
- **Notification types:**

| Type | Trigger | Action on tap | Foreground behavior |
| ---- | ------- | ------------- | ------------------- |
|      |         |               |                     |
|      |         |               |                     |

- **Permission request timing:** (when and how the app asks for notification permission)

---

## 🟢 Monitoring, Logging & Crash Reporting

- **Crash reporting tool:**
- **Logging approach:** (structured logs? log levels? where do they go?)
- **APM / performance monitoring:**
- **User-facing error IDs:** `[ ] Yes` `[ ] No`

---

## 🟢 CI/CD & Release

- **CI platform:**
- **Build triggers:**
- **Code signing approach:**
- **Release channels:** (e.g., internal → beta → production)
- **OTA updates:** `[ ] Yes (tool: ___)` `[ ] No`
- **App versioning scheme:**

---

## 🔴 Coding Standards & Conventions

> These rules are enforced on every line of code Claude writes.

### Naming conventions

- Files:
- Components / Widgets:
- Functions:
- Variables:
- Constants:
- Types / Interfaces:
- Enums:

### Code style

- **Max file length:** (e.g., 300 lines — split if longer)
- **Max function length:**
- **Import ordering:** (e.g., external → internal → relative, alphabetical within groups)
- **Linter config:** (paste or reference the config file)
- **Formatter:** (e.g., Prettier, dart format, ktlint)

### Documentation expectations

- **Inline comments:** when and where?
- **Doc comments on public APIs:** `[ ] Required` `[ ] Not required`
- **README per module:** `[ ] Yes` `[ ] No`

### Git conventions

- **Branch naming:** (e.g., `feature/MODULE-short-description`)
- **Commit format:** (e.g., conventional commits: `feat(auth): add biometric login`)
- **PR size preference:** (e.g., < 400 lines changed)

---

## 🔴 AI Collaboration Rules

> These are instructions for how Claude should behave during this project.

### Response format

- When I ask you to build a feature, always start with:
  1. A brief summary of your understanding of the requirement
  2. A file-by-file implementation plan (list every file you'll create/modify)
  3. Then the code
- After the code, list any assumptions you made and any open questions.

### Code generation rules

- Always generate complete, runnable files — no `// ... rest of component` shortcuts.
- Include all imports.
- Include all types/interfaces.
- Include basic error handling in every async operation.
- Include loading and error states for every screen that fetches data.
- Never hardcode strings that should be configurable or translatable.
- Never use `any` type (or equivalent in your language) unless explicitly approved.
- Always handle the null/empty case for lists, optional fields, and nullable types.

### What not to do

- Don't refactor code I haven't asked you to refactor.
- Don't change the tech stack or architecture unless I ask for a recommendation.
- Don't add libraries or dependencies without listing them first and getting approval.
- Don't generate placeholder/dummy data in production code — use clearly marked fixtures.

### Module workflow

When I say **"Build [module name]"**, follow this sequence:

1. Review this CLAUDE.md for relevant context
2. List the screens, components, services, and models involved
3. Propose the file structure for this module
4. Wait for my approval, then generate code
5. After code, list what was built, what's left, and what to build next

---

## Appendix: Reference Material

> Paste or link any additional context that doesn't fit above.

- **API docs link:**
- **Figma / design link:**
- **Existing codebase repo link:**
- **PRD / requirements doc:**
- **Competitor apps to reference for UX:**
- **Technical RFCs or ADRs:**

---

_Last updated: YYYY-MM-DD_
_Template version: 1.0_
