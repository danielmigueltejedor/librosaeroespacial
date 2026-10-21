export type Result<T, E> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly error: E };

export interface HttpRequest<B = unknown> {
  readonly method: "GET" | "POST" | "DELETE";
  readonly path: string;
  readonly clientIp: string;
  readonly body?: B;
}

export interface HttpResponse<T = unknown> {
  readonly status: number;
  readonly payload: T;
}

export class TokenBucketLimiter {
  private readonly buckets = new Map<string, { tokens: number; lastRefillMs: number }>();
  private readonly capacity: number;
  private readonly refillPerSecond: number;

  constructor(capacity: number, refillPerSecond: number) {
    if (!Number.isFinite(capacity) || capacity < 1 || !Number.isFinite(refillPerSecond) || refillPerSecond < 0) {
      throw new RangeError("capacity >= 1 y refillPerSecond >= 0 deben ser finitos");
    }
    this.capacity = capacity;
    this.refillPerSecond = refillPerSecond;
  }

  public allow(key: string, nowMs: number): boolean {
    if (!Number.isFinite(nowMs)) throw new RangeError("nowMs debe ser finito");
    const existing = this.buckets.get(key) ?? { tokens: this.capacity, lastRefillMs: nowMs };
    const effectiveNowMs = Math.max(nowMs, existing.lastRefillMs);
    const elapsedSec = (effectiveNowMs - existing.lastRefillMs) / 1000;
    const refilled = Math.min(this.capacity, existing.tokens + elapsedSec * this.refillPerSecond);
    if (refilled < 1) {
      this.buckets.set(key, { tokens: refilled, lastRefillMs: effectiveNowMs });
      return false;
    }
    this.buckets.set(key, { tokens: refilled - 1, lastRefillMs: effectiveNowMs });
    return true;
  }
}

export function validateOrderPayload(input: unknown): Result<{ sku: string; qty: number }, string> {
  if (typeof input !== "object" || input === null) {
    return { ok: false, error: "el cuerpo debe ser un objeto JSON" };
  }
  const candidate = input as Record<string, unknown>;
  if (typeof candidate.sku !== "string" || candidate.sku.trim().length < 3) {
    return { ok: false, error: "sku inválido: cadena de al menos 3 caracteres requerida" };
  }
  if (typeof candidate.qty !== "number" || !Number.isSafeInteger(candidate.qty) || candidate.qty <= 0) {
    return { ok: false, error: "qty inválido: entero positivo requerido" };
  }
  return { ok: true, value: { sku: candidate.sku.trim(), qty: candidate.qty } };
}
