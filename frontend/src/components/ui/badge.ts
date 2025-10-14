export function Badge(props) {
  return {
    type: 'ui-badge',
    label: props.label,
    tone: props.tone ?? 'neutral',
    icon: props.icon
  };
}
