# CLAUDE.md - Streetballer

## Executive Summary

For amateur basketball players who face a lack of playing opportunities, Streetballer is a mobile app that that helps them find courts, organize pick-up games, and compete with others. Unlike other community apps or local solutions, Streetballer lets players browse a global map of more than 50000 basketball courts, see when other players are playing, sign up to play wherever and whenever it suits them, and gamify the entire playing experience by building their team, recording scores, and earning league points.

## Project Overview

| Route               | Type            | Link to Screenshot                                                | Features                                                                   |
| ------------------- | --------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------- |
| /home               | Top-level Route | ![01-home.png](./.claude/screens/01-home.png)                     | Manage team, See nearby players/teams, Manage recent scores, Record scores |
| /games              | Top-level Route | ![02-games.png](./.claude/screens/02-games.png)                   | Find upcoming games                                                        |
| /courts             | Top-level Route | ![03-courts.png](./.claude/screens/03-courts.png)                 | Browse basketball courts, Add missing courts                               |
| /courts/:court_id   | Child Route     | ![04-court.png](./.claude/screens/04-court.png)                   | View court details, Find upcoming games, Sign up to play                   |
| /league             | Top-level Route | ![05-league.png](./.claude/screens/05-league.png)                 | Follow league rankings                                                     |
| /score              | Child Route     | ![06-score.png](./.claude/screens/06-score.png)                   | See score details, Confirm/reject scores                                   |
| /players            | Top-level Route | ![07-player.png](./.claude/screens/07-player.png)                 | See own player profile, See scores history                                 |
| /players/:player_id | Child Route     | ![07-player.png](./.claude/screens/07-player.png)                 | See player profile, See matchup history                                    |
| /settings           | Top-level Route | ![08-settings.png](./.claude/screens/08-settings.png)             | Manage account settings                                                    |
| /qr                 | Modal Overlay   | ![09-qr.png](./.claude/screens/09-qr.png)                         | Show own QR code, Invite people to Streetballer                            |
| /authentication     | Modal Overlay   | ![10-authentication.png](./.claude/screens/10-authentication.png) | Log in, Create account, Reset password                                     |

## Tech Stack

| Layer          | Technology                                      |
| -------------- | ----------------------------------------------- |
| Target OS      | Android, iOS, Web                               |
| Frontend       | Dart, Flutter                                   |
| Backend        | Python, FastAPI                                 |
| Database       | MongoDB                                         |
| Analytics      | PostHog                                         |
| Infrastructure | Google Cloud, Bazel, Jenkins, Docker, CodeMagic |

## Libraries & Tools

| Purpose               | Layer    | Libraries                   |
| --------------------- | -------- | --------------------------- |
| State Management      | Frontend | flutter_riverpod            |
| Dependency Injection  | Frontend | flutter_riverpod            |
| Navigation            | Frontend | go_router                   |
| Local Storage         | Frontend | flutter_secure_storage      |
| HTTP Client           | Frontend | http                        |
| Localization          | Frontend | intl, flutter_localizations |
| Maps                  | Frontend | google_maps_flutter         |
| Geolocation           | Frontend | geolocator                  |
| SVG Images            | Frontend | flutter_svg                 |
| QR Codes              | Frontend | mobile_scanner, qr_flutter  |
| Environment Variables | Frontend | envied                      |
| Testing               | Frontend | test                        |
| Package Manager       | Backend  | uv                          |
| Database Driver       | Backend  | pymongo                     |
| Credential Hashing    | Backend  | argon2-cffi                 |
| Cron Jobs             | Backend  | python-crontab              |
| Environment Variables | Backend  | python-dotenv               |
| Email Driver          | Backend  | smtplib                     |
| Authentication        | Backend  | pyjwt                       |
| Testing               | Backend  | pytest                      |

## Folder Structure

- frontend/ (Dart + Flutter Frontend)
  - dist/ (Production Code)
  - infrastructure/ (DevOps-related Files)
  - src/ (Source Code)
    - assets/ (Static Assets)
      - fonts/ (TTF Fonts)
      - icons/ (SVG Icons)
      - images/ (SVG/PNG/JPG Images)
      - locales/ (ARB Localization Files)
    - common/ (Project-scoped Functionality)
      - constants/ (Constant Values)
      - environment/ (Environment Connectors)
      - models/ (Data Models)
      - libraries/ (Wrappers for 3rd Party Libraries)
      - routes/ (Screen Routing)
      - screens/ (Comprehensive Screens)
      - services/ (Core Service Interfaces)
      - widgets/ (Modular Widgets)
      - utilities/ (Simple Utilities)
    - modules/ (Module-scoped Functionality)
      - {module-name}/ (Module Folder)
        - models/ (Data Models)
        - screens/ (Comprehensive Screens)
        - widgets/ (Modular Widgets)
        - logic/ (Business Logic)
    - main.dart (Application Entrypoint)
  - test/ (Test Directory)
    - helpers/ (Testing Helpers)
    - tests/ (Test Files)
- backend/ (Python + FastAPI Backend)
  - dist/ (Production Code)
  - infrastructure/ (DevOps-related Files)
  - seed/ (Seeding Folder)
    - data (Seeding Data)
    - helpers (Seeding Helpers)
    - seeds (Seeding Files)
    - seed.py (Seeding Entrypoint)
  - src/ (Source Code)
    - assets/ (Static Assets)
      - images/ (SVG/PNG/JPG/ICO Images)
      - locales/ (JSON Localization Files)
    - common/ (Project-scoped Functionality)
      - constants/ (Constant Values)
      - controllers/ (High-Level Route Controllers)
      - environment/ (Environment Connectors)
      - middleware/ (Router Middleware)
      - models/ (Data Models)
      - libraries/ (Wrappers for 3rd-party Libraries)
      - logic/ (Business Logic)
      - routes/ (Request Routing)
      - services/ (Core Service Interfaces)
      - utilities/ (Simple Utilities)
    - modules/ (Module-scoped Functionality)
      - {module-name}/ (Module Folder)
        - models/ (Data Models)
        - controllers/ (High-Level Route Controllers)
        - logic/ (Business Logic)
    - main.py (Application Entrypoint)
  - test/ (Testing Folder)
    - helpers (Testing Helpers)
    - tests (Testing Files)
    - test.py (Testing Entrypoint)

## General Preferences

| Do                                                                 | Don't                                                                  |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| Short files with a single specific responsibility                  | Complete but long files with multiple responsibilities                 |
| Verbose code that is easy to understand on its own                 | Extensive comments or abbreviated variable names                       |
| Reusable and customizable code components                          | Duplicate code implementation                                          |
| Repeated, consistent, junior-friendly patterns                     | Case-by-case logic, inconsistencies across files, complex patterns     |
| Strict type safety                                                 | Loose type flexibility                                                 |
| Recognizable business logic separate from technical implementation | Overlap of business logic and technical implementation                 |
| Performance-optimized code based on official documentation         | Compromise of performance for developer-friendliness                   |
| Specific and targeted libraries                                    | Heavy batteries-included libraries                                     |
| Popular, proven, well-documented libraries                         | Little-known, experimental, outdated libraries                         |
| Provider-agnostic custom library wrapping                          | Direct library calls in multiple places                                |
| Returning null/false/empty values instead of throwing errors       | Throwing errors when a null/false/empty value communicates the message |
| Detailed errors for developers, minimal errors for users           | Non-standard and unpredictable error structure                         |
| Local error handling with global error handling as a fallback      | Silent or blocking errors                                              |
| Efficient database indexing, querying, caching                     | Data duplication or inefficiencies in database interactions            |
| Skeleton-style or spinner-style loading states                     | Static loading states                                                  |
| Localization managed in centralized .arb or .json files            | Hard-coded text tokens                                                 |
| Environment variables managed in centralized .env files            | CLI arguments or hard-coded values to define environment variables     |
| Centralized documentation with README.md files                     | Distributed comments as a means of documentation                       |
| Ask questions, explain thinking, propose ideas when in doubt       | Guessing about decisions not specifically documented                   |

## Structural Choices

- Architecture: Build an easy-to-maintain monolith rather than complex highly optimized microservices.
- Authentication: Adhere to OAuth2 best practices and implement lazy login that only requires authentication for features that either A) read requester-specific data or B) write data.
- Testing: Follow a TDD approach and work in red/green/refactor cycles, only testing top-level logic only to recursively and efficiently ensure high coverage.
- Security: Robust baseline security comes first, beyond that, excellent user experience comes before additional potentially annoying security measures.
- Localization: English is the default locale with more languages to be added later.
- DevOps: Write and maintain scripts to enable an agile CI/CD pipeline.

## Detailed Documentation

Detailed requirements are documented in the .claude/ folder and structured as follows:

- models.md documents the data structures and business logic: This file governs the project-specific data models and rules
- views.md documents the user interface and design guidelines: This file along with the referenced screenshots govern the UI/UX design
- controllers.md documents the API specification and technical implementation: This file governs the backend API
- The subfolders in the .claude/ folder contains further assets that you may need to reference

## Cooperation Process

Cooperation is based on the Double Diamond framework by the British Design Council. You may shorten, skip, or merge steps when a given task allows it for token optimization.

1. Discover: Based on a one-line goal description, ask questions and browse documentation to explore context.
2. Define: Narrow the information down to specific requirements, methods, and expected output.
3. Develop: Execute the defined tasks and run tests.
4. Deliver: Implement feedback, document the changes, and commit to source control with an informative message.

## Coding Agent Comments (Managed by Coding Agent)

At the end of every session, update "Project Status", "Commands", and "Notes" autonomously and commit changes to source control with an informative commit message. Make sure this file never exceeds 300 lines. Prune "Notes" first to remove unnecessary lines.

### Project Status

| Task             | Comments                                         |
| ---------------- | ------------------------------------------------ |
| Last Task        | Build league module endpoint (157 tests passing) |
| Next Task        | Build settings module endpoints                  |
| Blocking Factors |                                                  |

### Commands

| Command                                                          | Task                 |
| ---------------------------------------------------------------- | -------------------- |
| `cd backend && uv run uvicorn src.main:app --port 3000 --reload` | Start dev server     |
| `cd backend && uv run pytest test/tests/ -v`                     | Run tests            |
| `cd backend && uv sync --dev`                                    | Install dependencies |

### Notes

- Backend lives in `backend/`, run all commands from that directory
- uv creates a `.venv` — IDE may show false "not installed" hints for system Python
- `.env` is gitignored; use `.env.example` as the template
- Add CLAUDE.md updates to the Notes section only; never edit sections above it
- Always enforce model field access levels (public/private/secret) when serializing API responses
- Implement business logic exactly as specified in models.md — never extrapolate
- MongoDB: use `$geoWithin $centerSphere` for range searches; `$nearSphere`/`$near` only for ordered nearest-document lookups
- MongoDB: use text indexes (`$text`) over regex (`$regex`) for text search
- MongoDB: when text + coordinates are both provided, search by text first then sort results by distance
- Data models: use dataclasses (`Player`, `Court`, `Game`, `Place`, `Score`) in `src/common/models/`; always call `Model.from_doc(doc)` when reading from DB; always call `model.to_doc()` when inserting to DB
- DB projections: every DB read must include an explicit projection dict; default to `{"_id": 1}` for existence checks; define projections as module-level constants near the top of logic files
- DB wrapper: use `get_one`/`get_many`/`insert_one`/`update_one`/`update_many`/`delete_one` from `src.common.libraries.database`; `insert_one` returns `str`; catch `DuplicateEntryError` (not pymongo's `DuplicateKeyError`)
