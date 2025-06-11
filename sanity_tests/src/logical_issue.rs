#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::default_numeric_fallback, reason="Focus on important lints")]

fn foo() -> i32 {
    println!("called foo");
    42
}


pub fn run() {
    if foo() == 1 {
        println!("One");
    } else if foo() == 1 {
        println!("Two");
    }
}
