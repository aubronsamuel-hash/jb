export function Button(props) {
  return {
    type: 'ui-button',
    label: props.label,
    variant: props.variant ?? 'primary',
    size: props.size ?? 'md',
    icon: props.icon,
    ariaLabel: props.ariaLabel ?? props.label,
    focusRing: '0 0 0 3px rgba(37, 99, 235, 0.45)'
  };
}
