# picopico

次の実行されてそうなコード片が見つかった。（`strings firmware.bin`）

```python
import storage
storage.disable_usb_drive()
import time
L=len
o=bytes
l=zip
import microcontroller
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
w=b"\x10\x53\x7f\x2b"
a=0x04
K=43
if microcontroller.nvm[0:L(w)]!=w:
 microcontroller.nvm[0:L(w)]=w
 O=microcontroller.nvm[a:a+K]
 h=microcontroller.nvm[a+K:a+K+K]
 F=o((kb^fb for kb,fb in l(O,h))).decode("ascii")
 S=Keyboard(usb_hid.devices)
 C=KeyboardLayoutUS(S)
 time.sleep(0.1)
 S.press(Keycode.WINDOWS,Keycode.R)
 time.sleep(0.1)
 S.release_all()
 time.sleep(1)
 C.write("cmd",delay=0.1)
 time.sleep(0.1)
 S.press(Keycode.ENTER)
 time.sleep(0.1)
 S.release_all()
 time.sleep(1)
 C.write(F,delay=0.1)
 time.sleep(0.1)
 S.press(Keycode.ENTER)
 time.sleep(0.1)
 S.release_all()
time.sleep(0xFFFFFFFF)
```

見やすくするために書き換えると次のようになる。
```python
# USBストレージを無効化
storage.disable_usb_drive()

CHECK_BYTES = b"\x10\x53\x7f\x2b"  # チェック用のバイト列
NVM_START = 0x04  # 非揮発性メモリの開始インデックス
DATA_LENGTH = 43  # 読み取るデータの長さ

if microcontroller.nvm[0:len(CHECK_BYTES)] != CHECK_BYTES:
    microcontroller.nvm[0:len(CHECK_BYTES)] = CHECK_BYTES
    data1 = microcontroller.nvm[NVM_START:NVM_START + DATA_LENGTH]
    data2 = microcontroller.nvm[NVM_START + DATA_LENGTH:NVM_START + DATA_LENGTH + DATA_LENGTH]
    decoded_command = bytes(kb ^ fb for kb, fb in zip(data1, data2)).decode("ascii")
...
    # デコードされたコマンドを実行
    keyboard_layout.write(decoded_command, delay=0.1)
    time.sleep(0.1)
```

`decoded_command`を復元するとフラグが得られそう。
`microcontroller.nvm`のデータがわからないといけないが、ファームウェアを全探索するとフラグが見つかった。

```
echo ACSC{349040c16c36fbba8c484b289e0dae6f}
```
