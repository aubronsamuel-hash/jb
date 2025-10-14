export class ApiClient {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl ?? 'https://api.coulisses-crew.local';
    this.headers = {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(options.headers ?? {})
    };
  }

  async get(path) {
    return {
      url: `${this.baseUrl}${path}`,
      headers: this.headers
    };
  }
}
