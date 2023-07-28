# authme - InterKosenCTF2020

`Username`と`Password`をBOFとROPでリークしてログインすることが目的。

## 解放

まず`fgets()`関数でオーバーフローが起きることがわかります。
`exit()`が呼び出されない処理を探すと、
`fgets()`の返り値が`NULL`のときに`return`されまず。

```c
  printf("Username: ");
  if (fgets(buf, 0x40, stdin) == NULL) return 1;
  if (strcmp(buf, username) != 0) auth = 0;

  printf("Password: ");
  if (fgets(buf, 0x40, stdin) == NULL) return 1;
  if (strcmp(buf, password) != 0) auth = 0;
```

pwntoolsでは`shutdown()`を使って出力方向を閉じると、`EOF`が送られます。

