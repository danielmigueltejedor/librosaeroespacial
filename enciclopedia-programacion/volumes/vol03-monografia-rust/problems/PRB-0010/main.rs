#[cfg(test)]
mod tests {
    #[test]
    fn verify_utf8_and_checked_arithmetic() {
        let s = "programación"; // 11 ASCII + 'ó' (2 bytes)
        assert_eq!(s.chars().count(), 12);
        assert_eq!(s.len(), 13);
        let max_u8: u8 = 250;
        assert_eq!(max_u8.checked_add(10), None);
        assert_eq!(max_u8.saturating_add(10), 255);
    }
}
