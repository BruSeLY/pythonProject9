import random
from PIL import Image
from main import FindMatch





with open("matches.txt", "r") as f:
    f = f.read().split("\n")
    find_match = f.copy()
    while True:
        buff = random.randint(0, len(find_match) - 1)
        print(find_match[buff].split(";")[0])
        if find_match[buff].split(";")[0] not in users[msg.from_user.id].matches_played:
            match = f[buff].split(";")
            break
        else:
            find_match[buff].remove()
    currentMatch = match[0]
    direThis1 = match[2][1:-1].split(", ")
    direThis = [i[1:-1] for i in direThis1]
    radiantThis1 = match[1][1:-1].split(", ")
    radiantThis = [i[1:-1] for i in radiantThis1]
    photoRadiant = Image.open("Background.jpg").resize((512 *5, 1520))
    im1 = Image.open(f"{radiantThis[0]}_icon.webp").convert("RGB").resize((512, 288))
    im2 = Image.open(f"{radiantThis[1]}_icon.webp").convert("RGB").resize((512, 288))
    im3 = Image.open(f"{radiantThis[2]}_icon.webp").convert("RGB").resize((512, 288))
    im4 = Image.open(f"{radiantThis[3]}_icon.webp").convert("RGB").resize((512, 288))
    im5 = Image.open(f"{radiantThis[4]}_icon.webp").convert("RGB").resize((512, 288))
    im6 = Image.open(f"{direThis[0]}_icon.webp").convert("RGB").resize((512, 288))
    im7 = Image.open(f"{direThis[1]}_icon.webp").convert("RGB").resize((512, 288))
    im8 = Image.open(f"{direThis[2]}_icon.webp").convert("RGB").resize((512, 288))
    im9 = Image.open(f"{direThis[3]}_icon.webp").convert("RGB").resize((512, 288))
    im10 = Image.open(f"{direThis[4]}_icon.webp").convert("RGB").resize((512, 288))
    photoRadiant.paste(im1, (0, 0))
    photoRadiant.paste(im2, (512, 0))
    photoRadiant.paste(im3, (512*2, 0))
    photoRadiant.paste(im4, (512*3, 0))
    photoRadiant.paste(im5, (512*4, 0))
    photoRadiant.paste(im6, (0, 1230))
    photoRadiant.paste(im7, (512, 1230))
    photoRadiant.paste(im8, (512*2, 1230))
    photoRadiant.paste(im9, (512*3, 1230))
    photoRadiant.paste(im10, (512*4, 1230))
