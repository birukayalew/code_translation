#![warn(clippy::not_unsafe_ptr_arg_deref)]
#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::print_stdout, reason="Focus on important lints")]
#![expect(clippy::undocumented_unsafe_blocks, reason="Focus on important lints")]
pub fn foo(x: *const u8) {
    println!("{}", unsafe { *x });
}

pub fn run() {
    let value: u8 = 99;
    let ptr: *const u8 = &value;
    foo(ptr);
}

// Lint is not being triggered for some reason.

