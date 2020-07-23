import telebot
from telebot import types
import sqlite3
from sqlite3 import Error
from time import sleep, ctime

bot = telebot.TeleBot('ввести токен')

print('START')


# Добавление юзернэйма в базу данных по команде /reg
def post_sql_query(sql_query):
    with sqlite3.connect('my.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
    return result


def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS USERS (user_id INTEGER PRIMARY KEY NOT NULL, username TEXT, 
    first_name TEXT, last_name TEXT, reg_date TEXT); '''
    post_sql_query(users_query)


def register_user(user, username, first_name, last_name):
    user_check_query = f'SELECT * FROM USERS WHERE user_id = {user};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO USERS (user_id, username, first_name,  last_name, reg_date) VALUES ({user}, "{username}", "{first_name}", "{last_name}", "{ctime()}");'
        post_sql_query(insert_to_db_query)
        create_tables()


@bot.message_handler(commands=['reg'])
def reg(message):
    register_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                  message.from_user.last_name)
    bot.send_message(message.from_user.id,
                     f'Добро пожаловать  {message.from_user.first_name}.\n Вы успешно зарегестрированы в моей БАЗЕ')


# связь с разработчиком
@bot.message_handler(commands=['developer'])
def developer(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Написать Разработчику в ВК", url="https://vk.com/d.otzgig"))
    markup.add(types.InlineKeyboardButton("Написать Разработчику в Telegram", url="https://t.me/MrRobot2033"))
    bot.send_message(
        message.chat.id,
        "Нажмите на кнопку ниже чтобы написать разработчику",
        parse_mode='html',
        reply_markup=markup
    )


# по команде /home юзер переходит на главную
@bot.message_handler(commands=['home'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('Игровые каналы')
    btn2 = types.KeyboardButton('IT каналы')
    btn3 = types.KeyboardButton('Другие каналы')
    btn4 = types.KeyboardButton('Каналы в Telegram')
    markup.add(btn1, btn2, btn3, btn4)
    send_mess = f"<b>Привет {message.from_user.first_name} {message.from_user.last_name}</b>!\nВыбери что тебя " \
                f"интересует: "
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


# обработчик кнопок
@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()

    if get_message_bot == "главная":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Игровые каналы')
        btn2 = types.KeyboardButton('IT каналы')
        btn3 = types.KeyboardButton('Другие каналы')
        btn4 = types.KeyboardButton('Каналы в Telegram')
        markup.add(btn1, btn2, btn3, btn4)
        final_message = "Выбирай, что тебя интересует"
    # игровые каналы
    elif get_message_bot == "игровые каналы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Warface')
        btn2 = types.KeyboardButton('Call of Duty Warzone')
        btn3 = types.KeyboardButton('STALKER')
        btn4 = types.KeyboardButton('Другие игры')
        btn5 = types.KeyboardButton('Главная')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        final_message = "Выбирай:"
    # если из каналов выбран тип каналов, делаем elif-ами
    elif get_message_bot == "warface":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("X-Medium", url="https://www.youtube.com/user/TheXmedium"))
        markup.add(types.InlineKeyboardButton("Мортид Ракутагин", url="https://www.youtube.com/user/mortidgames"))
        markup.add(types.InlineKeyboardButton("Дмитрий Крымский", url="https://www.youtube.com/user/StarGameWF"))
        markup.add(
            types.InlineKeyboardButton("Пираний", url="https://www.youtube.com/channel/UC_m4fuvI139NacUMfp5hIsA"))
        final_message = "👇🏻Рекомендую имеено эти каналы по игре Warface👇🏻"

    elif get_message_bot == "call of duty warzone":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("SHIMOROSHOW", url="https://www.youtube.com/user/shimoroshow"))
        markup.add(
            types.InlineKeyboardButton("BULLSEYE", url="https://www.youtube.com/channel/UCTQYEoylQHYGVT7JmN456nQ"))
        markup.add(
            types.InlineKeyboardButton("Ракутагин", url="https://www.youtube.com/channel/UCouRWTJRIZHZrLakWWqeBTQ"))
        final_message = "Рекомендую имеено эти каналы по игре Call of Duty Warzone"

    elif get_message_bot == "stalker":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Дмитрий Бэйл", url="https://www.youtube.com/channel/UCcAQJDkK-Xf-YGCGAdAY3Ig"))
        markup.add(types.InlineKeyboardButton("HugTV", url="https://www.youtube.com/channel/UC6NfOqNQUXZ3DsljUF0N6Zw"))
        markup.add(
            types.InlineKeyboardButton("GamePlayerRUS", url="https://www.youtube.com/channel/UC3XK_66wYwAyFf-9N07DK6g"))
        markup.add(
            types.InlineKeyboardButton("Ракутагин", url="https://www.youtube.com/channel/UCouRWTJRIZHZrLakWWqeBTQ"))
        final_message = "👇🏻Рекомендую имеено эти каналы по игре Stalker👇🏻"

    elif get_message_bot == "другие игры":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Дмитрий Бэйл", url="https://www.youtube.com/channel/UCcAQJDkK-Xf-YGCGAdAY3Ig"))
        markup.add(types.InlineKeyboardButton("SHIMOROSHOW", url="https://www.youtube.com/user/shimoroshow"))
        markup.add(
            types.InlineKeyboardButton("GamePlayerRUS", url="https://www.youtube.com/channel/UC3XK_66wYwAyFf-9N07DK6g"))
        markup.add(
            types.InlineKeyboardButton("Ракутагин", url="https://www.youtube.com/channel/UCouRWTJRIZHZrLakWWqeBTQ"))
        final_message = "👇🏻Вот блогеры, которых  рекомендую к просмотру👇🏻"
    # it каналы на ютуб
    elif get_message_bot == "it каналы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Python&Framework')
        btn2 = types.KeyboardButton('Верстка')
        btn3 = types.KeyboardButton('Информационная Безопастность')
        btn4 = types.KeyboardButton('Главная')
        markup.add(btn1, btn2, btn3, btn4)
        final_message = "Выбирай:"

    elif get_message_bot == "python&framework":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Диджитализируй!",
                                              url="https://www.youtube.com/channel/UC9MK8SybZcrHR3CUV4NMy2g"))
        markup.add(
            types.InlineKeyboardButton("Django School", url="https://www.youtube.com/channel/UC_hPYclmFCIENpMUHpPY8FQ"))
        markup.add(types.InlineKeyboardButton("IT каждый день",
                                              url="https://www.youtube.com/channel/UCAlRksF5338XmSMbwS3W7eA"))
        markup.add(
            types.InlineKeyboardButton("IT Hobbies", url="https://www.youtube.com/channel/UCXE4vvggmw3gpu59D-QSLjA"))
        markup.add(
            types.InlineKeyboardButton("Be Geek", url="https://www.youtube.com/channel/UCFXNO8bEhII2ocwsqgaMVZg"))
        markup.add(
            types.InlineKeyboardButton("Physics is Simple", url="https://www.youtube.com/channel/UCOR3MdR9iXj5jDuXefRwNAg"))
        final_message = "👇🏻Вот блогеры, которых  рекомендую к просмотру👇🏻"

    elif get_message_bot == "верстка":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("ВЕРСТАЧ", url="https://www.youtube.com/channel/UC5iRISBYuE3fdhPLfyzNkFQ"))
        markup.add(types.InlineKeyboardButton("Web Developer Blog",
                                              url="https://www.youtube.com/channel/UCe_H8hzx9WV7Ca7Ps5gt72Q"))
        markup.add(types.InlineKeyboardButton("WebForMySelf", url="https://www.youtube.com/user/webformyself/videos"))
        final_message = "👇🏻Вот блогеры, которых  рекомендую к просмотру👇🏻"

    elif get_message_bot == "информационная безопастность":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("UnderMind", url="https://www.youtube.com/channel/UCHo0495AAlj-dinGYf96Liw"))
        markup.add(types.InlineKeyboardButton("Чёрный Треугольник",
                                              url="https://www.youtube.com/channel/UCZ26MoNJKaGXFQWKuGVzmAg"))
        markup.add(
            types.InlineKeyboardButton("overbafer1", url="https://www.youtube.com/channel/UCspfe9lef7ApJaHQsOcPC1A"))
        markup.add(types.InlineKeyboardButton("Pulse", url="https://www.youtube.com/channel/UCojEUrPvEvkUXEU3QWwhCwg"))
        final_message = "👇🏻Вот блогеры, которых  рекомендую к просмотру👇🏻"

    elif get_message_bot == "другие каналы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Мой ТОП каналов')
        btn2 = types.KeyboardButton('Главная')
        markup.add(btn1, btn2)
        final_message = "Выбирай:"

    elif get_message_bot == "мой топ каналов":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("ROCK PRIVET", url="https://www.youtube.com/channel/UCaSstk9SM0Yi1sUcj11M_fA"))
        markup.add(
            types.InlineKeyboardButton("RADIO TAPOK", url="https://www.youtube.com/channel/UCYfYQ1lmPwPdxjBpW_rMJ7w"))
        markup.add(
            types.InlineKeyboardButton("Corey Taylor", url="https://www.youtube.com/channel/UCLQ1zmTPoqXZ6Vk0LVtQvkg"))
        markup.add(
            types.InlineKeyboardButton("notebook-31", url="https://www.youtube.com/channel/UCR1HSvPGgweMlKoHRkSkwjw"))
        markup.add(
            types.InlineKeyboardButton("PilotZX6R", url="https://www.youtube.com/channel/UCL-nbxU92PJiCfCJLFMQ6OA"))
        markup.add(types.InlineKeyboardButton("Видео от SoLiDa",
                                              url="https://www.youtube.com/channel/UCd72TnBJrgjj631Ajk2Nf7w"))
        markup.add(
            types.InlineKeyboardButton("AlexGyver", url="https://www.youtube.com/channel/UCgtAOyEQdAyjvm9ATCi_Aig"))
        markup.add(types.InlineKeyboardButton("SHIFU", url="https://www.youtube.com/channel/UCKvwrpqUvFNRinpTFouLLiQ"))
        markup.add(
            types.InlineKeyboardButton("Bonn Factory", url="https://www.youtube.com/channel/UCbR7t2EsutYbTG4p4b6L8tg"))
        markup.add(
            types.InlineKeyboardButton("SteelWood", url="https://www.youtube.com/channel/UCTpxthLF5mGs1FlefDjyBqw"))
        markup.add(types.InlineKeyboardButton("Левша", url="https://www.youtube.com/channel/UCQpBYQ0FkiKQju94WX1yveQ"))
        markup.add(types.InlineKeyboardButton("DreadCraftStation",
                                              url="https://www.youtube.com/channel/UC7MqkxmKYoxir8GorWg00wQ"))
        markup.add(types.InlineKeyboardButton("Serega Otvertka",
                                              url="https://www.youtube.com/channel/UCYVnuzrfrXHJ3Px3C9MKm3g"))
        markup.add(
            types.InlineKeyboardButton("SuperCrastan", url="https://www.youtube.com/channel/UCXFxgPppcehs2LoiKhkakQg"))
        markup.add(
            types.InlineKeyboardButton("Даня Крастер", url="https://www.youtube.com/channel/UCt34mT-socRqtiY9iO_LzYQ"))
        markup.add(types.InlineKeyboardButton("abvgat", url="https://www.youtube.com/channel/UC9QCSnXY8JR32jYNUVU8rgA"))
        markup.add(
            types.InlineKeyboardButton("abvgatstvo", url="https://www.youtube.com/channel/UCB739QvXJrU9zbFEqcV7oxA"))
        markup.add(types.InlineKeyboardButton("Bushcraft34RUS",
                                              url="https://www.youtube.com/channel/UCGhnOXbS-lw5GWow9bk8rbg"))
        final_message = "👇🏻Вот блогеры, которых  рекомендую к просмотру👇🏻"

    elif get_message_bot == "каналы в telegram":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Мои каналы')
        btn2 = types.KeyboardButton('Мои подписки')
        btn3 = types.KeyboardButton('Главная')
        markup.add(btn1, btn2, btn3)
        final_message = "Выбирай:"

    elif get_message_bot == "мои каналы":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Мой канал №1(ИБ)", url="https://t.me/hacktest2033"))
        markup.add(types.InlineKeyboardButton("Мой канал №2(develop)", url="https://t.me/develop_python_ub"))
        final_message = "Переходи на мои каналы в Telegram"

    elif get_message_bot == "мои подписки":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("LAMERLAND - overbafer1", url="https://t.me/overlamer1"))
        markup.add(types.InlineKeyboardButton("NIGHT_OWL", url="https://t.me/Nigh_Owl"))
        markup.add(types.InlineKeyboardButton("PulSe", url="https://t.me/Pulsechanel"))
        markup.add(types.InlineKeyboardButton("Termux - one", url="https://t.me/Termuxtop"))
        markup.add(types.InlineKeyboardButton("Kali Linux (ru)", url="https://t.me/kali_linux_ru"))
        markup.add(types.InlineKeyboardButton("IT каждый день", url="https://t.me/it_everyday"))
        final_message = "Переходи на каналы и прокачай свой СКИЛЛ"
    # Здесь различные дополнительные проверки и условия

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('Игровые каналы на YouTube')
        btn2 = types.KeyboardButton('IT каналы на YouTube')
        btn3 = types.KeyboardButton('Другие каналы на YouTube')
        btn4 = types.KeyboardButton('Каналы в Telegram')
        markup.add(btn1, btn2, btn3, btn4)
        final_message = "Так, так, так\nПостой, лучше нажми на одну из интерактивных кнопок ниже или напиши слэш /"

    bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)


bot.polling(none_stop=True)

print('\n#\n#\n#\nSTOP')
