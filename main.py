import requests
import json

from DONTSHARE import *


# link = "https://raw.githubusercontent.com/BlueHephaestus/mooncoin/refs/heads/main/000.png?token=GHSAT0AAAAAACVFSDN4VNEJCFC3KKPHGD62ZX5UC2Q"

# link = "https://github.com/BlueHephaestus/mooncoin/blob/main/000.png?raw=true"
link = "https://raw.githubusercontent.com/BlueHephaestus/mooncoin/refs/heads/main/000.png"
def update_token(token_addr, icon_fname, banner_fname, desc):
    url = f"https://ms.dexscreener.com/tokens/v1/solana/{token_addr}"

    payload = {
        'chainId': 'solana',
        'tokenAddress': '5fQEuytDt21sotZeekRyYGgK1oGZVdmF9yAHfSq4s1hQ',
        'description': "",
        'signature': SIGNATURE,
        'links': '[]',
    }
    # 'icon': link,
    files = []
    # files = [
    #     ('icon', ('2.png', open('2.png', 'rb'), 'image/png')),
    # ]
    # ('banner', ('2.png', open('2.png', 'rb'), 'image/png'))

    # files = [
    #     ('icon', (link, open('test.php.png','rb'), 'image/png')),
    # ]
    # files = {
    #     'icon': {"id": "myowntextfuckyouidowhatiwant"},
    # }
    # files = {
    #     'icon': link.encode("utf-8")
    # }
    # files.append(('icon', (icon_fname, link, 'image/*')))
    # files.append(('icon', (icon_fname, open(icon_fname, 'rb'), 'image/png')))
    files.append(('icon', (icon_fname, open("2.png", 'rb'), 'image/png')))
    "*.jpeg, *.jpg, *.png, *.webp, *.gif"
    #
    # if banner_fname is not None:
    #     files.append(('banner', (banner_fname, open(banner_fname, 'rb'), 'image/png')))

    headers = {
        'authority': 'ms.dexscreener.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'origin': 'https://dexscreener.com',
        'referer': 'https://dexscreener.com/',
        'sec-ch-ua': '"Not(A:Brand";v="24", "Chromium";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.content)
    if len(response.content):
        print(response.json())
    print(response.status_code)

with open("lookup.json", "r") as f:
    lookup = json.load(f)
update_token("5fQEuytDt21sotZeekRyYGgK1oGZVdmF9yAHfSq4s1hQ", "2.png", "2.png", "test desc")
