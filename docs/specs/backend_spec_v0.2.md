# APPLI Backend Specification (v0.2 - Complete)

Status: DRAFT (to freeze after step-10)  
Owner: Sam (Product/TD) + APPLI Backend Lead  
Repo: backend/  
Stack: FastAPI 0.115+, Python 3.11+, SQLAlchemy 2.0, Alembic, Postgres 15, Redis 7, MinIO (S3), RQ or Celery  
Encoding: ASCII only (no accents in code)

---

## 0. Table of contents

1. Scope & principles
2. Architecture & code layout
3. Multi tenancy & RBAC model
4. Data model (ERD, constraints, indexes)
5. API conventions (auth, versioning, pagination, sorting, filtering, idempotency, errors)
6. Modules (requirements, endpoints, schemas, rules, examples)
7. Background jobs & notifications
8. Files & documents
9. Calendars & exports (ICS, CSV, PDF)
10. Webhooks & integrations
11. Observability (metrics, logs, traces, audit)
12. Performance, caching, rate limiting
13. Security & compliance (GDPR, backups, DSR)
14. Config & environments
15. Migrations & seed data
16. Testing strategy & fixtures
17. CI/CD & quality gates
18. Versioning & deprecation policy
19. Acceptance criteria checklist
20. Roadmap steps (01..20) with deliverables
21. Glossary

---

## 1. Scope & principles

Backend provides:

* Planning: projects, venues, spaces, missions, shifts, assignments.
* HR/People: users, profiles, skills, availability, leaves.
* Finance light: timesheets, rates, costs, invoice stubs.
* Knowledge: equipment lists, checklists, notes, files.
* Comms: notifications (email, telegram), reminders, webhooks.
* Exports: ICS, CSV, PDF.

Principles:

* API first, deterministic, stable contracts.
* Secure by default: JWT, RBAC, minimized scopes, least privilege.
* Resilience: outbox, retries, idempotency, backoff.
* Observability by design.
* Windows-first dev scripts; ASCII-only docs.

Non-goals v0.2: full payroll, complex accounting, real-time sockets.

---

## 2. Architecture & code layout

Logical diagram:

```
[SPA/Clients] -> HTTP JSON -> [FastAPI]
                              |-> Services (domain)
                              |-> Event Bus (in-proc)
                              |-> Postgres (SQLAlchemy)
                              |-> Redis (cache, queues)
                              |-> S3 (files)
                              |-> Workers (RQ/Celery)
                              |-> SMTP / Telegram API
```

Code layout:

```
backend/
  app/
    core/           # settings, db, security, utils, error handling
    auth/           # login, refresh, invites, sessions
    orgs/           # org, memberships, roles
    projects/       # projects, venues, spaces
    planning/       # missions, shifts, assignments, availability
    people/         # profiles, skills, leaves
    timesheets/     # timesheets, rates, costs
    inventory/      # equipment, sets, checklists
    notes/          # notes, comments, tags
    files/          # presigned URLs, uploads
    notify/         # notifications, templates, deliveries, outbox
    calendar/       # ICS feeds, ranges
    exports/        # CSV, PDF jobs
    webhooks/       # endpoints to notify third parties
    audit/          # audit logs
    observability/  # metrics, trace
    api.py          # router assembly
    main.py         # FastAPI app factory
  migrations/       # alembic
  tests/            # unit, integration, e2e
  scripts/          # ps1 helpers
```

Service layering:

* Routers stay thin; they parse/validate requests and call services.
* Services implement business rules and compose repositories and adapters.
* Repositories isolate SQLAlchemy usage; no raw queries outside repositories.
* Background jobs reuse the same services layer to avoid divergent logic.
* Shared DTOs live under app/schemas and are reused by routers and workers.

Cross-cutting packages (core/, observability/, audit/) expose helpers that may
be imported by any module; all other packages depend only on core/ + schemas.

---

## 3. Multi tenancy & RBAC model

Tenancy:

* All business tables include org_id.
* Users are global; membership ties user to org with role.
* Queries MUST scope by org_id from auth context.

Roles (baseline):

* owner: full rights, billing, org settings.
* admin: manage users, projects, planning, exports.
* manager: manage planning inside projects they own or are assigned to.
* worker: read own assignments, confirm/decline, timesheets self.
* viewer: read-only org scope.

Default mappings:

* On org creation: creator becomes owner, owner also granted manager role on
  seed project for onboarding walkthrough.
* Each membership row stores primary_role plus optional scopes (project ids)
  when role == manager.

RBAC enforcement:

* Dependencies inject CurrentUser context (user_id, org_id, roles, scopes).
* Decorator `require_role(roles: list[str])` guards routers.
* Manager access: service methods accept optional project scope and check
  membership scopes before fetching data.
* Worker endpoints auto restrict by user_id == current user.

Permission matrix (excerpt):

```
Resource        owner admin manager worker viewer
org             CRUD  CRUD  R      R      R
project         CRUD  CRUD  CRU    R      R
mission         CRUD  CRUD  CRU    R      R
shift           CRUD  CRUD  CRU    R      R
assignment      CRUD  CRUD  CRU    U-self R-self
timesheet       CRUD  CRUD  CRU    CRU-self R-self
file_asset      CRUD  CRUD  CRU    C-self  R
```

ABAC rules:

* Self access: user can read/modify own profile, sessions, timesheets.
* Project scoped managers can CRUD inside projects where they are manager.

---

## 4. Data model (ERD, constraints, indexes)

ERD (text):

```
org (id PK, name, created_at, updated_at)
user (id PK, email unique, password_hash, full_name, phone, status, created_at)
membership (id PK, org_id FK->org, user_id FK->user, role, created_at, unique(org_id,user_id))
project (id PK, org_id, name, code unique(org_id,code), start_date, end_date, venue_id FK, status)
venue (id PK, org_id, name, address, city, country, notes)
space (id PK, org_id, venue_id, name)
mission (id PK, org_id, project_id, title, description, budget_cents, status)
shift (id PK, org_id, mission_id, space_id, role, start_utc, end_utc, required_count, unique(mission_id, start_utc, end_utc, role))
assignment (id PK, org_id, shift_id, user_id, status, note, unique(shift_id,user_id))
availability (id PK, org_id, user_id, date, status)
skill (id PK, org_id, name, unique(org_id,name))
user_skill (org_id, user_id, skill_id, level, PK(org_id,user_id,skill_id))
file_asset (id PK, org_id, bucket, key, mime, size, created_by, created_at, sha256)
note (id PK, org_id, entity_type, entity_id, body, created_by, created_at)
notification (id PK, org_id, channel, template_key, payload_json, status, last_error, created_at)
notification_outbox (id PK, org_id, event_key, entity_type, entity_id, payload_json, attempts, next_attempt_at)
timesheet (id PK, org_id, assignment_id, start_utc, end_utc, hours, rate_cents, cost_cents)
rate (id PK, org_id, role, amount_cents, unit, active)
invoice_stub (id PK, org_id, project_id, number, total_cents, status)
audit_log (id PK, org_id, actor_user_id, action, entity_type, entity_id, data_json, created_at)
session (id PK, user_id, refresh_id, ua, ip, created_at, revoked_at)
```

Indexes:

* Common filters: idx on (org_id), (project_id), (user_id), (start_utc), (end_utc), (status).
* Text search: trigram on project.name, mission.title (optional v0.3).

Cascades:

* Deleting org prohibited (soft delete only) until archival done.
* Project delete -> cascade missions, shifts, assignments, timesheets.

Soft delete:

* add deleted_at on project, mission, shift, assignment (v0.3) . For v0.2: hard delete allowed for draft only.

Row validators:

* shift.start_utc < shift.end_utc
* assignment count per shift <= required_count

IDs:

* Use bigint PK or ULID (string) for external exposure. For v0.2 keep bigint.
* External ids follow pattern `apli_<base62>` to simplify later migration.

Enumerations:

* mission.status: draft|scheduled|completed|cancelled.
* shift.role: free text but validated against known skills when provided.
* assignment.status: proposed|confirmed|declined|cancelled.
* availability.status: available|busy|tentative.
* invoice_stub.status: draft|sent|paid|cancelled.
* notification.status: pending|sent|failed.

---

## 5. API conventions

Base path: /api/v1
Auth: Bearer access JWT in Authorization header.
Content: application/json; UTF-8.
Datetime: ISO-8601 UTC; fields end with _utc.
Pagination: cursor (opaque) via next_cursor; fallback offset/limit.
Sorting: sort=field,-field2; allowed fields listed per endpoint.
Filtering: query params; multi-value via comma (status=confirmed,declined).
Idempotency: Idempotency-Key header honored on POST for creates.
Errors: RFC7807 structure {type,title,status,detail,instance,code,errors}
ETag: return ETag on GET detail; support If-None-Match.
Rate limit headers: X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After.
OpenAPI: /openapi.json and /docs; in prod gated behind admin token.

---

## 6. Modules

### 6.1 Core

Endpoints:

* GET /healthz -> 200 {status:"ok"}
* GET /readyz -> checks db, redis, s3
* GET /info -> {version, git_sha, build_date, env}

### 6.2 Auth

Flows:

* Password login -> access(15m), refresh(14d) tokens; refresh rotation.
* Invite-only signup: POST /auth/invite {email, role} (owner/admin) -> email link.
* Password reset: request + confirm.
* Sessions: list, revoke.

Endpoints:

* POST /auth/login {email,password}
* POST /auth/refresh {refresh}
* POST /auth/logout {refresh}
* POST /auth/invite {email, role}
* POST /auth/signup {token, full_name, password}
* POST /auth/password/reset/request {email}
* POST /auth/password/reset/confirm {token,new_password}
* GET  /auth/sessions
* POST /auth/sessions/{session_id}/revoke

Schemas (excerpt):

* LoginResponse { access_token, refresh_token, expires_in }
* Session { id, ua, ip, created_at, revoked_at }

Validation:

* Email normalized lower-case; password rules: >= 8 chars.
* Rate limit: 10 login/min/IP.

### 6.3 Orgs & Users

Endpoints:

* GET /orgs
* POST /orgs {name}
* GET /orgs/{org_id}
* PATCH /orgs/{org_id} {name}
* GET /orgs/{org_id}/members
* POST /orgs/{org_id}/members {user_id, role}
* PATCH /orgs/{org_id}/members/{member_id} {role}
* DELETE /orgs/{org_id}/members/{member_id}
* GET /users/self
* PATCH /users/self {full_name, phone}
* GET /users?org_id=...&q=...&skill=...
* GET /users/{user_id}

Rules:

* Only owner/admin can manage memberships.

### 6.4 Projects & Venues & Spaces

Endpoints:

* GET /projects?org_id=&status=&q=&sort=code,-start_date
* POST /projects {org_id,name,code,start_date,end_date,venue_id,status}
* GET /projects/{id}
* PATCH /projects/{id}
* DELETE /projects/{id} (only draft)
* GET /venues?org_id=&q=
* POST /venues {org_id,name,address,city,country}
* GET /venues/{id}
* PATCH /venues/{id}
* GET /spaces?org_id=&venue_id=
* POST /spaces {org_id,venue_id,name}

### 6.5 Planning (missions, shifts, assignments)

Endpoints:

* GET /missions?project_id=&status=&q=

* POST /missions {project_id,title,description,budget_cents,status}

* GET /missions/{id}

* PATCH /missions/{id}

* DELETE /missions/{id} (draft only)

* GET /shifts?mission_id=&from=&to=&role=&space_id=

* POST /shifts {mission_id,space_id,role,start_utc,end_utc,required_count}

* GET /shifts/{id}

* PATCH /shifts/{id}

* DELETE /shifts/{id}

* GET /assignments?shift_id=&user_id=&status=

* POST /assignments {shift_id,user_id}

* PATCH /assignments/{id} {status:"proposed|confirmed|declined|cancelled"}

* DELETE /assignments/{id}

Rules:

* Conflict: overlapping confirmed shifts for same user -> 409.
* required_count >= number of confirmed assignments.
* State machine: proposed -> confirmed|declined; confirmed -> cancelled.

### 6.6 Availability & Leaves

Endpoints:

* GET /availability?user_id=&from=&to=
* PUT /availability/bulk {items: [{user_id,date,status}]}
* GET /leaves?user_id=&from=&to=
* POST /leaves {user_id,start_utc,end_utc,reason}

### 6.7 People & Skills

Endpoints:

* GET /skills?org_id=
* POST /skills {org_id,name}
* DELETE /skills/{id}
* POST /users/{user_id}/skills {skill_id, level}

### 6.8 Inventory & Checklists

Endpoints:

* GET /equipment?org_id=&q=&tag=
* POST /equipment {org_id,name,brand,model,serial,tags:[]}
* GET /equipment/{id}
* PATCH /equipment/{id}
* POST /equipment_sets {org_id,name,item_ids:[]}
* GET /checklists?mission_id=
* POST /checklists {mission_id,items:[{label,done}]}

### 6.9 Notes & Comments

* POST /notes {entity_type,entity_id,body}
* GET /notes?entity_type=&entity_id=

### 6.10 Timesheets & Rates

Endpoints:

* GET /timesheets?project_id=&user_id=&from=&to=
* POST /timesheets {assignment_id,start_utc,end_utc,rate_cents}
* PATCH /timesheets/{id}
* DELETE /timesheets/{id}
* GET /rates?org_id=&role=
* POST /rates {org_id,role,amount_cents,unit}

Rules:

* hours computed = (end-start) in hours with 2 decimals.
* cost_cents = hours * rate_cents (rounded).

### 6.11 Notifications

* POST /notifications/test {channel:"email|telegram", to:"...", template_key, vars:{}}
* GET  /notifications?status=&from=&to=
* Delivery log per message.

Templates variables (examples):

* assignment_confirmed: {user_name, mission_title, shift_start_utc, shift_end_utc, venue_name}
* shift_reminder: {user_name, shift_start_local, location}

### 6.12 Files

* GET  /files/presign/upload {mime, size, filename} -> {url, fields, key}
* GET  /files/presign/download?key=...
* POST /files/complete {key, sha256}

Policy:

* Object key prefix: org/{org_id}/{yyyy}/{mm}/{ulid}_{filename}

### 6.13 Calendar

* GET /calendar/ics/user/{user_id}?token=... -> feed with confirmed assignments only.
* GET /calendar/ics/project/{project_id}
* GET /calendar/ics/org/{org_id}

ICS details:

* UID: assignment-<id>@appli
* SUMMARY: <role> - <mission_title>
* LOCATION: <venue> / <space>
* DTSTART/DTEND: UTC; clients render in local time.

### 6.14 Exports

* GET /exports/timesheets.csv?project_id=&from=&to=
* POST /exports/mission-sheet.pdf {mission_id} -> enqueue job; returns job id.
* GET /exports/jobs/{job_id}

---

## 7. Background jobs & notifications

Worker: app.worker (choose RQ first for simplicity).
Queues:

* default: exports, reminders
* mail: email deliveries
* telegram: telegram deliveries

Retry policy: expo backoff 1s..5m, max 5 attempts. Dead letter collection with reason.

Outbox pattern:

* Insert into notification_outbox within same tx as domain change.
* Worker polls, sends, updates attempts/next_attempt_at.

---

## 8. Files & documents

* MinIO/S3; presigned PUT for uploads; virus scan hook (clamav container optional v0.3).
* ACL via signed GET URLs (expire <= 15 min) + server-side checks for metadata endpoints.
* Large files: multipart presign (v0.3).

---

## 9. Calendars & exports

* ICS feeds are long-lived signed tokens per user/project/org; revocable.
* PDF generated via weasyprint wkhtmltopdf in worker; HTML templates kept in exports/ templates.
* CSV via server streaming for large ranges.

---

## 10. Webhooks & integrations

Use-cases:

* Assignment status change
* Timesheet created/updated

Endpoints:

* POST /webhooks/endpoints {url, secret, events:[...]}
* GET /webhooks/endpoints
* DELETE /webhooks/endpoints/{id}

Delivery:

* HMAC-SHA256 signature header: X-Appli-Signature: t=<ts>, s=<hex>
* Retry with exponential backoff, up to 10 attempts; event log stored.
* Idempotency: provide X-Appli-Event-Id header; receivers should dedupe.

---

## 11. Observability

Metrics (Prometheus):

* http_requests_total{path,method,status}
* http_request_duration_seconds{path}
* jobs_enqueued_total{queue}
* jobs_failures_total{queue}
* notifications_sent_total{channel,status}

Logs:

* JSON lines; fields: ts, level, msg, request_id, user_id, org_id, action, entity_type, entity_id.

Tracing:

* OpenTelemetry OTLP exporter; trace id returned via header Trace-Id.

Audit:

* audit_log rows for create/update/delete on sensitive entities (user, membership, assignment, timesheet, file_asset).

---

## 12. Performance, caching, rate limiting

Caching:

* Redis cache for reference data (skills, venues) TTL 5 min.
* ETag and If-None-Match on detail endpoints.

Rate limits:

* Auth: 60 req/min/IP; login: 10/min/IP; password reset: 3/hour/email.
* API: 1000 req/min/org; burst 200.
* Webhook deliveries: 30 attempts/min/endpoint to avoid flooding.

---

## 13. Security & compliance

Security checklist:

* Hash: argon2id for passwords.
* JWT: HS256 with rotation; store jti; blacklist used refresh.
* CORS: allow configured origins only.
* Headers: HSTS, no sniff, xss protect, frame deny.
* Input validation on all schemas; max lengths; uploaded file size limit.

GDPR:

* DSR endpoints: GET /gdpr/export/self, POST /gdpr/delete/self (queued, soft delete account, mask PII, keep audit min data).
* Data minimization: optional fields off by default.

Data residency & encryption:

* Postgres encrypted at rest via cloud provider (if self hosted use pgcrypto).
* S3 bucket enforces SSE-S3; keys rotated annually.
* Redis configured with AUTH secret and TLS when supported by env.

Backups:

* Daily pg_dump; retention 30d; monthly archive 6mo; tested restore runbook.

Data retention:

* Audit logs kept 1 year; notifications 90d; outbox 30d.

---

## 14. Config & environments

.env sample:

```
APP_ENV=dev
DB_URL=postgresql+psycopg://user:pass@db:5432/appli
REDIS_URL=redis://redis:6379/0
S3_ENDPOINT=http://minio:9000
S3_BUCKET=appli-files
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
SMTP_HOST=mailhog
SMTP_PORT=1025
TELEGRAM_BOT_TOKEN=...
JWT_SECRET=change_me
ACCESS_TOKEN_TTL_MIN=15
REFRESH_TOKEN_TTL_DAYS=14
RATE_LIMIT_PER_ORG_PER_MIN=1000
```

Environment matrix:

* dev: docker compose, seeded data, debug logging, mailhog/console outputs.
* staging: mirrors prod sizing, feature flags default ON, CI deploys on main.
* prod: replica count >= 2, debug disabled, telemetry exporters targeting ops
  stack, cron jobs enabled.

Configuration precedence: env vars > secrets manager > .env file. PowerShell
scripts load `.env` and allow overrides via `-Env` parameter.

---

## 15. Migrations & seed data

* Alembic with autogenerate then manual review; deterministic revision ids.
* Seed script creates: demo org, owner admin, 10 skills, demo venue/space, project with 2 missions, 6 shifts, 4 users, 8 assignments, timesheets.

---

## 16. Testing strategy & fixtures

* Unit tests: services, validators; DB mocked.
* Integration: real Postgres (test container), Redis, MinIO; pytest markers.
* API contract: snapshot OpenAPI + example based tests.
* E2E thin: login -> create project -> mission -> shifts -> assign -> ics.
* Coverage thresholds: 85 lines, 80 branches; fail CI under.

Fixtures:

* factory functions for org, user, membership, project, mission, shift, assignment.

---

## 17. CI/CD & quality gates

GitHub Actions jobs:

* lint: ruff, black check
* typecheck: mypy
* test: pytest with coverage, upload artifacts
* security: bandit, pip-audit
* docker: build backend image; trivy scan
* docs_guard: ensure spec and roadmap updated
* roadmap_guard: step ref present in commits
* release: tag vX.Y.Z, push image

Quality gates:

* All jobs must pass on PR before merge; branch protection on main.
* Required reviewers: backend lead + product (Sam) for specs touching docs.
* CI comments back OpenAPI diff and coverage deltas.

Deployment:

* Successful main build triggers staging deploy; prod requires manual approve
  with change ticket id logged in release notes.

---

## 18. Versioning & deprecation

* API path /api/v1; breaking changes only in v2.
* Deprecation header: X-API-Deprecated: true; X-API-EOL: 2026-03-31.
* Changelog in docs/CHANGELOG.md.

Version policy:

* Additive changes only within v1.x; remove fields via deprecation cycle
  (announce -> 90d overlap -> remove).
* Publish migration guides in docs/specs when introducing non-breaking but
  impactful behavior changes (ex: new mandatory query param for exports).

---

## 19. Acceptance criteria checklist (excerpt)

Auth:

* Login returns access+refresh; rotation works; session list shows active sessions; revoke works.
* Rate limit enforced on login.

Planning:

* Overlap conflict returns 409 with code PLAN_001.
* required_count cannot be under confirmed count (422 PLAN_002).

Calendar:

* ICS feed validates on ical parsers; events match confirmed assignments only.

Notifications:

* On confirm, outbox row created; worker delivers email; delivery log shows 200 status.

Files:

* Upload works via presign; sha256 stored; download presign expires.

Timesheets:

* cost_cents computed correctly with rounding; CSV export contains headers and rows.

Observability:

* /metrics exposes http_* metrics; traces visible on dev exporter.

---

## 20. Roadmap steps (01..20)

* step-01: bootstrap app, settings, health/info, logging base
* step-02: db setup, alembic, core tables (org, user, membership, session)
* step-03: auth flows (login, refresh, logout, invite, signup, password reset) + tests + rate limits
* step-04: orgs/users endpoints, RBAC middleware, role matrix tests
* step-05: projects/venues/spaces CRUD + filters/sort + tests
* step-06: missions CRUD + search + tests
* step-07: shifts CRUD + validations + indexes + tests
* step-08: assignments workflow + conflict detection + tests
* step-09: availability/leaves + bulk upsert + tests
* step-10: skills and people profiles + tests
* step-11: timesheets + rates + CSV export + tests
* step-12: notifications infra (outbox, templates, delivery workers) + tests
* step-13: files (S3 presign) + sha256 + tests
* step-14: calendar ICS feeds + tokens + tests
* step-15: PDF exports job + job status + tests
* step-16: observability (prom metrics, otel traces) + audit log hooks
* step-17: rate limiting middleware + headers + tests
* step-18: webhooks endpoints + signing + retries + tests
* step-19: seed data + demo script + load test (k6 smoke)
* step-20: hardening pass (security, indexes, constraints) + docs freeze

Each step produces: endpoints, schemas, migrations, tests, CI green, OpenAPI updated, README notes, acceptance checklist; VALIDATE? yes/no by Sam.

---

## 21. Glossary

* Mission: group of tasks within a project.
* Shift: time slot attached to a mission and role.
* Assignment: a user scheduled on a shift with a status.
* Outbox: durable queue in DB for eventual delivery by workers.
* DSR: data subject request.

---

## Appendix A. Error codes

* AUTH_001 invalid_credentials
* AUTH_002 refresh_invalid
* AUTH_003 too_many_attempts
* ORG_001 membership_required
* PLAN_001 overlap_conflict
* PLAN_002 required_count_violation
* FILE_001 upload_too_large
* FILE_002 virus_detected
* EXPT_001 export_failed

---

## Appendix B. Sorting and filtering per resource (excerpt)

projects: sort=name,code,start_date; filter=status,venue_id,q
missions: sort=title,status; filter=project_id,status,q
shifts: sort=start_utc,end_utc; filter=mission_id,role,space_id,from,to
assignments: sort=status; filter=shift_id,user_id,status

---

## Appendix C. Sequence examples (ASCII)

Assignment confirm -> email

```
Client -> API: PATCH /assignments/{id} {status: confirmed}
API: tx begin
API: update assignment
API: insert outbox(event=assignment.confirmed)
API: tx commit
Worker -> Outbox: fetch event
Worker -> SMTP: send email
Worker -> DB: log delivery
```

---

## Appendix D. OpenAPI

* Expose /openapi.json; generate clients later; examples on key endpoints.

---

END OF SPEC v0.2
