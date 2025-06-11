#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::let_underscore_must_use, reason="Focus on important lints")]
#![expect(clippy::unimplemented, reason="Focus on important lints")]
#![expect(clippy::let_underscore_untyped, reason="Focus on important lints")]


#[must_use]
fn double_must_use() -> Result<(), ()> {
    // Redundant attribute: `#[must_use]` is unnecessary here.
    unimplemented!();
}

// Preferred: remove #[must_use] if not needed.

pub fn run() {
    let _ = double_must_use();
}
