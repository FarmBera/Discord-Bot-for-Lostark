PATCH_TYPE = ( "점검", "패치", "긴급 점검" )
TITLE = f"Server is Under Maintance..."

TYPE = input("Maintance Types (No Input:점검, 1:패치, 2:긴급점검) >> ")
if (TYPE == ""):
    TYPE = PATCH_TYPE[0]
elif (TYPE == "1"):
    TYPE = PATCH_TYPE[int(TYPE)]
elif (TYPE == "2"):
    TYPE = PATCH_TYPE[int(TYPE)]

# print(f"TYPE >> {TYPE}, 유형:{type(TYPE)}")

MaintanceTime = str(input(f"{TYPE} 완료 예정 시각 >> "))
if (MaintanceTime == ""):
    MaintanceTime = f"알 수 없음"

DESC_PLUS = input("추가 설명 >> ")
if (DESC_PLUS == ""):
    DESC_PLUS == None


DESC = f"""
## 지금은 서버 {TYPE} 중 입니다.
{DESC_PLUS}
이용에 불편을 드려 죄송합니다.  
### 예상 완료 시간 
## {MaintanceTime}  
패치 작업은 조기 종료 될 수 있으며, 또한 지연될 수 있음을 알립니다. 
"""



# """
import discord
from discord import app_commands, Interaction
from datetime import timedelta
import csv
from MainList import pict_dir
from TOKEN import TOKEN_BOT as TOKEN

# 로그파일 기록하기
def send_log(cmd, time, user, guild, channel):
    log_f = open('logfile.csv', 'a', encoding='utf-8', newline='')
    time = (time + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
    wr = csv.writer(log_f)
    wr.writerow([user, time, f"[점검중]{cmd}", guild, channel])
    log_f.close()

class MyClient(discord.Client):
    async def on_ready(self):
        print('[Maintance] Logged on as {0}!'.format(self.user))
        # Change Bot State
        await self.change_presence(
            status=discord.Status.do_not_disturb, 
            activity=discord.Game("서버 점검")
        )
    
    async def on_message(self, message):
        # def send_log(picture, time, user, channel, guild):
        #     # 기록용 파일 열기
        #     log_file_path = "LogFile.txt"
        #     log_f = open(log_file_path, "a", encoding="UTF-8")
        #     time = (time + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
        #     log_f.write(f"\n{user}//{time} //>> Sent //{picture} at //{guild} //{channel}")
        #     log_f.close()
        
        trim_text = message.content.replace(" ", "")
        embed = discord.Embed(
            title=TITLE,
            description=DESC, 
            color=0xff0f00
        )
        image = discord.File("image_origin/image/saaddd.png", filename="image.png")
        embed.set_thumbnail(url='attachment://image.png')
        
        if message.author == self.user: return
        elif (message.content == "[로아콘도움"):
            await message.delete()
            await message.channel.send(embed=embed, file=image)
            send_log(cmd=trim_text, time=message.created_at, user=message.author, channel=message.channel, guild=message.guild)
        # elif (trim_text == '' or None): return
        elif (trim_text in pict_dir.keys()): 
            await message.delete()
            await message.channel.send(embed=embed, file=image)
            send_log(cmd=trim_text, time=message.created_at, user=message.author, channel=message.channel, guild=message.guild)
        else: return

# Execute Discord Bot
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

embed = discord.Embed(
    title=TITLE,
    description=DESC, 
    color=0xff0f00
)
image = discord.File("image_origin/image/saaddd.png", filename="image.png")
embed.set_thumbnail(url='attachment://image.png')

# cmd_0 = "test"
# @tree.command(name=cmd_0, description="테스트를 위한 명령어")
# async def self_test(interaction: discord.Interaction, name: str):
#     await interaction.response.send_message(f"Hello {name}!")
#     send_log(cmd=f"cmd:{cmd_0}", time=interaction.created_at, user=interaction.user, guild=interaction.guild, channel=interaction.channel)


cmd_102 = "패치노트"
@tree.command(name=cmd_102, description="로아스티커 봇 패치노트")
async def self_help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embed)
    send_log(cmd=f"cmd:{cmd_102}", time=interaction.created_at, user=interaction.user, guild=interaction.guild, channel=interaction.channel)


cmd_103 = "로아콘공지" ### 미완성
# cmd_103 = "로아콘소개" ### 미완성
@tree.command(name=cmd_103, description="로아 스티커 봇에 대하여...")
async def self_notice(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embed)
    send_log(f"cmd:{cmd_103}", interaction.created_at, interaction.user, interaction.channel, interaction.guild)   


cmd_105 = "로아콘도움"
@tree.command(name=cmd_105, description="로아 이모티콘 명령어 도움말")
async def self_help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embed, file=image)
    send_log(f"cmd:{cmd_105}", interaction.created_at, interaction.user, interaction.channel, interaction.guild)
    # (trim_text, message.created_at, message.author, message.channel, message.guild)


cmd_106 = "최근공지"
@tree.command(name=cmd_106, description="최근 로스트아크 공지 n개를 불러올 수 있습니다. (최대 6개)")
async def self_loa_latest_notice(interaction: discord.Interaction, number: int):
    await interaction.response.send_message(embed=embed, file=image)
    send_log(cmd=f"cmd:{cmd_106}", time=interaction.created_at, user=interaction.user, guild=interaction.guild, channel=interaction.channel)


cmd_107 = "모험섬"
@tree.command(name=cmd_107, description="오늘의 모험섬 목록 가져오기")
async def self_adventure_island(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embed)
    send_log(cmd=f"cmd:{cmd_107}", time=interaction.created_at, user=interaction.user, guild=interaction.guild, channel=interaction.channel)


cmd_108 = "캘린더" ### 미완성
@tree.command(name=cmd_108, description="오늘의 주요 캘린더 일정 가져오기")
async def self_calendar(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embed, file=image)
    send_log(cmd=f"cmd:{cmd_108}", time=interaction.created_at, user=interaction.user, guild=interaction.guild, channel=interaction.channel)   


cmd_200 = "로아콘" ### 미완성
@tree.command(name=cmd_200, description="특정 로아콘을 전송합니다. ")
async def self_loacorn(interaction: discord.Interaction, emoticon_name: str):
    await interaction.response.send_message(embed=embed, file=image)
    send_log(cmd=f"cmd:{cmd_200}:{emoticon_name}", time=interaction.created_at, user=interaction.user, guild=interaction.guild, channel=interaction.channel)


# Finally, Run Bot
client.run(TOKEN)
# """