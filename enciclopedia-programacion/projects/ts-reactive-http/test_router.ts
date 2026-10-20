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
