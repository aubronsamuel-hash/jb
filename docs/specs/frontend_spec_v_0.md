# APPLI Frontend Specification (v0.2 - Complete)

Status: DRAFT (to freeze after step-10)
Owner: Sam (Product/TD) + APPLI Frontend Lead
Repo: frontend/
Stack: React 18+, Vite, TypeScript 5, React Router 6.28+, React Query (TanStack Query) 5, TailwindCSS, shadcn/ui, Radix UI, Zustand or Redux Toolkit (thin), Recharts, date-fns, zod + react-hook-form, Playwright, Vitest, Storybook 8, MSW
Encoding: ASCII only (no accents in code). Windows-first scripts.

---

## 0. Table of contents

1. Scope & principles
2. Architecture & code layout
3. Design system & styling
4. Accessibility & i18n/l10n
5. State management & data layer
6. API client & error model
7. Routing & app shell
8. Feature modules (screens, components, flows)
9. Forms, validation, wizard patterns
10. Calendar, timeline, drag-and-drop
11. Notifications & toasts
12. Files upload & previews
13. Performance & offline
14. Security & privacy
15. Testing strategy
16. Storybook & visual regression
17. CI/CD & quality gates
18. Telemetry & logging
19. Config & env
20. Roadmap steps (01..20)
21. Glossary

---

## 1. Scope & principles

Frontend is a SPA for planning live events operations. It provides:
- Auth flows, session management, role-aware UI (RBAC).
- CRUD screens for projects, venues, missions, shifts, assignments.
- Planning UIs: calendar (day/week/month), timeline (Gantt-like), Kanban by status.
- People/skills, availability, timesheets, inventory, notes, files.
- Exports triggers (ICS/CSV/PDF) and job status.
- Notifications center (in-app), webhook status views (admin).

Principles:
- UX first: fast, keyboard-friendly, accessible, forgiving forms.
- Data driven: typed API client, cache-first queries, optimistic updates when safe.
- Deterministic: ASCII identifiers, consistent component API, no hidden magic.

---

## 2. Architecture & code layout

App shell diagram:
```
[Vite] -> [AppShell]
          |-- Header (global search, quick add)
          |-- Sidebar (org/project nav)
          |-- Main Outlet (router)
          |-- Toaster/Dialogs/Drawers/CommandK
```

Folder structure:
```
frontend/
  src/
    app/
      App.tsx            # router, providers
      routes.tsx         # route tree
      queryClient.ts     # react-query setup
      i18n/              # i18n resources
      theme.css          # tailwind base + tokens
      icons/             # lucide-react wrappers
      providers/         # AuthProvider, RBACGuard, ThemeProvider
    core/
      api/               # openapi client, fetch utils, interceptors
      auth/              # session store, guards, hooks
      rbac/              # ability utilities
      components/        # design system atoms/molecules
      hooks/             # shared hooks
      utils/             # date, format, csv
      dnd/               # drag and drop utilities
      forms/             # rfh + zod wrappers
    features/
      dashboard/
      projects/
      venues/
      planning/          # missions, shifts, assignments, calendar
      people/            # skills, availability, leaves
      timesheets/
      inventory/
      notes/
      files/
      notifications/
      settings/
      admin/
    styles/
    mocks/               # msw handlers
    test/
  public/
  scripts/               # ps1 utilities
```

Conventions:
- TypeScript strict; path aliases via tsconfig.
- Named exports for components; lowercase file names with dashes.
- No default exports except React pages and route modules.

---

## 3. Design system & styling

- TailwindCSS utility-first; design tokens defined via CSS variables.
- shadcn/ui components with Radix primitives; extend for domain.
- Color system: light theme default; dark theme optional v0.3.
- Sizing/spacing scale 4px multiples.
- Typography: Inter (system fallback); weight 400/600.
- Components: Button, Input, Select, Combobox, Badge, Avatar, Tooltip, Dialog, Drawer, Popover, Tabs, Breadcrumbs, DataTable, DatePicker, TimeRangePicker, Pagination.
- DataTable: TanStack Table with column defs, sorting, filtering, column visibility, row selection, CSV export.

---

## 4. Accessibility & i18n/l10n

- WCAG 2.1 AA targets; keyboard traps avoided; focus rings visible.
- ARIA labels for interactive components; semantic landmarks.
- I18n: en, fr (default fr). date-fns locale for formatting.
- Number/time zone: show times in local TZ; explicit UTC note in tooltips.

---

## 5. State management & data layer

- Server cache: React Query 5 with per-query keys; staleTime per resource.
- Client state: Zustand (or Redux Toolkit if needed) for UI-only state (panels open, filters, DnD temp state).
- Query keys: ["projects", params], ["missions", {projectId}], etc.
- Optimistic updates on fast toggles (assignment status), rollback on error.
- Infinite queries for long lists (activities, audit logs).

---

## 6. API client & error model

- openapi-typescript generated types from backend /openapi.json.
- API client: fetch with interceptors (auth, org scope, idempotency key for POST when needed).
- Unified error adapter to RFC7807 shape {type,title,status,detail,code,errors}.
- Retry policy: network 3x with jitter for idempotent GET only.
- 401 -> refresh token flow; 403 -> RBAC notice; 409/422 -> field messages.

---

## 7. Routing & app shell

Routes:
```
/
  /login
  /logout
  /switch-org
  /dashboard
  /projects
    /:projectId
      /overview
      /missions
      /calendar
      /timeline
      /people
      /timesheets
      /files
  /venues
  /planning
    /missions
    /shifts
    /assignments
  /people
  /timesheets
  /inventory
  /notifications
  /settings
    /org
    /profile
    /tokens
  /admin
    /webhooks
    /audit
```

Guards:
- AuthGuard redirects to /login.
- RBACGuard hides actions; feature flags by role.

Breadcrumbs and quick actions in page headers.

---

## 8. Feature modules

### 8.1 Auth
- Login form (email/password); remember me; password reset dialogs.
- Session viewer (devices with IP/UA); revoke.

### 8.2 Dashboard
- Cards: upcoming shifts (next 7 days), staffing gaps, project KPIs (hours, cost), recent activity, quick links.

### 8.3 Projects/Venues/Spaces
- Projects list with search, filters (status, venue), sorting, pagination.
- Project detail with tabs: overview (dates, venue map), missions table, people, files.

### 8.4 Planning
- Missions: list/create/edit; status chips; budget summary.
- Shifts: table + inline edit; bulk create by pattern; duplicate to days.
- Assignments: list with avatars; status changes via dropdown; conflict badges.

Views:
- Calendar: Day/Week/Month for shifts and personal assignments. Drag to move/resize (v0.3 resize), tooltips.
- Timeline: horizontal bars per mission; zoom (day/week); scroll sync; sticky headers.
- Kanban: by assignment status (proposed/confirmed/declined).

DnD:
- Drag person onto a shift to create assignment; collision checks with optimistic UI.

### 8.5 People & Skills
- Directory with search, skill filters, availability overlay.
- Profile panel drawer: contacts, skills tags, documents list.

### 8.6 Availability & Leaves
- Heatmap calendar; bulk edit; legends.

### 8.7 Timesheets & Rates
- Table inline edit start/end; compute hours live; CSV export; summary footer.

### 8.8 Inventory & Checklists
- Items grid/list with tags; assign sets to missions.
- Checklist per mission with progress bar.

### 8.9 Notes
- Threaded comments per entity; mentions @; attachments.

### 8.10 Files
- Upload via S3 presign; progress bar; virus status badge; preview (images/PDF); share signed link (copy).

### 8.11 Notifications
- In-app center: list deliveries, status, filters; test send dialog.

### 8.12 Settings
- Org: members roles; invite; tokens (PAT) management.
- Profile: locale, avatar, telegram chat id.

### 8.13 Admin
- Webhooks endpoints CRUD; deliveries log; signature copy helper.

---

## 9. Forms, validation, wizard patterns

- react-hook-form + zod schemas; reusable FormField component.
- Inline validation on blur; submit-level RFC7807 mapping.
- Wizards for: create project -> venue/space -> initial missions -> shifts template.
- Undo snackbar for destructive actions.

---

## 10. Calendar, timeline, drag-and-drop

- Calendar built with headless primitives; virtualization for large datasets.
- Timezone awareness; today marker; all-day vs timed slots.
- DnD library: dnd-kit; keyboard DnD enabled; collision detection custom for overlap.
- Ghost items during drag; revert animation on error.

---

## 11. Notifications & toasts

- Global Toaster (shadcn toast) with semantic variants: success, error, info.
- Background job polling (exports) -> toast when done with link to file.

---

## 12. Files upload & previews

- FileDialog supports drag-drop; accept filters by mime; max size guard.
- Image preview with EXIF orientation fix; PDF iframe preview.

---

## 13. Performance & offline

- Code-splitting by route; prefetch on hover for likely routes.
- React Query cache hydration; background refetch on window focus.
- PWA optional v0.3: service worker for caching static assets and last views.
- Virtualized lists (TanStack Virtual) for long tables.

---

## 14. Security & privacy

- Never store tokens in localStorage; use httpOnly cookies (preferred) or memory + refresh endpoint.
- CSRF protection if cookies used; same-site=strict.
- Escape HTML in notes; content security policy documented.
- Redact secrets in logs.

---

## 15. Testing strategy

- Unit: components and hooks via Vitest + RTL.
- Integration: page flows with MSW for API.
- E2E: Playwright (login, create project, plan shifts, assign user, export CSV).
- Accessibility: axe-core checks in Storybook.

Coverage thresholds: 80 lines, 75 branches (raise later).

---

## 16. Storybook & visual regression

- Storybook for all DS components and key feature widgets (Calendar, Timeline, DataTable, Forms).
- Controls and docs for props; stories co-located.
- Chromatic (or Storybook test-runner) for visual diffs.

---

## 17. CI/CD & quality gates

- GitHub Actions: lint (eslint, prettier check), typecheck, unit+integration, Storybook build, Playwright e2e (smoke), bundle size check, Lighthouse CI (basic), artifact uploads.
- Guards: docs_guard, roadmap_guard, commit_guard; require step ref.
- Preview deploys (Vercel/Netlify) on PR; env vars masked.

---

## 18. Telemetry & logging

- Sentry (or OpenTelemetry web) for errors; source maps uploaded.
- Client logs: level, message, route, user_id hash, org_id hash; opt-out in profile.

---

## 19. Config & env

- .env files: VITE_API_URL, VITE_SENTRY_DSN, VITE_BUILD_SHA, VITE_BUILD_TIME, VITE_FEATURE_FLAGS.
- Build-time injection of git sha, version; shown in /about modal.

---

## 20. Roadmap steps (01..20)

- step-01: scaffold Vite React TS, tailwind, shadcn, eslint/prettier, routes, auth shell
- step-02: API client gen from OpenAPI, interceptors, error adapter, auth flows
- step-03: RBAC guards, org switcher, session viewer
- step-04: Projects list/detail with CRUD forms + tests
- step-05: Venues/spaces CRUD + tables + tests
- step-06: Missions CRUD, search, filters; DataTable with presets
- step-07: Shifts table and bulk create; conflict badges
- step-08: Assignments board (kanban) + status updates, optimistic UI
- step-09: Calendar views (day/week/month) with shift rendering
- step-10: Timeline view (mission bars) with zoom and scroll sync
- step-11: People directory + profile drawer + skills tags
- step-12: Availability heatmap + bulk edit
- step-13: Timesheets table + CSV export + summary footer
- step-14: Files upload via presign + previews
- step-15: Notifications center + export job polling
- step-16: Settings (org, members, tokens) + profile
- step-17: Admin webhooks UI + deliveries log
- step-18: Storybook DS completeness + visual tests + a11y passes
- step-19: E2E Playwright smoke path; Lighthouse CI + bundle budget
- step-20: Hardening (perf, a11y, i18n pass), docs freeze

Each step ships: routes/components, tests, stories, CI green, docs updated, VALIDATE? yes/no by Sam.

---

## 21. Glossary

- App Shell: persistent layout containing header/sidebar.
- DnD: drag and drop interactions.
- DS: design system components shared across features.

---

## Appendix A. Key component APIs (excerpt)

CalendarProps:
```
{
  view: 'day'|'week'|'month',
  date: Date,
  onDateChange(d: Date): void,
  events: Array<{ id: number; start: Date; end: Date; title: string; color?: string; resource?: any }>,
  onEventClick?(id: number): void,
  onCreate?(slot: {start: Date; end: Date}): void,
  onMove?(id: number, range: {start: Date; end: Date}): Promise<void>,
}
```

DataTableProps<T>:
```
{
  columns: ColumnDef<T>[];
  data: T[];
  state?: TableState;
  onStateChange?: (s: TableState) => void;
  serverSide?: boolean;
}
```

FormDialogProps:
```
{
  title: string;
  schema: ZodSchema<any>;
  defaultValues?: any;
  onSubmit(values: any): Promise<void>;
}
```

---

## Appendix B. Error presentation mapping

- 401: show login dialog; keep intended route.
- 403: banner "Action not allowed"; hide destructive UI.
- 404: inline empty state with back link.
- 409: toast with conflict message, highlight conflicting items.
- 422: field messages mapped to form errors; focus first invalid.

---

## Appendix C. Keyboard shortcuts

- global: cmd/ctrl+k open command palette
- g p: go to projects, g d: dashboard, g c: calendar
- n: new on current page (project/mission/shift)

---

## Appendix D. Bundle budgets (initial targets)

- main chunk <= 180kb gz
- route chunks <= 120kb gz
- vendor split: react, router, query, recharts separate

---

## Appendix E. Sample env (.env.local)

```
VITE_API_URL=http://localhost:5173/api
VITE_SENTRY_DSN=
VITE_FEATURE_FLAGS=calendar,timeline,kanban
VITE_BUILD_SHA=local
VITE_BUILD_TIME=2025-10-13T00:00:00Z
```

---

END OF SPEC v0.2

