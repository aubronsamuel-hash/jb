export class ToastManager {
  constructor() {
    this.items = [];
  }

  push(toast) {
    const entry = {
      ...toast,
      id: `toast-${Date.now()}-${Math.round(Math.random() * 1000)}`
    };
    this.items.push(entry);
    return entry;
  }

  dismiss(id) {
    const index = this.items.findIndex((item) => item.id === id);
    if (index >= 0) {
      this.items.splice(index, 1);
    }
  }

  list() {
    return [...this.items];
  }

  summary() {
    return {
      type: 'toast-viewport',
      toasts: this.list()
    };
  }
}
