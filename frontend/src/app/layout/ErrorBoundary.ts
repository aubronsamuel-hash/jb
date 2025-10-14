export class ErrorBoundary {
  constructor(props = {}) {
    this.props = props;
    this.state = { hasError: false, errorMessage: null };
  }

  componentDidCatch(error) {
    this.state = {
      hasError: true,
      errorMessage: error.message
    };
  }

  reset() {
    this.state = { hasError: false, errorMessage: null };
  }

  render(children) {
    if (this.state.hasError) {
      return {
        type: 'error-boundary',
        title: this.props.fallbackTitle ?? 'Une erreur est survenue',
        retryAction: 'Reessayer',
        supportEmail: this.props.supportEmail ?? 'support@coulisses-crew.fr'
      };
    }
    return children;
  }
}
