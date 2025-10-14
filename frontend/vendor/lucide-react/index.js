function createIcon(name) {
  return function IconComponent(props = {}) {
    return {
      type: 'icon',
      name,
      size: props.size ?? 20,
      strokeWidth: props.strokeWidth ?? 2
    };
  };
}

export const Sun = createIcon('Sun');
export const Moon = createIcon('Moon');
export const Bell = createIcon('Bell');
export const Gauge = createIcon('Gauge');
export const CalendarRange = createIcon('CalendarRange');
export const MapPinned = createIcon('MapPinned');
export const Users = createIcon('Users');
export const Package = createIcon('Package');
export const Wallet = createIcon('Wallet');
export const Settings = createIcon('Settings');

export default {
  Sun,
  Moon,
  Bell,
  Gauge,
  CalendarRange,
  MapPinned,
  Users,
  Package,
  Wallet,
  Settings
};
