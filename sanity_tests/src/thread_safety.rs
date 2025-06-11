#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::min_ident_chars, reason="Focus on important lints")]
#![expect(clippy::items_after_statements, reason="Focus on important lints")]
#![expect(clippy::std_instead_of_core, reason="Focus on important lints")]
#![expect(clippy::std_instead_of_alloc, reason="Focus on important lints")]
#![expect(clippy::default_numeric_fallback, reason="Focus on important lints")]
use std::sync::Arc;
use std::cell::RefCell;

pub fn run() {
    // This is fine, as `i32` implements `Send` and `Sync`.
    let a = Arc::new(42);

    // `RefCell` is not `Sync`, so using it with `Arc` in a multithreaded context is unsafe.
    // Clippy will warn about this.
    let b = Arc::new(RefCell::new(42));

    // Preferred: Use a thread-safe alternative like `RwLock`.
    use std::sync::RwLock;
    let c = Arc::new(RwLock::new(42));
}
