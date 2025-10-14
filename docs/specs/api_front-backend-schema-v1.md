# Coulisses Crew API Front <-> Backend Schema v1

## Vue d ensemble

* Base URL Staging: https://api.staging.coulisses-crew.example/v1
* Base URL Prod: https://api.coulisses-crew.example/v1
* Transport: JSON over HTTPS, auth JWT (access + refresh)
* Date/heure: ISO 8601 (UTC) ex `2025-10-14T13:00:00Z`
* IDs: UUID v4 (string)
* Pagination: curseur (`limit` 1..200, defaut 50, `cursor` opaque, reponse `next_cursor`)
* Tri: `sort=field[:asc|:desc]`
* Filtres: query params (`status=active&role=TECH`), intervalles `start=..&end=..`
* Erreurs: `application/problem+json`
* Version: `/v1` + header `X-API-Version: 1`
* Idempotence pour POST sensibles: header `Idempotency-Key: <uuid>`
* Caches: ETag/If-None-Match sur GET (304 si non modifie)

Rate limit: 120 req/min/IP (429). RBAC serveur via claim `roles=["ADMIN","MANAGER","TECH","ACCOUNTANT"]`.

## 0. Modele d erreur

```
{
  "type": "https://api.coulisses-crew.example/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "Field 'email' is invalid",
  "instance": "req_01HE...",
  "errors": [{"field":"email","code":"invalid","message":"invalid email"}]
}
```

Codes communs: 400 bad_request, 401 unauthorized, 403 forbidden, 404 not_found, 409 conflict, 412 precondition_failed, 422 validation_error, 429 rate_limited, 500 server_error.

## 1. Auth

* `POST /v1/auth/login` -> `{ "access_token":"jwt", "refresh_token":"jwt", "user": {"id":"uuid","email":"sam@example.com","roles":["MANAGER"]} }`
* `POST /v1/auth/refresh` -> `{ "access_token":"jwt" }`
* `POST /v1/auth/logout` (Authorization: Bearer) -> 204

## 2. Users

### GET /v1/users

Query: `limit,cursor,search,role,status`

```
{
  "items": [
    {
      "id":"uuid",
      "email":"...",
      "first_name":"...",
      "last_name":"...",
      "roles":["TECH"],
      "status":"active",
      "avatar_url":null
    }
  ],
  "next_cursor": null
}
```

### POST /v1/users

```
{ "email":"...","first_name":"...","last_name":"...","roles":["TECH"],"password":"***" }
```

Response 201: `{ "id":"uuid" }`

### GET /v1/users/{id}

Renvoie le detail utilisateur.

### PATCH /v1/users/{id}

Mise a jour partielle, retourne le detail utilisateur.

### DELETE /v1/users/{id}

204.

## 3. Missions

Structure:

```
{
  "id":"uuid",
  "title":"Josephine Baker",
  "project_id": "uuid|null",
  "location":"Bobino",
  "start":"2025-11-24T08:00:00Z",
  "end":"2025-11-24T23:00:00Z",
  "status":"draft|confirmed|cancelled",
  "budget_eur": 1200.00,
  "notes":"...",
  "tags":["lumiere","video"],
  "created_by":"uuid",
  "created_at":"...",
  "updated_at":"..."
}
```

Endpoints:

* `GET /v1/missions` (query `limit,cursor,search,status,start,end,location,tag`)
* `POST /v1/missions` (creer mission, retourne mission 201)
* `GET /v1/missions/{id}` (detail + `assignments[]`)
* `PATCH /v1/missions/{id}` (update partiel)
* `DELETE /v1/missions/{id}` -> 204

### 3.1 Fichiers mission

`POST /v1/missions/{id}/files/presign`

```
{ "filename":"plan_lumiere.pdf", "content_type":"application/pdf" }
```

Response:

```
{ "upload_url":"https://s3...", "fields": {"key":"..."}, "file_url":"https://cdn..." }
```

### 3.2 Assignations

`Assignment`:

```
{
  "id":"uuid",
  "mission_id":"uuid",
  "user_id":"uuid",
  "role":"LIGHT_TECH|SOUND_TECH|STAGE_MANAGER|HMC|PIANIST|DANCER",
  "status":"invited|accepted|declined|confirmed",
  "check_in": "2025-11-24T09:58:00Z|null",
  "check_out":"2025-11-24T22:31:00Z|null"
}
```

Endpoints:

* `GET /v1/missions/{id}/assignments`
* `POST /v1/missions/{id}/assignments`
* `PATCH /v1/assignments/{id}`
* `DELETE /v1/assignments/{id}`

## 4. Planning (events)

`PlanningEvent`:

```
{
  "id":"uuid",
  "mission_id":"uuid|null",
  "resource_type":"USER|ROOM|GEAR",
  "resource_id":"uuid",
  "title":"Montage lumiere",
  "start":"...",
  "end":"...",
  "color":"#RRGGBB|null",
  "notes":"...",
  "status":"planned|busy|tentative"
}
```

Endpoints:

* `GET /v1/planning/events?start=..&end=..&resource_type=USER&resource_id=uuid`
* `POST /v1/planning/events` (support `Idempotency-Key`)
* `PATCH /v1/planning/events/{id}`
* `DELETE /v1/planning/events/{id}`

Exports:

* `GET /v1/planning/export.ics?start=..&end=..&scope=USER:uuid|ALL`
* `GET /v1/planning/export.csv?start=..&end=..`
* `GET /v1/planning/export.pdf?start=..&end=..`

Conflits: `POST /v1/planning/check-conflicts` -> `{ "conflicts": [ {"event_id":"uuid","type":"overlap","with":["uuid1","uuid2"]} ] }`

## 5. Notifications

Preferences:

* `GET /v1/notifications/prefs`
* `PATCH /v1/notifications/prefs` -> `{ "email": true, "telegram": true, "in_app": true, "quiet_hours": {"start":"22:00","end":"08:00"}}
`

Flux:

* `GET /v1/notifications?limit&cursor`
* `PATCH /v1/notifications/{id}` -> `{ "read": true }`

Webhook sortie (optionnel): `POST https://client.example/hooks/coulisses` (events mission.created, assignment.accepted, planning.updated).

## 6. Inventaire / Materiel

`InventoryItem`:

```
{
  "id":"uuid",
  "name":"Mac Aura",
  "sku":"CLAY-PAK-001",
  "qty_total": 24,
  "qty_available": 18,
  "location":"Depot A",
  "status":"ok|maintenance|missing",
  "tags":["lumiere"],
  "serials":["SN001","SN002"],
  "updated_at":"..."
}
```

Endpoints:

* `GET /v1/inventory/items?search&tag&status`
* `POST /v1/inventory/items`
* `GET /v1/inventory/items/{id}`
* `PATCH /v1/inventory/items/{id}`
* `DELETE /v1/inventory/items/{id}`

Liens mission:

* `GET /v1/missions/{id}/inventory`
* `POST /v1/missions/{id}/inventory` -> `{ "item_id":"uuid","qty":4 }`
* `DELETE /v1/missions/{id}/inventory/{item_id}`

## 7. Notes

`Note`:

```
{
  "id":"uuid",
  "scope":"mission|user|global",
  "scope_id":"uuid|null",
  "text":"Rappel gelatines R123 et L008",
  "mentions":["user:uuid","mission:uuid"],
  "author_id":"uuid",
  "created_at":"..."
}
```

Endpoints: `GET /v1/notes?scope=mission&scope_id=uuid`, `POST /v1/notes`, `DELETE /v1/notes/{id}`.

## 8. Paie / Temps de travail

`Timesheet`:

```
{
  "id":"uuid",
  "user_id":"uuid",
  "mission_id":"uuid",
  "date":"2025-11-24",
  "hours": 8.5,
  "rate_eur": 25.0,
  "break_minutes": 30,
  "overtime_hours": 1.0,
  "notes":"Remontage perches",
  "approved": false,
  "created_at":"...",
  "updated_at":"..."
}
```

Endpoints:

* `GET /v1/payroll/timesheets?user_id&mission_id&date_start&date_end`
* `POST /v1/payroll/timesheets` (idempotent mission_id+user_id+date)
* `PATCH /v1/payroll/timesheets/{id}`
* `POST /v1/payroll/timesheets/{id}/approve`

Exports:

* `GET /v1/payroll/export.csv?date_start=..&date_end=..&user_id=..`
* `GET /v1/payroll/export.pdf?date_start=..&date_end=..`

Resume: `GET /v1/payroll/summary?date_start=..&date_end=..&group_by=user|mission` -> `{ "currency":"EUR", "items": [ {"key":"user:uuid","hours":124.5,"gross":3120.00,"missions":8} ] }`

## 9. Recherche et tags

* `GET /v1/search?q=texte&types=mission,user,item` -> `{ "missions":[], "users":[], "items":[] }`
* `GET /v1/tags?scope=mission|inventory|note`
* `POST /v1/tags` -> `{ "scope":"mission","value":"video" }`
* `DELETE /v1/tags/{id}`

## 10. System / Sante

* `GET /v1/health` -> `{ "ok": true, "version":"1.0.0", "time":"..." }`
* `GET /v1/features` -> `{ "pwa":true, "webhooks":true, "multi_tenancy":false }
`

## 11. Schemas hints

### User (read)

```
{
  "id":"uuid",
  "email":"string",
  "first_name":"string",
  "last_name":"string",
  "roles":["ADMIN|MANAGER|TECH|ACCOUNTANT"],
  "status":"active|invited|disabled",
  "avatar_url":"string|null",
  "created_at":"datetime",
  "updated_at":"datetime"
}
```

### Mission (create)

```
{
  "title":"string(1..140)",
  "project_id":"uuid|null",
  "location":"string(1..140)",
  "start":"datetime",
  "end":"datetime",
  "status":"draft|confirmed|cancelled",
  "budget_eur":"number>=0|null",
  "notes":"string<=2000|null",
  "tags":["string"]
}
```

### PlanningEvent (create)

```
{
  "mission_id":"uuid|null",
  "resource_type":"USER|ROOM|GEAR",
  "resource_id":"uuid",
  "title":"string(1..140)",
  "start":"datetime",
  "end":"datetime",
  "color":"#RRGGBB|null",
  "notes":"string|null",
  "status":"planned|busy|tentative"
}
```

### InventoryItem (create)

```
{
  "name":"string",
  "sku":"string|null",
  "qty_total":"int>=0",
  "location":"string|null",
  "status":"ok|maintenance|missing",
  "tags":["string"],
  "serials":["string"]
}
```

### Timesheet (create)

```
{
  "user_id":"uuid",
  "mission_id":"uuid",
  "date":"YYYY-MM-DD",
  "hours":"number>=0",
  "rate_eur":"number>=0",
  "break_minutes":"int>=0",
  "overtime_hours":"number>=0",
  "notes":"string|null"
}
```

## 12. Enchainements front

1. Login -> dashboard: POST /auth/login, GET /planning/events, GET /missions?limit=20&status=confirmed, GET /notifications?limit=20.
2. Drag and drop planning: PATCH /planning/events/{id}, POST /planning/check-conflicts.
3. Assignation rapide: POST /missions/{id}/assignments, PATCH /notifications/{id}.

## 13. OpenAPI extrait

```
openapi: 3.0.3
info:
  title: Coulisses Crew API
  version: 1.0.0
servers:
  - url: https://api.coulisses-crew.example/v1
paths:
  /auth/login:
    post:
      summary: Login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email: { type: string, format: email }
                password: { type: string, minLength: 6 }
              required: [email, password]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token: { type: string }
                  refresh_token: { type: string }
                  user:
                    $ref: '#/components/schemas/User'
components:
  schemas:
    UUID:
      type: string
      format: uuid
    User:
      type: object
      properties:
        id: { $ref: '#/components/schemas/UUID' }
        email: { type: string, format: email }
        first_name: { type: string }
        last_name: { type: string }
        roles:
          type: array
          items: { type: string, enum: [ADMIN, MANAGER, TECH, ACCOUNTANT] }
        status: { type: string, enum: [active, invited, disabled] }
```

## 14. Checklist integration front

* Schemas Zod alignes, `safeParse` + mapping erreurs
* Intercepteurs 401 -> refresh -> retry (1 fois) sinon logout
* Headers communs: `Authorization`, `X-Client: web`, `X-Request-ID`
* Clefs React Query: `['missions', params]`, `['planning','range',start,end]`
* Upload: presign -> PUT S3 -> PATCH ressource avec `file_url`

## 15. Annexes

* RBAC front: ADMIN all, MANAGER manage_missions/view_planning/edit_planning/manage_inventory, TECH view_planning/self_timesheets, ACCOUNTANT view_payroll/manage_payroll.
* Statuts: Mission `draft|confirmed|cancelled`, Assignment `invited|accepted|declined|confirmed`, Inventory `ok|maintenance|missing`, PlanningEvent `planned|busy|tentative`.
