import Garedami.Src.Judge as judge
import ENUM
import dataBASS
import dataBassSQL as sql
from os import path


def doJudge(CSctipt: str):
    result = judge.judge(696969, "Cpp", path.join(
        ENUM.PATH, "Pattern_1"), CSctipt)
    score = result[1]*100//result[2]
    verdict = result[0]
    comment = result[5]
    if score == 0:
        if verdict in ENUM.JUDGE_BIG_VER:
            return ENUM.JUDGE_VERDICT % (verdict) + f"\n{ENUM.JUDGE_BIG_VER[verdict]}" + f"\n```\n{comment}\n```", False
        else:
            return ENUM.JUDGE_VERDICT % (verdict) + f"\n{ENUM.VERIF_NPERFEC}", False
    elif score < 100:
        return ENUM.JUDGE_VERDICT % (verdict) + f"\n{ENUM.VERIF_NPERFEC}", False
    else:
        return ENUM.JUDGE_VERDICT % (verdict) + f"\n{ENUM.VERIF_PERFECT}", True


def getData():
    return sql.exeAndGet('SELECT * FROM Verify')


def getDistinctData():
    allData = getData()
    isDone = set()
    result = []
    for e in reversed(allData):
        if e[0] not in isDone:
            result.append(e)
            isDone.add(e[0])

    return result


def getLenCodes(idPer: int):
    return len(sql.exeAndGet(f'SELECT * FROM Verify WHERE IdUser = {idPer}'))


def addCode(idPer: int, code: str):
    n = getLenCodes(idPer) + 1
    sql.exeAndCommit(f'INSERT INTO Verify VALUES({idPer}, {n}, \'{code}\')')


def removeId(idPer: int):
    sql.exeAndCommit(f'DELETE FROM Verify WHERE IdUser = {idPer}')


def getLastCode(idPer: int):
    data = sql.exeAndGet(f'SELECT * FROM Verify WHERE IdUser = {idPer}')
    if len(data) == 0:
        return "Wut"
    else:
        return data[-1][2]


if __name__ == "__main__":
    pass
