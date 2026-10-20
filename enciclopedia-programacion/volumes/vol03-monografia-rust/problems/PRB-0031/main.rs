use std::cell::RefCell;
use std::rc::Rc;
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn verify_iterators_and_rc_refcell() {
        let sum_sq: i64 = (1..=10).filter(|x| x % 2 == 0).map(|x| x * x).sum();
        assert_eq!(sum_sq, 4 + 16 + 36 + 64 + 100);
        let shared = Rc::new(RefCell::new(vec![1, 2]));
        let weak_ref = Rc::downgrade(&shared);
        assert_eq!(Rc::strong_count(&shared), 1);
        assert_eq!(Rc::weak_count(&shared), 1);
        shared.borrow_mut().push(3);
        assert_eq!(*weak_ref.upgrade().unwrap().borrow(), vec![1, 2, 3]);
    }
}
