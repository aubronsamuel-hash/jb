# APPLI Frontend Specification (v0.2 - Complete)

Status: DRAFT (to freeze after step-10)
Owner: Sam (Product/TD) + APPLI Frontend Lead
Repo: frontend/
Stack: React 18+, Vite, TypeScript 5, React Router 6.28+, React Query (TanStack Query) 5, TailwindCSS, shadcn/ui, Radix UI, Zustand or Redux Toolkit (thin), Recharts, date-fns, zod + react-hook-form, Playwright, Vitest, Storybook 8, MSW
Encoding: ASCII only (no accents in code). Windows-first scripts.

Changelog:
- Step-07: Consolidated Sam's v0.2 specification for distribution to squads.

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

Appendix A. Key component APIs (excerpt)
Appendix B. Error presentation mapping
Appendix C. Keyboard shortcuts
Appendix D. Bundle budgets (initial targets)
Appendix E. Sample env (.env.local)

---

## 1. Scope & principles

Frontend is a SPA for planning live events operations. It delivers the operator UI consumed by production, staffing, finance, and partner support.

In scope v0.2:
- Authentication flows, MFA enrollment, role-aware layout (RBAC) with support for multiple organizations.
- CRUD experiences for projects, venues, missions, shifts, and assignments across responsive breakpoints.
- Planning interfaces: calendar (day/week/month), timeline (Gantt-like), kanban by assignment status, and dashboards for staffing KPIs.
- People, skills, availability, timesheets, inventory, notes, and file management surfaces.
- Export triggers (ICS/CSV/PDF), job status monitors, and webhook visibility for administrators.

Non-goals v0.2 (defer to v0.3+):
- Real-time sockets for presence or chat.
- Offline-first mutations (read caching allowed).
- Advanced payroll and invoicing workflows.

Guiding principles:
- UX first: responsive, keyboard-friendly, accessible, with undo affordances.
- Deterministic: typed APIs, consistent component contracts, ASCII identifiers, minimal global state.
- Data driven: cache-first queries, optimistic updates when low risk, instrumentation for decision-making.

---

## 2. Architecture & code layout

App shell diagram:
```
[Vite] -> [AppShell]
          |-- Header (global search, quick add)
          |-- Sidebar (org/project navigation)
          |-- Main Outlet (router)
          |-- Command Palette, Toaster, Modals
```

Folder structure:
```
frontend/
  src/
    app/
      App.tsx            # router, providers
      routes.tsx         # route tree
      queryClient.ts     # react-query setup
      i18n/              # translations resources
      providers/         # AuthProvider, RBACGuard, ThemeProvider
      theme.css          # tailwind base + tokens
      icons/             # lucide-react wrappers
    core/
      api/               # openapi client, fetch utils, interceptors
      auth/              # session store, guards, hooks
      rbac/              # ability utilities, feature flag helpers
      components/        # design system atoms/molecules
      forms/             # rfh + zod wrappers
      hooks/             # shared hooks
      utils/             # date, format, csv
      dnd/               # drag and drop primitives
    features/
      dashboard/
      projects/
      venues/
      planning/          # missions, shifts, assignments, calendar
      people/            # directory, profiles, skills
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
- TypeScript strict mode enabled. Path aliases via tsconfig + vite config.
- Named exports for components and hooks; default exports allowed only for top-level route modules.
- Feature folders own their routes, loaders, data hooks, and tests.
- CSS handled via Tailwind + CSS modules when necessary; avoid SCSS.
- Keep Windows compatibility for scripts (PowerShell 7+).

---

## 3. Design system & styling

- TailwindCSS utility-first with tokens defined using CSS variables exposed in `:root` and mirrored in `theme.css`.
- shadcn/ui components with Radix primitives; extend tokens for APPLI brand colors and states (info/success/warning/danger).
- Iconography via lucide-react wrappers stored in `app/icons` to centralize tree-shaking.
- Typography: Inter (system fallback). Heading scale h1-h4 with responsive sizes.
- Spacing scale 4px multiples, radius scale 4/8/16.
- Components: Button, Input, Select, Combobox, Badge, Avatar, Tooltip, Dialog, Drawer, Popover, Tabs, Breadcrumbs, DataTable, DatePicker, TimeRangePicker, Pagination, Tag, EmptyState, Skeleton, StatCard.
- DataTable: TanStack Table with column configs, sorting, filtering, pinning, column visibility, row selection, CSV export hook.
- Loading states defined for skeleton, spinner, and inline placeholders; consistent 200ms minimum display to avoid flicker.
- Dark theme deferred to v0.3 but design tokens must support inversion.

---

## 4. Accessibility & i18n/l10n

- Target WCAG 2.1 AA; include keyboard navigation, skip links, visible focus states, and proper semantic landmarks.
- Use Radix primitives where possible for accessible behaviors; additional aria attributes documented per component.
- Support screen reader announcements for async operations (e.g., toast with `role="status"`).
- I18n: locales `fr` (default) and `en`. All copy stored in JSON resources with translation keys; never hardcode strings in JSX.
- Date/time formatting through date-fns with locale aware tokens. Numbers formatted using Intl APIs.
- Provide timezone indicator in planner views; convert backend UTC to user locale with tooltip showing UTC offset.

---

## 5. State management & data layer

- Server cache: React Query 5 with centralized `queryClient`. Configure `staleTime` and `gcTime` per resource class (projects, missions, assignments, notifications).
- Client state: Zustand store for ephemeral UI state (panes open, filters, DnD ghost state). If heavier coordination required, allow slice-based Redux Toolkit store but keep thin.
- Query keys follow `["resource", params]` pattern. Derived selectors avoid duplication by using memoized helpers.
- Mutations implement optimistic updates for status toggles, assignment reorder, and entity rename. Provide rollback on error and toast messaging.
- Infinite queries for audit logs, notifications, and people directories. Keep page size 25 by default with ability to override.
- Use MSW to mock API during Storybook and tests, mirroring backend RFC7807 errors.

---

## 6. API client & error model

- Generate typed client via `openapi-typescript` from backend `/openapi.json` as part of build script.
- Base fetch wrapper handles auth headers, org scope header, tracing headers, and idempotency keys (POST where necessary).
- Standardize errors to RFC7807-like shape `{type,title,status,detail,code,errors}`. Provide mapping utilities for forms and banners.
- Retry policy: GET requests network retry 3x with jitter; other verbs no automatic retry.
- Token refresh flow triggered on 401; if refresh fails redirect to `/login` with preserved intended route.
- 403 surfaces RBAC message; 404 surfaces inline empty state; 409/422 map to form-level or field-level errors.
- Telemetry for failed requests includes request id, route, and status.

---

## 7. Routing & app shell

Route tree:
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

- App shell hosts header (search, quick-add, user menu), sidebar (org/project navigation, planner shortcuts), toaster, command palette, and modal host.
- Guards: `AuthGuard` handles session redirect; `RBACGuard` hides unauthorized actions; feature flags based on org + role.
- Breadcrumbs derived from route metadata; quick actions (create project, add mission) available in header.
- Deep links encode project/mission context for shareable URLs; maintain query params for filters.

---

## 8. Feature modules (screens, components, flows)

### 8.1 Auth
- Login form (email/password) with remember me; password reset and MFA enrollment dialogs.
- Session viewer listing active devices (IP, user-agent) with revoke controls.
- Support SSO stub (v0.3) but design flows to extend easily.

### 8.2 Dashboard
- Cards: upcoming shifts (next 7 days), staffing gaps, project KPIs (hours, cost), recent activity timeline, quick links.
- Provide filter chips for organization, project, timeframe; persist selections per user.

### 8.3 Projects/Venues/Spaces
- Projects list with global search, filters (status, venue, owner), sorting, pagination, saved views.
- Project detail tabs: overview (dates, venues map, budget summary), missions table, people roster, files, activity log.
- Venues module manages venue and space definitions with map preview (static) and capacity metadata.

### 8.4 Planning
- Missions: list/create/edit, status chips, budget summary, assign primary owner.
- Shifts: table with inline edit, bulk create by pattern, duplicate across days, conflict detection.
- Assignments: list with avatars; drag people onto shifts; status change via dropdown; conflict badges.
- Views: Calendar Day/Week/Month for shifts/personal assignments with drag/move; Timeline (mission bars) with zoom + scroll sync; Kanban by assignment status.

### 8.5 People & Skills
- Directory with search, skill filters, availability overlay, and tag chips.
- Profile drawer: contact info, skills matrix, documents list, notes, availability calendar.

### 8.6 Availability & Leaves
- Heatmap calendar by person; supports bulk edit and import from CSV; legend explaining colors.

### 8.7 Timesheets & Rates
- Timesheet table with inline start/end editing, automatic hour calculation, CSV export, summary footer totals by project and person.
- Rate cards stored per role; enforce validation vs backend constraints.

### 8.8 Inventory & Checklists
- Inventory grid/list with tag filters, assignment to missions, low-stock alerts.
- Mission checklist with progress bar, reorderable tasks, support attachments per task.

### 8.9 Notes
- Threaded comments per entity; mentions using `@` with autocomplete; attachments preview; edit/delete with audit trail.

### 8.10 Files
- Upload via S3 presigned URLs; progress bar with cancel; virus scan status badge; preview images/PDF; copy signed link.

### 8.11 Notifications
- In-app center: list deliveries, filters by channel/state, mark as read, test send dialog for admins.

### 8.12 Settings
- Org: members roles, invites, tokens (PAT) management, region selection.
- Profile: locale, avatar upload, notification preferences, telegram chat id.

### 8.13 Admin
- Webhooks endpoints CRUD, delivery log with retry/resend, signature copy helper, event catalog reference.

---

## 9. Forms, validation, wizard patterns

- `react-hook-form` + `zod` schemas; central `FormField` component to handle labels, hints, errors.
- Inline validation on blur; submit-level error summary for RFC7807 `errors` payload.
- Wizards: create project -> venue/space -> initial missions -> shift template; allow exit/resume using URL state.
- Provide undo snackbar for destructive actions (delete mission, remove assignment).
- Autosave drafts for multi-step forms (projects, missions) using local storage keyed by org.

---

## 10. Calendar, timeline, drag-and-drop

- Calendar built with headless primitives; virtualization for long hour grids; timezone aware.
- DnD library: dnd-kit with keyboard drag support, collision detection for overlap, revert animation on failure.
- Timeline view uses horizontal virtualization, sticky headers, zoom controls (day/week) with trackpad support.
- Provide printing/export of timeline to PDF (basic) by step-10.
- Planner supports split view: calendar + sidebar for filtering resources.

---

## 11. Notifications & toasts

- Global toaster (shadcn) with semantic variants (success, error, info, warning) and action buttons when necessary.
- Background job polling (exports) -> toast when done with link to file; on failure show error details.
- Inline banners for blocking errors (e.g., data fetch failure) with retry button.

---

## 12. Files upload & previews

- FileDialog supports drag-drop, mime filters, size guard, virus scan status, and rename before upload.
- Image preview handles EXIF orientation; PDF preview via iframe; fallback icon for unknown types.
- Track upload progress in global queue; allow cancel/resume with backend support.

---

## 13. Performance & offline

- Code splitting per route chunk; use Suspense boundaries for lazy modules.
- Prefetch data on hover for likely routes (React Router loaders + React Query prefetch).
- React Query cache hydration on SSR/preview builds; background refetch on window focus with exponential backoff.
- Virtualized lists using TanStack Virtual for tables > 200 rows.
- PWA optional (v0.3) but service worker scaffolding prepared; offline notice component available.
- Bundle budgets tracked via CI; analyze bundle splits with Source Map Explorer.

---

## 14. Security & privacy

- Authentication tokens stored in httpOnly cookies (preferred) or memory with refresh; never localStorage.
- CSRF protection required when cookies used; embed anti-forgery token in forms.
- Escape HTML in notes/comments; sanitize uploads metadata; enforce Content Security Policy documented.
- Mask sensitive identifiers in logs/telemetry. Provide profile-level opt-out for analytics.
- Follow GDPR export/delete requests by delegating to backend endpoints but expose UI triggers.

---

## 15. Testing strategy

- Unit: components and hooks via Vitest + React Testing Library; ensure coverage thresholds (80 lines, 75 branches).
- Integration: page flows with MSW for API, covering planner flows, assignments, and settings.
- E2E: Playwright smoke covering login, project creation, scheduling shifts, assignment confirmation, export CSV, webhook check.
- Accessibility checks: Storybook test runner with axe-core; Playwright a11y assertions for key flows.
- Regression: Visual tests via Chromatic or Storybook test runner on DS components and planner views.

---

## 16. Storybook & visual regression

- Storybook documents all design system components and critical feature widgets (Calendar, Timeline, DataTable, Forms, Notifications, FileUpload).
- Stories co-located with components; use CSF3 format; controls for props to support product review.
- Visual regression via Chromatic (preferred) or Storybook test runner in CI; baseline updated after product sign-off.
- Provide docs tab with usage guidelines, accessibility notes, and tokens references.

---

## 17. CI/CD & quality gates

- GitHub Actions pipeline: lint (eslint, prettier check), typecheck, unit + integration tests, Storybook build, Playwright smoke, bundle size check, Lighthouse CI (basic), artifact uploads.
- Required checks: `lint`, `typecheck`, `test`, `storybook`, `playwright`, `lighthouse`, `bundle-budget`.
- Roadmap guard ensures commit messages reference step (Ref: docs/roadmap/step-XX.md). Docs guard ensures specs touched by doc changes.
- Preview deploys (Vercel/Netlify) for PRs with sanitized env vars; include Storybook static deploy for design review.
- Release tagging after QA sign-off; maintain changelog in docs/frontend.

---

## 18. Telemetry & logging

- Sentry (or OpenTelemetry web) for error tracking; upload source maps via CI.
- Custom logger capturing level, message, route, user_id hash, org_id hash; store in buffer and flush on page unload.
- Track page views, key interactions (assignment drag, export triggered), and performance metrics (LCP, CLS, TTFB) to analytics warehouse.
- Provide opt-out toggle in profile settings; respect DNT header by disabling analytics.

---

## 19. Config & env

- `.env` variables consumed by Vite: `VITE_API_URL`, `VITE_SENTRY_DSN`, `VITE_BUILD_SHA`, `VITE_BUILD_TIME`, `VITE_FEATURE_FLAGS`, `VITE_LAUNCH_DARKLY_CLIENT_ID` (future).
- Build-time injection of git SHA/version displayed in `/about` modal and console.
- Distinguish environments: local, staging, production; provide script to sync `.env.example` with typed config guard.
- Feature flags loaded at bootstrap to allow gating of planner enhancements.

---

## 20. Roadmap steps (01..20)

- step-01: scaffold Vite React TS, tailwind, shadcn, eslint/prettier, routes, auth shell
- step-02: API client generation from OpenAPI, interceptors, error adapter, auth flows
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

- App Shell: persistent layout containing header/sidebar and router outlet.
- DnD: drag and drop interactions.
- DS: design system components shared across features.
- RFC7807: standard error response format used by backend and frontend adapters.
- PAT: personal access token used for API automation.

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
- 409: toast with conflict message; highlight conflicting items.
- 422: field messages mapped to form errors; focus first invalid field.
- 500: generic error page with retry and support link.

---

## Appendix C. Keyboard shortcuts

- global: cmd/ctrl+k opens command palette.
- g p: go to projects, g d: dashboard, g c: calendar.
- n: new on current page (project/mission/shift).
- shift+/ : show shortcuts modal.

---

## Appendix D. Bundle budgets (initial targets)

- main chunk <= 180kb gzipped.
- route chunks <= 120kb gzipped.
- vendor split: react, router, query, recharts separate.
- avoid regressions >5% without approval; track in CI.

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
