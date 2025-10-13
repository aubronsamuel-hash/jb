const ELEMENT_SYMBOL = Symbol.for('orga.react.element');
const FRAGMENT_SYMBOL = Symbol.for('orga.react.fragment');

function flattenChildren(children) {
  const flat = [];
  for (const child of children) {
    if (Array.isArray(child)) {
      flat.push(...flattenChildren(child));
    } else if (child === null || child === undefined || child === false) {
      continue;
    } else {
      flat.push(child);
    }
  }
  return flat;
}

export function createElement(type, props = {}, ...children) {
  const normalizedChildren = flattenChildren(children);
  if (type === Fragment) {
    return normalizedChildren;
  }
  if (typeof type === 'function') {
    return type({ ...props, children: normalizedChildren });
  }
  return {
    $$typeof: ELEMENT_SYMBOL,
    type,
    props: {
      ...props,
      children: normalizedChildren
    }
  };
}

export const Fragment = FRAGMENT_SYMBOL;

export function useState(initialValue) {
  let state = typeof initialValue === 'function' ? initialValue() : initialValue;
  const setState = (next) => {
    state = typeof next === 'function' ? next(state) : next;
    return state;
  };
  return [state, setState];
}

export function useMemo(factory) {
  return factory();
}

export function useRef(initialValue = null) {
  return { current: initialValue };
}

export function useCallback(fn) {
  return fn;
}

export function useEffect() {}
export function useLayoutEffect() {}

export function forwardRef(renderFn) {
  return function ForwardRefComponent(props) {
    const ref = { current: null };
    return renderFn(props, ref);
  };
}

export function createContext(defaultValue) {
  const context = {
    value: defaultValue,
    defaultValue
  };
  context.Provider = function Provider(providerProps = {}) {
    context.value = providerProps.value;
    return providerProps.children;
  };
  context.Consumer = function Consumer(consumerProps = {}) {
    const value = context.value ?? context.defaultValue;
    if (typeof consumerProps.children === 'function') {
      return consumerProps.children(value);
    }
    return consumerProps.children;
  };
  return context;
}

export function useContext(context) {
  return context.value ?? context.defaultValue;
}

export default {
  createElement,
  Fragment,
  useState,
  useMemo,
  useRef,
  useCallback,
  useEffect,
  useLayoutEffect,
  forwardRef,
  createContext,
  useContext
};
