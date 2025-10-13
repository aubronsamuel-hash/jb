const suites = [];
let currentSuite = null;
let defaultSuite = null;

export function describe(name, fn) {
  if (typeof fn !== 'function') {
    throw new TypeError('describe callback must be a function');
  }
  const parentSuite = currentSuite;
  const suite = { name, tests: [] };
  suites.push(suite);
  currentSuite = suite;
  try {
    fn();
  } finally {
    currentSuite = parentSuite;
  }
}

export function it(name, fn) {
  const suite = currentSuite ?? getDefaultSuite();
  suite.tests.push({ name, fn });
}

export const test = it;

export function expect(received) {
  return {
    toBe(expected) {
      if (received !== expected) {
        throw new Error(`Expected ${expected} but received ${received}`);
      }
    }
  };
}

export function __getSuites() {
  return suites;
}

export function __reset() {
  suites.length = 0;
  currentSuite = null;
  defaultSuite = null;
}

function getDefaultSuite() {
  if (!defaultSuite) {
    defaultSuite = { name: 'default', tests: [] };
    suites.push(defaultSuite);
  }
  return defaultSuite;
}
