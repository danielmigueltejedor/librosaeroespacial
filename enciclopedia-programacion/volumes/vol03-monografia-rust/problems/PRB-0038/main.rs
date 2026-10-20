use std::sync::{mpsc, Arc, Mutex};
use std::thread;
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn verify_scoped_threads_arc_mutex_and_mpsc() {
        let data = [1_i64, 2, 3, 4, 5, 6, 7, 8];
        let counter = Arc::new(Mutex::new(0_i64));
        let (tx, rx) = mpsc::channel();
        thread::scope(|s| {
            for chunk in data.chunks(4) {
                let c = Arc::clone(&counter);
                let t = tx.clone();
                s.spawn(move || {
                    let partial: i64 = chunk.iter().sum();
                    *c.lock().unwrap() += partial;
                    t.send(partial).unwrap();
                });
            }
        });
        drop(tx);
        let channel_total: i64 = rx.iter().sum();
        assert_eq!(*counter.lock().unwrap(), 36);
        assert_eq!(channel_total, 36);
    }
}
