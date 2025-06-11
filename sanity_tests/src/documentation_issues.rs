#![expect(clippy::single_call_fn, reason="Focus on important lints")]
/// - This is the first item in a list
///        and this line is overindented
///
/// This documentation comment has formatting issues that Clippy can detect.
pub const fn run() {
}
