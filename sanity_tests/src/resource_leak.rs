#![expect(clippy::single_call_fn, reason="Focus on important lints")]
#![expect(clippy::expect_used, reason="Focus on important lints")]
use std::process::Command;

fn resource_leak_example() {
    // Not calling `.wait()` — this can leak OS resources like process IDs.
    let _child = Command::new("ls")
        .spawn()
        .expect("failed to execute child");
}

fn proper_resource_handling_example() {
    // Properly waits for the child process to finish.
    let mut child = Command::new("ls")
        .spawn()
        .expect("failed to execute child");

    child.wait().expect("failed to wait on child");
}

pub fn run() {
    resource_leak_example();
    proper_resource_handling_example();
}
