#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::shadow_unrelated, reason="Focus on important lints")]
#![expect(clippy::undocumented_unsafe_blocks, reason="Focus on important lints")]
#![expect(clippy::as_conversions, reason="Focus on important lints")]
#![expect(clippy::borrow_as_ptr, reason="Focus on important lints")]
#![expect(clippy::min_ident_chars, reason="Focus on important lints")]
#![expect(clippy::absolute_paths, reason="Focus on important lints")]
#![expect(clippy::unseparated_literal_suffix, reason="Focus on important lints")]

unsafe fn pointer_aliasing_example(x: &[*mut u32], y: &[*mut u32]) {
    for (&x, &y) in x.iter().zip(y) {
        // This causes aliasing: mutable references to potentially overlapping memory.
        core::mem::swap(&mut *x, &mut *y);
    }
}

pub fn run() {
    let mut a = 1u32;
    let mut b = 2u32;

    let x = vec![&mut a as *mut u32];
    let y = vec![&mut b as *mut u32];

    unsafe {
        pointer_aliasing_example(&x, &y);
    }
}
