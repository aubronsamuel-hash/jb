export type ApiClientInit = {
  baseUrl?: string;
  headers?: Record<string, string>;
  timeoutMs?: number;
};

export type NormalizedErrorBody = {
  error?: {
    code?: string;
    message?: string;
  };
  [key: string]: unknown;
};

export class ApiClientError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details: NormalizedErrorBody;

  constructor(message: string, options: { status: number; code: string; details?: NormalizedErrorBody }) {
    super(message);
    this.name = 'ApiClientError';
    this.status = options.status;
    this.code = options.code;
    this.details = options.details ?? {};
  }

  toToastMessage(): string {
    if (this.status === 409) {
      return 'Conflit detecte. Veuillez recharger le planning.';
    }
    if (this.status === 422) {
      return 'Verification echouee. Corrigez les champs surlignes.';
    }
    return 'Service indisponible. Reessayez dans quelques instants.';
  }
}

export class ApiClient {
  readonly baseUrl: string;
  readonly headers: Record<string, string>;
  readonly timeoutMs: number;

  constructor(options: ApiClientInit = {}) {
    this.baseUrl = options.baseUrl ?? 'https://api.coulisses-crew.local';
    this.headers = {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(options.headers ?? {})
    };
    this.timeoutMs = options.timeoutMs ?? 8000;
  }

  buildUrl(path: string): string {
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;
    return `${this.baseUrl.replace(/\/$/, '')}${normalizedPath}`;
  }

  get(path: string, init: { headers?: Record<string, string>; timeoutMs?: number } = {}) {
    return {
      url: this.buildUrl(path),
      method: 'GET',
      headers: { ...this.headers, ...(init.headers ?? {}) },
      timeoutMs: init.timeoutMs ?? this.timeoutMs
    };
  }

  static normalizeError(status: number, body: unknown): ApiClientError {
    const normalized: NormalizedErrorBody = typeof body === 'object' && body !== null ? (body as NormalizedErrorBody) : {};
    const payload = typeof normalized.error === 'object' && normalized.error !== null ? normalized.error : {};
    const resolvedCode = typeof payload.code === 'string' && payload.code ? payload.code : ApiClient.defaultCode(status);
    const resolvedMessage = typeof payload.message === 'string' && payload.message
      ? payload.message
      : ApiClient.defaultMessage(status);
    ApiClient.assertAscii(resolvedMessage);
    return new ApiClientError(resolvedMessage, { status, code: resolvedCode, details: normalized });
  }

  private static defaultCode(status: number): string {
    if (status === 409) {
      return 'conflict';
    }
    if (status === 422) {
      return 'validation_error';
    }
    return 'unexpected_error';
  }

  private static defaultMessage(status: number): string {
    if (status === 409) {
      return 'Conflit detecte lors de la mise a jour';
    }
    if (status === 422) {
      return 'Requete invalide envoyee au service';
    }
    return 'Erreur API inattendue';
  }

  private static assertAscii(value: string): void {
    for (let index = 0; index < value.length; index += 1) {
      if (value.charCodeAt(index) > 127) {
        throw new Error('Only ASCII messages are supported');
      }
    }
  }
}
