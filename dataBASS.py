import json
import ENUM
from os import path

guessNumberGame = dict()
verify = dict()
contest = dict()
questions = list()


def saveFile():
    temp = {"GNG" : guessNumberGame, "VER" : verify, "CON" : contest, "Q":questions}
    jsonContent = json.dumps(temp)
    with open(path.join(ENUM.PATH,"data.otog"),"w",encoding="utf-8") as f:
        f.write(jsonContent)

def loadFile():
    global guessNumberGame,verify,contest,questions
    if path.exists(path.join(ENUM.PATH,"data.otog")):
        with open(path.join(ENUM.PATH,"data.otog"),"r",encoding="utf-8") as f:
            jsonContent = f.read()
        try:
            jsonContent = json.loads(jsonContent)
        except:
            print("Load : Can't convert file back :(")
            return

        if "GNG" in jsonContent:
            guessNumberGame = jsonContent["GNG"]
        else:
            guessNumberGame = dict()
        
        if "VER" in jsonContent:
            verify = jsonContent["VER"]
        else:
            verify = dict()
        
        if "CON" in jsonContent:
            contest = jsonContent["CON"]
        else:
            contest = dict()

        if "Q" in jsonContent:
            questions = jsonContent["Q"]
        else:
            questions = list()
        
    else:
        print("data.otog not found...")


if __name__ == "__main__":
    print(guessNumberGame)