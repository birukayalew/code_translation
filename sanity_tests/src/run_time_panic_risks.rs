#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::shadow_reuse, reason="Focus on important lints")]
#![expect(clippy::print_stdout, reason="Focus on important lints")]
#![expect(clippy::indexing_slicing, reason="Focus on important lints")]
#![expect(clippy::uninlined_format_args, reason="Focus on important lints")]
#![expect(clippy::shadow_unrelated, reason="Focus on important lints")]


pub fn run() {
    // Accessing slice values using indices can lead to panics.
    let slice: Option<&[u32]> = Some(&[1, 2, 3]);
    if let Some(slice) = slice {
        println!("Risky access: {}", slice[0]);
    }

    // Preferred: Use pattern matching to safely access elements.
    let slice: Option<&[u32]> = Some(&[1, 2, 3]);
    if let Some(&[first, ..]) = slice {
        println!("Safe access: {}", first);
    }
}
