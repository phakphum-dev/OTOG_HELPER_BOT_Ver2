import discord,random

from discord import utils
import ENUM,dataBASS
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
    await client.Set_Bot_Namae(NAME)


@client.event
async def Set_Bot_Namae(Namae):
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
            if str(r) == "Adminstator":
                isAdmin = True

    isAdminChan = False
    if hasattr(mes.channel, 'changed_roles'):
        for r in mes.channel.changed_roles:
            if str(r) == "Adminstator":
                isAdminChan = True

    isAdmin = isAdmin and isAdminChan


    #List command goes here
    if thisCmd["command"].startswith(DEB + "test"):
        await cmd.test(client)
    
    if thisCmd["command"].startswith(DEB + "help"):
        await cmd.sayhelp(mes.channel, isAdmin)
    
    if thisCmd["command"].startswith(DEB + "change_log"):
        await cmd.sayCLog(mes.channel)
    
    if thisCmd["command"].startswith(DEB + "tasks") or thisCmd["command"].startswith(DEB + "problems"):
        await cmd.sayNProblems(mes)

    if thisCmd["command"].startswith(DEB + "ranking"):
        await cmd.sayRanking(mes)
    

    if thisCmd["command"].startswith(DEB + "otogradio"):
        if len(thisCmd["args"]) < 1:
            await cmd.sayThatChanel(mes,"ไม่ใส่ชื่อเพลง ก็ไม่เปิดให้!!!")
        else:
            await cmd.sayThatChanel(mes,"OK จัดให้ @author")
            await cmd.sayThatChanel(mes,f":musical_note:playing... {thisCmd['args'][0]}")
            await cmd.sayThatChanel(mes,f"||ล้อเล่น ไม่มีหรอก||")
    

    if thisCmd["command"].startswith(DEB + "hello"):
        thisHello = ENUM.HELLO_TEXT[random.randint(0,len(ENUM.HELLO_TEXT) - 1)]
        await cmd.sayThatChanel(mes,f"{thisHello} @author")
    
    if thisCmd["command"].startswith(DEB + "baka"):
        await cmd.sayThatChanel(mes,"<:baka:704310333120053248>")
    
    if thisCmd["command"].startswith(DEB + "guess_num"):
        idPer = mes.author.id
        if GNG.remain(idPer) == -1:
            await cmd.sayThatChanel(mes,":crossed_swords:โห๋ 1-1 ได้ครับเจ้า @author:crossed_swords:")
            await cmd.gngHowto(mes.channel)
            GNG.initPer(idPer)
            dataBASS.saveFile()
        else:
            await cmd.sayThatChanel(mes,"เห้ย อย่าเล่นซ้ำเซ่!!!!??\nเวลาจะทายให้พิมพ์ `guess(ตัวเลข)` เอา!!! @author")
    
    if thisCmd["command"].startswith(DEB + "guess") and not thisCmd["command"].startswith(DEB + "guess_num"):
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

    if isAdmin:
        
        if thisCmd["command"].startswith(DEB + "version"):
            await cmd.sayThatChanel(mes,f"{ENUM.VER} เด้อออ")
        
        if thisCmd["command"].startswith(DEB + "ann"):
            if thisCmd["value"].strip() == "":
                await cmd.sayThatChanel(mes,"ประกาศความว่างเปล่า?")
            else:
                await cmd.sayAnn(mes, client, thisCmd["value"].strip())
        
        if thisCmd["command"].startswith(DEB + "say"):
            if len(thisCmd["args"]) < 1:
                await cmd.sayThatChanel(mes,"ประกาศในห้องไหนอ่ะะะ")
            elif thisCmd["value"].strip() == "":
                await cmd.sayThatChanel(mes,"ประกาศความว่างเปล่า?")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"Channel_ID ควรเป็น int นะะ")
            else:
                await cmd.sayAnn(mes, client, thisCmd["value"].strip(), int(thisCmd["args"][0]))
        
        if thisCmd["command"].startswith(DEB + "read"):
            if thisCmd["value"].strip() == "":
                await cmd.sayThatChanel(mes,"ให้อ่านความว่างเปล่า")
            else:
                print(f"=======Read form {mes.author.display_name}=======")
                print(thisCmd["value"].strip())
                await cmd.sayThatChanel(mes,"อ่านสำเร็จ!!")
        
        if thisCmd["command"].startswith(DEB + "shutdown"):
            await cmd.sayThatChanel(mes,"ลาก่อย")
            await client.close()
            exit(0)
        

        if thisCmd["command"].startswith(DEB + "score_board"):
            if len(thisCmd["args"]) < 1:
                await cmd.sayThatChanel(mes,"CONTEST ไหนนน")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"ID ควรเป็น int นะะ")
            else:
                await cmd.sayContestRanking(int(thisCmd["args"][0]), mes.channel)
        
        if thisCmd["command"].startswith(DEB + "send_score_board"):
            if len(thisCmd["args"]) < 2:
                await cmd.sayThatChanel(mes,"ดู Argument ดีๆ")
            elif not isInt(thisCmd["args"][0]):
                await cmd.sayThatChanel(mes,"ID ควรเป็น int นะะ")
            elif not isInt(thisCmd["args"][1]):
                await cmd.sayThatChanel(mes,"channel_id ควรเป็น int นะะ")
            else:
                await cmd.sayContestRanking(int(thisCmd["args"][0]), client.get_channel(int(thisCmd["args"][1])))


def main(token:int, isTest:bool = False):
    global DEB,NAME

    if isTest:
        NAME = f"น้อนตัวน้อย V{ENUM.VER}"
        DEB = ">>"


    try:
        client.run(token)
    except:
        print(f"Wrong Token or Fucked up\nhere is token:{token}")
        exit(1)


