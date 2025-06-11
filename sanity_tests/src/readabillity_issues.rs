#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::default_numeric_fallback, reason="Focus on important lints")]

fn readability_issues_example() {
    let array = [1, 2, 3, 4];
    let first = array[2..].iter().next();
}

pub const fn run() {
}
