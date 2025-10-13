import snapshot from '../../../public/data/dashboard-snapshot.json' assert { type: 'json' };

export function loadDashboardSnapshot() {
  return JSON.parse(JSON.stringify(snapshot));
}
