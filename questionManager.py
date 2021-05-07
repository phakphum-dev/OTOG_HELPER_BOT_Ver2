import dataBASS,util,ENUM
#[idAuthor,idTask,question,[MesUID]]
def crtQuestion(idPer:int):
    crt = 0
    for q in dataBASS.questions:
        if q[0] == idPer:
            crt+=1
    
    return crt

def isAlreadyAsk(idPer:int,idTask:str):
    for q in dataBASS.questions:
        if q[0] == idPer and q[1] == idTask:
            return True
    
    return False


def lenAllQuest():
    return len(dataBASS.questions)


def newQuestion(idPer:int,idTask:str,q:str,mesID:list):
    dataBASS.questions.append([idPer,idTask,q,mesID])
    dataBASS.saveFile()


def modifyQuestion(idPer:int,idTask:str,qNew:str):
    for i in range(len(dataBASS.questions)):
        if dataBASS.questions[i][0] == idPer and dataBASS.questions[i][1] == idTask:
            dataBASS.questions[i][2] = qNew
            dataBASS.saveFile()
            return i
    
def removeQuestion(idPer:int,idTask:str):
    for i in range(len(dataBASS.questions)):
        if dataBASS.questions[i][0] == idPer and dataBASS.questions[i][1] == idTask:
            return removeQuestionInd(i)


def removeQuestionInd(i:int):
    tempMes = dataBASS.questions[i][3].copy()
    del dataBASS.questions[i]
    dataBASS.saveFile()
    return tempMes



def answerQuestion(client,qInd:int,ans:str):
    del dataBASS.questions[qInd]
    dataBASS.saveFile()
    #Send stuff here....


async def reloadMessage(client,index:int = -1):
    if index == -1:
        for i in range(lenAllQuest()):
            userMessage = await util.uID2Message(client, dataBASS.questions[i][3][0])
            await userMessage.edit(content = ENUM.QUEST_USER%(dataBASS.questions[i][1],dataBASS.questions[i][2],"รอไปก่อนแบบใจเย็นๆ..."))

            adminMessage = await util.uID2Message(client, dataBASS.questions[i][3][1])
            await adminMessage.edit(content = ENUM.QUEST_ADMIN%(i+1,dataBASS.questions[i][1],dataBASS.questions[i][2]))
    else:
        i = index
        userMessage = await util.uID2Message(client, dataBASS.questions[i][3][0])
        await userMessage.edit(content = ENUM.QUEST_USER%(dataBASS.questions[i][1],dataBASS.questions[i][2],"รอไปก่อนแบบใจเย็นๆ..."))

        adminMessage = await util.uID2Message(client, dataBASS.questions[i][3][1])
        await adminMessage.edit(content = ENUM.QUEST_ADMIN%(i+1,dataBASS.questions[i][1],dataBASS.questions[i][2]))
