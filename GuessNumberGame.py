import dataBASS
import ENUM
import dataBassSQL as sql
from random import randint as ri


def remain(idPer: int):
    res = sql.exeAndGet(
        f'SELECT Remain FROM GNG WHERE IdUser = {idPer}')
    if len(res) == 0:
        return -1
    else:
        return res[0][0]


def initPer(idPer: int):  # (idPer,remain,isCorrected,isTroll,Correct num)
    sql.exeAndCommit(
        f'INSERT INTO GNG VALUES({idPer}, 7, False, {(ri(1, 3) == 1)}, {ri(1, 100)})')


def removeGNG(idPer: int):  # (num,remain,isCorrected,isTroll)
    sql.exeAndCommit(f'DELETE FROM GNG WHERE IdUser = {idPer}')


def guess(idPer: int, numGuess: int):
    # (idPer,remain,isCorrected,isTroll,Correct num)
    thatData = sql.exeAndGet(
        f'SELECT * FROM GNG WHERE IdUser = {idPer}')[0]

    remain = thatData[1]
    isCorrected = thatData[2]
    getTrolled = thatData[3]
    correctOne = thatData[4]

    if getTrolled and remain == 1 and isCorrected:
        removeGNG(idPer)
        return ENUM.GNG_COR2 % (correctOne)

    if numGuess == correctOne:
        if getTrolled:
            if remain == 1:
                removeGNG(idPer)
                return ENUM.GNG_COR1 % (correctOne)
            else:
                remain -= 1
                sql.exeAndCommit(
                    f'UPDATE GNG SET Remain = {remain} WHERE IdUser = {idPer}')
                sql.exeAndCommit(
                    f'UPDATE GNG SET IsCorrect = True WHERE IdUser = {idPer}')
                return ENUM.GNG_GREA % (numGuess, remain)
        else:
            removeGNG(idPer)
            return ENUM.GNG_COR1 % (correctOne)
    else:
        if remain == 1:
            removeGNG(idPer)
            if numGuess > correctOne:
                return ENUM.GNG_LOSS_GREA % (numGuess) + '\n' + ENUM.GNG_LOSS_ANS % (correctOne)
            else:
                return ENUM.GNG_LOSS_LESS % (numGuess) + '\n' + ENUM.GNG_LOSS_ANS % (correctOne)
        else:
            remain -= 1
            sql.exeAndCommit(
                f'UPDATE GNG SET Remain = {remain} WHERE IdUser = {idPer}')
            if numGuess > correctOne:
                return ENUM.GNG_GREA % (numGuess, remain)
            else:
                return ENUM.GNG_LESS % (numGuess, remain)


if __name__ == "__main__":
    initPer(69)
    print(dataBASS.guessNumberGame[69])
    while remain(69) != -1:
        gues = int(input())
        print(guess(69, gues))
