#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::min_ident_chars, reason="Focus on important lints")]
#![expect(clippy::absolute_paths, reason="Focus on important lints")]
#![expect(clippy::std_instead_of_core, reason="Focus on important lints")]
#![expect(clippy::undocumented_unsafe_blocks, reason="Focus on important lints")]
#![expect(clippy::separated_literal_suffix, reason="Focus on important lints")]
fn unsafe_transmute_example() {
    let x = 1_u8;

    // Unnecessary and unsafe transmute.
    let b: bool = unsafe { std::mem::transmute(x) };
}

pub const fn run() {
}
