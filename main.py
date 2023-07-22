import requests
import telebot
from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession
from telebot import types # для указание типов
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("5678522382:AAEtQYOYSChWrI-1mItc0H6_Fq4MsLlgpAM")
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


print(matchesDict)

@bot.message_handler(content_types=["text"])
def main_text_logic(msg):
    global match, currentMatch, users
    if msg.from_user.id not in users:
        users[msg.from_user.id] = User(msg.from_user.id, msg.from_user.first_name)
    print(users[msg.from_user.id].user_id, users[msg.from_user.id].points, users[msg.from_user.id].status)
    usr = User(msg.from_user.id, msg.from_user.first_name)
    if "@dota2predict" in msg.text.lower():
        print(msg.text)
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Поставить очки")
        btn2 = types.KeyboardButton("Баланс")
        btn3 = types.KeyboardButton("Рейтинг")
        markup1.add(btn3, btn1, btn2)
        bot.send_message(msg.chat.id, f"Здравствуйте, {msg.from_user.first_name}. Хотите поставить на матч?", reply_markup=markup1)
        users[msg.from_user.id].status = "wait"
    if users[msg.from_user.id].status == "wait":
        if msg.text == "Поставить очки":
            with open("matches.txt", "r") as f:
                f = f.read().split("\n")
                match = f[0].split(';')

                print(match)
                currentMatch = match[0]
                direThis1 = match[2][1:-1].split(", ")
                direThis = [i[1:-1] for i in direThis1]
                radiantThis1 = match[1][1:-1].split(", ")
                radiantThis = [i[1:-1] for i in radiantThis1]
                print(radiantThis, direThis)
                bot.send_message(msg.chat.id, f'@{msg.from_user.first_name} \nRadiant: {", ".join(radiantThis)}\nDire: {", ".join(direThis)}\n',reply_markup=types.ReplyKeyboardRemove())
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("bet Radiant")
                btn2 = types.KeyboardButton("bet Dire")
                btn3 = types.KeyboardButton("Вернуться назад!")
                markup.add(btn1, btn3, btn2)

                bot.send_message(msg.chat.id, f'@{msg.from_user.first_name} \nВыберите команду, которая победит\nЧтобы это сделать введите <bet Radiant> или <bet Dire> без ковычек', reply_markup=markup)
                users[msg.from_user.id].status = "vote"
        if msg.text == "Баланс":
            bot.send_message(msg.chat.id, f"@{msg.from_user.first_name}, Баланс: {usr.points}", reply_markup=types.ReplyKeyboardRemove())
    if users[msg.from_user.id].status == "vote":
        vote(msg)
    if users[msg.from_user.id].status == "bet":
        play(msg, usr, match)


def play(msg, usr, match):
    if msg.text.isdigit():
        stavka = int(msg.text)
        print(usr.bet(msg, stavka, match))
        users[msg.from_user.id].status = "menu"


def vote(msg):
    global side
    if "bet" in msg.text.lower():
        if "bet radiant" == msg.text.lower():
            bot.send_message(msg.chat.id, f"Вы выбрали команду Radiant")
            side = 0
            bot.send_message(msg.chat.id, f"@{msg.from_user.first_name}, введите колличество очков", reply_markup=types.ReplyKeyboardRemove())
            users[msg.from_user.id].status = "bet"
        if "bet dire" == msg.text.lower():
            bot.send_message(msg.chat.id, f"Вы выбрали команду Dire")
            side = 1

            bot.send_message(msg.chat.id, f"@{msg.from_user.first_name}, введите колличество очков", reply_markup=types.ReplyKeyboardRemove())
            users[msg.from_user.id].status = "bet"
    if "вернуться назад!" == msg.text.lower():
        bot.send_message(msg.chat.id, f"Вы выбрали вернуться назад")
        users[msg.from_user.id].status = "menu"


bot.polling(none_stop=True, interval=0)
