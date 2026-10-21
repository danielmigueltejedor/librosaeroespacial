"use strict";
const assert = require("node:assert/strict");
function total(items) {
  let cents = 0;
  for (const item of items) {
    cents += item.price * item.quantity;
  }
  return cents;
}
function discount(cents, percent) {
  if (!Number.isInteger(percent) || percent < 0 || percent > 100) {
    throw new RangeError("percent");
  }
  return Math.floor(cents * (100 - percent) / 100);
}
function delivery(cents) {
  return cents >= 5000 ? 0 : 399;
}
assert.equal(total([{price: 125, quantity: 2}, {price: 300, quantity: 1}]), 550);
assert.equal(total([]), 0);
assert.equal(discount(101, 10), 90);
assert.equal(discount(100, 100), 0);
assert.throws(() => discount(100, -1), RangeError);
assert.throws(() => discount(100, 2.5), RangeError);
assert.equal(delivery(4999), 399);
assert.equal(delivery(5000), 0);
assert.equal(delivery(5001), 0);
console.log("javascript: OK");
