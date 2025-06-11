#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::unnecessary_literal_unwrap, reason="Focus on important lints")]
#![expect(clippy::default_numeric_fallback, reason="Focus on important lints")]
pub fn run() {
    let x: Result<i32, &str> = Ok(3);
    match x {
        Ok(_) => println!("ok"),
        Err(_) => panic!("err"),
    }
}
