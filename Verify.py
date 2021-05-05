import Garedami.Src.Judge as judge
import ENUM, dataBASS
from os import path

def doJudge(CSctipt:str):
    result = judge.judge(696969,"Cpp",path.join(ENUM.PATH, "Pattern_1"), CSctipt)
    score = result[1]*100//result[2]
    verdict = result[0]
    comment = result[5]
    if score == 0:
        if verdict in ENUM.JUDGE_BIG_VER:
            return ENUM.JUDGE_VERDICT%(verdict) + f"\n{ENUM.JUDGE_BIG_VER[verdict]}" + f"\n```\n{comment}\n```", False
        else:
            return ENUM.JUDGE_VERDICT%(verdict) + f"\n{ENUM.VERIF_NPERFEC}",False
    elif score < 100:
        return ENUM.JUDGE_VERDICT%(verdict) + f"\n{ENUM.VERIF_NPERFEC}",False
    else:
        return ENUM.JUDGE_VERDICT%(verdict) + f"\n{ENUM.VERIF_PERFECT}",True




def addCode(idPer:int, code:str):
    if str(idPer) not in dataBASS.verify:
        dataBASS.verify[str(idPer)] = [code]
    else:
        dataBASS.verify[str(idPer)].append(code)
    dataBASS.saveFile()

def getLenCodes(idPer:int):
    if str(idPer) not in dataBASS.verify:
        return 0
    else:
        return len(dataBASS.verify[str(idPer)])

def removeId(idPer:int):
    del dataBASS.verify[str(idPer)]
    dataBASS.saveFile()

def getLastCode(idPer:int):
    if str(idPer) not in dataBASS.verify:
        return "Wut'"
    else:
        return dataBASS.verify[str(idPer)][-1]



if __name__ == "__main__":
    pass