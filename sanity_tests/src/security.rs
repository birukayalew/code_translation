#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::print_stdout, reason="Focus on important lints")]
#![expect(clippy::uninlined_format_args, reason="Focus on important lints")]
#![expect(clippy::default_numeric_fallback, reason="Focus on important lints")]
#![expect(clippy::integer_division, reason="Focus on important lints")]
#[warn(clippy::integer_division_remainder_used)]
pub fn run() {
    // In cryptographic contexts, division can introduce timing side-channel vulnerabilities.
    let my_div = 10 / 2;

    // Consider using bit shifts for constant-time operations.
    let safer_div = 10 >> 1;

    println!("Insecure division: {}", my_div);
    println!("Safer shift: {}", safer_div);
}
