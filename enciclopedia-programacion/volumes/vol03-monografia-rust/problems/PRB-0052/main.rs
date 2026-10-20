pub fn crc32_ieee(data: &[u8]) -> u32 {
    let mut crc: u32 = 0xFFFF_FFFF;
    for &byte in data {
        crc ^= u32::from(byte);
        for _ in 0..8 {
            if (crc & 1) != 0 { crc = (crc >> 1) ^ 0xEDB8_8320; } else { crc >>= 1; }
        }
    }
    !crc
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn verify_crc32_standard_check_value() {
        // El valor estándar IEEE 802.3 de "123456789" es 0xCBF43926
        assert_eq!(crc32_ieee(b"123456789"), 0xCBF4_3926);
    }
}
