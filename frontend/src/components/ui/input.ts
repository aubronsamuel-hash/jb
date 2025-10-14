export function Input(props) {
  return {
    type: 'ui-input',
    id: props.id,
    label: props.label,
    placeholder: props.placeholder,
    inputType: props.type ?? 'text',
    required: props.required ?? false
  };
}
