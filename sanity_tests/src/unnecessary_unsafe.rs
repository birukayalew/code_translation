#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::undocumented_unsafe_blocks, reason="Focus on important lints")]
#![expect(clippy::std_instead_of_core, reason="Focus on important lints")]
use std::num::NonZeroUsize;

const fn unnecessary_unsafe_example() {

    // This uses unsafe unnecessarily.
    const PLAYERS_UNSAFE: NonZeroUsize = unsafe { NonZeroUsize::new_unchecked(3) };
}

pub const fn run() {
}

// code to try
// unsafe fn foo(a: i32) {

//     let b: *const i32 = &a as *const i32;

//     unsafe { *b}

// }