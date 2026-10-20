use rust_kv_engine::{crc32_ieee, KvEngine};

fn main() {
    let engine = KvEngine::new();
    engine.set("arquitectura:hexagonal", "puertos-y-adaptadores").expect("set ok");
    engine.set("arquitectura:limpia", "regla-de-dependencia").expect("set ok");
    let items = engine.scan_prefix("arquitectura:").expect("scan ok");
    let wal = engine.snapshot_wal().expect("wal ok");
    println!(
        "rust-kv-engine ok: registros={}, bytes_wal={}, crc32_std={:#010x}",
        items.len(),
        wal.len(),
        crc32_ieee(b"123456789")
    );
}
