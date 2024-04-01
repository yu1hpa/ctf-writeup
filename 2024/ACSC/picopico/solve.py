from tqdm import tqdm

f = open("./firmware.bin", "rb").read()

K = 43

for i in tqdm(range(len(f))):
    enc = f[i:i+K]
    key = f[i+K:i+K+K]
    cmd = bytes(e ^ k for e, k in zip(enc, key))
    if b"ACSC" in cmd:
        print(cmd)

# ACSC{349040c16c36fbba8c484b289e0dae6f}
