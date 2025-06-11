
#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#[warn(clippy::panic)]   // restriction group.
pub fn run() {
    // This panic is not appropriate in production code.
    panic!("Even with a good reason");
}