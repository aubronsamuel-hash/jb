export function Avatar(props) {
  const initials = props.initials ?? props.name.split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase();
  return {
    type: 'ui-avatar',
    name: props.name,
    initials,
    status: props.status ?? 'offline',
    ariaLabel: `${props.name} (${props.status ?? 'offline'})`
  };
}
