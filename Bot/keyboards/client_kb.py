from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup



b1 = KeyboardButton('Заполнить анкету заново')
b2 = KeyboardButton('Смотреть анкеты')
kb_fromAnk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
kb_fromAnk.add(b1).add(b2)

b3 = KeyboardButton('Продолжить просмотр анкет')
kb_pAnk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
kb_pAnk.add(b3)

b4 = KeyboardButton('🤝')
b5 = KeyboardButton('👎')

kb_inAnk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
kb_inAnk.row(b4, b5)

b6 = KeyboardButton('🤝')
b7 = KeyboardButton('💌')
b8 = KeyboardButton('👎')
b9 = KeyboardButton('💤')

kb_lookAnk = ReplyKeyboardMarkup(resize_keyboard=True)
kb_lookAnk.row(b6,  b8, b9)

urlkb = InlineKeyboardMarkup(row_width=1)
b0 = InlineKeyboardButton(text='Пользовательское соглашение 📄', url='https://docs.google.com/document/d/1mU_R-XNRl6wMNHHdkUrPbnpkRbMMdUC-rIv1Kt8X-vA/edit?usp=sharing') #url='https://disk.yandex.ru/i/inCyGq2QsFme9Q'
urlkb.add(b0)

b10 = KeyboardButton('Принять пользовательское соглашение')
kb_sogl = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
kb_sogl.add(b10)