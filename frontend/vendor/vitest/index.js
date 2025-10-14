const suites = [];
let currentSuite = null;
let defaultSuite = null;

function describe(name, fn) {
  if (typeof fn !== 'function') {
    throw new TypeError('describe callback must be une fonction');
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

function getDefaultSuite() {
  if (!defaultSuite) {
    defaultSuite = { name: 'default', tests: [] };
    suites.push(defaultSuite);
  }
  return defaultSuite;
}

function it(name, fn) {
  const suite = currentSuite ?? getDefaultSuite();
  suite.tests.push({ name, fn });
}

const test = it;

function expect(received) {
  return {
    toBe(expected) {
      if (received !== expected) {
        throw new Error(`Expected ${expected} but received ${received}`);
      }
    },
    toBeGreaterThan(expected) {
      if (!(typeof received === 'number' && received > expected)) {
        throw new Error(`Expected ${received} to be greater than ${expected}`);
      }
    },
    toBeDefined() {
      if (received === undefined) {
        throw new Error('Expected value to be defined');
      }
    },
    toContain(value) {
      if (!Array.isArray(received) && typeof received !== 'string') {
        throw new Error('toContain works with arrays ou strings');
      }
      if (!received.includes(value)) {
        throw new Error(`Expected ${received} to contain ${value}`);
      }
    }
  };
}

function __getSuites() {
  return suites;
}

function __reset() {
  suites.length = 0;
  currentSuite = null;
  defaultSuite = null;
}

module.exports = {
  describe,
  it,
  test,
  expect,
  __getSuites,
  __reset
};
