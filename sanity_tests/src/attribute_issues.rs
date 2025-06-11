// #![allow(clippy::should_panic_without_expect )]
// #![expect(clippy::single_call_fn, reason="Focus on important lints")]
struct RarelyUseful {
    some_field: u32,
    last: [u32; 0], // ⚠️ Triggers the lint
}

pub const fn run() {
    let _ = RarelyUseful {
        some_field: 42,
        last: [],
    };
}