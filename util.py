
import time

def isInt(wut:str)->bool:
    try:
        int(wut)
    except:
        return False
    
    return True

daysInThai = ["จันทร์","อังคาร","พุธ","พฤหัสบดี","ศุกร์","เสาร์","อาทิตย์"]
monthsInThai = ["","มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]

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

if __name__ == "__main__":
    print(getNowTimeInThai())