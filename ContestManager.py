import dataBASS
import OTOG_API
import time


def timeParse(con: str):
    con = con[: con.find(".")] + "Z"
    return time.mktime(time.strptime(con, "%Y-%m-%dT%H:%M:%SZ")) + 60 * 60 * 7


def verifyState():
    # state -3 is so longggg
    # state -2 is 1 day
    # state -1 is 1 hour
    # state 0 is now
    if time.time() > timeParse(dataBASS.contest["info"]["timeStart"]):
        state = 0
    elif time.time() > timeParse(dataBASS.contest["info"]["timeStart"]) - 60 * 60:
        state = -1
    elif time.time() > timeParse(dataBASS.contest["info"]["timeStart"]) - 60 * 60 * 24:
        state = -2
    else:
        state = -3

    dataBASS.contest["state"] = state


def reVerState():
    if time.time() > timeParse(dataBASS.contest["info"]["timeStart"]):
        nState = 0
    elif time.time() > timeParse(dataBASS.contest["info"]["timeStart"]) - 60 * 60:
        nState = -1
    elif time.time() > timeParse(dataBASS.contest["info"]["timeStart"]) - 60 * 60 * 24:
        nState = -2
    else:
        nState = -3

    if dataBASS.contest["state"] != nState and dataBASS.contest["ann"]:
        dataBASS.contest["state"] = nState
        if nState != 0:
            dataBASS.contest["ann"] = False


def mkNewContest(otogCon):
    dataBASS.contest = {"info": otogCon, "state": 0, "ann": False}
    verifyState()
    dataBASS.saveFile()


def timeState():

    if "info" not in dataBASS.contest:
        return "NoContest"
    else:
        timeStart = timeParse(dataBASS.contest["info"]["timeStart"])
        timeEnd = timeParse(dataBASS.contest["info"]["timeEnd"])

        if time.time() < timeStart:
            return "NotStart"
        elif time.time() < timeEnd:
            return "NotEnd"
        else:
            return "NoContest"


def reloading():
    if not OTOG_API.isWorking():
        return
    otogCon = OTOG_API.contestNow()
    if otogCon != -1:
        if "timeEnd" not in otogCon:
            dataBASS.contest = dict()
            dataBASS.saveFile()
            return
        else:
            timeStart = timeParse(otogCon["timeStart"])
            timeEnd = timeParse(otogCon["timeEnd"])
        if time.time() > timeEnd:
            dataBASS.contest = dict()
            dataBASS.saveFile()
        else:
            if "info" not in dataBASS.contest:
                mkNewContest(otogCon)
            elif dataBASS.contest["info"]["id"] != otogCon["id"]:
                mkNewContest(otogCon)
            elif dataBASS.contest["info"]["timeStart"] != otogCon["timeStart"]:
                mkNewContest(otogCon)
            else:
                dataBASS.contest["info"] = otogCon
                dataBASS.saveFile()


def isDuringContest():
    if "info" not in dataBASS.contest:
        return False
    else:
        return dataBASS.contest["state"] == 0


if __name__ == "__main__":
    reloading()
