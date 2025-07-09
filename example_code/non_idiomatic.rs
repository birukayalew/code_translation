use std::ptr;

struct MyBuffer {
    ptr: *mut u8,
    len: usize,
}

impl MyBuffer {
    fn new(size: usize) -> MyBuffer {
        let raw_ptr: *mut u8 = unsafe { libc::malloc(size) as *mut u8 };
        MyBuffer {
            ptr: raw_ptr,
            len: size,
        }
    }

    fn clear(&mut self) {
        unsafe { ptr::write_bytes(self.ptr, 0, self.len); }
    }
}

fn main() {
    let mut buf = MyBuffer::new(100);
    buf.clear();
}
