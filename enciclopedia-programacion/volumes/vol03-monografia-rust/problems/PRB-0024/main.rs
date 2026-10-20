use std::num::NonZeroU64;
pub fn parse_positive_pair(a: &str, b: &str) -> Result<u64, &'static str> {
    let x: u64 = a.parse().map_err(|_| "invalid_a")?;
    let y: u64 = b.parse().map_err(|_| "invalid_b")?;
    Ok(x + y)
}
#[cfg(test)]
mod tests {
    use super::*;
    use std::mem::size_of;
    #[test]
    fn verify_niche_and_result_propagation() {
        assert_eq!(size_of::<Option<&u64>>(), size_of::<&u64>());
        assert_eq!(size_of::<Option<NonZeroU64>>(), size_of::<u64>());
        assert_eq!(parse_positive_pair("15", "27"), Ok(42));
        assert_eq!(parse_positive_pair("15", "bad"), Err("invalid_b"));
    }
}
