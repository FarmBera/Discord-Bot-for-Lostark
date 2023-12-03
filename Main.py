import discord
from datetime import datetime
# import os, re
# import time
# import urllib.request

TOKEN = None
CHANNEL_ID = None
# PREFIX = '[' # 붙일 접두사 (지금은 작동 안함)

# 임시 배열
temp = []

# 토큰 불러오기 (토큰 저장된 파일 읽어서 )
file_path = "TOKEN.txt"
with open(file_path, 'r', encoding="UTF-8") as f:
    lines = f.readlines()
    for line in lines:
        temp.append(line.replace('\n', ''))

# 기록용 파일 열기
log_file_path = "ConversationLog.txt"
log_f = open(log_file_path, 'a', encoding="UTF-8")

# 시간 기록
now = datetime.now()
formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
log_f.write('\n' + formatted_date_time + '\n')

# 토큰 변수에 저장
TOKEN = temp[0]
CHANNEL_ID = temp[1]


# Working
""" 현재 나는 오류
파일 이름 불러와서 출력하면 
한글 인코딩 문제로 딕셔너리에서 key 값을 이용한 value를 뽑아낼 수가 없음
"""
pict_dir = {
    "[안줘": "image/01_모코코콘1_14_안줘.png",
    "[눈물팡": "image/01_모코코콘1_02_눈물팡_.png",
    "[죽은척": "image/02_모코코콘2_25_죽은척.png",
    "[놀자에몽": "image/00_SE_놀자에몽.png",
    "[두렵다": "image/02_모코코콘2_12_두렵다.png",
    "[빠직": "image/01_모코코콘1_17_빠직.png",
    "[놀자에요": "image/00_SE_놀자에요.png",
    "[핥짝": "image/02_모코코콘2_18_핥짝.png",
    "[모무룩": "image/01_모코코콘1_24_모무룩.png",
    "[신나": "image/02_모코코콘2_28_신나.png",
    "[멘탈": "image/01_모코코콘1_07_멘탈.png",
    "[빛": "image/02_모코코콘2_05_빛.png",
    "[방긋": "image/01_모코코콘1_09_방긋.png",
    "[좋아요": "image/02_모코코콘2_03_좋아요.png",
    "[호에엥": "image/02_모코코콘2_02_호에엥.png",
    "[못참지": "image/02_모코코콘2_19_못참지.png",
    "[헤헷": "image/02_모코코콘2_09_헤헷.png",
    "[줘": "image/01_모코코콘1_13_줘.png",
    "[물끄럼": "image/01_모코코콘1_12_물끄럼.png",
    "[ㅋㅋㅋ": "image/01_모코코콘1_06_ㅋㅋㅋ.png",
    "[이이잉": "image/02_모코코콘2_08_이이잉.png",
    "[카멘음": "image/00_SE_카멘_음.png",
    "[문열어": "image/01_모코코콘1_25_문열어.png",
    "[물음표": "image/01_모코코콘1_08_물음표.png",
    "[히죽": "image/02_모코코콘2_11_히죽.png",
    "[뀨": "image/02_모코코콘2_24_뀨.png",
    "[침묵": "image/02_모코코콘2_13_침묵.png",
    "[멈춰]": "image/02_모코코콘2_26_멈춰!.png",

}


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        # 봇 상태 바꾸기
        await self.change_presence(
            status=discord.Status.online, 
            activity=discord.Game("이모티콘 잔뜩 준비 완료")
        )

    async def on_message(self, message):
        trim_text = message.content.replace(" ", "")

        def log_message(auth, msgcontent):
            msg = str(auth) + ": " + str(msgcontent)
            print(msg)
            log_f.write(msg + '\n')

        if message.author == self.user:
            return
        elif (message.content == "[로아콘도움"):
            image = discord.File("image/00_SE_놀자에요.png", filename="image.png")
            embed = discord.Embed(title="지원이 도착했습니다!", color=0x00ff56)
            embed.set_thumbnail(url='attachment://image.png')
            # 모든 명령어 뺴내기
            all_commands = ""
            for key in pict_dir.keys():
                all_commands += str(f"{key}, ")
            embed.add_field(
                name="사용 가능한 명령어", 
                value=all_commands, 
                inline=True
            )
            await message.channel.send(embed=embed, file=image)
        elif (message.content == '[이스터에그'):
            await message.channel.send('강산씌!')
        elif (trim_text == '' or None):
                return
        elif (trim_text in pict_dir.keys()): 
            image = discord.File(pict_dir[trim_text], filename="image.png")
            embed = discord.Embed()
            # embed = discord.Embed(title=str(pict_dir[trim_text]), color=0x00ff56)
            # embed = discord.Embed(title=str(pict_dir[trim_text]))
            embed.set_image(url='attachment://image.png')
            await message.channel.send(embed=embed, file=image)
            log_message(message.author, message.content)
        else: 
            log_message(message.author, message.content)

# 디스코드 봇 실행
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)