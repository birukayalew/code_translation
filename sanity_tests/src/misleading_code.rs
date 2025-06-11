#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::missing_const_for_fn, reason="Focus on important lints")]

fn as_u64(x: u8) -> u64 {
    x as u64
}

pub const fn run() {
}