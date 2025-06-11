#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::min_ident_chars, reason="Focus on important lints")]
#![expect(clippy::implicit_return, reason="Focus on important lints")]

fn foo(values: &[u8]) -> bool {
    values.iter().any(|&v| v == 10)
}

pub const fn run() {
}
