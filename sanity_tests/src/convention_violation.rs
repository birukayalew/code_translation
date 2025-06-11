#[expect(clippy::default_numeric_fallback, reason="reason")]
#[expect(clippy::single_call_fn, reason="reason")]
pub const fn run() {
    let _x = 0;
    let y = _x + 1; 
}
