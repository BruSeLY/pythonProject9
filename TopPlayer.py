import operator

tierList = {}


with open("user.txt", "r") as f:
    f = f.read().split("\n")
    for row in f:
        row = row.split(";")
        tierList[row[1]] = int(row[-1])


print(tierList)
with open("TopPlayer.txt", "w") as f:
    if len(tierList) >= 5:
        for i in range(5):
            if i != 5:
                f.write(f"{max(tierList.items(), key=operator.itemgetter(1))[0]};{max(tierList.items(), key=operator.itemgetter(1))[1]}\n")
                del tierList[max(tierList.items(), key=operator.itemgetter(1))[0]]
            else:
                f.write(f"{max(tierList.items(), key=operator.itemgetter(1))[0]};{max(tierList.items(), key=operator.itemgetter(1))[1]}")
    else:
        f.write(f"{max(tierList.items(), key=operator.itemgetter(1))[0]};{max(tierList.items(), key=operator.itemgetter(1))[1]}")
