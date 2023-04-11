from random import randrange

import psycopg2
from confbd import host, user, password, db_name, port
from dispatcher import bot
from aiogram.dispatcher.filters import Text
from aiogram import types

from keyboards import kb_lookAnk

try:
    # connect
    connection = psycopg2.connect(
        host = host,
        port = port,
        user = user,
        password = password,
        dbname = db_name
    )
    with connection.cursor() as cursor:
        #cursor.execute(
        #    print(f"Select version: {cursor.fetchone()}" )
        #)

        pass
except Exception as _ex:
    print("{INFO} Error while working with PostreSQL", _ex)




class BotDB:

    def __init__(self, db_file):
        try:
            # connect
            self.conn = psycopg2.connect(
                host = host,
                port = port,
                user = user,
                password = password,
                dbname = db_name
            )
            self.cursor = self.conn.cursor()

        except Exception as _ex:
            print("{INFO} Error while working with PostreSQL", _ex)


    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        self.cursor.execute("SELECT id FROM public.users WHERE user_id = %s", (user_id,))
        #return bool(len(self.cursor.fetchone()[0]))
        return bool(len(self.cursor.fetchall()))



    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        self.cursor.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    def unget_user_id(self, id):
        """Достаем id юзера в базе по его user_id"""
        self.cursor.execute("SELECT user_id FROM users WHERE id = %s", (id,))
        return self.cursor.fetchone()[0]

    def add_user(self, user_id ):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO public.users (user_id) VALUES (%s)", (user_id,))
        return self.conn.commit()

    def user_take_polici(self, user_id, chat_id):
        self.cursor.execute("UPDATE public.users SET polici = True, chat_id = %s WHERE user_id = %s", (chat_id, user_id,))
        return self.conn.commit()

    def getUser_name(self, id):
        self.cursor.execute("SELECT chat_id FROM public.users WHERE user_id = %s", (self.unget_user_id(id),))
        return self.cursor.fetchone()[0]


    def add_record(self, user_id, name, age, description, sphere, photo, education, hobbie):

        """Проверяем, есть ли запись юзера"""
        self.cursor.execute("SELECT id FROM public.records WHERE users_id = %s", (self.get_user_id(user_id),))
        flag = bool(len(self.cursor.fetchall()))
        if flag:
            self.cursor.execute("UPDATE public.records SET name = %s, age = %s, decription = %s,sphere = %s,photo = %s, education = %s, hobbie = %s WHERE users_id = %s",
                                (name, age, description, sphere, photo,education,hobbie,  self.get_user_id(user_id)))
        else:
            """Создаем запись анкеты"""
            self.cursor.execute("INSERT INTO public.records (users_id, name, age, sphere, decription, photo,education,hobbie) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (self.get_user_id(user_id), name, age,  sphere, description, photo, education, hobbie))

        return self.conn.commit()


    def get_ank(self, user_id, message):
        """"Достаём юзера"""
        self.cursor.execute("SELECT * FROM public.records WHERE users_id = %s", (self.get_user_id(user_id),))
        feta = self.cursor.fetchone()
        name = feta [2]
        age = feta [3]
        spheres = feta [4]
        desqription = feta [5]
        photo = feta [6]
        education = feta [8]
        hobbie = feta [9]
        messageCap_template = """{name}, {age}\nHard skills: {spheres}\nSoft skills: {desqription}\nОбразование: {education}\nХобби: {hobbie}"""
        messageCap = messageCap_template.format(name=name, age=age, spheres=spheres, desqription=desqription, education=education, hobbie=hobbie)

        return bot.send_photo(message.from_user.id, photo, messageCap)



    def get_ankv(self, user_id, message):
        """"Достаём юзера"""
        self.cursor.execute("SELECT * FROM public.records WHERE users_id = %s", (self.get_user_id(user_id),))
        feta = self.cursor.fetchone()
        name = feta [2]
        age = feta [3]
        spheres = feta [4]
        desqription = feta [5]
        photo = feta [6]
        education = feta [8]
        hobbie = feta [9]
        messageCap_template = """{name}, {age}\nHard skills: {spheres}\nSoft skills: {desqription}\nОбразование: {education}\nХобби: {hobbie}"""
        messageCap = messageCap_template.format(name=name, age=age, spheres=spheres, desqription=desqription, education=education, hobbie=hobbie)

        return  bot.send_video(message.from_user.id, photo, caption = messageCap)

    def getfrengrecuest(self, user_id1, user_id2):
        self.cursor.execute("SELECT id FROM public.isfriend WHERE user_id1 = %s AND user_id2 = %s", (user_id1, self.get_user_id(user_id2)))
        fecha = self.cursor.fetchall()
        print(fecha)
        return bool(len(fecha))


    def finf_ank(self, user_id, message):
        self.cursor.execute("SELECT * FROM public.records WHERE users_id != %s", (self.get_user_id(user_id),))
        feta = self.cursor.fetchall()

        return feta


    def setlastankin(self, user_id1, user_id2):
        self.cursor.execute("UPDATE public.records SET lastank = %s WHERE users_id = %s",
                                (user_id2, self.get_user_id(user_id1)))
        return self.conn.commit()

    def getlastankin(self, user_id1):
        self.cursor.execute("SELECT lastank FROM public.records WHERE users_id = %s", [self.get_user_id(user_id1)])
        return self.cursor.fetchone()


    def tofriend(self, user_id1, user_id2):

        self.cursor.execute("INSERT INTO public.isfriend (user_id1,user_id2) VALUES (%s, %s)",
                            (self.get_user_id(user_id1),user_id2))

        self.conn.commit()
        """"Достаём юзера"""
        self.cursor.execute("SELECT * FROM public.records WHERE users_id = %s", (self.get_user_id(user_id1),))
        feta = self.cursor.fetchone()

        return feta


    def getRecFrend(self, user_id2, user_id1):
        self.cursor.execute("UPDATE public.isfriend SET is_frend = True WHERE user_id1 = %s AND user_id2 = %s", (user_id1, user_id2))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
