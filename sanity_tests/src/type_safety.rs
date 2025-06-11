#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::integer_division_remainder_used, reason="Focus on important lints")]
#![expect(clippy::integer_division, reason="Focus on important lints")]
#![expect(clippy::arithmetic_side_effects, reason="Focus on important lints")]
#![expect(clippy::std_instead_of_core, reason="Focus on important lints")]
#![warn(clippy::non_zero_suggestions)]
use std::num::{NonZeroU32, NonZeroU64};

fn type_safety_example(x: u64, y: NonZeroU32) {
    // Bad: Converting NonZeroU32 to u64 unnecessarily.
    let r1 = x / u64::from(y.get());
}

pub const fn run() {

}
