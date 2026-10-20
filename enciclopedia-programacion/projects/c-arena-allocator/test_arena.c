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

    uint8_t frame[] = {0xA5, 0x5A, 0x01, 0x03, 0x00, 0x00, 0x00, 0x04, 'T', 'E', 'L', 'E'};
    TelemetryPacket pkt;
    assert(parse_telemetry_packet(frame, sizeof(frame), &pkt) == true);
    assert(pkt.version == 1 && pkt.flags == 3 && pkt.payload_len == 4);
    assert(memcmp(pkt.payload, "TELE", 4) == 0);

    /* Trama truncada debe rechazarse limpiamente */
    assert(parse_telemetry_packet(frame, 10, &pkt) == false);

    arena_reset(&arena);
    assert(arena.offset == 0);
    printf("c-arena-allocator ok: align=%zu, p2[0]=0x%llx\n",
           alignof(uint64_t), (unsigned long long)p2[0]);
    return 0;
}
