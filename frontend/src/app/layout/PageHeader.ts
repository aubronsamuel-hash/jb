export function PageHeader(props) {
  const { theme, navigation, currentPath, locale } = props;
  const items = navigation.map((item) => ({
    ...item,
    isActive: item.path === currentPath,
    ariaLabel: `${item.label} - ${item.description}`
  }));
  const actions = [
    {
      id: 'toggle-theme',
      label: theme.mode === 'light' ? 'Activer mode sombre' : 'Activer mode clair',
      target: 'theme-toggle',
      ariaLabel: 'Basculer le theme clair ou sombre'
    },
    {
      id: 'open-notifications',
      label: 'Notifications',
      target: 'notifications-panel',
      ariaLabel: 'Voir les notifications recents'
    }
  ];
  return {
    type: 'page-header',
    title: 'Coulisses Crew',
    subtitle: 'Socle frontend orchestrant planning, missions et equipes.',
    navigation: items,
    actions,
    themeMode: theme.mode,
    locale
  };
}
