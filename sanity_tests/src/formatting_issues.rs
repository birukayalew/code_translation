#![expect(clippy::print_stdout, reason="Focus on important lints")]
#![expect(clippy::use_debug, reason="Focus on important lints")]
#![expect(clippy::uninlined_format_args, reason="Focus on important lints")]
#![expect(clippy::single_call_fn, reason="Focus on important lints")]
use std::path::Path;

pub fn run() {
    // Unnecessary debug formatting (certain characters can be escaped).
    let path = Path::new("...");
    println!("The path is {:?}", path);
}

