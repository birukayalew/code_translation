
#![expect(clippy::future_not_send, reason="Focus on important lints")]
#![expect(clippy::arithmetic_side_effects, reason="Focus on important lints")]
#![expect(clippy::let_underscore_future, reason="Focus on important lints")]
#![expect(clippy::unused_async, reason="Focus on important lints")]
#![expect(clippy::single_call_fn, reason="Focus on important lints")]
use core::cell::RefCell;

async fn baz() {
    // Simulate some awaitable work
}

async fn foo(x: &RefCell<u32>) {
    let mut y = x.borrow_mut(); // This is held across await
    *y += 1;
    baz().await; // ⚠️ Lint should trigger here
}

pub fn run() {
    let x = RefCell::new(42);
    let _ = foo(&x);
}
