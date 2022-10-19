# -*- coding: utf-8 -*-

from time import sleep
import requests
from Broadcast import Shout, Color
from bs4 import BeautifulSoup

default = Shout()


class VK:

    @default.announcement
    def __init__(self, token=None, group=None, api_version=5.101, waiting_time=10) -> None:
        self.token = token
        self.group = group
        self.API_version = api_version
        self.waiting_time = waiting_time

        self.session = requests.Session()

        self.url = "https://21.ru"
        self.key = 0
        self.ts = 0

        self.user_url = "https://21.ru"
        self.user_key = 0
        self.user_ts = 0

        if group:
            self.getConnection()
        else:
            self.user_Connection()

    @default.announcement
    def method(self, method, values=None):

        values = values.copy() if values else {}

        if 'v' not in values:
            values['v'] = self.API_version

        if self.token:
            values['access_token'] = self.token

        response = None
        i = 0
        while not response:
            try:
                response = self.session.post(
                    'https://api.vk.com/method/' + method,
                    values,
                )
            except Exception as e:
                print(Color.bold + "[CUSTOM] " + Color.red + Color.bold + str(e) + Color.default)
                sleep(5)
            i += 1
            if i > 10:
                response = {'error': {'error_code': "CUSTOM", 'error_msg': "Достигнут предел попыток."}}

        if response.ok:
            response = response.json()

        try:
            return response['response']
        except Exception:
            try:
                code = response['error']['error_code']
                if code != 10:
                    print(Color.bold + "[" + str(code) + "] " + Color.red + Color.bold + str(
                        response['error']['error_msg']) + Color.default)
                    print(values)
                else:
                    sleep(5)
                return response
            except Exception:
                return {"error": 1}

    @default.announcement
    def getConnection(self, update=True):

        response = self.method('groups.getLongPollServer', {'group_id': self.group})

        if "error" not in response:
            self.url = response['server']
            self.key = response['key']

            if update:
                self.ts = response['ts']

    @default.announcement
    def user_Connection(self, update=True):

        response = self.method('messages.getLongPollServer')

        if "error" not in response:
            self.user_url = response['server']
            self.user_key = response['key']

            if update:
                self.user_ts = response['ts']

    @default.announcement
    def getEvent(self):

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
        except Exception as e:
            print(e)

        if 'failed' not in response:
            self.ts = response['ts']

            return response['updates']

        elif response['failed'] == 1:
            self.ts = response['ts']

        elif response['failed'] == 2:
            self.getConnection(update=False)

        elif response['failed'] == 3:
            self.getConnection()

        return []

    @default.announcement
    def getBot(self):
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
            self.user_Connection(update=False)

        elif response['failed'] == 3:
            self.user_Connection()

        return []

    @default.announcement
    def download_photo(self, img_link, destination):
        p = requests.get(img_link)
        with open(destination, "wb") as out:
            out.write(p.content)
            out.close()

    @default.announcement
    def upload_photo(self, url, params):
        r = requests.post(url, files=params)
        r = r.json()
        photo = r.get('photo') or r.get('photos_list')
        params = {'server': r['server'], 'photo': photo, 'photos_list': photo, 'hash': r['hash']}
        return params

    @default.announcement
    def get_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
        page = self.session.get(url, headers=headers)
        i = 0
        while page.status_code != 200 and i < 10:
            page = self.session.get(url, headers=headers)
            i += 1
        if page.status_code == 200:
            return BeautifulSoup(page.text, "html.parser")
        return []


if __name__ == "__main__":

    obj = VK()
    while True:
        obj.getEvent()
