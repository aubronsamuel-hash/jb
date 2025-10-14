class I18nInstance {
  constructor() {
    this.language = 'en';
    this.resources = {};
  }

  init(options = {}) {
    this.language = options.lng ?? 'en';
    this.resources = options.resources ?? {};
    return this;
  }

  t(key) {
    const langPack = this.resources[this.language] ?? {};
    const translation = langPack.translation ?? {};
    return translation[key] ?? key;
  }

  changeLanguage(nextLanguage) {
    this.language = nextLanguage;
    return Promise.resolve(nextLanguage);
  }
}

export function createInstance() {
  return new I18nInstance();
}

export default { createInstance };
