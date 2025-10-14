export type AssignmentFeed = {
  items: Array<{
    id: string;
    status: string;
    user: { id: string; name: string; role: string };
    mission: { id: string; title: string };
    startsAt: string;
    endsAt: string;
    updatedAt: string;
    location: string;
  }>;
  pageInfo: {
    limit: number;
    nextCursor: string | null;
    previousCursor: string | null;
  };
  summary: {
    total: number;
    byStatus: Record<string, number>;
  };
  generatedAt: string | null;
};

export function sanitizeAssignmentFeed(payload: unknown): AssignmentFeed {
  const fallback = {
    items: [],
    pageInfo: { limit: 0, nextCursor: null, previousCursor: null },
    summary: { total: 0, byStatus: {} },
    generatedAt: null
  } satisfies AssignmentFeed;

  if (!payload || typeof payload !== 'object') {
    return fallback;
  }

  const source = payload as Record<string, unknown>;
  const rawItems = Array.isArray(source.items) ? source.items : [];

  const items = rawItems
    .filter((entry) => entry && typeof entry === 'object')
    .map((entry) => {
      const value = entry as Record<string, unknown>;
      const mission = (value.mission as Record<string, unknown>) ?? {};
      const user = (value.user as Record<string, unknown>) ?? {};
      return {
        id: String(value.id ?? ''),
        status: String(value.status ?? 'pending'),
        user: {
          id: String(user.id ?? ''),
          name: String(user.name ?? ''),
          role: String(user.role ?? 'unknown')
        },
        mission: {
          id: String(mission.id ?? ''),
          title: String(mission.title ?? '')
        },
        startsAt: String(value.startsAt ?? ''),
        endsAt: String(value.endsAt ?? ''),
        updatedAt: String(value.updatedAt ?? ''),
        location: String(value.location ?? '')
      };
    });

  const pageInfoSource = (source.pageInfo as Record<string, unknown>) ?? {};
  const summarySource = (source.summary as Record<string, unknown>) ?? {};

  return {
    items,
    pageInfo: {
      limit: Number(pageInfoSource.limit ?? items.length),
      nextCursor: pageInfoSource.nextCursor ? String(pageInfoSource.nextCursor) : null,
      previousCursor: pageInfoSource.previousCursor ? String(pageInfoSource.previousCursor) : null
    },
    summary: {
      total: Number(summarySource.total ?? items.length),
      byStatus: (summarySource.byStatus as Record<string, number>) ?? {}
    },
    generatedAt: source.generatedAt ? String(source.generatedAt) : null
  } satisfies AssignmentFeed;
}

export function computeAssignmentAccessibilityHints(feed: AssignmentFeed): string {
  const pending = feed.summary.byStatus['pending'] ?? 0;
  const declined = feed.summary.byStatus['declined'] ?? 0;
  const confirmed = feed.summary.byStatus['confirmed'] ?? 0;
  return [
    `Total ${feed.summary.total}`,
    `Confirmes ${confirmed}`,
    `En attente ${pending}`,
    `Declines ${declined}`
  ].join(' | ');
}
