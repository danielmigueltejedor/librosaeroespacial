#include "arena.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    alignas(max_align_t) uint8_t backing[256];
    Arena arena;
    arena_init(&arena, backing, sizeof(backing));

    uint8_t *p1 = arena_alloc_aligned(&arena, 3, 1);
    assert(p1 != NULL);
    uint64_t *p2 = arena_alloc_aligned(&arena, sizeof(uint64_t) * 4, alignof(uint64_t));
    assert(p2 != NULL);
    assert(((uintptr_t)p2 % alignof(uint64_t)) == 0);
    p2[0] = 0x1122334455667788ULL;
    p2[3] = 0xCAFEBABECAFED00DULL;

    /* Desbordamiento controlado debe devolver NULL sin UB */
    void *overflow = arena_alloc_aligned(&arena, 512, 8);
    assert(overflow == NULL);

    assert(arena_alloc_aligned(&arena, 1, 0) == NULL);
    assert(arena_alloc_aligned(&arena, 1, 3) == NULL);
    assert(arena_alloc_aligned(&arena, 0, 1) == NULL);
    assert(arena_alloc_aligned(&arena, SIZE_MAX, 1) == NULL);
    size_t saved = arena.offset;
    arena.offset = SIZE_MAX;
    assert(arena_alloc_aligned(&arena, 1, 1) == NULL);
    arena.offset = saved;

    uint8_t frame[] = {0xA5, 0x5A, 0x01, 0x03, 0x00, 0x00, 0x00, 0x04, 'T', 'E', 'L', 'E'};
    TelemetryPacket pkt;
    assert(parse_telemetry_packet(frame, sizeof(frame), &pkt) == true);
    assert(pkt.version == 1 && pkt.flags == 3 && pkt.payload_len == 4);
    assert(memcmp(pkt.payload, "TELE", 4) == 0);

    /* Trama truncada debe rechazarse limpiamente */
    assert(parse_telemetry_packet(frame, 10, &pkt) == false);

    assert(!parse_telemetry_packet(NULL, 100, &pkt));
    assert(!parse_telemetry_packet(frame, 7, &pkt));
    assert(!parse_telemetry_packet(frame, sizeof(frame), NULL));
    frame[0] = 0;
    assert(!parse_telemetry_packet(frame, sizeof(frame), &pkt));

    arena_reset(&arena);
    assert(arena.offset == 0);
    printf("c-arena-allocator ok: align=%zu, p2[0]=0x%llx\n",
           alignof(uint64_t), (unsigned long long)p2[0]);
    return 0;
}
