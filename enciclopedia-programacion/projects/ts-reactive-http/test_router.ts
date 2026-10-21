import assert from "node:assert/strict";
import test from "node:test";
import { TokenBucketLimiter, validateOrderPayload } from "./router.ts";

test("validateOrderPayload accepts valid payload and rejects malformed objects", () => {
  const valid = validateOrderPayload({ sku: "RUST-BOOK-01", qty: 3 });
  assert.equal(valid.ok, true);
  if (valid.ok) {
    assert.equal(valid.value.sku, "RUST-BOOK-01");
    assert.equal(valid.value.qty, 3);
  }
  const invalid = validateOrderPayload({ sku: "A", qty: 0 });
  assert.equal(invalid.ok, false);
});

test("TokenBucketLimiter enforces burst capacity and refills deterministically", () => {
  const limiter = new TokenBucketLimiter(2, 1);
  assert.equal(limiter.allow("10.0.0.1", 1000), true);
  assert.equal(limiter.allow("10.0.0.1", 1000), true);
  assert.equal(limiter.allow("10.0.0.1", 1000), false);
  assert.equal(limiter.allow("10.0.0.1", 2000), true);
});


test("limiter rejects nonfinite configuration and does not refill twice after clock rollback", () => {
  assert.throws(() => new TokenBucketLimiter(0, 1), RangeError);
  assert.throws(() => new TokenBucketLimiter(2, NaN), RangeError);
  const limiter = new TokenBucketLimiter(1, 1);
  assert.equal(limiter.allow("a", 1000), true);
  assert.equal(limiter.allow("a", 0), false);
  assert.equal(limiter.allow("a", 1000), false);
  assert.equal(limiter.allow("a", 2000), true);
  assert.throws(() => limiter.allow("a", Infinity), RangeError);
});

test("quantity must be a positive safe integer", () => {
  for (const qty of [NaN, Infinity, 1.5, 0, -1, Number.MAX_SAFE_INTEGER + 1]) {
    assert.equal(validateOrderPayload({ sku: "ABC", qty }).ok, false);
  }
});
