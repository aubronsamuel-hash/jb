export function DataTable(props) {
  return {
    type: 'ui-data-table',
    caption: props.caption,
    columns: props.columns,
    rowCount: props.rows.length,
    ariaRole: 'table'
  };
}
