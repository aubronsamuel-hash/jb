export function Toast(props) {
  return {
    id: props.id ?? 'toast-preview',
    title: props.title,
    description: props.description,
    variant: props.variant,
    duration: props.duration
  };
}
