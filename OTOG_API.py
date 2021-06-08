import requests
import json


def getNumProblems():
    response = requests.get("https://otog.cf/api/problem")
    if response.status_code != 200:
        return -1
    else:
        return len(response.json())


def getRanking():
    response = requests.get("https://otog.cf/api/user")
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
    response = requests.get(f"https://otog.cf/api/contest/{nCon}/scoreboard")
    if response.status_code != 200:
        return -1
    else:
        data = response.json()

        result = dict()
        result["name"] = data["name"]
        result["problem"] = list()
        for problem in data["problems"]:
            result["problem"].append(
                (f"({problem['id']}){problem['name']} : {problem['score']} คะแนน"))

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

    response = requests.get("https://otog.cf/api/user/online")
    if response.status_code != 200:
        return -1
    else:
        data = response.json()
        outStr = ""
        if len(data) <= 7:
            for i in range(len(data)-1):
                outStr += data[i]["showName"] + ","
            outStr += "และ" + data[i]["showName"][-1]
        else:
            outStr += f"คน {len(data)} คน"
        return outStr


def contestNow():

    # with open("TestContent.txt","r",encoding="utf8") as f:
    #     x = json.loads(f.read())
    # return x

    response = requests.get(f"https://otog.cf/api/contest/now")
    if response.status_code != 200:
        return -1
    else:
        try:
            data = response.json()
        except:
            return dict()
        thisContest = dict()
        for k in data:
            if k != "problems":
                thisContest[k] = data[k]
        return thisContest


if __name__ == "__main__":
    print(getUserLife())
