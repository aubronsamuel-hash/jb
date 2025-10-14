export function Select(props) {
  return {
    type: 'ui-select',
    id: props.id,
    label: props.label,
    options: props.options,
    placeholder: props.placeholder,
    ariaExpanded: false
  };
}
