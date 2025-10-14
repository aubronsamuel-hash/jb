import { create } from 'zustand';

export const useThemeStore = create((set, get) => ({
  mode: 'light',
  availableModes: ['light', 'dark'],
  setMode: (mode) => {
    set({ mode });
  },
  toggleMode: () => {
    const next = get().mode === 'light' ? 'dark' : 'light';
    set({ mode: next });
    return next;
  }
}));
