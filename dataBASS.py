import json
import ENUM
from os import path

guessNumberGame = dict()


def saveFile():
    temp = {"GNG" : guessNumberGame}
    jsonContent = json.dumps(temp)
    with open(path.join(ENUM.PATH,"data.otog"),"w",encoding="utf-8") as f:
        f.write(jsonContent)

def loadFile():
    global guessNumberGame
    if path.exists(path.join(ENUM.PATH,"data.otog")):
        with open(path.join(ENUM.PATH,"data.otog"),"r",encoding="utf-8") as f:
            jsonContent = f.read()
        try:
            jsonContent = json.loads(jsonContent)
        except:
            print("Load : Can't convert file back :(")
            return
        guessNumberGame = jsonContent["GNG"]
    else:
        print("data.otog not found...")


if __name__ == "__main__":
    guessNumberGame[1231241241] = (12,3)
    guessNumberGame[1212] = (12,3)
    #saveFile()
    loadFile()
    print(guessNumberGame)