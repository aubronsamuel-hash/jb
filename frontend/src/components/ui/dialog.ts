export function Dialog(props) {
  return {
    type: 'ui-dialog',
    id: props.id,
    title: props.title,
    description: props.description,
    confirmLabel: props.confirmLabel,
    cancelLabel: props.cancelLabel,
    role: 'dialog',
    ariaModal: true
  };
}
