import discord


TOKEN = None
CHANNEL_ID = None

# 임시 배열
temp = []

# 토큰 불러오기 (토큰 저장된 파일 읽어서 )
file_path = "TOKEN.txt"
with open(file_path, "r") as file:
    lines = file.readlines()
    for line in lines:
        temp.append(line.replace('\n', ''))
        # print(line)

# 토큰 변수에 저장
# print(temp)
TOKEN = temp[0]
CHANNEL_ID = temp[1]

# 저장 결과 출력
# print(f'token >> {TOKEN}')
# print(f'channel id >> {CHANNEL_ID}')


# 디스코드 클라이언트 클래스
class MyClient(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        await channel.send("Hello World")


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)