export function createPlaceholderPage(id, description) {
  return {
    type: 'placeholder-page',
    id,
    title: `Module ${id}`,
    description,
    expectedRelease: 'Roadmap S1'
  };
}
