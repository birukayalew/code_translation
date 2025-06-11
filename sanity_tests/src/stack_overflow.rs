#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::print_stdout, reason="Focus on important lints")]
#![expect(clippy::min_ident_chars, reason="Focus on important lints")]
#![expect(clippy::unseparated_literal_suffix, reason="Focus on important lints")]
#![expect(clippy::large_stack_frames, reason="Focus on important lints")]
// Large local arrays may cause stack overflow.
pub fn run() {
    let a = [0u32; 1_000_000];
    println!("{}", a[0]);
}
