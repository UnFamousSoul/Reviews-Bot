# -*- coding: utf-8 -*-

from datetime import datetime
from random import randint
from threading import Thread
from time import sleep, time
import pyautogui

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from VK import VK
from Database import DB
from Broadcast import Color, Shout

data = DB()
default = Shout()


class Instrument:

    def __init__(self) -> None:
        self.vk = VK(data.token)
        self.secret = [
            VK("Второй аккаунт"),
            VK("Третий аккаунт"),
            VK("Четвёртый аккаунт"),
            VK("Мой токен"),
            self.vk
        ]
        self.index = 0

    @default.announcement
    def plus_secret(self):
        self.index += 1
        if self.index >= len(self.secret):
            self.index = 0

    @default.announcement
    def announce(self, user=None, post_id=None, text=None, key="comment"):
        date = datetime.now().strftime("%d.%m %H:%M:%S")
        user_info = self.vk.method('users.get', {'user_ids': user})[0]
        first_name = user_info.get('first_name')
        last_name = user_info.get('last_name')
        if key == "comment":
            print(
                f"{Color.blue}{date} {Color.default}{Color.bold}{post_id} ({user}) "
                f"{first_name} {last_name}:{Color.blue} {text}{Color.default}")
        if key == "approved":
            print(
                f"{Color.blue}{date} {Color.default}{Color.bold}({user}) "
                f"{first_name} {last_name}:{Color.blue} Добавлен в сообщество.{Color.default}")

    @default.announcement
    def func(self, array, text):

        for i in range(len(array)):
            if array[i] in text:
                return True
        return False

    @default.announcement
    def time_transfer(self, seconds):
        days = int(seconds / 86400)
        hours = int(seconds / 3600) - 24 * days
        minutes = int(seconds / 60) - 60 * hours - 60 * 24 * days
        seconds = seconds - 60 * minutes - 60 * 60 * hours - 60 * 60 * 24 * days

        reply = ""
        if days > 0:
            reply += f"{days} дней "
        if hours > 0:
            reply += f"{hours} часов "
        if minutes > 0:
            reply += f"{minutes} минут "
        if seconds > 0:
            reply += f"{seconds} секунд"

        return reply

    @default.announcement
    def base_fix(self, text):
        response = ""
        for i in range(len(text)):
            symbol = text[i]
            if symbol == "\"":
                symbol = "\"\""
            if symbol == "'":
                symbol = "''"
            response += symbol
        return response

    @default.announcement
    def shorter(self, text):
        short_text = text[:30]
        if len(text) > 30:
            short_text += "..."
        return short_text

    @default.announcement
    def message(self, peer_id, text=None, attachment=None, group=None):
        print(
            f"{Color.bold}[*] {Color.light_blue}{Color.bold} Отправлено сообщение {Color.default}\"{text}\""
            f" с вложением \"{attachment}\"{Color.blue}{Color.bold} ({peer_id}) {Color.default}")
        self.vk.method('messages.send', {
            'peer_id': peer_id,
            'message': text,
            'random_id': randint(0, 100000),
            'attachment': attachment,
            'group_id': group
        })

    @default.announcement
    def choosing(self, sizes_array):
        max_height = 0
        response = {"url": "0"}
        for i in range(len(sizes_array)):
            body = sizes_array[i]
            if body["height"] > max_height:
                max_height = body["height"]
                response = body
        return response["url"]

    @default.announcement
    def save_photos(self, attachments, post_id):
        for i in range(len(attachments)):
            data.check_dir(f"{data.directory}databases/reviews/{post_id}")
            attachment_type = attachments[i]["type"]
            print(attachments[i][attachment_type])
            attachment_body = attachments[i][attachment_type]["sizes"]
            url = self.choosing(attachment_body)
            if url != "0":
                ins.vk.download_photo(
                    url,
                    f"{data.directory}databases/reviews/{post_id}/{i + 1}.jpg"
                )

    @default.announcement
    def upload_photo(self, target, number, method_upload="photos.getMessagesUploadServer", param="peer_id",
                     method_save="photos.saveMessagesPhoto"):

        directory = f"{data.directory}databases\\reviews\\{number}"
        attachments = ""

        vk_info = ins.vk.method(method_upload, {param: target})
        data_response = data.check_photos(directory)
        for i in range(data_response):
            vk_response = ins.vk.upload_photo(vk_info["upload_url"], {"photo": open(f"{directory}\\{i + 1}.jpg", "rb")})

            photo = ins.vk.method(method_save, vk_response)[0]
            photo_owner = photo["owner_id"]
            photo_id = photo["id"]
            attachments += f"photo{photo_owner}_{photo_id},"
        return attachments.removesuffix(",")

    @default.announcement
    def delete_quote(self, text):
        response = ""
        for i in range(len(text)):
            if text[i] not in ["\"", "'"]:
                response += text[i]
        return response

    @default.announcement
    def black_list(self, text):

        data_response = data.get_all(f"SELECT * FROM blacklisted")

        for i in range(len(data_response)):
            if data_response[i][0] in text:
                return True
        return False


ins = Instrument()


class Install(Thread):

    def __init__(self, user, url) -> None:
        Thread.__init__(self)
        self.width, self.height = (None, None)
        self.driver = None
        self.timeout = None

        self.user = user
        self.url = str(url)
        self.destination = f"{data.directory}databases\\temp\\"

    @default.announcement
    def run_driver(self):
        self.width, self.height = pyautogui.size()
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
            "select_file_dialogs.allowed": False,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "download_restrictions": 0,
            "savefile.default_directory": f"{self.destination}",
            "directory_upgrade": True,
            "download.prompt_for_download": False})
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_extension(f"{data.directory}\\vpn.crx")
        self.driver = Chrome(options=options)
        self.timeout = 2

        self.driver.get("chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html")
        button = self.get_element((By.ID, "ConnectionButton"))
        sleep(8)

        hadlers = self.driver.window_handles
        while len(hadlers) > 1:
            self.driver.switch_to.window(hadlers[1])
            hadlers.pop(1)
            self.driver.close()
        self.driver.switch_to.window(hadlers[0])

        button.click()
        self.driver.maximize_window()

    @default.announcement
    def get_element(self, element, times=0, located=None):
        response = None
        if not located:
            located = self.driver
        i = 0
        while not response and (i <= times or times == 0):
            try:
                response = WebDriverWait(located, self.timeout).until(ec.presence_of_element_located(element))
            except Exception as e:
                print(e)
                self.driver.refresh()
            i += 1
        return response

    @default.announcement
    def is_registered(self):

        if self.driver.title == "MangaLib | Регистрация":
            vk_info = {
                "login": "Логин",
                "password": "Пароль"
            }

            reg_button = self.get_element((By.CLASS_NAME, "social-sign_vk"))
            reg_button.click()

            email_field = self.get_element((By.NAME, "email"))
            email_field.send_keys(vk_info["login"])

            pass_field = self.get_element((By.NAME, "pass"))
            pass_field.send_keys(vk_info["password"])

            login_button = self.get_element((By.ID, "install_allow"))
            login_button.click()

            sleep(4)

            self.purse_hentlib()
            return False
        return True

    @default.announcement
    def check_hentlib(self):
        if self.driver.title.endswith("Хентай Манга онлайн."):
            return True
        return False

    @default.announcement
    def click_button(self, button):
        try:
            button.click()
            return True
        except Exception as e:
            print(e)
            return False

    @default.announcement
    def im_old_enough(self):
        checkbox = self.get_element((By.CLASS_NAME, "control.control_checkbox"), 5)
        checkbox.click()
        alarm_buttons = self.get_element((By.CLASS_NAME, "button.button_md.button_orange.reader-caution-continue"), 5)
        alarm_buttons.click()

    @default.announcement
    def purse_hentlib(self):
        self.driver.get(self.url)
        name = self.get_element((By.CLASS_NAME, "media-name__main"))
        alt_name = self.get_element((By.CLASS_NAME, "media-name__alt"))
        final_name = f"{name.text} ({alt_name.text})"

        button = self.get_element((By.LINK_TEXT, "Начать читать"))
        button.click()

        if self.is_registered():
            self.im_old_enough()
            ins.message(self.user, f"─────────────────────\nИдёт загрузка манги \"{final_name}\".")

            count = 0
            while "Чтение" in self.driver.title:

                pic = self.driver.find_elements(By.CLASS_NAME, "reader-view__wrap")

                for i in range(len(pic)):

                    page = self.get_element((By.TAG_NAME, "img"), located=pic[i])

                    _checker = data.check_format(count + 1)
                    clicker = 0
                    while not _checker:
                        pic = self.driver.find_elements(By.CLASS_NAME, "reader-view__wrap")
                        page = self.get_element((By.TAG_NAME, "img"), located=pic[i])
                        sleep(0.5)
                        pyautogui.rightClick(self.width / 2, self.height / 2)
                        pyautogui.moveRel(128, 40, duration=0.1)
                        pyautogui.leftClick()
                        sleep(2)
                        pyautogui.typewrite(list(f"{count + 1}") + ['enter'])
                        sleep(0.5)

                        timer = data.check_format(count + 1)
                        if timer != "jpg":
                            self.driver.refresh()

                        clicker += 1
                        if clicker > 10:
                            ins.message(self.user, f"─────────────────────\nНе удалось получить страницы манги.")
                            return 0

                        _checker = data.check_format(count + 1)
                        sleep(1.5)

                    is_click = self.click_button(page)
                    while not is_click:
                        is_click = self.click_button(page)

                    count += 1

            response = ins.vk.method("photos.createAlbum",
                                     {"title": final_name, "group_id": data.fullhent, "upload_by_admins_only": 1})
            i = 0
            while "error" in response and i < 10:
                response = ins.vk.method("photos.createAlbum",
                                         {"title": final_name, "group_id": data.fullhent, "upload_by_admins_only": 1})
                i += 1

            ins.message(self.user, f"─────────────────────\nЗагрузка в альбом страниц манги.")

            self.upload_photo(response["id"], count)
            data.delete_temp(count)
            ins.message(self.user, f"─────────────────────\nЗагрузка манги \"{final_name}\" завершена.")

    @default.announcement
    def quote_replacer(self, text):
        response = ""
        for i in list(text):
            if i == "'":
                i = '"'
            response += i
        return response

    @default.announcement
    def check_henchan(self, soup):
        border = soup.findAll('a', class_='bordr')
        for i in border:
            if i.get("title") == "О проекте Хентай-тян!":
                return True

    @default.announcement
    def get_access_henchan(self, url):
        if "?" in url:
            array = url.split("?")
            return array[0] + "?development_access=true&" + array[1]
        return url

    @default.announcement
    def upload_photo(self, album_id, length):

        vk_info = ins.vk.method("photos.getUploadServer", {"album_id": album_id, "group_id": data.fullhent})
        for i in range(length):
            print(i)
            vk_response = ins.vk.upload_photo(vk_info["upload_url"],
                                              {"photo": open(f"{self.destination}{i + 1}.jpg", "rb")})

            param = {"album_id": album_id, "group_id": data.fullhent}
            param.update(vk_response)
            ins.vk.method("photos.save", param)

    @default.announcement
    def purse_henchan(self, page):
        name = page.findAll('a', class_='title_top_a')
        domain = self.url.removeprefix("https://").removeprefix("http://").split("/")[0]
        hentai_url = "https://" + domain + page.findAll('p', class_='extra_off')[2].a.get("href") + "#page=1"
        hentai_url = self.get_access_henchan(hentai_url)

        _soup = ins.vk.get_page(hentai_url)

        temp = _soup.findAll('script')[2]
        temp = str(temp).split('var data = ')[1]
        temp = str(temp).split('createGallery(data)')[0]
        temp = self.quote_replacer(temp)

        result = data.get_dict(temp)['fullimg']
        name = name[0].text
        length = len(result)

        ins.message(self.user, f"─────────────────────\nИдёт загрузка манги \"{name}\".")

        for i in range(length):
            thread = Thread(target=ins.vk.download_photo, args=(result[i], f"{self.destination}{i + 1}.jpg"))
            thread.start()

        response = ins.vk.method("photos.createAlbum",
                                 {"title": name, "group_id": data.fullhent, "upload_by_admins_only": 1})
        i = 0
        while "error" in response and i < 10:
            response = ins.vk.method("photos.createAlbum",
                                     {"title": name, "group_id": data.fullhent, "upload_by_admins_only": 1})
            i += 1

        ins.message(self.user, f"─────────────────────\nЗагрузка в альбом страниц манги.")

        self.upload_photo(response["id"], length)
        data.delete_temp(length)
        ins.message(self.user, f"─────────────────────\nЗагрузка манги \"{name}\" завершена.")

    @default.announcement
    def run(self):
        page = ins.vk.get_page(self.url)
        ins.message(self.user, f"─────────────────────\nПолучена информация о странице.")

        if page:
            if self.check_henchan(page):
                self.purse_henchan(page)
            else:
                ins.message(self.user, f"─────────────────────\nСтраница не прошла проверку шаблонов.")
        else:
            self.run_driver()
            self.driver.get(self.url)
            if self.check_hentlib():
                self.purse_hentlib()
            else:
                ins.message(self.user, f"─────────────────────\nНе удалось загрузить страницу {self.url}.")
            self.driver.quit()


class HentReview(Thread):

    def __init__(self) -> None:
        Thread.__init__(self)
        self.vk = VK(data.token, data.hentreview)

        self.lenths = [
            len(data.firstwords) - 1,
            len(data.mainwords) - 1,
            len(data.links) - 1
        ]
        self.index = [
            randint(0, self.lenths[0]),
            randint(0, self.lenths[1]),
            randint(0, self.lenths[2])
        ]

    @default.announcement
    def checker(self, post_id):

        post = f"-{data.hentreview}_{post_id}"
        response = ins.secret[ins.index].method('wall.getById', {'posts': post})
        while 'error' in response:
            ins.plus_secret()
            response = ins.secret[ins.index].method('wall.getById', {'posts': post})

        if len(response) != 0:

            response = response[0]
            text = response["text"]

            short_text = ins.shorter(text)

            if ins.func(data.review_triggers, text.lower()):

                if response["post_type"] == "post":

                    post_date = response["date"]
                    author = response.get("created_by") or 0

                    if post_date + data.seconds >= int(time()):

                        data_response = data.get_one(f"SELECT * FROM statistic WHERE id = {post_id}")

                        if not data_response:
                            data.save(f"INSERT INTO statistic VALUES ({post_id}, {post_date}, {author})")
                            print(
                                f"{Color.bold}[*] {Color.blue}{Color.bold} Добавлена запись в очередь на статистику "
                                f"{Color.default}\"{short_text}\"{Color.blue}{Color.bold} ({post}) {Color.default}"
                                "" + ins.time_transfer(data.seconds + (post_date - int(time()))))

                    data_response = data.get_one(f"SELECT * FROM reviews WHERE id = {post_id}")

                    if not data_response:
                        if "attachments" in response:
                            ins.save_photos(response["attachments"], post_id)
                        text = ins.base_fix(text)
                        data.save(f"INSERT INTO reviews VALUES ({post_id}, \"{text}\", {author}, \"Пусто\", 0)")
                        print(
                            f"{Color.bold}[*] {Color.blue}{Color.bold} Добавлена запись в базу данных {Color.default}"
                            f"\"{short_text}\"{Color.blue}{Color.bold} ({post}) {Color.default}")

                        return True

    @default.announcement
    def walker(self, max_number, min_number=0):
        if min_number >= 10:
            min_number -= 10
        print(f"{Color.bold}[*] Идёт проверка записей Hentreview... {Color.default}")
        for i in range(min_number, max_number + 1):
            difference = max_number - i
            print(f"{Color.blue}{Color.bold}{difference} ({i}){Color.default}")
            thread = Thread(target=self.checker, args=(i,))
            thread.start()
            sleep(0.10)

    @default.announcement
    def update(self, force_zero=False):

        response = ins.secret[ins.index].method("wall.get", {'owner_id': -1 * data.hentreview, 'count': 1})
        while 'error' in response:
            ins.plus_secret()
            response = ins.secret[ins.index].method("wall.get", {'owner_id': -1 * data.hentreview, 'count': 1})

        if "items" in response:
            min_number = 0
            if not force_zero:
                base_response = data.get_one(f"SELECT * FROM reviews ORDER BY id DESC")
                if base_response:
                    min_number = base_response[0]
            self.walker(response["items"][0]["id"], min_number)

    @default.announcement
    def special_random(self):

        for i in range(len(self.index)):

            self.index[i] += 1
            if self.index[i] >= self.lenths[i]:
                self.index[i] = 0

    @default.announcement
    def add_link(self, text, link):

        if "[LINK]" in text:
            array = text.split("[LINK]")
            first_part = array[0]
            second_part = array[1]
            return f"{first_part} {link} {second_part}"
        return f"{text} {link}"

    @default.announcement
    def generate_comment(self, post_id, user, text, comment, review_text):

        first = data.firstwords[self.index[0]]
        second = data.mainwords[self.index[1]]

        reply = self.add_link(f"{first} {second}", data.links[self.index[2]])
        thread = Thread(target=ins.announce, args=(user, f"{post_id}", text))
        thread.start()

        photo = ""
        if randint(0, 4) == 4:
            photo = "photo-142736087_457240199"

        self.special_random()
        self.vk.method('wall.createComment', {
            'owner_id': -data.hentreview,
            'post_id': post_id,
            'from_group': data.hentreview,
            'message': reply,
            'reply_to_comment': comment,
            'attachments': photo})

        if user not in data.admins:
            data.save(f"INSERT INTO already VALUES ({user})")

        short_reply = ins.shorter(reply)
        short_response = ins.shorter(review_text)
        print(
            f"{Color.bold}[*] {Color.blue}{Color.bold}Добавлен комментарий"
            f"\"{short_reply}\" на запись \"{short_response}\" ({post_id}){Color.default}")

    @default.announcement
    def run(self):
        while True:
            sleep(data.per)
            response = self.vk.getEvent()

            if response:

                response = response[0]
                event = response['object']
                event_type = response["type"]

                if event_type in ['wall_reply_new', 'wall_reply_edit']:

                    user = event["from_id"]
                    text = event["text"].lower()
                    post_id = event["post_id"]
                    event_id = event["id"]

                    if user != data.hentreview or user != data.fullhent:
                        blacklist = ins.black_list(text)

                        if blacklist:
                            self.vk.method("wall.deleteComment", {
                                "owner_id": f"-{data.hentreview}",
                                "comment_id": event_id
                            })
                            short_text = ins.shorter(event["text"])
                            print(
                                f"{Color.bold}[*] {Color.blue}{Color.bold}Удалён комментарий \"{short_text}\" "
                                f"на записи (-{data.hentreview}_{post_id}){Color.default}")

                        if user > 0 and user and not blacklist:
                            array = data.get_one(f"SELECT * FROM already WHERE id = {user}")

                            if not array:
                                if ins.func(data.triggers, text) and not ins.func(data.exceptions, text):

                                    response = data.get_one(f"SELECT * FROM reviews WHERE id = {post_id}")
                                    if response:
                                        self.generate_comment(post_id, user, text, event_id, response[1])
                                    else:
                                        keypass = self.checker(post_id)
                                        if keypass:
                                            self.generate_comment(post_id, user, text, event_id, "<Just Added>")

                if event_type == 'wall_post_new':
                    if ins.func(data.review_triggers, event["text"].lower()):
                        owner_id = event["owner_id"]
                        if event["post_type"] == "post":
                            post_id = event["id"]
                            post_date = event["date"]
                            text = event["text"]
                            author = event.get("created_by") or 0

                            short_text = ins.shorter(text)
                            post = f"{owner_id}_{post_id}"

                            text = ins.base_fix(text)
                            ins.save_photos(event["attachments"], post_id)

                            data.save(f"INSERT INTO statistic VALUES ({post_id}, {post_date}, {author})")
                            data.save(f"INSERT INTO reviews VALUES ({post_id}, \"{text}\", {author}, \"Пусто\", 0)")
                            print(
                                f"{Color.bold}[*] {Color.blue}{Color.bold} Добавлена запись в очередь на статистику "
                                f"{Color.default}\"{short_text}\"{Color.blue}{Color.bold} ({post}) {Color.default}"
                                "" + ins.time_transfer(data.seconds + (post_date - int(time()))))

                if event_type == 'message_new':
                    text = str(event["text"]).removesuffix(" ").removesuffix("\n")
                    user = int(event["from_id"])
                    print(
                        f"{Color.bold}[*] {Color.blue}{Color.bold}Получена команда \"{text}\" ({user}){Color.default}")
                    if text != '':
                        command = ins.base_fix(text.lower()).split()[0].split("\n")[0]

                        data_response = data.get_one(f"SELECT * FROM commands WHERE trigger = \"{command}\"")
                        if data_response:
                            ins.message(user, data_response[0], data_response[1], data.hentreview)


class Statistics(Thread):

    def __init__(self):
        Thread.__init__(self)

    @default.announcement
    def run(self):
        while True:

            response = data.get_one("SELECT * FROM statistic ORDER BY time ASC")
            if response:
                if int(time()) - response[1] >= data.seconds:
                    post_id = response[0]
                    post = ins.vk.method('wall.getById', {'posts': f"-{data.hentreview}_{post_id}"})
                    if post:
                        post = post[0]

                        likes, wall_reposts, mail_reposts, views, comments = "N", "N", "N", "N", "N"
                        f_likes, f_wall_reposts, f_mail_reposts, f_views, f_comments = "N", "N", "N", "N", "N"

                        if "likes" in post:
                            likes = post["likes"]["count"]
                        if "reposts" in post:
                            reposts = post["reposts"]
                            wall_reposts = reposts["wall_count"]
                            mail_reposts = reposts["mail_count"]
                        if "views" in post:
                            views = post["views"]["count"]
                        if "comments" in post:
                            comments = post["comments"]["count"]

                        data_response = data.get_one(f"SELECT * FROM reviews WHERE id = {post_id}")
                        if data_response:
                            full_id = data_response[4]
                            if full_id != 0:
                                full_post = f"-{data.fullhent}_{full_id}"
                                full = ins.vk.method('wall.getById', {'posts': full_post})
                                if full:
                                    full = full[0]
                                    if "likes" in full:
                                        f_likes = full["likes"]["count"]
                                    if "reposts" in full:
                                        f_reposts = full["reposts"]
                                        f_wall_reposts = f_reposts["wall_count"]
                                        f_mail_reposts = f_reposts["mail_count"]
                                    if "views" in full:
                                        f_views = full["views"]["count"]
                                    if "comments" in full:
                                        f_comments = full["comments"]["count"]

                            reply = (f"─────────────────────\n"
                                     f"Обзоры на Хент/fullhent\n\nЛайки: [id0|{likes}]\\[id0|{f_likes}]"
                                     f"\nРепосты на стену: [id0|{wall_reposts}]\\[id0|{f_wall_reposts}]\n"
                                     f"Репосты в сообщения: [id0|{mail_reposts}]\\[id0|{f_mail_reposts}]\n"
                                     f"Просмотры: [id0|{views}]\\[id0|{f_views}]\n"
                                     f"Комментарии: [id0|{comments}]\\[id0|{f_comments}]"
                                     )
                            author = response[2]
                            if author != 0:
                                author_info = ins.vk.method('users.get', {'user_ids': author})[0]
                                first_name = author_info.get('first_name')
                                last_name = author_info.get('last_name')
                                reply += f"\n\nАвтор: [id{author}|{first_name} {last_name}]"

                            ins.vk.method('messages.send', {
                                'peer_id': data.admins[0],
                                'message': reply,
                                'random_id': randint(0, 100000),
                                'attachment': f"wall-{data.hentreview}_{post_id}"
                            })
                            text = post["text"]
                            short_text = ins.shorter(text)

                            print(
                                f"{Color.bold}[*] {Color.blue}{Color.bold}Сделана статистика"
                                f"{short_text}\" ({post_id}){Color.default}")
                    data.save(f"DELETE FROM statistic WHERE id = {post_id}")
            sleep(data.cooldown)


class Deleter(Thread):

    def __init__(self):
        Thread.__init__(self)

    @default.announcement
    def run(self):
        while True:
            response = data.get_one("SELECT * FROM timed ORDER BY time ASC")
            if response:
                if response[2] - int(time()) <= 0:
                    data.save(f"DELETE FROM timed WHERE id = {response[1]} AND owner = {response[0]}")
                    ins.vk.method("wall.delete", {"owner_id": response[0], "post_id": response[1]})
            sleep(data.per)


class Check(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.index = 0
        self.array = [data.hentreview, data.hentreview]

    @default.announcement
    def plus_index(self):
        self.index += 1
        if self.index >= len(ins.secret):
            self.index = 0

    @default.announcement
    def walker(self, data_response, group, column):
        post = data_response[column]

        temp = post
        if group == data.fullhent:
            temp = -post
        deleted_response = data.get_one(f"SELECT * FROM deleted WHERE id = {temp}")

        if post != 0 and not deleted_response:
            response = None
            while not response:
                response = ins.secret[self.index].method('wall.getComments', {'owner_id': -group, 'post_id': post})
            while 'error' in response:
                if response["error"]["error_code"] == 15:
                    response2 = ins.secret[self.index].method('wall.getById', {'posts': f"{-group}_{post}"})
                    if response2 and "deleted_reason" in response2[0]:
                        if group == data.hentreview:
                            data.save(f"INSERT INTO deleted VALUES ({data_response[0]})")
                        if group == data.fullhent:
                            data.save(f"INSERT INTO deleted VALUES ({-data_response[0]})")
                    break
                else:
                    self.plus_index()
                    response = ins.secret[self.index].method('wall.getComments', {'owner_id': -group, 'post_id': post})

    @default.announcement
    def update(self, group, column):

        data_response = data.get_all(f"SELECT * FROM reviews ORDER BY id DESC")

        for i in range(len(data_response)):
            thread = Thread(target=self.walker, args=(data_response[i], group, column))
            thread.start()
            sleep(0.5)

    @default.announcement
    def run(self):
        while True:
            sleep(data.cooldown)

            self.update(data.hentreview, 0)
            self.update(data.fullhent, 4)


class Fullhent(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.vk = VK(data.token, data.fullhent)

    @default.announcement
    def add_user(self, user):
        self.vk.method('groups.approveRequest', {'group_id': data.fullhent, 'user_id': user})
        thread = Thread(target=ins.announce, args=(user, None, None, "approved"))
        thread.start()

    @default.announcement
    def check_requests(self):
        response = self.vk.method('groups.getRequests', {'group_id': data.fullhent, 'count': 200})['items']
        for i in range(len(response)):
            thread = Thread(target=self.add_user, args=(response[i],))
            thread.start()
            sleep(0.10)

    @default.announcement
    def checker(self, post_id):

        post = f"-{data.fullhent}_{post_id}"

        response = ins.secret[ins.index].method('wall.getById', {'posts': post})
        while 'error' in response:
            ins.plus_secret()
            response = ins.secret[ins.index].method('wall.getById', {'posts': post})

        if len(response) != 0:
            response = response[0]
            text = response["text"]
            if "copy_history" in response:
                if response["post_type"] == "post":
                    forwarded_id = response["copy_history"][0]["id"]
                    data_response = data.get_one(f"SELECT * FROM reviews WHERE id = {forwarded_id}")
                    if data_response:
                        text = ins.base_fix(text)
                        print(
                            f"{Color.bold}[*] {Color.blue}{Color.bold}Добавлен фул ({post_id}) к посту "
                            f"-{data.hentreview}_{forwarded_id}{Color.default}")
                        data.save(
                            f"UPDATE reviews SET full = \"{text}\", full_id = {post_id} WHERE id = {forwarded_id}")
                    else:
                        full_response = data.get_one(f"SELECT * FROM unknown WHERE id = {post_id}")
                        if not full_response:
                            text = ins.base_fix(text)
                            print(
                                f"{Color.bold}[*] {Color.blue}{Color.bold}Добавлен фул ({post_id}) в базу"
                                f" данных (неопределён){Color.default}")
                            data.save(f"INSERT INTO unknown VALUES ({post_id}, \"{text}\")")

    @default.announcement
    def walker(self, max_number, min_number=0):
        print(f"{Color.bold}[*] Идёт проверка записей Fullhent... {Color.default}")
        for i in range(min_number, max_number + 1):
            difference = max_number - i
            print(f"{Color.light_blue}{Color.bold}{difference} ({i}){Color.default}")
            thread = Thread(target=self.checker, args=(i,))
            thread.start()
            sleep(0.10)

    @default.announcement
    def update(self, force_zero=False):

        response = ins.secret[ins.index].method("wall.get", {'owner_id': -1 * data.fullhent, 'count': 1})
        while 'error' in response:
            ins.plus_secret()
            response = ins.secret[ins.index].method("wall.get", {'owner_id': -1 * data.fullhent, 'count': 1})

        if "items" in response:
            min_number = 0
            if not force_zero:
                base_response = data.get_one(f"SELECT * FROM reviews ORDER BY full_id DESC")
                if base_response:
                    min_number = base_response[4]
            self.walker(response["items"][0]["id"], min_number)

    @default.announcement
    def run(self):
        while True:
            sleep(data.per)

            response = self.vk.getEvent()

            if response:

                response = response[0]
                event = response['object']
                event_type = response["type"]

                if event_type in ['wall_reply_new', 'wall_reply_edit']:

                    text = event["text"].lower()
                    post_id = event["post_id"]
                    owner_id = event["owner_id"]

                    blacklist = ins.black_list(text)

                    if blacklist:
                        self.vk.method("wall.deleteComment", {
                            "owner_id": f"-{data.fullhent}",
                            "comment_id": event["id"]
                        })
                        short_text = ins.shorter(event["text"])
                        print(
                            f"{Color.bold}[*] {Color.blue}{Color.bold}Удалён комментарий \"{short_text}\""
                            f" на записи ({owner_id}_{post_id}){Color.default}")

                if event_type == "group_join":
                    if event["join_type"] == "request":
                        thread = Thread(target=self.add_user, args=(event['user_id'],))
                        thread.start()

                if event_type == "wall_post_new":
                    post_id = event["id"]
                    text = event["text"]
                    if "copy_history" in event:
                        if event["post_type"] == "post":
                            forwarded_id = event["copy_history"][0]["id"]
                            response = data.get_one(f"SELECT * FROM reviews WHERE id = {forwarded_id}")
                            if response:
                                print(
                                    f"{Color.bold}[*] {Color.blue}{Color.bold}Добавлен фул ({post_id}) к посту"
                                    f" -{data.hentreview}_{forwarded_id}{Color.default}")
                                text = ins.base_fix(text)
                                data.save(
                                    f"UPDATE reviews SET full = \"{text}\", full_id = {post_id} WHERE id = "
                                    f"{forwarded_id}")
                            else:
                                full_response = data.get_one(f"SELECT * FROM unknown WHERE id = {post_id}")
                                if not full_response:
                                    text = ins.base_fix(text)
                                    print(
                                        f"{Color.bold}[*] {Color.blue}{Color.bold}Добавлен фул ({post_id}) в "
                                        f"базу данных (неопределён){Color.default}")
                                    data.save(f"INSERT INTO unknown VALUES ({post_id}, \"{text}\")")


class Bot(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._ = "─────────────────────\n{}"
        self.fix = 0
        self.secret = []
        self.key = 0

        self.help = {
            "0": """Команды

                [id0|check]/[id0|проверка] - Проверка работоспособности.
                [id0|seek]/[id0|поиск] - Поиск обзора по названию фула.
                [id0|force_fulls]/[id0|обновить_фулы] - Обновить фулы в базу данных.
                [id0|force_reviews]/[id0|обновить_обзоры] - Обновить обзоры в базу данных.
                [id0|sql] - Взаимодействие с базой данных с помощью SQL запросов.
                [id0|album]/[id0|альбом] - Создание альбома с произведением хентайного характера.
                [id0|clear]/[id0|очистить] - Удаление остаточных файлов (обязательно при сбое в работе)
                [id0|delete]/[id0|удалить] - Удаление поста через какое-то время.

                [id0|assist]/[id0|поддержка] - Поддержка бота.
                [id0|commands]/[id0|команды] - Команды в группе.
                [id0|banwords]/[id0|банворды] - Запрещённые символы в комментариях."

                [id0|wipe]/[id0|очистка] - Полное удаление базы данных.
                """,

            "1": """Это игра! Здесь тебе нужно соединить правый носок (Обзор) и левый носок (Фул).

                [id0|get]/[id0|получить] - Список обзоров без фуллов.
                [id0|fulls]/[id0|фулы] - Список фуллов без обзоров.
                [id0|set]/[id0|поставить] - Соединить фул и обзор.
                [id0|deleted]/[id0|удалённые] - Просмотреть удалённые посты.

                [id0|exit]/[id0|выйти] - Выйти из игры.
                """,

            "2": """Пост будет удалён из базы данных. Ты уверен?

                [id0|yes]/[id0|да] - Подтвердить действие.
                [id0|no]/[id0|нет] - Отказаться от действия.
            """,

            "3": """Это отдел для команд, которые могут писать в сообщество подписчики,
            а само сообщество отвечать твоим текстом и вложениями.

                [id0|добавить]/[id0|add] - Добавить команду.
                [id0|delete]/[id0|удалить] - Удаление команды.
                [id0|see]/[id0|просмотр] - Просмотр всех команд.

                [id0|exit]/[id0|выйти] - Выход в главное меню.
                """,

            "4": """База данных будет удалена. Ты уверен?

                [id0|yes]/[id0|да] - Подтвердить действие.
                [id0|no]/[id0|нет] - Отказаться от действия.
                """,

            "5": """Это отдел для символов, которые запрещены для написания комментариях.

                [id0|add]/[id0|добавить] - Добавить.
                [id0|delete]/[id0|удалить] - Удалить.
                [id0|see]/[id0|просмотр] - Просмотр.

                [id0|exit]/[id0|выйти] - Выйти в главное меню.
                """,

            "6": """Используй [id0|/>] или [id0|/<] для перелистывания. [id0|exit]/[id0|выйти] - Выйти в меню.""",

            "7": """Используй [id0|/>] или [id0|/<] для перелистывания. [id0|exit]/[id0|выйти] - Выйти в меню игры.""",

            "8": """Используй [id0|/>] или [id0|/<] для перелистывания. [id0|exit]/[id0|выйти] - Выйти в меню игры.""",

            "9": """Используй [id0|/>] или [id0|/<] для перелистывания. [id0|exit]/[id0|выйти] - Выйти в меню.""",

            "10": """Используй [id0|/>] или [id0|/<] для перелистывания. [id0|exit]/[id0|выйти] - Выйти в меню игры.
            Чтобы восстановить пост напиши [id0|/restore] или [id0|/восстановить]"""
        }

        self.local_help = self.help[str(self.key)]

    @default.announcement
    def raw_message_list(self, data_response, peer_id):
        ins.message(peer_id, self._.format("Найдено следующее:\n\n"))
        sleep(0.5)
        for i in range(len(data_response)):
            ins.message(peer_id, self._.format(f"{i + 1}. {data_response[i]}"))
            sleep(0.5)

    @default.announcement
    def update_time(self, user):
        data.save(f"UPDATE dialog SET time = {int(time())} WHERE id = {user}")

    @default.announcement
    def update_branch(self, branch, user):
        self.fix = 0
        self.secret = []
        self.key = branch

        self.local_help = self.help[str(branch)]

        data.save(f"UPDATE dialog SET branch = {branch}, time = {int(time())} WHERE id = {user}")

    @default.announcement
    def integer_check(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    @default.announcement
    def set_review(self, review_id, full_id, user):

        data_response = data.get_one(f"SELECT * FROM reviews WHERE id = {review_id} AND full_id = 0")
        if data_response:

            post = f"-{data.fullhent}_{full_id}"
            full_response = ins.secret[ins.index].method('wall.getById', {'posts': post})
            while 'error' in full_response:
                ins.plus_secret()
                full_response = ins.secret[ins.index].method('wall.getById', {'posts': post})

            if len(full_response) != 0:
                full_text = full_response[0]["text"]
                data.save(f"UPDATE reviews SET full = {full_text}, full_id = {full_id} WHERE id = {review_id}")
            else:
                ins.message(user, self._.format("Не удалось получить пост из fullhent. Существует ли он?"))
        else:
            ins.message(user, self._.format("Обзора с этим айди без фула не существует."))

    @default.announcement
    def get_date(self, string):

        words = string.split()
        date_indexs = ["w", "d", "h", "m", "s", "н", "д", "ч", "м", "с"]
        date_meaning = [604800, 86400, 3600, 60, 1, 604800, 86400, 3600, 60, 1]
        ret_time = 0

        temp2 = "2F4"
        for i in range(len(words)):

            control = True
            temp1 = words[len(words) - 1 - i]

            for j in range(len(date_indexs)):

                if date_indexs[j] in temp1:

                    temp = temp1.split(date_indexs[j])[0]
                    if temp + date_indexs[j] == temp1:
                        try:
                            ret_time += int(temp) * date_meaning[j]
                            control = False
                            break
                        except Exception as e:
                            print(e)
                            control = True
                            break

            if control and i != 0:
                temp2 = words[len(words) - i]
                break

            if len(words) - 1 == 0 and ret_time != 0:
                temp2 = temp1
                break

        if temp2 != "2F4":
            string = string.split(temp2)[0]
            string = string[:len(string) - 1]

        return [string, ret_time]

    @default.announcement
    def plus_fix(self):
        self.fix += 1
        if self.fix > len(self.secret):
            self.fix = 0

    @default.announcement
    def minus_fix(self):
        self.fix -= 1
        if self.fix < 0:
            self.fix = len(self.secret)

    @default.announcement
    def check_id(self, string):
        array = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", ","]
        response = ""
        for i in range(len(string)):
            if string[i] not in array:
                response = int(string[:i])
                break
        if response == "":
            if string != "":
                response = int(string)
            else:
                response = 0
        return response

    @default.announcement
    def deleted(self, array, user):
        response = ""
        for i in array:
            ins.vk.method("wall.delete", {"owner_id": i[0], "post_id": i[1]})
            response += f"Удалён пост {i[1]}\n"
        ins.message(user, self._.format(response))

    @default.announcement
    def run(self):
        while True:
            sleep(data.per)

            response = ins.vk.getBot()
            if response:

                event = response[0]

                if event[0] == 4:
                    user = int(event[3])
                    if user in data.announceed:
                        text = str(event[6])
                        if text.startswith(data.command_trigger):
                            command = text.removeprefix(data.command_trigger)
                            rest = command
                            command = command.split()[0]
                            print(
                                f"{Color.bold}[*] {Color.blue}{Color.bold} Получена команда {Color.default}"
                                f"\"{rest}\" {Color.default}")

                            dialog = data.get_one(f"SELECT * FROM dialog WHERE id = {user}")

                            if dialog:
                                if int(time()) - dialog[1] >= 300:
                                    self.update_branch(0, user)

                            else:
                                self.update_branch(0, user)

                            # Пасхалки

                            if command in ["secret", "секрет"]:
                                ins.message(user, self._.format(f"Gfy 6th Jr @@#56-21_hr4567515"))
                                command = "block"

                            if command == "936":
                                ins.message(user, self._.format(
                                    "название дай блять гандон ебаный каждый пост одно и тоже блять"
                                    " ну что за тупой дегенерат в админах НАЗВАНИЕ ГДЕ СУКА"))
                                command = "block"

                            if command in ["verus", "верус"]:
                                ins.message(user, self._.format(
                                    "OMFG Verus pam pam pam pam pam pam pam tadadam pam pam SUS Verus sussy"),
                                            "video277262202_456239139")
                                command = "block"

                            if command in ["хентайлиб", "hentailib", "hentlib", "хентлиб"]:
                                ins.message(user, self._.format("https://www.youtube.com/watch?v=qvAQGO0K7SY"))
                                command = "block"

                            if command in ["sus", "amogus", "амогус", "сас"]:
                                ins.message(user, self._.format("nice ass, kitten"))

                            if command in ["key", "ключ"]:
                                ins.message(user, self._.format(f"Ключ: {self.key}"))
                                command = "block"

                            if self.key == 0:

                                if command in ["check", "проверка"]:
                                    ins.message(user, self._.format("Я работаю."))

                                elif command in ["seek", "поиск"]:

                                    param = rest.removeprefix("seek").removeprefix("поиск").removeprefix(" ")

                                    if param not in ["Пусто", ""]:

                                        data_response = data.get_multi(
                                            f"SELECT * FROM reviews WHERE full LIKE '%{param}%' "
                                            f"OR string LIKE '%{param}%'")
                                        if data_response:
                                            self.update_branch(9, user)
                                            self.secret = data_response
                                            command = "current"
                                        else:
                                            ins.message(user, self._.format("Ничего не найдено."))

                                    if param == "Пусто":
                                        ins.message(user, self._.format(
                                            "Хей-хей! Ты не можешь так просто взять и сломать скрипты."))

                                elif command in ["force_fulls", "обновить_фулы"]:
                                    fullhent.update(True)
                                    ins.message(user, self._.format("Выполняется."))

                                elif command in ["force_reviews", "обновить_обзоры"]:
                                    hentreview.update(True)
                                    ins.message(user, self._.format("Выполняется."))

                                elif command == "sql":
                                    param = rest.removeprefix("sql").removeprefix(" ")

                                    if param != "":
                                        try:
                                            data_response = data.get_multi(param)
                                            if data_response == [] or not data_response:
                                                data.save(param)
                                                ins.message(user, self._.format("Ничего не выдано. Сохраняю команду."))
                                            else:
                                                self.raw_message_list(data_response, user)
                                        except Exception as e:
                                            ins.message(user,
                                                        self._.format(f"Получена ошибка при выполнении запроса: {e}."))
                                    else:
                                        ins.message(user, self._.format("Напиши SQL запрос после этой команды."))

                                elif command in ["assist", "поддержка"]:
                                    self.update_branch(1, user)
                                    ins.message(user, self._.format(self.local_help))

                                elif command in ["commands", "команды"]:
                                    self.update_branch(3, user)
                                    ins.message(user, self._.format(self.local_help))

                                elif command in ["wipe", "очистка"]:
                                    self.update_branch(4, user)
                                    ins.message(user, self._.format(self.local_help))

                                elif command in ["banwords", "банворды"]:
                                    self.update_branch(5, user)
                                    ins.message(user, self._.format(self.local_help))

                                elif command in ["album", "альбом"]:
                                    param = rest.removeprefix("album").removeprefix("альбом").removeprefix(
                                        " ").removesuffix(" ").removesuffix("\n")

                                    if param != "":
                                        thread = Install(user, param)
                                        thread.start()
                                    else:
                                        ins.message(user, self._.format(
                                            "Слушай, не очень я хотел бы тебя сильно обидеть, но ты немножко"
                                            " отстаешь в развитии от среднестатистического представителя homo"
                                            " sapiens. Напиши, пожалуйста, ссылку на произведение."))

                                elif command in ["clear", "очистить"]:
                                    was_deleted = data.delete_temp(1000)
                                    ins.message(user, self._.format(f"Было удалено [id0|{was_deleted}] из папки temp."))

                                elif command in ["delete", "удалить"]:

                                    param = rest.removeprefix("delete").removeprefix("удалить").removeprefix(" ")
                                    temp = self.get_date(param)
                                    attachment = []

                                    if temp[0] == '':
                                        message = ins.vk.method("messages.getById", {"message_ids": event[1]})
                                        if "items" in message:
                                            attachments = message["items"][0]["attachments"]
                                            if attachments:
                                                attachment_type = attachments[0]["type"]
                                                attachment_body = attachments[0][attachment_type]
                                                if attachment_type == "wall":
                                                    attachment.append(
                                                        [attachment_body["from_id"], attachment_body["id"]])
                                    else:
                                        if "https://vk.com/" in temp[0] and "wall" in temp[0] and "_" in temp[0]:
                                            temp1 = temp[0].split("wall")[1]
                                            owner = self.check_id(temp1)
                                            post_id = self.check_id(temp1.split("_")[1])
                                            attachment.append([owner, post_id])

                                    if len(attachment) != 0:
                                        if temp[1] != 0:
                                            response = ""
                                            str_time = ins.time_transfer(temp[1])
                                            for i in attachment:
                                                data.save(
                                                    f"INSERT INTO timed VALUES "
                                                    f"({i[0]}, {i[1]}, {int(time()) + temp[1]})")
                                                response += f"Пост {i[1]} будет удалён через {str_time}\n"
                                            ins.message(user, self._.format(response))
                                        else:
                                            self.deleted(attachment, user)
                                    else:
                                        ins.message(user, self._.format(
                                            "Напиши, пожалуйста, пост в сообщении, ну"
                                            " или отправь вложением вместе с командой."))

                                elif command != "block":
                                    command = "current"

                            if self.key == 1:

                                if command in ["get", "получить"]:
                                    data_response = data.get_all("SELECT * FROM reviews WHERE full_id = 0")
                                    if data_response:
                                        self.update_branch(8, user)
                                        self.secret = data_response
                                        command = "current"
                                    else:
                                        self.update_time(user)
                                        ins.message(user, self._.format("Пусто!"))

                                elif command in ["fulls", "фулы"]:
                                    data_response = data.get_all("SELECT * FROM unknown")
                                    if data_response:
                                        self.update_branch(7, user)
                                        self.secret = data_response
                                        command = "current"
                                    else:
                                        self.update_time(user)
                                        ins.message(user, self._.format("Пусто!"))

                                elif command in ["del", "удалить"]:
                                    self.update_time(user)
                                    param = rest.removeprefix("del").removeprefix("удалить").removeprefix(" ")
                                    if param != "":
                                        param_is_integer = self.integer_check(param)
                                        if param_is_integer:
                                            param = int(param)
                                            data_response = data.get_one(f"SELECT * FROM unknown WHERE id = {param}")
                                            if data_response:
                                                self.update_branch(2, user)
                                                self.fix = param
                                            else:
                                                ins.message(user, self._.format(f"Данный пост не существует."))

                                elif command in ["exit", "выйти"]:
                                    self.update_branch(0, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command in ["set", "поставить"]:
                                    self.update_time(user)
                                    param = rest.removeprefix("set").removeprefix("поставить").removeprefix(" ")

                                    if param != "":
                                        param_array = param.split()
                                        first = param_array[0]
                                        second = param.removeprefix(first).removeprefix(" ")
                                        first_is_integer = self.integer_check(first)
                                        second_is_integer = self.integer_check(second)

                                        attachment = ""
                                        message = ins.vk.method("messages.getById", {"message_ids": event[1]})
                                        if "items" in message:
                                            attachments = message["items"][0]["attachments"]
                                            if attachments:
                                                attachment_type = attachments[0]["type"]
                                                attachment_body = attachments[0][attachment_type]
                                                if attachment_body["from_id"] == -data.fullhent:
                                                    attachment = attachment_body["id"]

                                        if first_is_integer:
                                            review_id = int(first)

                                            if second_is_integer:
                                                full_id = int(second)
                                                self.set_review(review_id, full_id, user)

                                            if attachment != "":
                                                full_id = attachment
                                                self.set_review(review_id, full_id, user)

                                            else:
                                                ins.message(user, self._.format("Не удалось определить фул."))
                                        else:
                                            ins.message(user, self._.format("Не удалось определить айди обзора."))
                                    else:
                                        ins.message(user, self._.format(
                                            "Напиши после команды айди обзора и либо айди фула, либо сам"
                                            "пост из fullhent. Как то так:\n/set 72 3\n/set 19927 6809\n"
                                            "/set 14933 [репост поста]"))

                                elif command in ["deleted", "удалённые"]:
                                    deleted_response = data.get_all("SELECT * FROM deleted")
                                    if deleted_response:
                                        self.update_branch(10, user)
                                        self.secret = deleted_response
                                        command = "current"
                                    else:
                                        self.update_time(user)
                                        ins.message(user, self._.format("Пусто!"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 2:

                                if command in ["yes", "да"]:
                                    self.update_branch(1, user)
                                    data.save(f"DELETE FROM unknown WHERE id = {self.fix}")
                                    ins.message(user, self._.format(f"Выполнено.\n\n{self.local_help}"))

                                elif command in ["no", "нет"]:
                                    self.update_branch(1, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 3:

                                if command in ["add", "добавить"]:
                                    self.update_time(user)
                                    param = rest.removeprefix("add").removeprefix("добавить").removeprefix(" ")
                                    trigger = param.split()[0].split("\n")[0].split("<br>")[0].lower()
                                    for i in range(5):
                                        trigger = trigger.removesuffix("\n").removeprefix("\n").removeprefix(
                                            " ").removesuffix(" ").removeprefix("<br>").removesuffix("<br>")
                                    trigger = ins.delete_quote(trigger)

                                    data_response = data.get_one(
                                        f"SELECT * FROM commands WHERE trigger = \"{trigger}\"")

                                    if not data_response:
                                        reply = param[len(trigger):]
                                        for i in range(5):
                                            reply = reply.removeprefix(" ").removeprefix("\n").removeprefix("<br>")

                                        attachment = ""
                                        message = ins.vk.method("messages.getById", {"message_ids": event[1]})
                                        if "items" in message:
                                            attachments = message["items"][0]["attachments"]
                                            for i in range(len(attachments)):
                                                attachment_type = attachments[i]["type"]
                                                attachment_body = attachments[i][attachment_type]

                                                owner = attachment_body.get("owner_id") or attachment_body.get(
                                                    "from_id")
                                                a_id = attachment_body["id"]
                                                attachment += f"{attachment_type}{owner}_{a_id}"
                                                if 'access_key' in attachment_body:
                                                    key = attachment_body['access_key']
                                                    attachment += f"_{key}"
                                                attachment += ","

                                        attachment = attachment.removesuffix(",")
                                        if reply != "" or attachment != "":
                                            data.save(
                                                "INSERT INTO commands VALUES "
                                                f"(\"{reply}\", \"{attachment}\", \"{trigger}\")")
                                            ins.message(user, self._.format(f"Выполнено. Команда {trigger} добавлена."))
                                        else:
                                            ins.message(user, self._.format(f"Не удалось определить ответ."))
                                    else:
                                        ins.message(user, self._.format(f"Данная команда уже существует."))

                                elif command in ["delete", "удалить"]:
                                    self.update_time(user)
                                    param = rest.removeprefix("delete").removeprefix("удалить").removeprefix(" ")
                                    trigger = param.split()[0].split("\n")[0].lower()
                                    trigger = ins.delete_quote(trigger)

                                    data_response = data.get_one(
                                        f"SELECT * FROM commands WHERE trigger = \"{trigger}\"")

                                    if data_response:
                                        data.save(f"DELETE FROM commands WHERE trigger = \"{trigger}\"")
                                        ins.message(user, self._.format(f"Выполнено. Команда {trigger} удалена."))
                                    else:
                                        ins.message(user, self._.format("Не удалось найти такую команду."))

                                elif command in ["see", "просмотр"]:
                                    self.update_time(user)

                                    data_response = data.get_all(f"SELECT * FROM commands")
                                    if data_response:
                                        self.update_branch(6, user)
                                        self.secret = data_response
                                        command = "current"
                                    else:
                                        ins.message(user, self._.format("Команд нету, но вы держитесь. :)"))

                                elif command in ["exit", "выход"]:
                                    self.update_branch(0, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 4:

                                if command in ["yes", "да"]:
                                    self.update_branch(0, user)
                                    data.wipe()
                                    ins.message(user, self._.format(f"Выполнено.\n\n{self.local_help}"))

                                elif command in ["no", "нет"]:
                                    self.update_branch(0, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 5:

                                if command in ["add", "добавить"]:
                                    self.update_time(user)
                                    param = rest.removeprefix("add").removeprefix("добавить").removeprefix(" ")
                                    param = param.split()[0].lower()
                                    param = ins.base_fix(param)

                                    data_response = data.get_one(
                                        f"SELECT * FROM blacklisted WHERE banword = \"{param}\"")
                                    if not data_response:
                                        data.save(f"INSERT INTO blacklisted VALUES (\"{param}\")")
                                        ins.message(user, self._.format(f"Выполнено. Банворд {param} добавлен."))
                                    else:
                                        ins.message(user, self._.format(f"Данный банворд уже существует."))

                                elif command in ["delete", "удалить"]:
                                    self.update_time(user)
                                    param = rest.removeprefix("delete").removeprefix("удалить").removeprefix(" ")
                                    param = param.split()[0].lower()
                                    param = ins.base_fix(param)

                                    data_response = data.get_one(
                                        f"SELECT * FROM blacklisted WHERE banword = \"{param}\"")
                                    if data_response:
                                        data.save(f"DELETE FROM blacklisted WHERE banword = \"{param}\"")
                                        ins.message(user, self._.format(f"Выполнено. Банворд {param} удалён."))
                                    else:
                                        ins.message(user, self._.format(f"Не удалось найти такой банворд.."))

                                elif command in ["see", "просмотр"]:
                                    self.update_time(user)

                                    data_response = data.get_all(f"SELECT * FROM blacklisted")
                                    if data_response:
                                        reply = self._.format(f"Все банворды:\n\n")
                                        for i in range(len(data_response)):
                                            reply += f"{i + 1}. {data_response[i][0]}"

                                        ins.message(user, reply)
                                    else:
                                        ins.message(user, self._.format("Банвордов нету."))

                                elif command in ["exit", "выход"]:
                                    self.update_branch(0, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 6:

                                if command in [">", "&gt;"]:
                                    self.plus_fix()

                                elif command in ["<", "&lt;"]:
                                    self.minus_fix()

                                elif command in [">", "<", "&lt;", "&gt;", "current", "текущий"]:
                                    self.update_time(user)
                                    ins.message(user, self._.format(
                                        f"{self.local_help}\n\n{self.fix + 1}/{len(self.secret)}\n\n"
                                        f"Команда: {self.secret[self.fix][2]}\n\n{self.secret[self.fix][0]}"),
                                                self.secret[self.fix][1])
                                    command = "-"

                                elif command in ["exit", "выйти"]:
                                    self.update_branch(3, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 7:

                                if command in [">", "&gt;"]:
                                    self.plus_fix()

                                elif command in ["<", "&lt;"]:
                                    self.minus_fix()

                                elif command in [">", "<", "&lt;", "&gt;", "current", "текущий"]:
                                    self.update_time(user)
                                    ins.message(user, self._.format(
                                        f"{self.local_help}\n\n{self.fix + 1}/{len(self.secret)}\n\n"
                                        f"Айди: {self.secret[self.fix][0]}"),
                                                f"wall-{data.fullhent}_{self.secret[self.fix][0]}")
                                    command = "-"

                                elif command in ["exit", "выйти"]:
                                    self.update_branch(1, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 8:

                                if command in [">", "&gt;"]:
                                    self.plus_fix()

                                elif command in ["<", "&lt;"]:
                                    self.minus_fix()

                                elif command in [">", "<", "&lt;", "&gt;", "current", "текущий"]:
                                    self.update_time(user)
                                    ins.message(user, self._.format(
                                        f"{self.local_help}\n\n{self.fix + 1}/{len(self.secret)}\n\n"
                                        f"Айди: {self.secret[self.fix][0]}"),
                                                f"wall-{data.hentreview}_{self.secret[self.fix][0]}")
                                    command = "-"

                                elif command in ["exit", "выйти"]:
                                    self.update_branch(1, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 9:

                                if command in [">", "&gt;"]:
                                    self.plus_fix()

                                elif command in ["<", "&lt;"]:
                                    self.minus_fix()

                                elif command in [">", "<", "&lt;", "&gt;", "current", "текущий"]:
                                    self.update_time(user)

                                    reply = (f"{self.local_help}\n\n{self.fix + 1}/{len(self.secret)}\n\n"
                                             f"Айди: {self.secret[self.fix][0]}")
                                    if self.secret[self.fix][4] != 0:
                                        reply += (f"\nФул: https://vk.com/wall-{data.fullhent}_"
                                                  f"{self.secret[self.fix][4]}\n\n{self.secret[self.fix][3]}")

                                    ins.message(user, self._.format(reply),
                                                f"wall-{data.hentreview}_{self.secret[self.fix][0]}")
                                    command = "-"

                                elif command in ["exit", "выйти"]:
                                    self.update_branch(0, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if self.key == 10:

                                if command in ["restore", "восстановить"]:
                                    self.update_time(user)

                                    post_column = 1
                                    post_column_name = "id"
                                    post_id = self.secret.pop(self.fix)[0]
                                    starting_id = post_id
                                    if post_id < 0:
                                        post_column = 3
                                        post_column_name = "full_id"
                                        post_id = -post_id

                                    data_response = data.get_one(
                                        f"SELECT * FROM reviews WHERE {post_column_name} = {post_id}")

                                    owner = -data.fullhent
                                    attachment = f"wall-{data.hentreview}_" + str(data_response[0])
                                    if post_id > 0:
                                        owner = -data.hentreview
                                        attachment = ins.upload_photo(data.hentreview, post_id,
                                                                      "photos.getWallUploadServer", "group_id",
                                                                      "photos.saveWallPhoto")

                                    ins.vk.method("wall.post", {
                                        "owner_id": owner,
                                        "from_group": 1,
                                        "message": f"Данный обзор был удалён по непонятным причинам"
                                                   "из сообщества. Данный обзор является перезаливом!"
                                                   "\n─────────────────────\n"
                                                   f"{data_response[post_column]}",
                                        "attachments": attachment
                                    })

                                    data.save(f"DELETE FROM deleted WHERE id = {starting_id}")

                                    if len(self.secret) != 0:
                                        self.plus_fix()
                                        command = "current"
                                    else:
                                        self.update_branch(1, user)
                                        ins.message(user, self._.format(f"Посты кончились...\n\n{self.local_help}"))

                                elif command in [">", "&gt;"]:
                                    self.plus_fix()

                                elif command in ["<", "&lt;"]:
                                    self.minus_fix()

                                elif command in [">", "<", "&lt;", "&gt;", "current", "текущий"]:
                                    self.update_time(user)
                                    attachment = None

                                    post_column = 1
                                    post_column_name = "id"
                                    post_id = self.secret[self.fix][0]
                                    if post_id < 0:
                                        post_column = 3
                                        post_column_name = "full_id"
                                        post_id = -post_id
                                    if post_id > 0:
                                        attachment = ins.upload_photo(user, post_id)

                                    data_response = data.get_one(
                                        f"SELECT * FROM reviews WHERE {post_column_name} = {post_id}")

                                    ins.message(
                                        user,
                                        self._.format(
                                            f"{self.local_help}\n\n{self.fix + 1}/{len(self.secret)}\n\n"
                                            f"Айди: {post_id}\n\n{data_response[post_column]}"),
                                        attachment
                                    )
                                    command = "-"

                                elif command in ["exit", "выйти"]:
                                    self.update_branch(1, user)
                                    ins.message(user, self._.format(f"Выходим...\n\n{self.local_help}"))

                                elif command != "block":
                                    command = "current"

                            if command in ["help", "помощь", "", "current"] and command != "block":
                                ins.message(user, self._.format(self.local_help))


if __name__ == "__main__":
    hentreview = HentReview()
    fullhent = Fullhent()
    statistic = Statistics()
    bot = Bot()
    checker = Check()
    deleter = Deleter()

    statistic.start()
    hentreview.start()
    fullhent.start()
    bot.start()
    checker.start()
    deleter.start()

    hentreview.update()
    fullhent.update()
