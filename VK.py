# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup

from Broadcast import Shout, Color


class VK:

    def __init__(self, token=None, group=None, api_version=5.101, waiting_time=10):
        self.token = token
        self.group = group
        self.API_version = api_version
        self.waiting_time = waiting_time

        self.session = requests.Session()

        self.url = "https://21.ru" if group else None
        self.key = 0 if group else None
        self.ts = 0 if group else None

        self.user_url = "https://21.ru"
        self.user_key = 0
        self.user_ts = 0

        if group:
            self.get_long_poll_server()
        else:
            self.get_user_long_poll_server()

    def method(self, method_name, values=None):
        values = values.copy() if values else {}

        values.setdefault('v', self.API_version)

        if self.token:
            values['access_token'] = self.token

        response = None

        for i in range(11):
            try:
                response = self.session.post(
                    f'https://api.vk.com/method/{method_name}', json=values
                )
            except requests.exceptions.RequestException as e:
                print(f"[CUSTOM] {Color.red}[{i}] {e}{Color.default}")
                time.sleep(5)
                continue
            break

        if response.ok:
            response = response.json()

        if 'response' in response:
            return response['response']

        if 'error' in response:
            error_code = response['error']['error_code']
            if error_code != 10:
                print(
                    f"{Color.bold}[{error_code}] {Color.red}{response['error']['error_msg']}{Color.default}")
                print(values)

        return response

    def get_long_poll_server(self, update=True):
        response = self.method('groups.getLongPollServer', {'group_id': self.group})

        if "error" not in response:
            self.url = response['server']
            self.key = response['key']

            if update:
                self.ts = response['ts']

    def get_user_long_poll_server(self, update=True):
        response = self.method('messages.getLongPollServer')

        if "error" not in response:
            self.user_url = response['server']
            self.user_key = response['key']

            if update:
                self.user_ts = response['ts']

    def get_event(self):
        if not self.group:
            return []

        values = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.waiting_time,
        }

        response = {'failed': 3}

        try:
            response = self.session.get(
                self.url,
                params=values,
                timeout=self.waiting_time + 10
            ).json()
        except requests.exceptions.RequestException as e:
            print(f"[CUSTOM] {Color.red}{e}{Color.default}")

        if 'failed' not in response:
            self.ts = response['ts']
            return response['updates']

        elif response['failed'] == 1:
            self.ts = response['ts']

        elif response['failed'] == 2:
            self.get_long_poll_server(update=False)

        elif response['failed'] == 3:
            self.get_long_poll_server()

        return []

    def get_bot(self):
        values = {
            'act': 'a_check',
            'key': self.user_key,
            'ts': self.user_ts,
            'wait': self.waiting_time,
        }
        response = {'failed': 3}

        try:
            response = self.session.get(
                f"http://{self.user_url}",
                params=values,
                timeout=self.waiting_time + 10
            ).json()
        except Exception as e:
            print(e)

        if 'failed' not in response:
            self.user_ts = response['ts']

            return response['updates']

        elif response['failed'] == 1:
            self.user_ts = response['ts']

        elif response['failed'] == 2:
            self.get_user_long_poll_server(update=False)

        elif response['failed'] == 3:
            self.get_user_long_poll_server()

        return []

    def download_photo(self, img_link, destination):
        p = requests.get(img_link)
        with open(destination, "wb") as out:
            out.write(p.content)

    def upload_photo(self, url, params):
        r = requests.post(url, files=params)
        r = r.json()
        photo = r.get('photo') or r.get('photos_list') or None
        if not photo:
            return None

        return {'server': r['server'], 'photo': photo, 'hash': r['hash']}

    def get_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
        page = self.session.get(url, headers=headers)

        for i in range(10):
            if page.status_code == 200:
                break
            page = self.session.get(url, headers=headers)

        if page.status_code != 200:
            return []

        return BeautifulSoup(page.text, "html.parser")


if __name__ == "__main__":
    obj = VK()
    while True:
        obj.get_event()
