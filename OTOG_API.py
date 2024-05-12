import requests
import json

_otog_host = ""
_otog_api_host = ""

def init(host: str, api_host: str):
    global _otog_host, _otog_api_host
    _otog_host = host
    _otog_api_host = api_host


def getNumProblems():
    try:
        response = requests.get(f"{_otog_api_host}/problem")
    except:
        return -1

    if response.status_code != 200:
        return -1
    else:
        return len(response.json())


def getRanking():
    try:
        response = requests.get(f"{_otog_api_host}/user")
    except:
        return -1

    if response.status_code != 200:
        return -1
    else:
        data = response.json()
        ranking = list()

        for user in data:
            if user["role"] == "user" and user["rating"] != None:
                ranking.append((user["rating"], user["showName"]))

        ranking.sort(key=lambda x: x[0])
        ranking.reverse()

        return ranking


def getRankingContest(nCon: int):
    try:
        response = requests.get(f"{_otog_api_host}/contest/{nCon}/scoreboard")
    except:
        return -1
    if response.status_code != 200:
        return -1
    else:
        data = response.json()

        result = dict()
        result["name"] = data["name"]
        result["problem"] = list()
        for problem in data["problems"]:
            result["problem"].append(
                (f"({problem['id']}){problem['name']} : {problem['score']} คะแนน")
            )

        result["ranking"] = list()

        for user in data["users"]:
            if user["role"] == "user":
                scores = []
                timeUse = 0
                for sc in user["submissions"]:
                    scores.append(sc["score"])
                    timeUse += sc["timeUsed"]
                result["ranking"].append((user["showName"], scores, timeUse))

            result["ranking"].sort(key=lambda x: sum(x[1]))
            result["ranking"].reverse()

        return result


def getUserLife():
    try:
        response = requests.get(f"{_otog_api_host}/user/online")
    except:
        return -1
    if response.status_code != 200:
        return -1
    else:
        data = response.json()
        outStr = ""
        if len(data) == 0:
            return 0
        elif len(data) == 1:
            outStr += f"{data[0]['showName']} (คนเหงา)"
        elif len(data) <= 7:
            for i in range(len(data) - 1):
                outStr += data[i]["showName"] + ", "
            outStr = outStr[:-1] + "และ" + data[-1]["showName"]
        else:
            outStr += f"คน {len(data)} คน"
        return outStr


def contestNow():

    # with open("TestContent.txt","r",encoding="utf8") as f:
    #     x = json.loads(f.read())
    # return x

    response = requests.get(f"{_otog_api_host}/contest/now")
    if response.status_code != 200:
        return -1
    else:
        try:
            data = response.json()
        except:
            return -1
        
        if data["currentContest"] is None:
            return -1
        
        thisContest = dict()
        for k in data["currentContest"]:
            if k != "problems":
                thisContest[k] = data["currentContest"][k]
        return thisContest


def isWorking() -> bool:
    try:
        response = requests.get(_otog_host, timeout=5)
    except:
        return False
    return 200 <= response.status_code < 300


if __name__ == "__main__":
    print(isWorking())
