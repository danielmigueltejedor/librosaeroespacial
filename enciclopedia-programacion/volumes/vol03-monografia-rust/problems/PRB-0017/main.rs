pub fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() >= y.len() { x } else { y }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn verify_lifetimes_and_disjoint_borrows() {
        let s1 = String::from("rust-systems");
        let res = {
            let s2 = "c";
            longest(s1.as_str(), s2)
        };
        assert_eq!(res, "rust-systems");
        let mut data = [10, 20, 30, 40];
        let (left, right) = data.split_at_mut(2);
        left[0] += 5;
        right[1] += 10;
        assert_eq!(data, [15, 20, 30, 50]);
    }
}
