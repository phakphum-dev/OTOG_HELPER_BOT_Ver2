import requests


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
                ranking.append((user["rating"],user["showName"]))
        
        ranking.sort(key=lambda x: x[0])
        ranking.reverse()

        return ranking

def getRankingContest(nCon:int):
    response = requests.get(f"https://otog.cf/api/contest/{nCon}/scoreboard")
    if response.status_code != 200:
        return -1
    else:
        data = response.json()

        result = dict()
        result["name"] = data["name"]
        result["problem"] = list()
        for problem in data["problems"]:
            result["problem"].append((f"({problem['id']}){problem['name']} : {problem['score']} คะแนน"))

        result["ranking"] = list()

        for user in data["users"]:
            if user["role"] == "user":
                scores = []
                timeUse = 0
                for sc in user["submissions"]:
                    scores.append(sc["score"])
                    timeUse += sc["timeUsed"]
                result["ranking"].append((user["showName"],scores,timeUse))
        
            result["ranking"].sort(key=lambda x: sum(x[1]))
            result["ranking"].reverse()

        return result


if __name__ == "__main__":
    print(getRankingContest(20))

