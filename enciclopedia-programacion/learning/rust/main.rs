fn parse_line(text: &str) -> Result<u32, String> {
    text.trim().parse::<u32>().map_err(|_| "invalid reading".to_string())
}
fn sum_valid(lines: &[&str]) -> u64 {
    let mut total = 0_u64;
    for line in lines {
        if let Ok(value) = parse_line(line) {
            total += u64::from(value);
        }
    }
    total
}
fn bounded_add(left: u32, right: u32) -> Option<u32> {
    left.checked_add(right)
}
fn main() {
    assert_eq!(parse_line(" 12 "), Ok(12));
    assert!(parse_line("-1").is_err());
    assert!(parse_line("").is_err());
    assert_eq!(sum_valid(&["2", "bad", "3"]), 5);
    assert_eq!(sum_valid(&[]), 0);
    assert_eq!(bounded_add(2, 3), Some(5));
    assert_eq!(bounded_add(u32::MAX, 1), None);
    println!("rust: OK");
}
