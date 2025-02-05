# -*- coding: UTF-8 -*-
"""
先注册 azure 应用，确保应用有以下权限:
Files.Read.All、Files.ReadWrite.All
Sites.Read.All、Sites.ReadWrite.All
User.Read.All、User.ReadWrite.All
Directory.Read.All、Directory.ReadWrite.All
Mail.Read、Mail.ReadWrite、MailboxSettings.Read
MailboxSettings.ReadWrite
注册后一定要再点代表 xxx 授予管理员同意，否则 outlook api 无法调用
"""
import argparse
import json
import sys
import time
import random
import requests as req


def get_access_token(id, secret, refresh_token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': id,
        'client_secret': secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    html = req.post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        data=data,
        headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    with open(path, 'w+') as f:
        f.write(refresh_token)
    return access_token


def main():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()
    global count
    localtime = time.asctime(time.localtime(time.time()))
    access_token = get_access_token(id, secret, refresh_token)
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    apis = [
        'https://graph.microsoft.com/v1.0/me/drive/root',
        'https://graph.microsoft.com/v1.0/me/drive',
        'https://graph.microsoft.com/v1.0/drive/root',
        'https://graph.microsoft.com/v1.0/me/messages',
        'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
        'https://graph.microsoft.com/v1.0/me/drive/root/children',
        'https://graph.microsoft.com/v1.0/me/mailFolders',
        'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
    ]
    a = random.randint(1,9)
    try:
        r = req.get(url=apis[a], headers=headers)
            print('调用成功，apis[a])
    else:
        print('调用失败，apis[a])
    except:
        print('pass')
        pass
    print('此次运行结束时间为：', localtime)


if __name__ == "__main__":
    path = sys.path[0] + r'/refresh_token.txt'
    count = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', dest='id')
    parser.add_argument('-s', '--secret', dest='secret')
    args = parser.parse_args()
    id = args.id
    secret = args.secret
    for _ in range(3):
        main()
