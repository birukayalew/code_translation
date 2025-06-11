#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::uninlined_format_args, reason="Focus on important lints")]
pub fn run() {
    let text = "line1\nline2\nline3\n";
    for line in text.trim().split('\n') {
        println!("{}", line);
    }
}



