import { Link, Outlet } from 'react-router-dom';
import { describeThemeModes } from '../design-system/index.js';
import { appNavigation, createNavigationRoleBadges } from '../navigation.js';

export function AppLayout({ theme, navigation = appNavigation }) {
  const designSystem = {
    themeModes: describeThemeModes(),
    navigationBadges: createNavigationRoleBadges({ navigation, theme })
  };
  return {
    type: 'app-layout',
    theme,
    navigation,
    designSystem,
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
