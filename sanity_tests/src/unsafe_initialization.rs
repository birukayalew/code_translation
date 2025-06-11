#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::std_instead_of_core, reason="Focus on important lints")]
#![expect(clippy::undocumented_unsafe_blocks, reason="Focus on important lints")]
use std::mem::MaybeUninit;

const fn clippy_example_unsafe_initialization() {
    // Undefined behavior: reading uninitialized memory.
    let _: usize = unsafe { MaybeUninit::uninit().assume_init() };
}
    
pub const fn run() {
}
