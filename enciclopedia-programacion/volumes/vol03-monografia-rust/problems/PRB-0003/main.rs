#[cfg(test)]
mod tests {
    use std::mem::size_of;
    #[test]
    fn verify_pointer_and_vec_layouts() {
        let w = size_of::<usize>();
        assert_eq!(size_of::<&u64>(), w);
        assert_eq!(size_of::<&[u64]>(), 2 * w);
        assert_eq!(size_of::<Vec<u64>>(), 3 * w);
    }
}
