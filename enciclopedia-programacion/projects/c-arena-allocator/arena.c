#include "arena.h"
#include <string.h>

static bool is_power_of_two(size_t x) {
    return x != 0 && (x & (x - 1)) == 0;
}

void arena_init(Arena *a, uint8_t *backing, size_t capacity) {
    a->buffer = backing;
    a->capacity = capacity;
    a->offset = 0;
}

void *arena_alloc_aligned(Arena *a, size_t size, size_t alignment) {
    if (!a || !a->buffer || size == 0 || !is_power_of_two(alignment)) {
        return NULL;
    }
    uintptr_t base = (uintptr_t)(a->buffer);
    uintptr_t current = base + a->offset;
    size_t mask = alignment - 1;
    uintptr_t aligned = (current + mask) & ~((uintptr_t)mask);
    size_t padding = (size_t)(aligned - current);
    if (padding > a->capacity - a->offset || size > a->capacity - a->offset - padding) {
        return NULL;
    }
    a->offset += padding + size;
    void *ptr = (void *)aligned;
    memset(ptr, 0, size);
    return ptr;
}

void arena_reset(Arena *a) {
    if (a) {
        a->offset = 0;
    }
}

bool parse_telemetry_packet(const uint8_t *raw, size_t raw_len, TelemetryPacket *out) {
    if (!raw || !out || raw_len < 8) {
        return false;
    }
    uint16_t magic = (uint16_t)((uint16_t)raw[0] << 8) | (uint16_t)raw[1];
    if (magic != 0xA55Au) {
        return false;
    }
    uint8_t version = raw[2];
    uint8_t flags = raw[3];
    uint32_t len = ((uint32_t)raw[4] << 24)
                 | ((uint32_t)raw[5] << 16)
                 | ((uint32_t)raw[6] << 8)
                 | (uint32_t)raw[7];
    if (len > raw_len - 8) {
        return false;
    }
    out->magic = magic;
    out->version = version;
    out->flags = flags;
    out->payload_len = len;
    out->payload = raw + 8;
    return true;
}
