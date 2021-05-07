import discord,random

from discord import utils
import ENUM,dataBASS,Verify,ContestManager,questionManager
import BigDisCommand as cmd
from util import *
import GuessNumberGame as GNG

DEB = "" #Before Command
NAME = "OTOG - One Tambon One Grader"

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    dataBASS.loadFile()
    ContestManager.reloading()
    client.loop.create_task(cmd.botStatus(client))
    await client.Set_Bot_Namae(NAME)


@client.event
async def Set_Bot_Namae(Namae):

    if len(Namae) > 28:Namae = Namae[:28]+"..."

    for GG in client.guilds:
        await GG.me.edit(nick = Namae)

@client.event
async def on_guild_join(guild):
    await guild.system_channel.send("กราบสวัสดีพ่อแม่พี่น้องครับ")

@client.event
async def on_member_join( member):
    ALL_ROLE = member.guild.roles

    role = discord.utils.get(ALL_ROLE,name = "return 0;")
    await member.edit(roles = [role])

    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'สวัสดีเจ้า {0.mention} สู่ {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

@client.event
async def on_member_remove( member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'ลาก่อย {0.mention}!'.format(member)
        await guild.system_channel.send(to_send)



@client.event
async def on_message(mes):

    if mes.content.strip().lower() == DEB+"help":
        await cmd.sayhelp(mes.channel) 
        await cmd.sayThatChanel(mes,f"ทีหลังพิมพ์คำสั่งควรมีวงเล็บด้วยนะ @author")
        return

    thisCmd = cmd.parseCommand(mes.content.lower())

    #Check first
    if mes.author.id == client.user.id:
        return

    if thisCmd == False:
        return
    
    #Check admin
    isAdmin = False
    if hasattr(mes.author, 'roles'):
        for r in mes.author.roles:
            if str(r) == "Administrator":
                isAdmin = True

    isAdminChan = False
    if hasattr(mes.channel, 'changed_roles'):
        for r in mes.channel.changed_roles:
            if str(r) == "Administrator":
                isAdminChan = True

    isAdmin = isAdmin and isAdminChan


    #List command goes here
    if thisCmd["command"]==(DEB + "test"):
        await cmd.test(client)
    
    if thisCmd["command"]==(DEB + "help"):
        await cmd.sayhelp(mes.channel, isAdmin)
    
    if thisCmd["command"]==(DEB + "change_log"):
        await cmd.sayCLog(mes.channel)
    
    if thisCmd["command"]==(DEB + "tasks") or thisCmd["command"]==(DEB + "problems"):
        await cmd.sayNProblems(mes)

    if thisCmd["command"]==(DEB + "ranking"):
        await cmd.sayRanking(mes)
    
    if thisCmd["command"]==(DEB + "contest"):
        await cmd.sayContestInfo(mes)
    

    if thisCmd["command"]==(DEB + "otogradio"):
        if len(thisCmd["args"]) < 1:
            await cmd.sayThatChanel(mes,"ไม่ใส่ชื่อเพลง ก็ไม่เปิดให้!!!")
        else:
            await cmd.sayThatChanel(mes,"OK จัดให้ @author")
            await cmd.sayThatChanel(mes,f":musical_note:playing... {thisCmd['args'][0]}")
            await cmd.sayThatChanel(mes,f"||ล้อเล่น ไม่มีหรอก||")
    

    if thisCmd["command"]==(DEB + "hello"):
        thisHello = ENUM.HELLO_TEXT[random.randint(0,len(ENUM.HELLO_TEXT) - 1)]
        await cmd.sayThatChanel(mes,f"{thisHello} @author")
    
    if thisCmd["command"]==(DEB + "baka"):
        await cmd.sayThatChanel(mes,"<:baka:704310333120053248>")
    
    if thisCmd["command"]==(DEB + "guess_num"):
        idPer = mes.author.id
        if GNG.remain(idPer) == -1:
            await cmd.sayThatChanel(mes,":crossed_swords:โห๋ 1-1 ได้ครับเจ้า @author:crossed_swords:")
            await cmd.gngHowto(mes.channel)
            GNG.initPer(idPer)
            dataBASS.saveFile()
        else:
            await cmd.sayThatChanel(mes,"เห้ย อย่าเล่นซ้ำเซ่!!!!??\nเวลาจะทายให้พิมพ์ `guess(ตัวเลข)` เอา!!! @author")
    
    if thisCmd["command"]==(DEB + "guess"):
        idPer = mes.author.id
        
        if GNG.remain(idPer) != -1:
            await mes.delete()
        
        if GNG.remain(idPer) == -1:
            await cmd.sayThatChanel(mes,"ฮั่นแน่ อยากเล่นด้วยละสิ @author\nเวลาจะเล่นให้ใช้คำสั่ง `guess_num()` ก่อนเด้ออ")
        elif len(thisCmd["args"]) < 1:
            await cmd.sayThatChanel(mes,"จะทายความว่างเปล่าหรอ... ไม่น่าใช่น้าาาา")
        elif thisCmd["args"][0].strip() == "*":
            await cmd.sayThatChanel(mes,ENUM.GNG_GIVE)
            GNG.removeGNG(idPer)
        elif not isInt(thisCmd["args"][0].strip()):
            await cmd.sayThatChanel(mes,f"{thisCmd['args'][0].strip()} ไม่น่าใช่ตัวเลขจำนวนเต็มน้าาาา")
        else:
            gus = int(thisCmd["args"][0].strip())
            if gus <= 0 or gus > 100:
                await cmd.sayThatChanel(mes,"1 ถึง 100...\n๑ ถึง ๑๐๐...\n***หนึ่งถึงร้อยยยยย!!!!***")
            else:
                result = GNG.guess(idPer, gus)
                await cmd.sayThatChanel(mes,result)

    if thisCmd["command"]==(DEB + "question"):
        idPer = mes.author.id
        if len(thisCmd["args"]) < 1:
            await mes.author.send("เมื่อเจ้าถามอะไรอ่ะ??? เจ้าลืมใส่ชื่อโจทย์...")
        elif thisCmd["value"] == "":
            if questionManager.isAlreadyAsk(idPer, thisCmd["args"][0]):
                
                ids = questionManager.removeQuestion(idPer, thisCmd["args"][0])
                for idd in ids:
                    delMes = await uID2Message(client,idd)
                    await delMes.delete()
                await questionManager.reloadMessage(client)
                await mes.author.send(f":x:ลบคำถาม `{thisCmd['args'][0]}` เรียบร้อยแล้ว...")
            else:
                await mes.author.send("เมื่อเจ้าถามอะไรอ่ะ??? เจ้าถามความว่างเปล่ารี?")
        else:
            if questionManager.isAlreadyAsk(idPer, thisCmd["args"]):
                await mes.author.send(f":arrows_counterclockwise: เปลี่ยนคำถาม `{thisCmd['args'][0]}` เรียบร้อยแล้ว...")
                idQ = questionManager.modifyQuestion(idPer, thisCmd["args"][0], thisCmd["value"])
                await questionManager.reloadMessage(client, idQ)
            else:
                if questionManager.crtQuestion(idPer) >= 5:
                    await mes.author.send("เจ้าหมดโค้วต้าการถามแล้ว... รอก่อนนะ")
                else:
                    mesIds = []
                    mesIds.append(messageToUniqueID(await mes.author.send(ENUM.QUEST_USER%(thisCmd["args"][0],thisCmd["value"],"รอไปก่อนแบบใจเย็นๆ..."))))
                    mesIds.append(messageToUniqueID(await client.get_channel(ENUM.QUE_CHANNEL).send(ENUM.QUEST_ADMIN%(questionManager.lenAllQuest()+1,thisCmd["args"][0],thisCmd["value"]))))
                    questionManager.newQuestion(idPer, thisCmd["args"][0], thisCmd["value"], mesIds)
        try:
            await mes.delete()
        except:
            print("Can't delete message...")

    if isAdmin:
        
        if thisCmd["command"]==(DEB + "version"):
            await cmd.sayThatChanel(mes,f"{ENUM.VER} เด้อออ")
        
        if thisCmd["command"]==(DEB + "ann"):
            if thisCmd["value"].strip() == "":
                await cmd.sayThatChanel(mes,"ประกาศความว่างเปล่า?")
            else:
                await cmd.sayAnn(mes, client, thisCmd["value"].strip())
        
        if thisCmd["command"]==(DEB + "say"):
            if len(thisCmd["args"]) < 1:
                await cmd.sayThatChanel(mes,"ประกาศในห้องไหนอ่ะะะ")
            elif thisCmd["value"].strip() == "":
                await cmd.sayThatChanel(mes,"ประกาศความว่างเปล่า?")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"Channel_ID ควรเป็น int นะะ")
            else:
                await cmd.sayAnn(mes, client, thisCmd["value"].strip(), int(thisCmd["args"][0]))
        
        if thisCmd["command"]==(DEB + "read"):
            if thisCmd["value"].strip() == "":
                await cmd.sayThatChanel(mes,"ให้อ่านความว่างเปล่า")
            else:
                print(f"=======Read form {mes.author.display_name}=======")
                print(thisCmd["value"].strip())
                await cmd.sayThatChanel(mes,"อ่านสำเร็จ!!")
        
        if thisCmd["command"]==(DEB + "shutdown"):
            await cmd.sayThatChanel(mes,"ลาก่อย")
            await client.close()
            exit(0)
        

        if thisCmd["command"]==(DEB + "score_board"):
            if len(thisCmd["args"]) < 1:
                await cmd.sayThatChanel(mes,"CONTEST ไหนนน")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"ID ควรเป็น int นะะ")
            else:
                await cmd.sayContestRanking(int(thisCmd["args"][0]), mes.channel)
        
        if thisCmd["command"]==(DEB + "send_score_board"):
            if len(thisCmd["args"]) < 2:
                await cmd.sayThatChanel(mes,"ดู Argument ดีๆ")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"ID ควรเป็น int นะะ")
            elif not isInt(thisCmd["args"][1]):
                await cmd.sayThatChanel(mes,"channel_id ควรเป็น int นะะ")
            else:
                await cmd.sayContestRanking(int(thisCmd["args"][0]), client.get_channel(int(thisCmd["args"][1])))

        if thisCmd["command"]==(DEB + "test_verify"):
            code = thisCmd["value"].strip()
            if code == "":
                await cmd.sayThatChanel(mes,"ส่งความว่างเปล่ามาตรวจ?? เยี่ยมไปเล้ยยย")
            else:
                await cmd.sayThatChanel(mes,"ตรวจแป๊ป")
                await cmd.sayThatChanel(mes,Verify.doJudge(code)[0])

        if thisCmd["command"]==(DEB + "force_reload"):
            ContestManager.reloading()
            await cmd.sayThatChanel(mes,"จัดให้ห้ห้ห้ห้!!")

        if thisCmd["command"]==(DEB + "check_verify"):
            if len(dataBASS.verify) == 0:
                await cmd.sayThatChanel(mes,"เย่... ยังไม่มีใครมา Verify เลย\n*เ ห ง า จุ ง*")
            else:
                strr = f"ตอนนี้มี `{len(dataBASS.verify)}` คนที่กำลังอยู่ในระหว่างการดำเนินการ Verify...\n"
                for ids in dataBASS.verify:
                    strr += f"-{await cmd.getNameFromId(client, mes, int(ids))}({ids}) เหลืออีก {5 - len(dataBASS.verify[ids])} ครั้ง\n"
                strr += f"\nรายงาน ณ {getNowTimeInThai()}"
                
                await cmd.sayThatChanel(mes,strr)
        
        if thisCmd["command"]==(DEB + "watch_code_verify"):
            if len(thisCmd["args"]) < 1:
                await cmd.sayThatChanel(mes,"ค ว า ม ว่ า ง เ ป ล่ า")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"ID ควรเป็นจำนวนเต็มนะะนะนะนะนะนะ")
            elif Verify.getLenCodes(int(thisCmd["args"][0])) == 0:
                await cmd.sayThatChanel(mes,"ไม่มีข้อมูลการ Verify ของ ID นี้นะ")
            else:
                idPer = int(thisCmd['args'][0])
                strr = f"======ข้อมูล Verify ของ {await cmd.getNameFromId(client, mes, idPer)}======\n\n"
                for i in range(len(dataBASS.verify[str(idPer)])):
                    strr += f"การส่งครั้งที่ {i+1}...\n```cpp\n{dataBASS.verify[str(idPer)][i]}\n```\n\n"
                
                strr += f"\nรายงาน ณ {getNowTimeInThai()}"
            
            await cmd.sayThatChanel(mes,strr)
        

        if thisCmd["command"]==(DEB + "q_remove"):
            if len(thisCmd["args"]) < 1:
                await cmd.sayThatChanel(mes,"ล บ ค ว า ม ว่ า ง เ ป ล่ า")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"ID ควรเป็นจำนวนเต็มนะะนะนะนะนะนะ")
            else:
                idQ = int(thisCmd["args"][0])
                if idQ > questionManager.lenAllQuest() or idQ <= 0:
                    await cmd.sayThatChanel(mes,f"หา id {idQ} ไม่เจออ่ะะะ")
                else:
                    strRes = f":x:ลบคำถาม `{dataBASS.questions[idQ-1][1]}` ที่ถามว่า `{dataBASS.questions[idQ-1][2]}` เรียบร้อยแล้ว...\nสำเร็จโดย {mes.author.name}"
                    idms = questionManager.removeQuestionInd(idQ-1)
                    for idd in idms:
                        delMes = await uID2Message(client,idd)
                        await delMes.delete()
                    await questionManager.reloadMessage(client)
                    await client.get_channel(ENUM.QUE_HIS_CHANNEL).send(strRes)
            await mes.delete()

        if thisCmd["command"]==(DEB + "q_clear"):
            strRes = f":fireworks:ระเบิดทุกๆคำถามเรียบร้อยแล้ว <:knowthatfeel:704310526200512622>\nสำเร็จโดย {mes.author.name}"
            
            for i in range(questionManager.lenAllQuest()-1,-1,-1):
                idms = questionManager.removeQuestionInd(i)
                for idd in idms:
                    delMes = await uID2Message(client,idd)
                    await delMes.delete()
            
            await client.get_channel(ENUM.QUE_HIS_CHANNEL).send(strRes)
            await mes.delete()
        
        if thisCmd["command"]==(DEB + "q_answer"):
            if len(thisCmd["args"]) < 1:
                await cmd.sayThatChanel(mes,"ตอบข้อไหนอ่ะ??")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"ID ควรเป็นจำนวนเต็มนะะนะนะนะนะนะ")
            elif thisCmd["value"] == "":
                await cmd.sayThatChanel(mes,"ตอบความว่างเปล่า??\nถ้าจะลบคำถามให้ใช้ `q_remove(<id>)` นะๆ")
            else:
                idQ = int(thisCmd["args"][0]) - 1
                
                if idQ >= questionManager.lenAllQuest() or idQ < 0:
                    await cmd.sayThatChanel(mes,f"หา id {idQ} ไม่เจออ่ะะะ")
                else:
                    bigQuestId = dataBASS.questions[idQ][1]
                    bigQuest = dataBASS.questions[idQ][2]
                    bigQuestAnswer = thisCmd["value"]
                    strRes = f":white_check_mark:ตอบคำถามสำเร็จโดย {mes.author.name}\nในข้อ `{bigQuestId}`\n:regional_indicator_q: : `{bigQuest}`\n:regional_indicator_a: : `{bigQuestAnswer}`"
                    idms = questionManager.removeQuestionInd(idQ)
                    
                    userMess = await uID2Message(client,idms[0])
                    await userMess.channel.send(ENUM.QUEST_USER%(bigQuestId,bigQuest,bigQuestAnswer))
                    await userMess.delete()

                    admiMess = await uID2Message(client,idms[1])
                    await admiMess.delete()

                    await questionManager.reloadMessage(client)
                    await client.get_channel(ENUM.QUE_HIS_CHANNEL).send(strRes)
            await mes.delete()
    #PART Verify
    if thisCmd["command"]==(DEB + "verify"):
        
        correctedRole = False
        if hasattr(mes.author, 'roles'):
            for r in mes.author.roles:
                correctedRole = correctedRole or (str(r) == "return 0;")
        else:
            return

        if not correctedRole:
            await mes.delete()
            return
        
        code = thisCmd["value"].strip()
        idPer = mes.author.id
        if code == "":
            await mes.author.send("ฮัลโล่ว เอ็งส่งโค้ดว่างเปล่ามาอ่ะ ตรวจไม่ได้เว้ยยย")
            await mes.delete()
            return

        if Verify.getLenCodes(idPer) == 5:
            await mes.author.send(ENUM.VERIF_NOPE)
            await mes.delete()
            return

        Verify.addCode(idPer, code)
        result = Verify.doJudge(code)

        if result[1]:#pass
            newRole = discord.utils.get(mes.guild.roles,name = "OTOGer")
            await mes.author.send(f"```cpp\n{code}```\n")
            await mes.author.send(result[0])
            await mes.author.edit(roles = [newRole])
            await mes.delete()
            Verify.removeId(idPer)
        else:
            await mes.author.send(f"```cpp\n{code}```\n")
            await mes.author.send(result[0])
            remain = 5 - Verify.getLenCodes(idPer)
            if remain == 0:
                await mes.author.send(ENUM.VERIF_END)
            else:
                await mes.author.send(ENUM.VERIF_REMAIN%(remain))
            await mes.delete()


def main(token:int, isTest:bool = False):
    global DEB,NAME

    if isTest:
        cmd.defaultName = f"น้อนตัวน้อย V{ENUM.VER}"
        NAME = f"น้อนตัวน้อย V{ENUM.VER}"
        DEB = ">>"


    try:
        client.run(token)
    except:
        print(f"Wrong Token or Fucked up\nhere is token:{token}")
        exit(1)


