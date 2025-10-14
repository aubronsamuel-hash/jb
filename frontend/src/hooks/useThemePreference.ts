import { useThemeStore } from '../state/theme-store';
import { createAppTheme } from '../app/theme';

export function useThemePreference() {
  const state = useThemeStore();
  return {
    mode: state.mode,
    availableModes: state.availableModes,
    theme: createAppTheme(state.mode),
    toggle: state.toggleMode,
    setMode: state.setMode
  };
}
