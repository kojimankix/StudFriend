from random import randrange
from aiogram.utils.markdown import link


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram import dispatcher
from aiogram.utils.markdown import hide_link

from dispatcher import dp, bot
import config
import re
from keyboards.client_kb import kb_inAnk, kb_fromAnk, kb_lookAnk, kb_sogl, urlkb
from bot import BotDB
import json
import string


lastank = 0

class FSMstart(StatesGroup):
    starting = State()
    helouing = State()

# КЛАСС ДЛЯ СОСТОЯНИЯ РЕГИСТРАЦИИ АНКЕТЫ
class FSMreg(StatesGroup):
    name = State()
    age = State()
    photo = State()
    spheres = State()
    desqription = State()
    education = State()
    hobbie = State()

class FSMlike(StatesGroup):
    fLike = State()

class FSMlook(StatesGroup):
    looking = State()
    messaging = State()

#@dp.message_handler(commands = "pp")
#async def asd(message: types.Message):
#    await FSMlike.fLike.set()
#    await message.answer("Твоя анкета кому-то понравилась! ")
#    await message.answer("Анкета кого-то", reply_markup=kb_inAnk)


#@dp.message_handler(state=FSMlike.fLike)
#async def getADS(message: types.Message, state: FSMlike):
#    if message.text == "🤝":
#        await message.answer("Хорошо пообщаться вам!(%s)", message.from_user.full_name)
#        messageCap_template = """Хорошо пообщаться вам! {name}"""
#        lastankasd = BotDB.getlastankin(message.from_user.id)
#        foruser = BotDB.getRecFrend(message.from_user.id, lastankasd)
#        messageCap = messageCap_template.format(name=message.from_user.full_name)
#        await bot.send_message(foruser, messageCap)
#
#    if message.text == "👎":
#        await message.answer("Поищем ещё людей")
#    await state.finish()
#    await FSMlook.looking.set()
#    await message.answer("Чья-то анкета", reply_markup=kb_lookAnk)

# ХЭНДЛЕР ДЛЯ ОТМЕНЫ
@dp.message_handler(state="*", commands = "отмена")
@dp.message_handler(Text(equals='Отмена', ignore_case = True), state="*")
async def cancelHandler(message: types.Message, state: FSMreg):
    curent_state = await state.get_state()
    if curent_state is None:
        return
    await state.finish()
    await message.reply("ОК")
async def cancelHandler2(message: types.Message, state: FSMlike):
    curent_state = await state.get_state()
    if curent_state is None:
        return
    await state.finish()
    await message.reply("ОК")

@dp.message_handler(state=FSMlike.fLike)
@dp.message_handler(Text(equals="🤝"), state=FSMlook.looking)
@dp.message_handler(Text(equals="👎"), state=FSMlook.looking)
@dp.message_handler(Text(equals="Смотреть анкеты"), state=None)
async def lookAnks(message: types.Message):
    if message.text == "🤝":
        lastankasd = BotDB.getlastankin(message.from_user.id)
        if(not BotDB.getfrengrecuest(lastankasd, message.from_user.id)):
            #метод для добавления

            feta = BotDB.tofriend(message.from_user.id, lastankasd)

            name = feta [2]
            age = feta [3]
            spheres = feta [4]
            desqription = feta [5]
            photo = feta [6]
            education = feta [8]
            hobbie = feta [9]
            messageCap_template = """{name}, {age}\nHard skills: {spheres}\nSoft skills: {desqription}\nОбразование: {education}\nХобби: {hobbie}"""
            messageCap = messageCap_template.format(name=name, age=age, spheres=spheres, desqription=desqription, education=education, hobbie=hobbie)


            tsel_user = BotDB.unget_user_id(lastankasd)
            await bot.send_message(tsel_user, "Твоя анкета кому-то понравилась!")

            state = dp.current_state(chat=tsel_user, user=tsel_user)
            await state.set_state(FSMlook.looking)


            try:
                await bot.send_photo(tsel_user, photo, messageCap,     reply_markup=kb_inAnk)
            except:
                print("не робит фото")
            try:
                await bot.send_video(tsel_user, photo, caption = messageCap,     reply_markup=kb_inAnk)
            except:
                print("не робит видео")

            BotDB.setlastankin(BotDB.unget_user_id(lastankasd), BotDB.get_user_id(message.from_user.id))

            await message.reply('Предложение дружить отправлено\nЖдите ответа')
        else:
            #добавление в др
            await message.answer("Ваше желание дружить взаимно!")
            messageCap = hide_link('tg://user?id=753623377')

            #messageCap_template = '<a href="tg://user?id={user_id}">Имя</a>'
            #messageCap = messageCap_template.format(user_id = BotDB.unget_user_id(lastankasd))
            messageCap_template = '@{username}'
            messageCap = messageCap_template.format(username = BotDB.getUser_name(lastankasd))

            await message.answer(messageCap)
            await message.answer('Хорошо пообщаться вам!')
            #messageCap_template = """Хорошо пообщаться вам! {name}"""
            BotDB.getRecFrend(message.from_user.id, lastankasd)
            #messageCap = messageCap_template.format(name=message.from_user.full_name)
            #await bot.send_message(foruser, messageCap)

    await FSMlook.looking.set()

    feta = BotDB.finf_ank(message.from_user.id, message)
    long = len(feta)
    ank = randrange(0, long)

    BotDB.setlastankin(message.from_user.id, feta[ank][1])
    name = feta [ank][2]
    age = feta [ank][3]
    spheres = feta [ank][4]
    desqription = feta [ank][5]
    photo = feta [ank][6]
    education = feta [ank][8]
    hobbie = feta [ank][9]


    messageCap_template = """{name}, {age}\nHard skills: {spheres}\nSoft skills: {desqription}\nОбразование: {education}\nХобби: {hobbie}"""
    messageCap = messageCap_template.format(name=name, age=age, spheres=spheres, desqription=desqription, education=education, hobbie=hobbie)

    try:
        await bot.send_photo(message.from_user.id, photo, messageCap,     reply_markup=kb_lookAnk)
    except:
        print("не робит фото")
    try:
        await bot.send_video(message.from_user.id, photo, caption = messageCap,     reply_markup=kb_lookAnk)
    except:
        print("не робит видео")



#@dp.message_handler(Text(equals="💌"), state=FSMlook.looking)
#async def looPerskAnk(message: types.Message, state: FSMlook):
#    await message.reply('Напишите сообщение для пользователя', reply_markup=None)
#    await FSMlook.next()



#@dp.message_handler(state=FSMlook.messaging)
#async def read(message: types.Message):
#    if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')} \
#            .intersection(set(json.load(open('NL/nl.json')))) != set():
#        await message.reply('Маты запрещены!')
#        await message.delete()
#    else:
#        await message.reply('Сообщение отправлено\nЖдите ответа')
#        await FSMlook.looking.set()
#        await message.answer("Чья-то анкета", reply_markup=kb_lookAnk)


#@dp.message_handler(Text(equals="👎"), state=FSMlook.looking)
#async def looPerskAnk(message: types.Message, state=FSMlook):
#    #Следущая анкета
#    await message.answer("Чья-то анкета", reply_markup=kb_lookAnk)

@dp.message_handler(Text(equals="💤"), state=FSMlook.looking)
async def looPerskAnk(message: types.Message, state=FSMlook):
    await message.answer("Твоя анкета выглядит вот так:", reply_markup=kb_fromAnk)
    try:
        await BotDB.get_ank(message.from_user.id, message)
    except:
        print("не робит фото")
    try:
        await BotDB.get_ankv(message.from_user.id, message)
    except:
        print("не робит видео")
    await state.finish()


# ХЭНДЛЕРЫ ДЛЯ СОСТОЯНИЯ РЕГИСТРАЦИИ АНКЕТЫ
@dp.message_handler(Text(equals="Заполнить анкету заново"), state=None)
async def st(message: types.Message):
    await FSMreg.name.set()
    await message.answer("Как тебя зовут?")

@dp.message_handler(state=FSMreg.name)
async def getName(message: types.Message, state: FSMreg):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMreg.next()
    await message.answer("Сколько тебе лет?")

@dp.message_handler(state=FSMreg.age)
async def getAge(message: types.Message, state: FSMreg):
    try:
        if int(message.text) < 16:
            await message.answer("Тебе должно быть больше 16-ти лет")
        if int(message.text) > 122:
            await message.answer("Тебе не может быть больше лет, чем старейшим из когда-либо живших на Земле людей!")
        else:
            if int(message.text) >= 16:
                async with state.proxy() as data:
                    data['age'] = message.text
                await FSMreg.next()
                await message.answer("Пришли своё фото или видео")
    except:
        await message.answer("Введи пожалуйста корректный возраст")

@dp.message_handler(content_types=['video'], state=FSMreg.photo)
async def getPhoto(message: types.Message, state: FSMreg):
    async with state.proxy() as data:
        data['photo'] = message.video.file_id
    await FSMreg.next()
    await message.answer("Напиши, что ты умеешь? (hard skills)")


@dp.message_handler(content_types=['photo'], state=FSMreg.photo)
async def getPhoto(message: types.Message, state: FSMreg):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMreg.next()
    await message.answer("Напиши, что ты умеешь? (hard skills)")

@dp.message_handler(state=FSMreg.photo)
async def getPhoto(message: types.Message, state: FSMreg):
    await message.answer("Отправь ")


@dp.message_handler(state=FSMreg.spheres)
async def getSpheres(message: types.Message, state: FSMreg):
    async with state.proxy() as data:
        data['spheres'] = message.text
    await FSMreg.next()
    await message.answer("Расскажи о своих Soft skills")






@dp.message_handler(state=FSMreg.desqription)
async def getDesqr(message: types.Message, state: FSMreg):
    mesamesa = message
    async with state.proxy() as data:
        data['desqription'] = message.text
    await FSMreg.next()
    await message.answer("Какой твой уровень образования?")


@dp.message_handler(state=FSMreg.education)
async def getSpheres(message: types.Message, state: FSMreg):
    async with state.proxy() as data:
        data['education'] = message.text
    await FSMreg.next()
    await message.answer("Какие твои хобби и интересы?")


@dp.message_handler(state=FSMreg.hobbie)
async def getSpheres(message: types.Message, state: FSMreg):
    async with state.proxy() as data:
        data['hobbie'] = message.text

    await message.answer("Твоя анкета выглядит вот так:")
    #await message.answer(data['name'], data['age'], data['spheres'], data['desqription'])
    #await message.answer("Имя", data['name'], ", ", data['age'], " лет. \n ", data['spheres'], "\n", data['desqription'])
    BotDB.add_record(message.from_user.id, data['name'], data['age'], data['spheres'], data['desqription'], data['photo'],data['education'],data['hobbie'] )
    name = data['name']
    age = data['age']
    spheres = data['spheres']
    desqription = data['desqription']
    education = data['education']
    hobbie = data['hobbie']
    messageCap_template = """{name}, {age}\nHard skills: {spheres}\nSoft skills: {desqription}\nОбразование: {education}\nХобби: {hobbie}"""
    messageCap = messageCap_template.format(name=name, age=age, spheres=spheres, desqription=desqription, education=education, hobbie=hobbie)

    try:
        await bot.send_photo(message.from_user.id, data['photo'], messageCap)
    except:
        print("не робит фото")
    try:
        await bot.send_video(message.from_user.id, data['photo'], caption = messageCap)
    except:
        print("не робит видео")


    await message.answer("Рад познакомиться!", reply_markup=kb_fromAnk)
    await state.finish()




# ХЭНДЛЕР СТАРТА
@dp.message_handler(commands = "start")
async def helouing(message: types.Message):
    await FSMstart.starting.set()
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать! Я умный бот написанный на Python. "
                                                         "Моя цель - свести тебя с нужными людьми.", reply_markup=kb_sogl)
    await message.answer("Для начала, тебе необходимо принять пользовательское соглашение", reply_markup=urlkb)
    await FSMstart.next()

@dp.message_handler(Text(equals="Принять пользовательское соглашение"),state=FSMstart.helouing)
async def start(message: types.Message, state = FSMstart):
    chat_id = message.from_user.username
    BotDB.user_take_polici(message.from_user.id, chat_id)
    await state.finish()
    await FSMreg.name.set()
    await message.answer("Теперь, давай познакомимся!\nКак тебя зовут?")

# ХЭНДЛЕР ЛЮБОГО ВВОДА
@dp.message_handler()
async def read(message: types.Message):
        if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')}\
            .intersection(set(json.load(open('NL/nl.json')))) != set():
            await message.reply('Маты запрещены!')
            await message.delete()

