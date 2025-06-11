#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::let_underscore_untyped, reason="Focus on important lints")]
#![expect(clippy::as_conversions, reason="Focus on important lints")]
#![expect(clippy::missing_const_for_fn, reason="Focus on important lints")]
#![expect(clippy::fn_to_numeric_cast, reason="Focus on important lints")]
// This cast is invalid: casting a function directly to i64 can cause truncation.
// fn fun() -> i32 {
//     1
// }

pub fn run() {
    let ptr: *const u32 = &42_u32;
    let mut_ptr: *mut u32 = &mut 42_u32;
    let _ = ptr as *const i32;
}
