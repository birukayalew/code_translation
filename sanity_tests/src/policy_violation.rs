#![allow(clippy::missing_docs_in_private_items, reason="To focus only on macro violation")]
#![allow(clippy::print_stdout, reason="To focus only on macro violation")]
#![allow(clippy::single_call_fn, reason="To focus only on macro violation")]
#![allow(clippy::default_numeric_fallback, reason="To focus only on macro violation")]
#![allow(clippy::dbg_macro, reason="To focus only on macro violation")]


fn main() {
    let x = 42;
    dbg!(x);
}

pub fn run(){
    main();
}
