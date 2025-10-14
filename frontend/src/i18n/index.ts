import { createInstance } from 'i18next';
import { frResources } from './fr';

export function createI18n(options = {}) {
  const instance = createInstance();
  const language = options.language ?? 'fr';
  instance.init({
    lng: language,
    fallbackLng: language,
    resources: {
      fr: frResources,
      ...(options.resources ?? {})
    }
  });
  return {
    language,
    t: (key) => instance.t(key)
  };
}
