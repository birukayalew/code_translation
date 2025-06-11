#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::std_instead_of_core, reason="Focus on important lints")]
#![expect(clippy::arithmetic_side_effects, reason="Focus on important lints")]

use std::time::{Duration, Instant};

pub fn run() {
    // Unchecked subtraction could cause underflow on certain platforms.
    let time_passed = Instant::now() - Duration::from_secs(5);
}
