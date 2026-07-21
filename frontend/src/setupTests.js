// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
// Old Testing Library releases expect this Node timer alias in Jest's jsdom.
global.setImmediate = global.setImmediate || ((callback, ...args) => (
  setTimeout(callback, 0, ...args)
));
global.clearImmediate = global.clearImmediate || clearTimeout;

require('@testing-library/jest-dom');
