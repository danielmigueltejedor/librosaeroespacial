//! Motor clave-valor concurrente con registro Write-Ahead Log (WAL) en formato binario
//! y suma de comprobación CRC32 determinista.

use std::collections::BTreeMap;
use std::fmt;
use std::sync::{Arc, RwLock};

/// Errores tipados del motor de almacenamiento.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum KvError {
    EmptyKey,
    CorruptedRecord { offset: usize, expected_crc: u32, actual_crc: u32 },
    UnexpectedEof { offset: usize },
    InvalidUtf8,
    LockPoisoned,
}

impl fmt::Display for KvError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyKey => write!(f, "la clave no puede estar vacía"),
            Self::CorruptedRecord { offset, expected_crc, actual_crc } => write!(
                f,
                "registro corrupto en byte {offset}: CRC esperado {expected_crc:#010x}, obtenido {actual_crc:#010x}"
            ),
            Self::UnexpectedEof { offset } => write!(f, "fin de flujo inesperado en byte {offset}"),
            Self::InvalidUtf8 => write!(f, "secuencia UTF-8 inválida en clave o valor"),
            Self::LockPoisoned => write!(f, "cerrojo RwLock contaminado por pánico previo"),
        }
    }
}

impl std::error::Error for KvError {}

/// Calcula CRC32 (polinomio IEEE 802.3 0xEDB88320) sin dependencias externas.
pub fn crc32_ieee(bytes: &[u8]) -> u32 {
    let mut crc: u32 = 0xFFFF_FFFF;
    for &b in bytes {
        crc ^= u32::from(b);
        for _ in 0..8 {
            let mask = (crc & 1).wrapping_neg();
            crc = (crc >> 1) ^ (0xEDB8_8320 & mask);
        }
    }
    !crc
}

/// Operación registrada en el Write-Ahead Log.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum WalOp {
    Put { key: String, value: String },
    Delete { key: String },
}

impl WalOp {
    /// Serializa un registro en formato `[crc32:4][op:1][klen:4][vlen:4][key][value]`.
    pub fn encode(&self) -> Vec<u8> {
        let mut payload = Vec::new();
        match self {
            Self::Put { key, value } => {
                payload.push(1u8);
                payload.extend_from_slice(&(key.len() as u32).to_le_bytes());
                payload.extend_from_slice(&(value.len() as u32).to_le_bytes());
                payload.extend_from_slice(key.as_bytes());
                payload.extend_from_slice(value.as_bytes());
            }
            Self::Delete { key } => {
                payload.push(2u8);
                payload.extend_from_slice(&(key.len() as u32).to_le_bytes());
                payload.extend_from_slice(&0u32.to_le_bytes());
                payload.extend_from_slice(key.as_bytes());
            }
        }
        let crc = crc32_ieee(&payload);
        let mut frame = Vec::with_capacity(4 + payload.len());
        frame.extend_from_slice(&crc.to_le_bytes());
        frame.extend_from_slice(&payload);
        frame
    }

    /// Reconstruye la secuencia de operaciones validando cada CRC32.
    pub fn decode_stream(stream: &[u8]) -> Result<Vec<Self>, KvError> {
        let mut cursor = 0usize;
        let mut ops = Vec::new();
        while cursor < stream.len() {
            if cursor + 13 > stream.len() {
                return Err(KvError::UnexpectedEof { offset: cursor });
            }
            let expected_crc = u32::from_le_bytes(stream[cursor..cursor + 4].try_into().unwrap());
            let op_code = stream[cursor + 4];
            let klen = u32::from_le_bytes(stream[cursor + 5..cursor + 9].try_into().unwrap()) as usize;
            let vlen = u32::from_le_bytes(stream[cursor + 9..cursor + 13].try_into().unwrap()) as usize;
            let frame_end = cursor + 13 + klen + vlen;
            if frame_end > stream.len() {
                return Err(KvError::UnexpectedEof { offset: cursor });
            }
            let payload = &stream[cursor + 4..frame_end];
            let actual_crc = crc32_ieee(payload);
            if expected_crc != actual_crc {
                return Err(KvError::CorruptedRecord {
                    offset: cursor,
                    expected_crc,
                    actual_crc,
                });
            }
            let key = std::str::from_utf8(&stream[cursor + 13..cursor + 13 + klen])
                .map_err(|_| KvError::InvalidUtf8)?
                .to_owned();
            let op = match op_code {
                1 => {
                    let value = std::str::from_utf8(&stream[cursor + 13 + klen..frame_end])
                        .map_err(|_| KvError::InvalidUtf8)?
                        .to_owned();
                    Self::Put { key, value }
                }
                2 => Self::Delete { key },
                _ => return Err(KvError::CorruptedRecord { offset: cursor, expected_crc, actual_crc }),
            };
            ops.push(op);
            cursor = frame_end;
        }
        Ok(ops)
    }
}

#[derive(Default)]
struct EngineState {
    index: BTreeMap<String, String>,
    wal_bytes: Vec<u8>,
}

/// Motor KV concurrente seguro entre hilos (`Clone + Send + Sync`).
#[derive(Clone, Default)]
pub struct KvEngine {
    inner: Arc<RwLock<EngineState>>,
}

impl KvEngine {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn from_wal(stream: &[u8]) -> Result<Self, KvError> {
        let ops = WalOp::decode_stream(stream)?;
        let mut index = BTreeMap::new();
        for op in ops {
            match op {
                WalOp::Put { key, value } => {
                    index.insert(key, value);
                }
                WalOp::Delete { key } => {
                    index.remove(&key);
                }
            }
        }
        Ok(Self {
            inner: Arc::new(RwLock::new(EngineState {
                index,
                wal_bytes: stream.to_vec(),
            })),
        })
    }

    pub fn set(&self, key: impl Into<String>, value: impl Into<String>) -> Result<(), KvError> {
        let key = key.into();
        if key.is_empty() {
            return Err(KvError::EmptyKey);
        }
        let value = value.into();
        let frame = WalOp::Put { key: key.clone(), value: value.clone() }.encode();
        let mut guard = self.inner.write().map_err(|_| KvError::LockPoisoned)?;
        guard.wal_bytes.extend_from_slice(&frame);
        guard.index.insert(key, value);
        Ok(())
    }

    pub fn get(&self, key: &str) -> Result<Option<String>, KvError> {
        let guard = self.inner.read().map_err(|_| KvError::LockPoisoned)?;
        Ok(guard.index.get(key).cloned())
    }

    pub fn delete(&self, key: &str) -> Result<bool, KvError> {
        if key.is_empty() {
            return Err(KvError::EmptyKey);
        }
        let frame = WalOp::Delete { key: key.to_owned() }.encode();
        let mut guard = self.inner.write().map_err(|_| KvError::LockPoisoned)?;
        guard.wal_bytes.extend_from_slice(&frame);
        Ok(guard.index.remove(key).is_some())
    }

    pub fn scan_prefix(&self, prefix: &str) -> Result<Vec<(String, String)>, KvError> {
        let guard = self.inner.read().map_err(|_| KvError::LockPoisoned)?;
        Ok(guard
            .index
            .range(prefix.to_owned()..)
            .take_while(|(k, _)| k.starts_with(prefix))
            .map(|(k, v)| (k.clone(), v.clone()))
            .collect())
    }

    pub fn snapshot_wal(&self) -> Result<Vec<u8>, KvError> {
        let guard = self.inner.read().map_err(|_| KvError::LockPoisoned)?;
        Ok(guard.wal_bytes.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;

    #[test]
    fn crc32_matches_standard_check_value() {
        assert_eq!(crc32_ieee(b"123456789"), 0xCBF4_3926);
    }

    #[test]
    fn crud_and_wal_recovery_roundtrip() {
        let engine = KvEngine::new();
        engine.set("sensor:temp", "298.15").unwrap();
        engine.set("sensor:pres", "101325").unwrap();
        engine.delete("sensor:temp").unwrap();
        let wal = engine.snapshot_wal().unwrap();

        let restored = KvEngine::from_wal(&wal).unwrap();
        assert_eq!(restored.get("sensor:temp").unwrap(), None);
        assert_eq!(restored.get("sensor:pres").unwrap().as_deref(), Some("101325"));
    }

    #[test]
    fn detects_bit_flip_corruption_in_wal() {
        let engine = KvEngine::new();
        engine.set("clave", "valor_integro").unwrap();
        let mut wal = engine.snapshot_wal().unwrap();
        let last = wal.len() - 1;
        wal[last] ^= 0x01;
        let err = KvEngine::from_wal(&wal).err().expect("debe detectar corrupción CRC32");
        assert!(matches!(err, KvError::CorruptedRecord { .. }));
    }

    #[test]
    fn concurrent_writers_and_prefix_scan_are_consistent() {
        let engine = KvEngine::new();
        let mut handles = Vec::new();
        for worker in 0..4 {
            let cloned = engine.clone();
            handles.push(thread::spawn(move || {
                for i in 0..25 {
                    let k = format!("nodo:{worker:02}:{i:02}");
                    cloned.set(k, format!("v-{worker}-{i}")).unwrap();
                }
            }));
        }
        for h in handles {
            h.join().unwrap();
        }
        let all = engine.scan_prefix("nodo:").unwrap();
        assert_eq!(all.len(), 100);
    }
}
