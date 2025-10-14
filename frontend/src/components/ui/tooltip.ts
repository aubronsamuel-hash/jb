export function Tooltip(props) {
  return {
    type: 'ui-tooltip',
    id: props.id,
    triggerLabel: props.triggerLabel,
    content: props.content,
    placement: props.placement ?? 'top',
    role: 'tooltip'
  };
}
