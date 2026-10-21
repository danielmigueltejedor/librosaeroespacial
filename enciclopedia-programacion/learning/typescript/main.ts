type Result = { ok: true; value: number } | { ok: false; error: string };
function parseCount(input: unknown): Result {
  if (typeof input !== "number" || !Number.isSafeInteger(input) || input < 0) {
    return { ok: false, error: "invalid count" };
  }
  return { ok: true, value: input };
}
function describe(result: Result): string {
  if (result.ok) {
    return `count=${result.value}`;
  }
  return `error=${result.error}`;
}
function withDefault(input: unknown, fallback: number): number {
  const result = parseCount(input);
  return result.ok ? result.value : fallback;
}
function check(condition: boolean): void {
  if (!condition) throw new Error("test failed");
}
check(parseCount(0).ok);
check(!parseCount("3").ok);
check(!parseCount(NaN).ok);
check(!parseCount(-1).ok);
check(!parseCount(1.5).ok);
check(describe(parseCount(3)) === "count=3");
check(describe(parseCount(null)) === "error=invalid count");
check(withDefault(0, 7) === 0);
check(withDefault(undefined, 7) === 7);
console.log("typescript: OK");
