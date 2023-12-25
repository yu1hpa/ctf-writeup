from pwn import *

HOST = "netcat-pwn.wanictf.org"
PORT = 9001
file = ""
context(os = 'linux', arch = 'amd64')
#context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
#io = process(file)
io = remote(HOST, PORT)

eq = io.recvuntil(b"=")
print(eq)
l = eq[-11:-8]
r = eq[-5:-2]
print(int(l))
print(int(r))
print(int(l) + int(r))
s = int(l) + int(r)
io.sendline(str(s))

io.interactive()
