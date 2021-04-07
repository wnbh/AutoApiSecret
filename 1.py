import os
import re
import random
import requests

REFRESH_TOKEN_FILE = '1.txt'
REDIRECT_URI = 'http://localhost:53682/'


def get_value(name):
    return re.findall(".+'(.+)'", os.getenv(name))[0]


def refresh_token(new_token=None):
    with open(REFRESH_TOKEN_FILE, mode='r+', encoding='utf-8') as f:
        if not new_token:
            return f.read()
        f.write(new_token)


def get_access_token():
    data = requests.post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token(),
            'client_id': get_value('CLIENT_ID'),
            'client_secret': get_value('CLIENT_SECRET'),
            'redirect_uri': REDIRECT_URI
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    ).json()

    refresh_token(data['refresh_token'])
    return data['access_token']


def invoke_api():
    apis = [
        'https://graph.microsoft.com/v1.0/users',
        'https://graph.microsoft.com/v1.0/groups',
        'https://graph.microsoft.com/v1.0/sites/root',
        'https://graph.microsoft.com/v1.0/sites/root/sites',
        'https://graph.microsoft.com/v1.0/sites/root/drives',
        'https://graph.microsoft.com/v1.0/sites/root/columns',
        'https://graph.microsoft.com/v1.0/me/',
        'https://graph.microsoft.com/v1.0/me/events',
        'https://graph.microsoft.com/v1.0/me/people',
        'https://graph.microsoft.com/v1.0/me/contacts',
        'https://graph.microsoft.com/v1.0/me/calendars',
        'https://graph.microsoft.com/v1.0/me/drive',
        'https://graph.microsoft.com/v1.0/me/drive/root',
        'https://graph.microsoft.com/v1.0/me/drive/root/children',
        'https://graph.microsoft.com/v1.0/me/drive/recent',
        'https://graph.microsoft.com/v1.0/me/drive/sharedWithMe',
        'https://graph.microsoft.com/v1.0/me/onenote/pages',
        'https://graph.microsoft.com/v1.0/me/onenote/sections',
        'https://graph.microsoft.com/v1.0/me/onenote/notebooks',
        'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
        'https://graph.microsoft.com/v1.0/me/mailFolders',
        'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
        'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        'https://graph.microsoft.com/v1.0/me/messages',
        "https://graph.microsoft.com/v1.0/me/messages?$filter=importance eq 'high'",
        'https://graph.microsoft.com/v1.0/me/messages?$search="hello world"',
        'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top',
    ]

    headers = {
        'Authorization': get_access_token(),
        'Content-Type': 'application/json'
    }

    for period in range(random.randint(10, 50)):
        print('========================================')
        random.shuffle(apis)
        for idx, api in enumerate(apis):
            try:
                if requests.get(api, headers=headers).status_code == 200:
                    print('{:>10s} | {:<30s}'.format(
                        f'周期 {period + 1}',
                        f'{api} 调用成功')
                    )
            except Exception:
                pass
        print('========================================')


if __name__ == '__main__':
    invoke_api()
