#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::default_numeric_fallback, reason="Focus on important lints")]
#![expect(clippy::min_ident_chars, reason="Focus on important lints")]
#![expect(clippy::integer_division_remainder_used, reason="Focus on important lints")]
#![expect(clippy::integer_division, reason="Focus on important lints")]
pub const fn run() {
    let a = 100;
    let b = 200;
    let midpoint = (a + b) / 2; 
}
