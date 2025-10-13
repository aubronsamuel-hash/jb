import { queryKeys } from '../query-client.js';
import { findNavigationItem } from '../navigation.js';

export function PlaceholderView({ id, title, description }) {
  const navItem = id ? findNavigationItem(id) : null;
  return {
    type: 'placeholder-view',
    id: id ?? 'unknown',
    title: title ?? navItem?.label ?? 'En construction',
    description: description ?? navItem?.description ?? 'Module a implementer',
    queryKey: queryKeys[id] ?? [id ?? 'unknown']
  };
}
