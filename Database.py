# -*- coding: utf-8 -*-

from PIL import Image
import json
import sqlite3
from os import mkdir, remove
from os.path import dirname, exists
import sys
from Broadcast import Shout, Color

default = Shout()

class DB:

    @default.announcement
    def __init__(self) -> None:
        
        self.directory = dirname(__file__) + "\\"

        self.settings_path = self.directory + "settings.json"
        self.database_path = self.directory + "databases\\data.db"

        self.check_dir(f"{self.directory}databases")
        self.check_dir(f"{self.directory}databases\\reviews")
        self.check_dir(f"{self.directory}databases\\temp")
        self.create()

        self.default = {
                'Auth': {
                    'token': "Токен."
                },
                'IDs': {
                    'admins': [165585385, 000000000],
                    'fullhent': 182888356,
                    'hentreview': 181869431
                },
                'Quest': {
                    'exceptions': ["|", "[", "]"],
                    'triggers': ["ссылк", "что за хент", "ссыль", "название", "full", "соурс", "фул", "сурс"]
                },
                'Reply': {
                    'firstwords': ["Хай", "Привет", "Йоу", "Дорогой подписчик", "Блять", "Дружок пирожок", "Дарова", 
                                   "Прив", "Ну, привет", "Ну, привет, дружок пирожок", "Еще один на мою голову...", 
                                   "Многоуважаемый подписчик", "Каждый день одно и то же...", 
                                   "Никак вы, блять, не научитесь...", "Ну ты серьёзно... Капец", 
                                   "А в блок ссылок посмотреть..."],
                    'links': ["vk.com\\full_hent", "[full_hent|фулл]"],
                    'mainwords': ["если речь шла о фулле из обзора, то он вот [LINK].",
                                  "ты наверное ищешь фулл? [LINK].", "[LINK]", "[LINK] - вступление автоматическое.", 
                                  "[LINK]", "вот твой фулл. [LINK]", "иди уже дрочи. Вот фулл... [LINK]", 
                                  "всем от нас только одно и надо... [LINK]"]
                },
                'Statics': {
                    'per': 86400,
                    'seconds': 172800,
                    'review_triggers': ['введение', 'сюжет', 'вывод']
                },
                'Work': {
                    'per': 0.1,
                    'timecheck': 10,
                    'timeout': 300
                }
            }

        self.main_info = self.get_main_info()

        if self.main_info == self.default:
            input(f"\n{Color.red}{Color.bold}Произошла ошибка при чтении файла настроек. . .\n  "
                  f"{Color.default}Вставьте в файл данные заново.\n")
            sys.exit()

        self.Auth = self.main_info['Auth']
        self.IDs = self.main_info['IDs']
        self.Quest = self.main_info['Quest']
        self.Reply = self.main_info['Reply']
        self.Statics = self.main_info['Statics']
        self.Work = self.main_info['Work']
        self.Bot = self.main_info['Bot']

        self.token = self.Auth['token']

        self.admins = self.IDs["admins"]
        self.fullhent = self.IDs["fullhent"]
        self.hentreview = self.IDs["hentreview"]

        self.exceptions = self.Quest["exceptions"]
        self.triggers = self.Quest["triggers"]

        self.firstwords = self.Reply["firstwords"]
        self.links = self.Reply["links"]
        self.mainwords = self.Reply["mainwords"]

        self.cooldown = self.Statics["per"]
        self.seconds = self.Statics["seconds"]
        self.review_triggers = self.Statics["review_triggers"]

        self.per = self.Work["per"]

        self.command_trigger = self.Bot["command_trigger"]

        self.announceed = self.admins + [209309485]

    @default.announcement
    def get_one(self, text):
        cursor = sqlite3.connect(self.database_path)
        response = cursor.execute(f"{text}")
        info = response.fetchone()
        cursor.close()
        return info
    
    @default.announcement
    def get_multi(self, text, number=10):
        cursor = sqlite3.connect(self.database_path)
        response = cursor.execute(f"{text}")
        info = response.fetchmany(number)
        cursor.close()
        return info
    
    @default.announcement
    def get_all(self, text):
        cursor = sqlite3.connect(self.database_path)
        response = cursor.execute(f"{text}")
        info = response.fetchall()
        cursor.close()
        return info
    
    @default.announcement
    def save(self, text):
        cursor = sqlite3.connect(self.database_path)
        cursor.execute(f"{text}")
        cursor.commit()
        cursor.close()
    
    @default.announcement
    def get_main_info(self):

        try:
            with open(self.settings_path, "r", encoding='utf-8') as file:
                settings = json.load(file)
                return settings
            
        except IOError:
            return self.doFile()
    
    @default.announcement
    def doFile(self):

        with open(self.settings_path, "w", encoding='utf-8') as file:
            json.dump(self.default, file, sort_keys=True, indent=4, ensure_ascii=False)

        return self.default
    
    @default.announcement
    def create(self):
        self.save("CREATE TABLE IF NOT EXISTS already(id INTEGER)")
        self.save("CREATE TABLE IF NOT EXISTS statistic(id INTEGER, time INTEGER, author INTEGER)")
        self.save("CREATE TABLE IF NOT EXISTS reviews(id INTEGER, string TEXT, author INTEGER, "
                  "full TEXT, full_id INTEGER)")
        self.save("CREATE TABLE IF NOT EXISTS dialog(id INTEGER, time INTEGER, branch INTEGER)")
        self.save("CREATE TABLE IF NOT EXISTS unknown(id INTEGER, string TEXT)")
        self.save("CREATE TABLE IF NOT EXISTS commands(reply_text TEXT, reply_attachments TEXT, trigger TEXT)")
        self.save("CREATE TABLE IF NOT EXISTS blacklisted(banword TEXT)")
        self.save("CREATE TABLE IF NOT EXISTS deleted(id INTEGER)")
        self.save("CREATE TABLE IF NOT EXISTS timed(owner INTEGER, id INTEGER, time INTEGER)")

    @default.announcement
    def wipe(self):
        self.save("DELETE FROM already WHERE EXISTS (SELECT * FROM already)")
        self.save("DELETE FROM statistic WHERE EXISTS (SELECT * FROM statistic)")
        self.save("DELETE FROM reviews WHERE EXISTS (SELECT * FROM reviews)")
        self.save("DELETE FROM dialog WHERE EXISTS (SELECT * FROM dialog)")
        self.save("DELETE FROM unknown WHERE EXISTS (SELECT * FROM unknown)")
        self.save("DELETE FROM commands WHERE EXISTS (SELECT * FROM commands)")
        self.save("DELETE FROM blacklisted WHERE EXISTS (SELECT * FROM blacklisted)")
        self.save("DELETE FROM deleted WHERE EXISTS (SELECT * FROM deleted)")
        self.save("DELETE FROM timed WHERE EXISTS (SELECT * FROM timed)")
    
    @default.announcement
    def check_dir(self, name):
        if not exists(name):
            mkdir(name)
    
    @default.announcement
    def check_photos(self, dir_path):
        for i in range(10):
            photo_path = f"{dir_path}\\{i+1}.jpg"
            if not exists(photo_path):
                return i
        return 9
    
    @default.announcement
    def get_dict(self, text):
        return json.loads(text)

    @default.announcement
    def delete_temp(self, num):
        for i in range(num):
            try:
                remove(f"{self.directory}databases\\temp\\{i+1}.jpg")
            except WindowsError:
                return i
        return 1000
    
    @default.announcement
    def check_format(self, number):
        if exists(f"{self.directory}databases\\temp\\{number}.jpg"):
            return "jpg"
            
        if exists(f"{self.directory}databases\\temp\\{number}.webp"):
            pic = Image.open(f"{self.directory}databases\\temp\\{number}.webp").convert("RGB")
            pic.save(f"{self.directory}databases\\temp\\{number}.jpg", "jpeg")
            remove(f"{self.directory}databases\\temp\\{number}.webp")
            return "jpg"
    
    
if __name__ == "__main__":
    obj = DB()
    print(obj.check_format(1))
