export function createNotFoundPage() {
  return {
    type: 'not-found',
    title: 'Page introuvable',
    actionLabel: 'Retour au tableau de bord',
    destination: '/'
  };
}
