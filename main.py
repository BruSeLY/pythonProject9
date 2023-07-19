import requests
import telebot
from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession
from telebot import types # для указание типов



#
# session = HTMLSession()
# url = "https://www.opendota.com/matches/highMmr"
# r = session.get(url)
# r.html.render(sleep=1, keep_page=True, scrolldown=1)
# matches_not_final = {}
# r = r.html.links
#
# matches = {}
# t = 0
# for i in r:
#     if len(i) == 19:
#         matches_not_final[t] = i[9:]
#         t += 1
#
# heroes = requests.get("https://api.opendota.com/api/heroes").json()

# with open ("heroes.txt", "w") as f:
#     for i in range(len(heroes)):
#         if i != len(heroes) - 1:
#             f.write(f'{heroes[i]["id"]};{heroes[i]["localized_name"]}\n')
#         else:
#             f.write(f'{(heroes[i]["id"])};{heroes[i]["localized_name"]}')

total_radiant = 0
total_dire = 0
rate = 0.5

#
# for i in range(len(matches_not_final)):
#     response = requests.get('https://api.opendota.com/api/matches/' + matches_not_final[i]).json()
#
#     radiant = []
#     dire = []
#     if "picks_bans" in response:
#         for j in range(10):
#             if response['picks_bans'][j]["team"] == 0:
#                 radiant.append(str(response["picks_bans"][j]["hero_id"]))
#             else:
#                 dire.append(str(response["picks_bans"][j]["hero_id"]))
#     sl = dict()
#     with open ("heroes.txt", "r") as f:
#         s = f.read().split("\n")
#         for row in s:
#             row = row.split(";")
#             sl[row[0]] = row[1]
#     if "radiant_win" in response:
#         radiantWin = response["radiant_win"]
#     if len(radiant) == 5 and len(dire) == 5:
#         for j in range(5):
#             radiant[j] = sl[radiant[j]]
#         for j in range(5):
#             dire[j] = sl[dire[j]]
#         with open("matches.txt", "w") as f:
#             if i < len(matches_not_final):
#                 f.write(f"{response['match_id']};{radiant};{dire};{radiantWin};{total_radiant};{total_dire};{rate}\n")
#             else:
#                 f.write(f"{response['match_id']};{radiant};{dire};{radiantWin};{total_radiant};{total_dire};{rate}")

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
                with open("matches.txt", "a") as a:
                    a.split("\n")

                    if not(win_or_loss):
                        users[msg.from_user.id].points -= put_points
                        f.write(f'{msg.from_user.id};{self.points};{put_points};{side}{win_or_loss}')
                        bot.send_message(msg.chat.id, f"@{self.name}, вы поставили {put_points} и проиграли. Баланс: {users[msg.from_user.id].points}", reply_markup=types.ReplyKeyboardRemove())
                    else:
                        users[msg.from_user.id].points += (float(match[-1]) * put_points)
                        f.write(f'{msg.from_user.id};{self.points};{put_points};{side}{win_or_loss}')
                        bot.send_message(msg.chat.id, f"@{self.name}, вы поставили {put_points} и победили. Баланс: {users[msg.from_user.id].points}", reply_markup=types.ReplyKeyboardRemove())
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
        markup1.add(btn1)
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
                bot.send_message(msg.chat.id, f'@{msg.from_user.first_name} \nRadiant: {", ".join(radiantThis)}\nDire: {", ".join(direThis)}\nКоэффицент: {match[6]}',reply_markup=types.ReplyKeyboardRemove())
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("bet Radiant")
                btn2 = types.KeyboardButton("bet Dire")
                btn3 = types.KeyboardButton("Вернуться назад!")
                markup.add(btn1, btn3, btn2)

                bot.send_message(msg.chat.id, f'@{msg.from_user.first_name} \nВыберите команду, которая победит\nЧтобы это сделать введите <bet Radiant> или <bet Dire> без ковычек', reply_markup=markup)
                users[msg.from_user.id].status = "vote"
    if users[msg.from_user.id].status == "vote":
        vote(msg)
    if users[msg.from_user.id].status == "bet":
        play(msg, usr, match)


def play(msg, usr, match):
    if "bet" in msg.text.lower():
        if msg.text.split()[1].isdigit():
            stavka = int(msg.text.split()[1])
            print(usr.bet(msg, stavka, match))
            users[msg.from_user.id].status = "menu"


def vote(msg):
    global side
    if "bet" in msg.text.lower():
        if "bet radiant" == msg.text.lower():
            bot.send_message(msg.chat.id, f"Вы выбрали команду Radiant",
                             reply_markup=types.ReplyKeyboardRemove())
            side = 0

            bot.send_message(msg.chat.id, f"@{msg.from_user.first_name}, введите колличество очков через <bet колличество очков> без ковычек")
            users[msg.from_user.id].status = "bet"
        if "bet dire" == msg.text.lower():
            bot.send_message(msg.chat.id, f"Вы выбрали команду Dire",
                             reply_markup=types.ReplyKeyboardRemove())
            side = 1

            bot.send_message(msg.chat.id, f"@{msg.from_user.first_name}, введите колличество очков через <bet колличество очков> без ковычек")
            users[msg.from_user.id].status = "bet"
    if "вернуться назад!" == msg.text.lower():
        bot.send_message(msg.chat.id, f"Вы выбрали вернуться назад",
                         reply_markup=types.ReplyKeyboardRemove())
        users[msg.from_user.id].status = "menu"


bot.polling(none_stop=True, interval=0)
