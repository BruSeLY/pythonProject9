from requests_html import HTMLSession
import requests


session = HTMLSession()
url = "https://www.opendota.com/matches/highMmr"
r = session.get(url)
r.html.render(sleep=1, keep_page=True, scrolldown=2, timeout=25)
matches_not_final = {}
r = r.html.links


matches = {}
t = 0
for i in r:
    if len(i) == 19:
        matches_not_final[t] = i[9:]
        t += 1
print(1)
print(len(matches_not_final))
for i in range(len(matches_not_final)):
    with open("matches.txt", "a") as a:

        response = requests.get('https://api.opendota.com/api/matches/' + matches_not_final[i]).json()

        radiant = []
        dire = []
        if "picks_bans" in response:
            for j in range(len(response['picks_bans'])):
                if response['picks_bans'][j]["team"] == 0 and response["picks_bans"][j]["is_pick"] is True:
                    radiant.append(str(response["picks_bans"][j]["hero_id"]))
                elif response['picks_bans'][j]["team"] == 1 and response["picks_bans"][j]["is_pick"] is True:
                    dire.append(str(response["picks_bans"][j]["hero_id"]))
            sl = dict()
            with open ("heroes.txt", "r") as f:
                s = f.read().split("\n")
                for row in s:
                    row = row.split(";")
                    sl[row[0]] = row[1]
            if "radiant_win" in response:
                radiantWin = response["radiant_win"]
            if len(radiant) == 5 and len(dire) == 5:
                for j in range(5):
                    radiant[j] = sl[radiant[j]]
                for j in range(5):
                    dire[j] = sl[dire[j]]
                if i < len(matches_not_final):
                    a.write(f"{response['match_id']};{radiant};{dire};{radiantWin}\n")
                else:
                    a.write(f"{response['match_id']};{radiant};{dire};{radiantWin}")
            radiant = []
            dire = []
            radiantWin = None
            response = ""

print("END")
