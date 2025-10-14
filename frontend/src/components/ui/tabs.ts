export function Tabs(props) {
  const items = props.items.map((item) => ({
    ...item,
    ariaControls: `${props.id}-${item.id}-panel`
  }));
  return {
    type: 'ui-tabs',
    id: props.id,
    items,
    activeId: props.activeId,
    role: 'tablist'
  };
}
