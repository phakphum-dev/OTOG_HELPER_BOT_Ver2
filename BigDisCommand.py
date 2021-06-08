from discord.colour import Color
import ENUM
import OTOG_API
import util
import dataBASS
import ContestManager
from discord import Embed, Colour, File, Activity, Status, ActivityType, Game
from os import path, remove
import asyncio
import time

defaultName = "OTOG - One Tambon One Grader"


def parseCommand(content: str):
    content = content.strip()
    command = content[:content.find("(")]
    command = command.lower()
    args = []
    value = ""
    if content.find("(") == -1 or content.find(")") == -1:
        return False

    for chunk in content[content.find("(")+1:content.find(")")].split(','):
        args.append(chunk.strip())

    if len(content) > content.find(")")+1:
        value = content[content.find(")")+1:].strip()

    if len(args) == 1 and args[0] == "":
        return {"command": command, "args": [], "value": value}

    return {"command": command, "args": args, "value": value}


async def botStatus(client):
    timeTick = ENUM.TIME_F_NORMAL
    userLife = -1
    while True:
        TIMF = ENUM.TIME_F_NORMAL

        if ContestManager.isDuringContest():
            TIMF = ENUM.TIME_F_CONTEST

        if timeTick >= TIMF:
            # Reloading API stuff goes here
            timeTick %= TIMF
            if not util.isSleepTime():
                ContestManager.reloading()
                userLife = OTOG_API.getUserLife()

        if "info" in dataBASS.contest:
            # Contest
            ContestManager.reVerState()
            if not dataBASS.contest["ann"]:
                dataBASS.contest["ann"] = True
                state = dataBASS.contest["state"]
                strAnn = ""
                if state == -1:
                    if 59*60 <= abs(time.time() - ContestManager.timeParse(dataBASS.contest["info"]["timeStart"])) <= 61*60:
                        strAnn = ENUM.CON_ANN_TEXT % (
                            "1 ชั่วโมง", util.pickOne(ENUM.CON_FUNNY_Q))
                    else:
                        strAnn = ENUM.CON_ANN_TEXT % (util.lenTimeInThai(time.time(), ContestManager.timeParse(
                            dataBASS.contest["info"]["timeStart"])), util.pickOne(ENUM.CON_FUNNY_Q))
                elif state == -2:

                    if 23.5*60*60 <= abs(time.time() - ContestManager.timeParse(dataBASS.contest["info"]["timeStart"])) <= 24.5*60*60:
                        strAnn = ENUM.CON_ANN_TEXT % (
                            "1 วัน", util.pickOne(ENUM.CON_FUNNY_Q))
                    else:
                        strAnn = ENUM.CON_ANN_TEXT % (util.lenTimeInThai(time.time(), ContestManager.timeParse(
                            dataBASS.contest["info"]["timeStart"]), "m"), util.pickOne(ENUM.CON_FUNNY_Q))

                if strAnn != "":

                    x = await client.get_channel(ENUM.ANN_CHANNEL).send(content=strAnn)
                    await sayContestInfo(x)
        if util.isSleepTime():
            botName = defaultName
            botStatus = Status.idle
            botActivi = Game(name="น้องนอนอยู่")
        elif ContestManager.timeState() == "NoContest":
            botName = defaultName
            if userLife == -1:
                botStatus = Status.dnd
                botActivi = Activity(name="ไม่รู้ว่ามีคนทำโจทย์กี่คน... help()",
                                     type=ActivityType.playing, url="https://otog.cf/")
            elif userLife == 0:
                botStatus = Status.online
                botActivi = Activity(
                    name="ป่าช้า help()", type=ActivityType.listening, url="https://otog.cf/")
            else:
                botStatus = Status.online
                botActivi = Activity(
                    name=f"คน {userLife} ทำโจทย์ help()", type=ActivityType.watching, url="https://otog.cf/")
        elif ContestManager.timeState() == "NotStart":
            botName = defaultName
            botStatus = Status.online
            botActivi = Game(
                name=f"รอทำคอนเทส {dataBASS.contest['info']['id']}:{dataBASS.contest['info']['name']} ในอีก {util.lenTimeInThai(time.time(),ContestManager.timeParse(dataBASS.contest['info']['timeStart']))} help()")
        else:
            botName = f"{dataBASS.contest['info']['id']}:{dataBASS.contest['info']['name']}"
            botStatus = Status.dnd
            botActivi = Game(
                name=f"เหลือเวลา {util.lenTimeInThai(time.time(),ContestManager.timeParse(dataBASS.contest['info']['timeEnd']))}")

        try:
            await client.Set_Bot_Namae(botName)
            await client.change_presence(status=botStatus, activity=botActivi)
        except:
            print("Warning... Can't change status")
        await asyncio.sleep(5)


async def sayhelp(chan, isAdmin: bool = False):
    em = Embed(title=":grey_question:สิ่งที่น้อมทำได้:grey_question:",
               description="มีแค่นี้แหละ", colour=Colour.from_rgb(255, 133, 29))
    em.add_field(name=":grey_question:help()",
                 value="ก็ที่ทำอยู่ตอนนี้แหละ", inline=False)
    em.add_field(name=":trophy:contest()",
                 value="คอนเทสที่กำลังจะมาถึง", inline=False)
    em.add_field(name=":person_playing_handball:tasks()",
                 value="จำนวนโจทย์ตอนนี้", inline=False)
    em.add_field(name=":military_medal:ranking()",
                 value="คำสั่งไว้ขิงกัน", inline=False)
    em.add_field(name=":question:question(<ชื่อโจทย์>) <คำถาม>",
                 value="ถามคำถามเกี่ยวกับโจทย์ <ชื่อโจทย์>\nและ<คำถาม>ควรตอบเป็น Yes/No(ใช่/ไม่ใช่)", inline=False)
    em.add_field(name=":wrench:change_Log()",
                 value="เป็นการตรวจสอบว่าบอทในรุ่นปัจจุบันมีอะไรเปลี่ยนแปลงบ้าง", inline=False)
    em.add_field(name=":musical_note:OtogRadio(<ชื่อเพลง>)",
                 value="ขอเพลงได้ๆๆ", inline=False)

    await chan.send(content=None, embed=em)

    em = Embed(title=":speech_balloon:คำสั่งคนเหงา:speech_balloon:",
               description="มีแค่นี้แหละ", colour=Colour.from_rgb(255, 133, 29))
    em.add_field(name=":speech_balloon:hello()",
                 value="คำสั่งคนเหงา", inline=False)
    em.add_field(name=":1234:guess_num()", value="เล่นเกมทายเลข", inline=False)

    await chan.send(content=None, embed=em)

    if isAdmin:
        em = Embed(title=":grey_question:สิ่งที่แอดมินทำได้:grey_question:",
                   description="แค่ในนี้เท่านั้น", colour=Colour.red())
        #em.add_field(name = ":orange_heart:user_life()",value = "ดูว่าใครมีชีวิตอยู่บ้าง",inline=False)
        em.add_field(name=":1234:Version()",
                     value="ตรวจสอบ Version", inline=False)
        em.add_field(name=":loudspeaker:ann() <Text>",
                     value="ประกาศๆๆๆๆ", inline=False)
        em.add_field(name=":loudspeaker:say(<Channel_ID>) <Text>",
                     value="ส่ง <Text> ไปยังห้อง <Channel_ID>", inline=False)
        em.add_field(name=":eyes:read() <Text>",
                     value="เป็นการสั่งให้ตัว Console อ่าน <Text> แล้วทำการปริ้นออกมา", inline=False)
        em.add_field(name=":question:q_answer(<id>) <text>",
                     value="ตอบคำถามที่ <id> โดยคำถามจะหายด้วย", inline=False)
        em.add_field(name=":question:q_remove(<id>)",
                     value="ลบคำถามที่ <id>", inline=False)
        em.add_field(name=":question:q_clear()",
                     value="clear คำถามทั้งหมด(ต้องแน่ใจจริงๆว่าจะทำ)", inline=False)
        em.add_field(name=":exclamation:test()",
                     value="ดูว่าน้องยังมีชีวิตอยู่ไหม", inline=False)
        em.add_field(name=":exclamation:test_Verify()\\n<Code in C/C++>",
                     value="ทดสอบว่า Grader แมวๆยังใช้ได้ไหม", inline=False)
        em.add_field(name=":exclamation:check_Verify()",
                     value="ดูว่ามีใครมา Verify ไหม", inline=False)
        em.add_field(name=":exclamation:Watch_Code_Verify(<id>)",
                     value="ดู Code ของ <id>", inline=False)
        em.add_field(name=":exclamation:Force_Reload()",
                     value="บังคับให้รีโหลดฐานข้อมูลใหม่", inline=False)
        em.add_field(name=":sleeping_accommodation:shutdown()",
                     value="ชื่อก็บอกอยู่แล้ว", inline=False)
        em.add_field(name=":checkered_flag:Score_Board(<id>)",
                     value="ไว้ใช้ดูคะแนนในคอนเทส <id>", inline=False)
        em.add_field(name=":checkered_flag:Send_Score_Board(<id>, <channel_id>)",
                     value="ไวส่งคะแนนใน <channel_id> ของคอนเทส <id>", inline=False)
        await chan.send(content=None, embed=em)


async def getNameFromId(client, mes, idPer: int):
    cliUser = await client.fetch_user(idPer)
    try:
        guid = mes.guild
    except:
        if cliUser == None:
            return f"(หาชื่อไม่เจอ ดิสคอร์ดมันโง่!!!!)"
        return cliUser.display_name
    if guid.get_member(idPer) == None:
        if cliUser == None:
            return f"(หาชื่อไม่เจอ ดิสคอร์ดมันโง่!!!!)"
        return cliUser.display_name
    return guid.get_member(idPer).display_name


async def test(client):
    await client.get_channel(ENUM.DEBUG_CHANNEL).send("ยังมีชีวิตยุ้ว")


async def sayThatChanel(mes, content: str):
    await mes.channel.send(content.replace("@author", mes.author.mention))


async def sayNProblems(mes):
    result = OTOG_API.getNumProblems()
    if result == -1:
        await sayThatChanel(mes, "เว็บบึ้มง่ะ @author")
    else:
        await sayThatChanel(mes, f"ตอนนี้มีทั้งหมด `{result} ข้อ`\nแล้วเจ้าทำยัง????")


async def sayRanking(mes):
    ranking = OTOG_API.getRanking()
    if ranking == -1:
        await sayThatChanel(mes, "เว็บบึ้มง่ะ @author")
    else:
        thisEm = Embed(title="Ranking <:oo:706363373079756851><:t_:706363391366660107><:og:706363407124922389><:g_:706363356172255263>",
                       colour=Colour.from_rgb(255, 133, 29))
        thisEm.set_author(name="Otog", icon_url="https://otog.cf/logo196.png")

        for i in range(0, min(10, len(ranking))):
            thisEm.add_field(name=util.nameWithPlace(
                ranking[i][1], i + 1), value=str(ranking[i][0]))

        footerTag = ""

        if len(ranking) > 10:
            footerTag += "และยังมีอีกหลายคน...\nคนต่อไปอาจจะเป็นคุณ ณ ณ\n"

        footerTag += "ประกาศ ณ " + util.getNowTimeInThai()

        thisEm.set_footer(text=footerTag)

        await mes.channel.send(content=None, embed=thisEm)


async def sayContestRanking(conId: int, chan):
    data = OTOG_API.getRankingContest(conId)
    if data == -1:
        await chan.send("เว็บบึ้มง่ะ หรือหาคอนเทสไม่เจอออ")
    else:
        thisEm = Embed(title=f"Scoreboard Contest#{conId}", colour=Colour.from_rgb(
            255, 133, 29), url="https://otog.cf/contest/history/"+str(conId))
        thisEm.set_author(name=f"{data['name']}",
                          icon_url="https://otog.cf/logo196.png")

        for i in range(0, min(10, len(data["ranking"]))):
            thisName = util.nameWithPlace(
                f"{data['ranking'][i][0]} ({sum(data['ranking'][i][1])}) ใช้เวลา {data['ranking'][i][2]/1000:.2f} วินาที", i + 1)
            thisValue = ' '.join(list(map(str, data['ranking'][i][1])))

            thisEm.add_field(name=thisName, value=thisValue)

        footerTag = ""

        if len(data["ranking"]) > 10:
            footerTag += "และยังมีอีกหลายคน...\nคนต่อไปอาจจะเป็นคุณ ณ ณ\n\n"

        for i in range(len(data["problem"])):
            footerTag += f"{i+1}.{data['problem'][i]}\n"

        footerTag += "ประกาศ ณ " + util.getNowTimeInThai()

        thisEm.set_footer(text=footerTag)

        await chan.send(content=None, embed=thisEm)


async def sayContestInfo(mes):

    if "info" not in dataBASS.contest:
        await mes.channel.send(ENUM.CONTEST_NO)
    else:
        conInfo = dataBASS.contest["info"]

        thisEm = Embed(title=f"Incoming Contest#{conInfo['id']}", colour=Colour.from_rgb(
            255, 133, 29), url="https://otog.cf/contest")
        thisEm.set_author(
            name=f"{conInfo['name']}", icon_url="https://otog.cf/logo196.png")
        thisEm.add_field(name="การแข่งแบบ", value=conInfo['mode'])
        thisEm.add_field(name="การตรวจแบบ", value=conInfo['gradingMode'])
        thisEm.add_field(name="เวลาเริ่ม", value=util.formatInThai(
            ContestManager.timeParse(conInfo['timeStart'])), inline=False)
        thisEm.add_field(name="เวลาจบ", value=util.formatInThai(
            ContestManager.timeParse(conInfo['timeEnd'])), inline=False)
        thisEm.add_field(name="ระยะเวลา", value=util.lenTimeInThai(ContestManager.timeParse(
            conInfo['timeStart']), ContestManager.timeParse(conInfo['timeEnd'])), inline=False)

        thisEm.set_footer(text="ประกาศ ณ " + util.getNowTimeInThai())

        await mes.channel.send(content=None, embed=thisEm)


async def sayCLog(chan):
    CLog = "ตอนนี้ก็ไม่รู้เหมือนกัน"

    if path.exists(path.join(ENUM.PATH, "changeLog.txt")):
        with open(path.join(ENUM.PATH, "changeLog.txt"), "r", encoding="utf8") as f:
            CLog = f.read().strip()

    await chan.send(CLog)


async def sayCLog(chan):
    CLog = "ตอนนี้ก็ไม่รู้เหมือนกัน"

    if path.exists(path.join(ENUM.PATH, "changeLog.txt")):
        with open(path.join(ENUM.PATH, "changeLog.txt"), "r", encoding="utf8") as f:
            CLog = f.read().strip()

    await chan.send(CLog)


async def sayAnn(mes, client, content: str):
    await sayAnother(mes, client, ENUM.ANN_TITLE+content, ENUM.ANN_CHANNEL)


async def sayAnother(mes, client, content: str, chan: int):
    if len(mes.attachments) > 0:
        files = []
        filesPaths = []
        for thisFile in mes.attachments:
            thisPath = path.join(ENUM.PATH, thisFile.filename)
            await thisFile.save(thisPath)
            filesPaths.append(thisPath)

            files.append(File(fp=thisPath, filename=thisFile.filename))
        await client.get_channel(chan).send(content=content, files=files)
        for thisPath in filesPaths:
            try:
                remove(thisPath)
            except:
                pass
    else:
        await client.get_channel(chan).send(content=content)


async def gngHowto(chan):

    thisEM = Embed(title="How to play...",
                   colour=Colour.from_rgb(163, 204, 255))
    thisEM.set_author(name="Guess number Game",
                      icon_url="https://otog.cf/logo196.png")
    thisEM.add_field(name=":1234:วิธีการเล่นคือ",
                     value="ข้าจะคิดเลขหนึ่งตัวตั้งแต่ 1 ถึง 100 เจ้าต้องทายเลขของข้าให้ถูกภายใน 7 ครั้ง", inline=False)
    thisEM.add_field(name="สามารถทายโดยการ guess(ตัวเลข) เช่น guess(12)",
                     value="นั้นคือเจ้าทายว่าเลขของข้านั้นคือ 12", inline=False)
    thisEM.add_field(name=":arrow_down:ถ้าเลขที่เจ้าตอบมันต่ำกว่า",
                     value="ข้าก็จะบอกต่ำไป", inline=False)
    thisEM.add_field(name=":arrow_up:แต่ถ้าเลขเจ้ามันสูงไป",
                     value="ข้าก็จะบอกสูงไป", inline=False)
    thisEM.add_field(name=":white_check_mark:แต่ถ้าถูก",
                     value="ข้าจะบอกว่าถูกเอง", inline=False)
    thisEM.add_field(name=":x:ถ้าเจ้ากลัวที่จะแพ้ข้า",
                     value="ก็สามารถออกได้โดยการ guess(*) เอา หึๆๆๆ", inline=False)
    await chan.send(content=None, embed=thisEM)
