#![expect(clippy::single_call_fn, reason="Focus on important lints")]
pub const fn run() {
    let x = u64::MAX;
    let y = x as f64;
}
