#[repr(C)]
struct BadLayoutC { a: u8, b: u64, c: u8 }
struct GoodLayoutRust { a: u8, b: u64, c: u8 }
macro_rules! vec_of_squares {
    ($($x:expr),* $(,)?) => {
        vec![$(($x) * ($x)),*]
    };
}
#[cfg(test)]
mod tests {
    use super::*;
    use std::mem::size_of;
    #[test]
    fn verify_repr_and_declarative_macro() {
        assert_eq!(size_of::<BadLayoutC>(), 24);
        assert_eq!(size_of::<GoodLayoutRust>(), 16);
        let sq = vec_of_squares![2, 3, 5];
        assert_eq!(sq, vec![4, 9, 25]);
    }
}
