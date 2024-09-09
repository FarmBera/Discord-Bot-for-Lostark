import discord
from discord.ext import tasks
from discord import app_commands  # , Interaction
# from datetime import timedelta, datetime, timezone
import datetime
import csv

# import time, json, sys, pandas as pd

from MainList import pict_dir
import req_notice as request_notice
import req_island as request_island
# import request.req_island as request_island
from module.kr_jamo import korean_jamo
from Variables import BOT_NOTICE
from Variables import PrivacyPolicy
from Variables import ch_list as ch_list
from Variables import send_log_request
from Variables import BOT_GAME
from Variables import BOT_PATCHNOTE_TITLE
from Variables import BOT_PATCHNOTE
from Variables import SPREADSHEET_URL

# TODO: Commit 전에 토큰 확인할 것!
from TOKEN import TOKEN_BOT as TOKEN

log_file_path = "logfile.csv"


# Write Log Files
def send_log(cmd, time, user, guild, channel):
    log_f = open(log_file_path, "a", encoding="UTF-8", newline="")
    # time = (time + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S") # for KR Timezone
    time = (time + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")  # for US Timezone
    wr = csv.writer(log_f)
    wr.writerow([user, time, cmd, guild, channel])
    log_f.close()


kst = datetime.timezone(datetime.timedelta(hours=9))
times = [
    datetime.time(hour=17, minute=42, tzinfo=kst),
]

class MyClient(discord.Client):
    async def on_ready(self):
        await self.wait_until_ready()
        await tree.sync()
        # Change Bot State
        await self.change_presence(
            status=discord.Status.online, activity=discord.Game(BOT_GAME)
        )
        self.auto_send_notice.start()  # for Lostark Notice
        print(f"Logged on as {self.user}!")
        # user = await client.fetch_user()
        # await user.send("Bot Running Start!")


    # Auto Check New LostArk Notice
    @tasks.loop(minutes=5.0)
    async def auto_send_notice(self):
        request_notice.RunRequest()
        notice_result = request_notice.to_send_DESC
        if notice_result is None or notice_result == "":
            return
        
        for ch in ch_list:
            embed = discord.Embed(
                title="새로운 로스트아크 공지사항이 올라왔습니다!",
                description=notice_result,
                color=0xCEFF00,
            )
            channel = await self.fetch_channel(ch)
            # image = discord.File("image_origin/image/banguht.png", filename="image.png")
            # embed.set_thumbnail(url="attachment://image.png")
            # await channel.send(embed=embed, file=image)
            await channel.send(embed=embed)  # only send text

        send_log_request(type="AutoCheckNotice", istrue=True, var1="Notice Sent")
        return


    # on Message imcoming
    async def on_message(self, message):
        trim_text = message.content.replace(" ", "")

        if message.author == self.user:
            return

        # Print Emoticon
        elif trim_text in pict_dir.keys():
            usrname = message.author.display_name
            usr_josa = korean_jamo(usrname)
            
            image = discord.File(pict_dir[trim_text], filename="image.png")
            embed = discord.Embed(
                # description=f"**{usrname}** (이)가 **{trim_text}** 전송!",
                description=f"**{usrname}**{usr_josa} **{trim_text}** 전송!",
            )
            embed.set_image(url="attachment://image.png")
            await message.delete()
            await message.channel.send(embed=embed, file=image)
            send_log(
                cmd=trim_text,
                time=message.created_at,
                user=message.author,
                guild=message.guild,
                channel=message.channel,
            )

        else:
            return


# Execute Discord Bot
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)


cmd_102 = "패치노트"
@tree.command(name=cmd_102, description="로아스티커 봇 패치노트")
async def self_patchnote(interaction: discord.Interaction):
    all_commands = []  # Conut all commands
    for key in pict_dir.keys():
        all_commands.append(str(f"{key}"))
    # Create Discord Embed
    embed = discord.Embed(
        title=BOT_PATCHNOTE_TITLE,
        description=BOT_PATCHNOTE,
        color=0x00FF56,
    )
    # image = discord.File("image_origin/image/playtogeth.png", filename="image.png")
    # embed.set_thumbnail(url='attachment://image.png')
    # embed.add_field(name="명령어에 대한 지원이 도착했습니다!", value=result, inline=True)
    await interaction.response.send_message(embed=embed)
    send_log(
        cmd=f"cmd:{cmd_102}",
        time=interaction.created_at,
        user=interaction.user,
        guild=interaction.guild,
        channel=interaction.channel,
    )


cmd_103 = "로아콘공지"
@tree.command(name=cmd_103, description="로아 스티커 봇에 대하여...")
async def self_notice(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"공지사항",
        description=BOT_NOTICE,
        color=0xCEFF00,
    )
    # image = discord.File("image_origin/image/saaddd.png", filename="image.png")
    # embed.set_thumbnail(url='attachment://image.png')
    # await interaction.response.send_message(embed=embed, file=image)
    await interaction.response.send_message(embed=embed)
    send_log(
        cmd=f"cmd:{cmd_103}",
        time=interaction.created_at,
        user=interaction.user,
        channel=interaction.channel,
        guild=interaction.guild,
    )


cmd_105 = "로아콘도움"
@tree.command(name=cmd_105, description="로아 이모티콘 명령어 도움말")
async def self_help(interaction: discord.Interaction):
    all_commands = []  # Count all commands's length
    for key in pict_dir.keys():
        all_commands.append(str(f"{key}"))

    embed = discord.Embed(
        title="이모티콘 명령어 모음 (스프레드시트)",
        url=SPREADSHEET_URL,
        description=f"""
        ## 명령어에 대한 지원이 도착했습니다!
        > 사용 가능한 명령어: {len(all_commands)}개
        
        **디스코드 출력 텍스트 제한**으로 인하여, 
        **봇 명령어 조회**는 *상단 링크 참고* 부탁드립니다.  
        
        ## 사용법
        채팅창에 "[" 입력하고 뒤에 로아콘 이름 입력!
        ex)  [놀자에요
        
        또는, **/로아콘** 커맨드 입력!
        
        (현재 자동완성 기능은 지원하지 않습니다. )
        """,
        color=0x00FF56,
    )
    # 사진 있는 버전
    # image = discord.File("image_origin/image/playtogeth.png", filename="image.png")
    # embed.set_thumbnail(url="attachment://image.png")
    # embed.add_field(name="명령어에 대한 지원이 도착했습니다!", value=result, inline=True)
    # await interaction.response.send_message(embed=embed, file=image)

    # 사진 없는 버전
    await interaction.response.send_message(embed=embed)
    send_log(
        cmd=f"cmd:{cmd_105}",
        time=interaction.created_at,
        user=interaction.user,
        channel=interaction.channel,
        guild=interaction.guild,
    )
    # (trim_text, message.created_at, message.author, message.channel, message.guild)


cmd_106 = "최근공지"
@tree.command(name=cmd_106, description="최근 로스트아크 공지 n개를 불러올 수 있습니다. (최대 6개)")
async def self_loa_getnotice(interaction: discord.Interaction, number: int):
    # COUNT = 5
    COUNT = number
    limit = 6  # number limiter
    if COUNT > limit:
        embed = discord.Embed(
            title=f"개수 제한",
            description=f"최대 {limit}개까지만 불러올 수 있습니다. \n>>{COUNT} 를 입력하셨습니다. ",
            color=0xFFAA00,
        )
        image = discord.File(
            "image_origin/image_kong/ppongkong.png", filename="image.png"
        )
        embed.set_thumbnail(url="attachment://image.png")
        await interaction.response.send_message(embed=embed, file=image)
        send_log(
            cmd=f"cmd:{cmd_106}:{COUNT}",
            time=interaction.created_at,
            user=interaction.user,
            guild=interaction.guild,
            channel=interaction.channel,
        )
    elif COUNT <= 0:
        embed = discord.Embed(title=f"가장 최근 공지 {COUNT}...개...?", color=0xFFAA00)
        image = discord.File("image_origin/image/whatyousay.png", filename="image.png")
        embed.set_thumbnail(url="attachment://image.png")
        await interaction.response.send_message(embed=embed, file=image)
        send_log(
            cmd=f"cmd:{cmd_106}:{COUNT}",
            time=interaction.created_at,
            user=interaction.user,
            guild=interaction.guild,
            channel=interaction.channel,
        )
    else:
        request_notice.open_file()
        # request_notice.get_all_res_data(0)
        DESCRYPTION = ""
        # DESCRYPTION += f"**{interaction.user}**(이)가 **{cmd_106}** (을)를 보냈어요\n "
        for i in range(COUNT):
            time = datetime.strptime(
                request_notice.res_arr[i]["Date"], "%Y-%m-%dT%H:%M:%S.%f"
            ).strftime("%Y-%m-%d %H:%M")
            DESCRYPTION += f"""\n## [{request_notice.res_arr[i]["Title"]}]({request_notice.res_arr[i]["Link"]})
            {time}에 작성된 {request_notice.res_arr[i]["Type"]} 글입니다. 
            """
        embed = discord.Embed(
            title=f"가장 최근 공지 {COUNT}개!", description=DESCRYPTION, color=0xCEFF00
        )
        image = discord.File("image_origin/image/banguht.png", filename="image.png")
        embed.set_thumbnail(url="attachment://image.png")
        await interaction.response.send_message(embed=embed, file=image)
        send_log(
            cmd=f"cmd:{cmd_106}:{COUNT}",
            time=interaction.created_at,
            user=interaction.user,
            guild=interaction.guild,
            channel=interaction.channel,
        )


cmd_107 = "모험섬"
@tree.command(name=cmd_107, description="오늘의 모험섬 목록 가져오기")
async def self_adventure_island(interaction: discord.Interaction):
    # 캘린더 컨텐츠 불러오기
    request_island.RunRequest()
    if request_island.to_send_DESC is None or request_island.to_send_DESC == "":
        return
    embed = discord.Embed(
        title="오늘의 모험섬 컨텐츠", description=request_island.to_send_DESC, color=0xCEFF00
    )
    await interaction.response.send_message(embed=embed)
    send_log(
        cmd=f"cmd:{cmd_107}",
        time=interaction.created_at,
        user=interaction.user,
        guild=interaction.guild,
        channel=interaction.channel,
    )


cmd_108 = "캘린더"  ### 미완성
@tree.command(name=cmd_108, description="오늘의 주요 캘린더 일정 가져오기")
async def self_calendar(interaction: discord.Interaction):
    # todo_delay: 캘린더 컨텐츠 불러오는거 구현

    # Not prepared command
    embed = discord.Embed(
        title="아직 준비 중인 명령어입니다...",
        # description=request_calendar.to_send_DESC,
        # color=0xceff00
        color=0xFFAA00,
    )
    image = discord.File("image_origin/image/saaddd.png", filename="image.png")
    embed.set_thumbnail(url="attachment://image.png")
    await interaction.response.send_message(embed=embed, file=image)
    send_log(
        cmd=f"cmd:{cmd_108}",
        time=interaction.created_at,
        user=interaction.user,
        guild=interaction.guild,
        channel=interaction.channel,
    )


cmd_140 = "캐릭터"  ### 미완성
@tree.command(name=cmd_140, description="오늘의 주요 캘린더 일정 가져오기")
async def self_character(interaction: discord.Interaction, nickname: str):
    # todo_delay: 캐릭터 정보 불러오는거 구현

    # Not prepared command
    embed = discord.Embed(
        title="아직 준비 중인 명령어입니다...",
        description=f"입력한 닉네임: **{nickname}**",
        # description=request_calendar.to_send_DESC,
        # color=0xceff00
        color=0xFFAA00,
    )
    image = discord.File("image_origin/image/saaddd.png", filename="image.png")
    embed.set_thumbnail(url="attachment://image.png")
    await interaction.response.send_message(embed=embed, file=image)

    send_log(
        cmd=f"cmd:{cmd_140}",
        time=interaction.created_at,
        user=interaction.user,
        guild=interaction.guild,
        channel=interaction.channel,
    )


cmd_180 = "개인정보처리방침"
@tree.command(name=cmd_180, description="LoaStickers-Bot-개인정보처리방침")
async def self_privacy_policy(interaction: discord.Interaction):
    embed = discord.Embed(
        title="",
        description=PrivacyPolicy,
        color=0xFFFF00
    )
    await interaction.response.send_message(embed=embed)


cmd_200 = "로아콘"
@tree.command(name=cmd_200, description="특정 로아콘을 전송합니다. ")
async def self_loacorn(interaction: discord.Interaction, emoticon_name: str):
    # todo_done: 로아콘 전송하는거 만들기
    trim_text = emoticon_name.replace(" ", "")
    trim_text = f"[{trim_text}"
    usrname = interaction.user.display_name

    # Print Emoticon
    if trim_text not in pict_dir.keys():
        image = discord.File("image_origin/image/saaddd.png", filename="image.png")
        embed = discord.Embed(
            title=f"**{emoticon_name}** 는 없는 이모티콘 입니다...",
            description=f"**/로아콘도움** 명령어를 입력하면 도움말이 나옵니다!",
            # color=0xceff00
            color=0xFFAA00,
        )
        embed.set_thumbnail(url="attachment://image.png")

    else:
        image = discord.File(pict_dir[trim_text], filename="image.png")
        embed = discord.Embed(
            title=f"**{emoticon_name}**",
        )
        embed.set_image(url="attachment://image.png")

    await interaction.response.send_message(embed=embed, file=image)

    send_log(
        cmd=f"cmd:{cmd_200}:{emoticon_name}",
        time=interaction.created_at,
        user=interaction.user,
        guild=interaction.guild,
        channel=interaction.channel,
    )


# Finally, Run Bot
client.run(TOKEN)
