import requests
import telebot
from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession
from telebot import types # для указание типов
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("5678522382:AAEesuQUS9qppa5MIjPik_JyKAXuc-6uIAc")
gameStarted = False
users = {}
print("END")

side = ""
currentMatch = None


class User:
    def __init__(self, uid, name):
        global users
        self.user_id = uid
        self.status = "menu"
        self.points = 100
        self.name = name
        self.wins = 0
        self.lost = 0
        self.rating = None
        with open("user.txt", "w") as f:
            f.write(f'{uid};{name};{self.points}')

    def bet(self, msg, put_points, match):
        global side, currentMatch
        win_or_loss = False
        if users[msg.from_user.id].points < put_points:
            bot.send_message(msg.chat.id, f"Недостаточно очков. Баланс: {users[msg.from_user.id].points}", reply_markup=types.ReplyKeyboardRemove())
            users[msg.from_user.id].status = "vote"
        else:
            with open("transaction.txt", "a") as f:
                print(len(match))
                print(match[3])

                if side == 0 and match[3] == "True":
                    win_or_loss = True
                elif side == 1 and match[3] == "False":
                    win_or_loss = True
                if not(win_or_loss):
                    users[msg.from_user.id].points -= put_points
                    f.write(f'{msg.from_user.id};{self.points};{put_points};{side}{win_or_loss}')
                    bot.send_message(msg.chat.id, f"@{self.name}, вы поставили {put_points} и проиграли. Баланс: {users[msg.from_user.id].points}", reply_markup=types.ReplyKeyboardRemove())
                    self.lost += 1
                else:
                    users[msg.from_user.id].points += (2 * put_points)
                    f.write(f'{msg.from_user.id};{self.points};{put_points};{side}{win_or_loss}')
                    bot.send_message(msg.chat.id, f"@{self.name}, вы поставили {put_points} и победили. Баланс: {users[msg.from_user.id].points}", reply_markup=types.ReplyKeyboardRemove())
                    self.wins += 1

                bot.send_message(msg.chat.id, f"@{self.name}, спасибо, что играете в нашу игру!!!")

        side = None
        currentMatch = None
        win_or_loss = False

    def get_status(self):
        return self.status


match = ""
matchesDict = {}
with open("matches.txt", "r") as f:
    f = f.read()
    f = f.split("\n")
    for row in f:
        row.split(";")
        print(row)

usr = None
print(matchesDict)
msg = None
message_id_bot = 0


@bot.message_handler(content_types=["text"])
def main_text_logic(mesg):
    global match, currentMatch, users, msg, message_id_bot, usr
    msg = mesg
    if msg.from_user.id not in users:
        users[msg.from_user.id] = User(msg.from_user.id, msg.from_user.first_name)
    print(users[msg.from_user.id].user_id, users[msg.from_user.id].points, users[msg.from_user.id].status)
    usr = User(msg.from_user.id, msg.from_user.first_name)
    if "@dota2predict" in msg.text.lower():
        print(msg.text)
        markup1 = InlineKeyboardMarkup()
        btn4 = InlineKeyboardButton('Рейтинг', callback_data='Rating')
        btn5 = InlineKeyboardButton('Поставить на матч', callback_data='Play')
        btn6 = InlineKeyboardButton('Баланс', callback_data='Balance')

        markup1.row(btn4, btn6)
        markup1.row(btn5)
        message_id_bot = bot.send_message(msg.chat.id, f"Здравствуйте, {msg.from_user.first_name}. Хотите поставить на матч?", reply_markup=markup1)
        # users[msg.from_user.id].status = "wait"
    # if users[msg.from_user.id].status == "wait":
    #     if msg.text == "Поставить очки":
    #         with open("matches.txt", "r") as f:
    #             f = f.read().split("\n")
    #             match = f[0].split(';')
    #             time.sleep(3)
    #             print(match)
    #             currentMatch = match[0]
    #             direThis1 = match[2][1:-1].split(", ")
    #             direThis = [i[1:-1] for i in direThis1]
    #             radiantThis1 = match[1][1:-1].split(", ")
    #             radiantThis = [i[1:-1] for i in radiantThis1]
    #             print(radiantThis, direThis)
    #             bot.edit_message_text(chat_id = message_id_bot.chat.id, message_id = message_id_bot.message_id,
    #                                   text=f'@{msg.from_user.first_name} \nRadiant: {", ".join(radiantThis)}\nDire: {", ".join(direThis)}\n',reply_markup=types.ReplyKeyboardRemove())
    #             markup = InlineKeyboardMarkup()
    #             btn1 = InlineKeyboardButton('bet Radiant', callback_data='btn1')
    #             btn2 = InlineKeyboardButton('Вернуться!', callback_data='btn2')
    #             btn3 = InlineKeyboardButton('bet Dire', callback_data='btn3')
    #
    #             markup.row(btn1, btn3)
    #             markup.row(btn2)
    #             time.sleep(2)
    #             bot.edit_message_text(chat_id = message_id_bot.chat.id, message_id = message_id_bot.message_id,
    #                                   text= f'@{msg.from_user.first_name} \nВыберите команду, которая победит\nЧтобы это сделать введите <bet Radiant> или <bet Dire> без ковычек', reply_markup=markup)
    #             users[msg.from_user.id].status = "vote"
    if users[msg.from_user.id].status == "bet":
        play(msg, usr, match)


def play(msg, usr, match):
    if msg.text.isdigit():
        stavka = int(msg.text)
        print(usr.bet(msg, stavka, match))
        users[msg.from_user.id].status = "menu"





@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global users, side, msg, message_id_bot, usr, match, currentMatch
    if call.data == 'btn1':
        side = 0
        bot.edit_message_text(chat_id = message_id_bot.chat.id, message_id = message_id_bot.message_id, text= f"@{msg.from_user.first_name}, введите колличество очков")
        users[msg.from_user.id].status = "bet"
    elif call.data == 'btn2':
        bot.edit_message_text(chat_id=message_id_bot.chat.id, message_id=message_id_bot.message_id,
                              text=f"@{msg.from_user.first_name}, вы выбрали вернуться назад")
        users[msg.from_user.id].status = "menu"
    elif call.data == 'btn3':
        side = 1
        bot.edit_message_text(chat_id = message_id_bot.chat.id, message_id = message_id_bot.message_id, text= f"@{msg.from_user.first_name}, введите колличество очков")
        users[msg.from_user.id].status = "bet"
    elif call.data == "Balance":
        time.sleep(5)
        bot.edit_message_text(chat_id=message_id_bot.chat.id, message_id=message_id_bot.message_id,
                              text=f"@{msg.from_user.first_name}, Баланс: {usr.points}")
    elif call.data == "Play":
        with open("matches.txt", "r") as f:
            f = f.read().split("\n")
            match = f[0].split(';')
            time.sleep(10)
            print(match)
            currentMatch = match[0]
            direThis1 = match[2][1:-1].split(", ")
            direThis = [i[1:-1] for i in direThis1]
            radiantThis1 = match[1][1:-1].split(", ")
            radiantThis = [i[1:-1] for i in radiantThis1]
            print(radiantThis, direThis)
            bot.edit_message_text(chat_id=message_id_bot.chat.id, message_id=message_id_bot.message_id,
                                  text=f'@{msg.from_user.first_name} \nRadiant: {", ".join(radiantThis)}\nDire: {", ".join(direThis)}\n')
            markup = InlineKeyboardMarkup()
            btn1 = InlineKeyboardButton('bet Radiant', callback_data='btn1')
            btn2 = InlineKeyboardButton('Вернуться!', callback_data='btn2')
            btn3 = InlineKeyboardButton('bet Dire', callback_data='btn3')

            markup.row(btn1, btn3)
            markup.row(btn2)

            bot.edit_message_text(chat_id=message_id_bot.chat.id, message_id=message_id_bot.message_id,
                                  text=f'@{msg.from_user.first_name} \nВыберите команду, которая победит\nЧтобы это сделать введите <bet Radiant> или <bet Dire> без ковычек',
                                  reply_markup=markup)
            users[msg.from_user.id].status = "vote"
    elif call.data == "Рейтинг":
        pass


bot.polling(none_stop=True, interval=0)

# button1 = InlineKeyboardButton('Кнопка 1', callback_data='button1')
# button2 = InlineKeyboardButton('Кнопка 2', callback_data='button2')
# button3 = InlineKeyboardButton('Кнопка 3', callback_data='button3')
# button4 = InlineKeyboardButton('Кнопка 4', callback_data='button4')
#
# markup = InlineKeyboardMarkup()
# markup.row(button1, button2)
# markup.row(button3, button4)