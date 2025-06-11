#![expect(clippy::expl_impl_clone_on_copy, reason="Focus on important lints")]
#![expect(clippy::missing_trait_methods, reason="Focus on important lints")]
#![expect(clippy::implicit_return, reason="Focus on important lints")]
#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#[derive(Eq, PartialEq)]
struct Foo(u32);

impl Clone for Foo {
    fn clone(&self) -> Self {
        Self(self.0)
    }
}

impl Copy for Foo {}
pub const fn run() {
}
