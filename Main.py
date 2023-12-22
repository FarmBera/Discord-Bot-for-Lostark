# %%
import discord
from datetime import datetime
# import os, re
# import time
# import urllib.request

TOKEN = None
CHANNEL_ID = None
# PREFIX = '[' # 붙일 접두사 (지금은 작동 안함)

temp = [] # 임시 배열

# 토큰 저장된 파일 읽어서 
file_path = "TOKEN.txt"
with open(file_path, 'r', encoding="UTF-8") as f:
    lines = f.readlines()
    for line in lines:
        temp.append(line.replace('\n', ''))

# 토큰 변수에 저장
TOKEN = temp[0]
CHANNEL_ID = temp[1]

# %%
# Working
""" 현재 나는 오류
파일 이름 불러와서 출력하면 인코딩 문제로 딕셔너리에서 값을 뽑아낼 수가 없음
"""
pict_dir = {
    "[뀨": "image/ku.png",
    "[눈물팡": "image/sosaaaadd.png",
    "[놀자에요": "image/playtogeth.png",
    "[놀자에몽": "image/playmong.png",
    "[두렵다": "image/afraid.png",
    "[모무룩": "image/saaddd.png",
    "[멘탈": "image/mental.png",
    "[못참지": "image/cannot.png",
    "[멈춰]": "image/stop.png",
    "[문열어": "image/openthedoor.png",
    "[물음표": "image/whaaat.png",
    "[물끄럼": "image/lookstraight.png",
    "[방긋": "image/banguht.png",
    "[빛": "image/light.png",
    "[빠직": "image/bazik.png",
    "[신나": "image/happpy.png",
    "[안줘": "image/nogive.png",
    "[이이잉": "image/yiiiing.png",
    "[줘": "image/giveme.png",
    "[좋아요": "image/good.png",
    "[죽은척": "image/notdeath.png",
    "[침묵": "image/nocomment.png",
    "[ㅋㅋㅋ": "image/zzz.png",
    "[카멘음": "image/kamenummm.png",
    "[호에엥": "image/wooow.png",
    "[핥짝": "image/hehheh.png",
    "[헤헷": "image/hahat.png",
    "[히죽": "image/smile.png",
    
    # 응애 모코콩
    "[감사콩": "image_kong/thankyou.png",
    "[물줘콩": "image_kong/waterme.png",
    "[씨익콩": "image_kong/zkong.png",
    "[노래콩": "image_kong/songkong.png",
    "[뿅콩": "image_kong/ppongkong.png",
    "[더줘콩": "image_kong/givememorekong.png",
    "[도망콩": "image_kong/runkong.png",
    "[잘자콩": "image_kong/goodnightkong.png",
    "[냠냠콩": "image_kong/nyamyanmkong.png",
    "[촉촉콩": "image_kong/sadkong.png",
    "[꺼억콩": "image_kong/fullkong.png",
    "[츄릅콩": "image_kong/yummykong.png",

    # Special Edition
}

# %%
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
        if message.author == self.user:
            return
        elif (message.content == "[로아콘도움"):
            image = discord.File("image/playtogeth.png", filename="image.png")
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
        else:
            return

# 디스코드 봇 실행
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)