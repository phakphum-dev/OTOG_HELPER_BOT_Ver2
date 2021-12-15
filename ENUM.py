from os import path

PATH = path.dirname(__file__)
VER = "Beta 2.0.2"
DEBUG_CHANNEL = 920575763063910400
ANN_CHANNEL = 920575234128638012
CON_ANN_CHANNEL = 920575234128638012
QUE_CHANNEL = 920577600835964928
QUE_HIS_CHANNEL = 920577689537097748
ANN_TITLE = ":loudspeaker:@everyoneปุกาศ:loudspeaker:\n"

CON_ANN_TEXT = "ทุกๆคนน\nอีก `%s` จะมีคอนเทส!!\n%s"
CON_FUNNY_Q = ["わくわく", "เตรียมตัวให้พร้อมมม",
               "เตรียมคีย์บอร์ดและ #include ให้พร้อม", "เตรียมตัวเปิดตัว IDE คู่ใจได้เลย"]


HELLO_TEXT = ["สวัสดีเจ้า", "สวัสดีจ้า", "สวัสดีครับ", "สวัสดีค่ะ", "ສະບາຍດີ", "Annyeonghaseyo", "Kon'nichiwa", "Hello",
              "привет!", "ว่าไง", ";w;?", "Meow Meooww?", ":wave:", "https://giphy.com/gifs/capoo-halloween-3ov9k0OmfNYeLdK4gg", "Nǐ hǎo"]


# Guess number game
GNG_COR1 = ":white_check_mark:ถถถถถูกต้อง ตัวเลขข้าคือ %d เก่งไม่เบาเลยนะเจ้า @author\nhttps://tenor.com/view/think-about-it-use-your-brain-use-the-brain-think-brain-gif-7914082"
GNG_LESS = ":arrow_up: %d ของเจ้าน่ะมันต่ำเกิน... เหลือ: %d ครั้งนะเจ้า @author"
GNG_GREA = ":arrow_down: %d ของเจ้าน่ะมันสูงเกิน... เหลือ: %d ครั้งนะเจ้า @author"
GNG_LOSS_LESS = ":x: %d น่ะมันต่ำเกิน... เจ้าแพ้แล้ว @author"
GNG_LOSS_GREA = ":x: %d น่ะมันสูงเกิน... เจ้าแพ้แล้ว @author"
GNG_LOSS_ANS = "เฉลยคือ %d <a:capoobounce:704257345966047242>"
GNG_COR2 = ":white_check_mark:ข้าล้อเล่น ๆๆ จริง ๆ %d มันถูกละ555 เจ้าชนะนะ @author <a:capoobounce:704257345966047242>"
GNG_GIVE = ":x:เจ้ายอมแพ้สินะ @author"


# MINI_Grader
JUDGE_BIG_VER = {
    "JudgeError": "เฮ้ยๆๆๆ มันไม่ใช่สิที่ควรจะเป็น\nงั้นรอก่อนนะ หรือถ้าไม่มีอะไรทำก็ด่า Admin เล่นๆได้ :)",
    "SrcError": "ฮั่นแน่น่น่น่ อยากจะลองบึ้มเกรดเดอร์ล่ะสิหึ\nไม่ได้แดกกูหรอก",
    "Compile Error": "โค้ดเจ้ายังอ่อนหัด!!"
}
JUDGE_VERDICT = "ผลตรวจคือ `%s`"

VERIF_PERFECT = "ยินดีต้อนรับเข้าสู่เซิฟแห่งความฮา...OTOG"
VERIF_NPERFEC = "แต่ก็ยังไม่ผ่านอ่ะนะ ลองใหม่นะหึหึ"
VERIF_REMAIN = "ตอนนี้เหลือโอกาสเพียง **%d** ครั้งเท่านั้น ระวังด้วย"
VERIF_END = "เจ้าหมดโอกาสแล้ว...\nลองติดต่อรุ่นพี่เอาครับ"
VERIF_NOPE = "ส่งมาก็ไม่ตรวจครับ หยิ่ง...\nลองติดต่อรุ่นพี่เอาครับ:)"

CONTEST_NO = "ไม่มีการแข่งจ้าา วันนี้นอนได้\nอนาคตอาจจะมี"

TIME_F_NORMAL = 60*10//5
TIME_F_CONTEST = 60*2//5

QUEST_USER = ":question:ในข้อ `%s` \n:regional_indicator_q: : `%s`\n:regional_indicator_a: : %s"
QUEST_ADMIN = ":question:#%d : มีน้องถามมาว่า ในข้อ `%s` ถามมาว่า `%s`"
