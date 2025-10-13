import { Link, Outlet } from 'react-router-dom';
import { appNavigation } from '../navigation.js';

export function AppLayout({ theme, navigation = appNavigation }) {
  return {
    type: 'app-layout',
    theme,
    navigation,
    children: [
      {
        type: 'app-header',
        title: 'Orga',
        subtitle: 'Planning spectacles & equipes techniques'
      },
      {
        type: 'app-navigation',
        items: navigation.map((item) => ({
          id: item.id,
          label: item.label,
          link: Link({ to: item.path, children: item.label, variant: 'nav' })
        }))
      },
      {
        type: 'app-content',
        outlet: Outlet()
      }
    ]
  };
}
