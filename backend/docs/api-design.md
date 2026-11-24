# API design (Sprint 1) - SA-5

Sources: team use case diagram, workflow diagram and architecture document (SA-3, SA-4).
This file describes the API of the whole project. Endpoints marked (later sprint) are designed here but built after Sprint 1.
Anything not stated in the team documents is listed under "Open questions" at the end.

## Actors and roles

Three actors, as in the use case diagram:

| Actor | Role code | Notes |
|---|---|---|
| Candidat | CANDIDAT | Two states. Invité: no account, identified by a chat session and its X-Session-Token. Connecté: has an account (SA-27). |
| Responsable | RESPONSABLE | Linked to one institution (IIT or ISB). Manages the program information, interviews and decisions of that institution only. Reads its dossiers and dashboards. |
| Administrateur | ADMINISTRATEUR | Manages institutions, accounts and access, configures the AI models, reads all dashboards. |

## Access rules

Legend: yes = allowed, own = only on its own data, own institution = only on data of the institution the Responsable is linked to, no = refused.

### Catalog (Superviser les informations des formations, S'informer)

| Endpoint | Invité | Candidat connecté | Responsable | Administrateur |
|---|---|---|---|---|
| GET /api/institutions | yes | yes | yes | yes |
| POST, PUT /api/institutions | no | no | no | yes |
| GET /api/programs | yes | yes | yes | yes |
| GET /api/programs/{id} | yes | yes | yes | yes |
| GET /api/programs/{id}/fees?year= | yes | yes | yes | yes |
| GET /api/programs/{id}/deadlines?year= | yes | yes | yes | yes |
| GET /api/programs/{id}/admission-conditions?year= | yes | yes | yes | yes |
| POST /api/programs | no | no | own institution | no |
| PUT, DELETE /api/programs/{id} | no | no | own institution | no |
| POST, PUT, DELETE on fees, deadlines, admission-conditions | no | no | own institution | no |
| POST /api/documents (upload a brochure for the RAG corpus) | no | no | own institution | no |

### Chat (Échanger avec le chatbot, texte ou audio)

| Endpoint | Invité | Candidat connecté | Responsable | Administrateur |
|---|---|---|---|---|
| POST /api/chat/sessions | yes | yes | no | no |
| GET /api/chat/sessions/{id}/messages | own | own | no | no |
| POST /api/chat/sessions/{id}/messages (text) | own | own | no | no |
| POST /api/chat/sessions/{id}/audio (multipart) (later sprint) | own | own | no | no |
| POST /api/chat/sessions/{id}/claim (SA-28) | no | own | no | no |

### Accounts

| Endpoint | Invité | Candidat connecté | Responsable | Administrateur |
|---|---|---|---|---|
| POST /api/auth/register | yes | no | no | no |
| POST /api/auth/login | yes | yes | yes | yes |
| GET, POST, PUT, DELETE /api/admin/users | no | no | no | yes |

### Candidat: préinscription, QCM et entretien

| Endpoint | Invité | Candidat connecté | Responsable | Administrateur |
|---|---|---|---|---|
| POST /api/applications (body: program_id and personal information) | no | yes | no | no |
| GET /api/applications/me | no | own | no | no |
| GET /api/applications/{id}/qcm (later sprint) | no | own | no | no |
| POST /api/applications/{id}/qcm/answers (later sprint) | no | own | no | no |
| GET /api/applications/{id}/interview-slots | no | own | no | no |
| POST /api/applications/{id}/interview-slots/{slot_id}/confirm | no | own | no | no |

The usual path for an invité: chat freely, choose a program, register an account (POST /api/auth/register), claim the conversation (SA-28), then send POST /api/applications with the chosen program_id.

### Responsable: dossiers, entretiens, décisions, statistiques

| Endpoint | Invité | Candidat connecté | Responsable | Administrateur |
|---|---|---|---|---|
| GET /api/applications | no | no | own institution | no |
| GET /api/applications/{id} (dossier, plus résumé IA and QCM result in a later sprint) | no | own | own institution | no |
| GET /api/interviews | no | no | own institution | no |
| PUT /api/interviews/{id} | no | no | own institution | no |
| POST /api/applications/{id}/decision | no | no | own institution | no |
| GET /api/dashboard/stats | no | no | own institution | yes |

### Administrateur: configuration IA

| Endpoint | Invité | Candidat connecté | Responsable | Administrateur |
|---|---|---|---|---|
| GET /api/admin/ai-config | no | no | no | yes |
| PUT /api/admin/ai-config (choix du LLM, paramètres RAG) | no | no | no | yes |

## Conventions

- JSON fields are snake_case (FastAPI default).
- year defaults to the current admission cycle and the response echoes the year used.
- Lists are paginated with page (from 0) and size (default 20).
- Errors have the form {"error": {"code": "invalid_session", "message": "...", "details": null}}.
- 401 means not authenticated or invalid credentials. 403 means authenticated but not allowed, or an invalid chat session.
- A Responsable who touches data of another institution gets 403.
- Chat session id is a UUIDv4. Access also requires the random session token in the X-Session-Token header. The server stores only a SHA-256 hash of the token.
- Logged-in users send their credentials in the Authorization header. The exact mechanism is decided in SA-27.


