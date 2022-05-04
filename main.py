import sqlite3
import requests
import telebot
from telebot import types

import config
import SDapi


bot = telebot.TeleBot(config.TG_token)
connectDB = sqlite3.connect('tg_sg_bd.db', check_same_thread=False)
cursor = connectDB.cursor()

def tokenSDforUser(user_id):
    cursor.execute("SELECT user_token_sd FROM user WHERE user_tg_id = ?", (user_id,))
    usTokenSD = cursor.fetchall()
    connectDB.commit()
    return (usTokenSD[0][0])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/registration")
    btn2 = types.KeyboardButton("Список моих открытых заявок")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="""\
    Привет {0.first_name}!\
    Это bot отдела helpdesk в МШУ Сколково.\
    Сотрудники отдела могут управлять заявками.\
    """.format(message.from_user), reply_markup=markup)
    user_data = message.chat.id,message.from_user.id,message.from_user.first_name,message.from_user.last_name,message.from_user.username
    cursor.execute("INSERT OR IGNORE INTO user (user_tg_id,user_chat_id,user_name,user_surname,user_username) VALUES (?,?,?,?,?)",user_data)
    connectDB.commit()

@bot.message_handler(commands=['registration'])
def registration_sd(message):
    mesg = bot.send_message(message.chat.id, text="Напиши свой API key от Service Desk")
    bot.register_next_step_handler(mesg, add_SDapi)

def add_SDapi(message):
    user_data = message.text, message.from_user.id
    cursor.execute("UPDATE user SET user_token_sd = ? WHERE user_tg_id = ?", user_data)
    connectDB.commit()


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def message_processing(message):
    if message.text == 'Список моих открытых заявок':
        SD_open_requests = SDapi.my_open_request(tokenSDforUser(message.from_user.id))
        markup = telebot.types.InlineKeyboardMarkup()

        for i in range(len(SD_open_requests)):
            markup.add(telebot.types.InlineKeyboardButton(text=f'{SD_open_requests[i][0]} : {SD_open_requests[i][2]}', callback_data=f"{SD_open_requests[i][0]}"))
        bot.send_message(message.chat.id, "Открытые заяки helpdesk",reply_markup=markup )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
            bot.send_message(call.message.chat.id, f'{call.message}')


bot.infinity_polling()


