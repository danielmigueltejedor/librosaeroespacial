#ifndef ARENA_H
#define ARENA_H

#include <stdalign.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct {
    uint8_t *buffer;
    size_t capacity;
    size_t offset;
} Arena;

typedef struct {
    uint16_t magic;
    uint8_t version;
    uint8_t flags;
    uint32_t payload_len;
    const uint8_t *payload;
} TelemetryPacket;

void arena_init(Arena *a, uint8_t *backing, size_t capacity);
void *arena_alloc_aligned(Arena *a, size_t size, size_t alignment);
void arena_reset(Arena *a);
bool parse_telemetry_packet(const uint8_t *raw, size_t raw_len, TelemetryPacket *out);

#endif
