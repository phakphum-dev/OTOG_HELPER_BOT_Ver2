
import time, random

def isInt(wut:str)->bool:
    try:
        int(wut)
    except:
        return False
    
    return True

daysInThai = ["จันทร์","อังคาร","พุธ","พฤหัสบดี","ศุกร์","เสาร์","อาทิตย์"]
monthsInThai = ["","มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]

def formatInThai(thatTime:float)->str:
    tt = time.gmtime(thatTime + 7*60*60)
    return f"เวลา {tt.tm_hour:02d}:{tt.tm_min:02d}:{tt.tm_sec:02d} วัน{daysInThai[tt.tm_wday]}ที่ {tt.tm_mday} เดือน{monthsInThai[tt.tm_mon]} ปี {tt.tm_year+543}"

def getNowTimeInThai()->str:
    now = time.localtime()
    return f"เวลา {now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d} วัน{daysInThai[now.tm_wday]}ที่ {now.tm_mday} เดือน{monthsInThai[now.tm_mon]} ปี {now.tm_year+543}"

def nameWithPlace(name:str, place:int)->str:
    if place == 1:
        return f":one:{name}:first_place:"
    elif place == 2:
        return f":two:{name}:second_place:"
    elif place == 3:
        return f":three:{name}:third_place:"
    elif place == 4:
        return f":four:{name}:medal:"
    elif place == 5:
        return f":five:{name}:medal:"
    elif place == 6:
        return f":six:{name}:medal:"
    elif place == 7:
        return f":seven:{name}:medal:"
    elif place == 8:
        return f":eight:{name}:medal:"
    elif place == 9:
        return f":nine:{name}:medal:"
    elif place == 10:
        return f":keycap_ten:{name}:medal:"
    return ""

def lenTimeInThai(time1:float,time2:float,lim:str = "")->str:
    delta = int(abs(time1 - time2))
    sec = delta%60
    minu = (delta//60)%(60)
    hour = (delta//(60*60))%(24)
    days = (delta//(60*60*24))

    res = ""
    if days != 0: res += f"{days} วัน "
    if hour != 0 and lim != "h": res += f"{hour} ชั่วโมง "
    if minu != 0 and lim != "m" and lim != "h": res += f"{minu} นาที "
    if sec != 0 and lim != "s" and lim != "m" and lim != "h": res += f"{sec} วินาที "
    return res.strip()

def pickOne(x:list):
    return x[random.randint(0,len(x)-1)]


def isSleepTime():
    now = time.localtime()
    return 2 <= now.tm_hour <= 6

def messageToUniqueID(mes):
    mesID = mes.id
    chanID = mes.channel.id
    return (mesID,chanID)

async def uID2Message(client,Ids):
    mesId = Ids[0]
    chaId = Ids[1]
    try:
        Cha = await client.fetch_channel(chaId)
    except:
        
        return None
    

    try :
        mes = await Cha.fetch_message(mesId)
    except:
        return None

    return mes


if __name__ == "__main__":
    print(getNowTimeInThai())