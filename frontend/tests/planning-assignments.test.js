import fs from 'node:fs';
import { describe, expect, test } from 'vitest';

const assignmentsSource = fs.readFileSync('./src/features/planning/assignments.ts', 'utf8');

describe('planning assignments source', () => {
  test('sanitizes payload and exposes helper', () => {
    expect(assignmentsSource).toContain('export function sanitizeAssignmentFeed');
    expect(assignmentsSource).toContain("id: String(value.id ?? '')");
    expect(assignmentsSource).toContain("status: String(value.status ?? 'pending')");
  });

  test('accessibility hints include totals', () => {
    expect(assignmentsSource).toContain("`Total ${feed.summary.total}`");
    expect(assignmentsSource).toContain("`Confirmes ${confirmed}`");
    expect(assignmentsSource).toContain("`En attente ${pending}`");
  });
});
