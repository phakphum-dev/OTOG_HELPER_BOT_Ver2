import dataBASS
import ENUM
from random import randint as ri


def remain(idPer:int):
    if str(idPer) not in dataBASS.guessNumberGame:
        return -1
    else:
        return dataBASS.guessNumberGame[str(idPer)][1]

def initPer(idPer:int):    #(num,remain,isCorrected,isTroll)
    dataBASS.guessNumberGame[str(idPer)] = [ri(1,100),7,False,(ri(1,3) == 1)]
    dataBASS.saveFile()


def removeGNG(idPer:int):    #(num,remain,isCorrected,isTroll)
    del dataBASS.guessNumberGame[str(idPer)]
    dataBASS.saveFile()

def guess(idPer:int, numGuess:int):
    correctOne = dataBASS.guessNumberGame[str(idPer)][0]
    getTrolled = dataBASS.guessNumberGame[str(idPer)][3]

    if getTrolled and dataBASS.guessNumberGame[str(idPer)][1] == 1 and dataBASS.guessNumberGame[str(idPer)][2]:
        del dataBASS.guessNumberGame[str(idPer)]
        dataBASS.saveFile()
        return ENUM.GNG_COR2%(correctOne)

    if numGuess == correctOne:
        if getTrolled:
            if dataBASS.guessNumberGame[str(idPer)][1] == 1:
                del dataBASS.guessNumberGame[str(idPer)]
                dataBASS.saveFile()
                return ENUM.GNG_COR1%(correctOne)
            else:
                dataBASS.guessNumberGame[str(idPer)][1]-=1
                dataBASS.guessNumberGame[str(idPer)][2] = True
                return ENUM.GNG_GREA%(numGuess, dataBASS.guessNumberGame[str(idPer)][1])
        else:
            del dataBASS.guessNumberGame[str(idPer)]
            dataBASS.saveFile()
            return ENUM.GNG_COR1%(correctOne)
    else:
        if dataBASS.guessNumberGame[str(idPer)][1] == 1:
            del dataBASS.guessNumberGame[str(idPer)]
            dataBASS.saveFile()
            if numGuess > correctOne:
                return ENUM.GNG_LOSS_GREA%(numGuess) + '\n' + ENUM.GNG_LOSS_ANS%(correctOne)
            else:
                return ENUM.GNG_LOSS_LESS%(numGuess) + '\n' + ENUM.GNG_LOSS_ANS%(correctOne)
        else:
            dataBASS.guessNumberGame[str(idPer)][1]-=1
            if numGuess > correctOne:
                return ENUM.GNG_GREA%(numGuess, dataBASS.guessNumberGame[str(idPer)][1])
            else:
                return ENUM.GNG_LESS%(numGuess, dataBASS.guessNumberGame[str(idPer)][1])

if __name__ == "__main__":
    initPer(69)
    print(dataBASS.guessNumberGame[69])
    while remain(69)!=-1:
        gues = int(input())
        print(guess(69,gues))
