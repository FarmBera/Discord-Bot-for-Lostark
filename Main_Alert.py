import discord
from discord.ext import tasks
from discord import app_commands
import datetime
import csv


# TODO: Commit 전에 토큰 확인할 것!
from TOKEN import TOKEN_fortest as TOKEN

log_file_path: str = "logfile_alert.csv"
userAlert: bool = True
today = str(datetime.datetime.now())[:10]


kst = datetime.timezone(datetime.timedelta(hours=9))
times = [
    # datetime.time(hour=17, minute=55, tzinfo=kst),
    
    datetime.time(hour=18, minute=30, tzinfo=kst),  # 모험섬 19시: 30분 전
    datetime.time(hour=18, minute=55, tzinfo=kst),  # 모험섬 19시: 5분 전
    
    # datetime.time(hour=19, minute=20, tzinfo=kst),  # 모코콩: 10분 전
    # datetime.time(hour=19, minute=25, tzinfo=kst),  # 모코콩: 5분 전
    # datetime.time(hour=19, minute=45, tzinfo=kst),  # 에라스모: 15분 전
    # datetime.time(hour=19, minute=55, tzinfo=kst),  # 에라스모: 5분 전
    
    datetime.time(hour=20, minute=30, tzinfo=kst),  # 모험섬 21시: 30분 전
    datetime.time(hour=20, minute=55, tzinfo=kst),  # 모험섬 21시: 5분 전
    datetime.time(hour=22, minute=30, tzinfo=kst),  # 모험섬 23시: 30분 전
    datetime.time(hour=22, minute=55, tzinfo=kst),  # 모험섬 23시: 5분 전
]

time_advIsland_t = [
    "19:00",
    "21:00",
    "23:00",
]
time_advIsland = [
    "18:41",
    "18:30", # 19시: 30분 전
    "18:55", # 19시: 5분 전
    
    "20:30", # 21시: 30분 전
    "20:55", # 21시: 5분 전
    
    "22:30", # 23시: 30분 전
    "22:55", # 23시: 5분 전
]

"""모코콩, 에라스모 시간
time_mokokong_t = "19:30"
time_mokokong = [
    "19:20",  # 모코콩: 10분 전
    "19:25",  # 모코콩: 5분 전
]

time_more_t = "20:00"
time_more = [
    "19:45",  # 에라스모: 15분 전
    "19:55",  # 에라스모: 5분 전
]
"""


def send_log(cmd="null", user="System", guild="DM", channel="DM") -> None:
    log_f = open(log_file_path, "a", encoding="UTF-8", newline="")
    time = datetime.datetime.now()
    # time = (time + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")  # for US Timezone
    wr = csv.writer(log_f)
    wr.writerow([user, time, cmd, guild, channel])
    log_f.close()


def getTime() -> str:
    return str(datetime.datetime.now())[11:16]


def getTimeDetail() -> str:
    return datetime.datetime.now()


def ToggleAlert() -> bool:
    global userAlert
    userAlert = not userAlert
    return userAlert


def AlertStateKR() -> str:
    # global userAlert
    on = '켜짐 ON'
    off = '꺼짐 OFF'
    # return '켜짐 ON' if userAlert else '꺼짐 OFF'
    return on if userAlert else off


def getContent() -> str:
    title = ""
    desc = ""
    time_now = getTime()
    # time_now = "18:30"
    
    if time_now in time_advIsland:
        title = "모험섬"
        desc = "섬마 득템 기원!\n유물 나침반 가쥬아~!~!"
    # elif time_now in time_mokokong:
    #     title = "모코콩 아일랜드"
    #     desc = "~~모코콩 기여워 헿~~"
    # elif time_now in time_more:
    #     title = "에라스모"
    #     desc = "꿀팁: 미리가서 고렙 애들이랑 파티 먹고 있으면 기여도 냠냠하기 편함\n빨리 끝나는 **1채**로 가는걸 추천\n\n섬마 득템 기원!!!!!"
    else:
        title = "getContent() ERROR"
        desc = "get컨텐츠 오류"
        print("Select Content ERROR >> from getContent()")
    
    
    # 시간 문자열을 datetime 객체로 변환
    
    ## 현재 시간을 datetime 객체로
    time_format = "%H:%M"
    time2 = datetime.datetime.strptime(time_now, time_format)
    # print(type(time2))

    time_str1 = ""
    # 모험섬인 경우, 
    if title == "모험섬":
        temp = []
        for item in time_advIsland_t:
            item = datetime.datetime.strptime(item, time_format)
            temp.append(time2 - item)
        
        temp = min(temp); # print(temp)
        
        # 구버전
        # hours, remain = divmod(temp.seconds, 3600)
        # minutes, _ = divmod(remain, 60)
        # time_remain = f"{hours}:{minutes}"
        
        # 신버전
        temp = temp.total_seconds() / 60
        time_remain = abs(int(temp))
        print(f"time_remain >> {time_remain}")
        
        return title, desc, time_remain
    
    elif title == "모코콩 아일랜드":
        time_str1 = "19:30"
    
    elif title == "에라스모":
        time_str1 = "20:00"


    time1 = datetime.datetime.strptime(time_str1, time_format)


    # 두 datetime 객체 간 차이 계산
    time_diff = time2 - time1

    # 차이를 시간과 분으로 분리
    # hours, remain = divmod(time_diff.seconds, 3600)
    # minutes, _ = divmod(remain, 60)
    minutes_difference = time_diff.total_seconds() / 60

    # time_remain = f"{remain}"
    time_remain = abs(int(minutes_difference))
    # print(f"시간 차이: {hours}시간 {minutes}분")
    
    print(title)
    print(desc)
    print(time_remain)
    return title, desc, time_remain


class ButtonFunction(discord.ui.View):
    global userAlert
    # state = "켜짐 ON" if userAlert is True else "꺼짐 OFF"

    def __init__(self):
        super().__init__(timeout=7000)

    @discord.ui.button(label="알림 ON", style=discord.ButtonStyle.success, row=1)
    async def button1(
        self, interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        global userAlert
        
        user = interaction.user
        print(user.id, user.display_name)
        
        userAlert = True
        
        await interaction.response.send_message(
            f"오늘 알림을 다시 켰어요. \n알림 상태: {AlertStateKR()}"
        )
        # print("Alert ON Action")
        print(f"User Toggled Alert: ON")

    @discord.ui.button(label="알림 OFF", style=discord.ButtonStyle.danger, row=1)
    async def button2(
        self, interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        global userAlert
        
        user = interaction.user
        print(user.id, user.display_name)
        
        ToggleAlert()
        
        await interaction.response.send_message(
            f"오늘은 알림이 울리지 않습니다. \n알림 상태: {AlertStateKR()}"
        )
        print(getTimeDetail())
        # print("Alert OFF Action")
        print("User Toggled Alert: OFF")
        send_log(cmd=f"Change State OFF", user=user.display_name, channel="DM")


class MyClient(discord.Client):
    async def on_ready(self):
        await self.wait_until_ready()
        await tree.sync()
        # Change Bot State
        await self.change_presence(
            status=discord.Status.online, activity=discord.Game("모험섬 알림 준비")
        )
        self.reloading.start()
        self.aaaaa.start()
        startmsg = f"Logged on as {self.user}! at {datetime.datetime.now()}"
        print(startmsg)
        # user = await client.fetch_user(494382047943589889)
        # await user.send("Bot Running Start!")


    @tasks.loop(hours=4)
    async def reloading(self):
        global times, today
        date_now = datetime.datetime.now()
        today = str(date_now)[:10]
        # week = datetime.datetime.weekday(date_now)
        print(today)
        
        """ 주석 모음
        #  요일별 값
        # 0: Mon
        # 1: Tue
        # 2: Wed
        # 3: Thu
        # 4: Fri
        # 5: Sat
        # 6: Sun
        # if 0 <= week <= 4 or week == 6:
        #     times = [
        #         # datetime.time(hour=10, minute=30, tzinfo=kst), # 11 시
        #         datetime.time(hour=18, minute=30),  # 19시: 30분 전
        #         datetime.time(hour=20, minute=30),  # 21시: 30분 전
        #         datetime.time(hour=22, minute=30),  # 23시: 30분 전
        #         datetime.time(hour=22, minute=34),  # 23시: 30분 전
        #     ]
        # elif week == 5:
        #     times = [
        #         # datetime.time(hour=10, minute=30, tzinfo=kst), # 11 시
        #         datetime.time(hour=8, minute=30),  # 9시: 30분 전
        #         datetime.time(hour=10, minute=30),  # 11시: 30분 전
        #         datetime.time(hour=12, minute=30),  # 13시: 30분 전
        #         datetime.time(hour=18, minute=30),  # 19시: 30분 전
        #         datetime.time(hour=20, minute=30),  # 21시: 30분 전
        #         datetime.time(hour=22, minute=30),  # 23시: 30분 전
        #     ]
        # else:
        #     times = []
        #     print("Error")
        """


    # @tasks.loop(minutes=10.0)
    @tasks.loop(time=times)
    async def aaaaa(self):
        global userAlert, today
        today = str(datetime.datetime.now())[:10]

        def getDate() -> str:
            date = str(datetime.datetime.now())[:10]
            return date

        if getDate() != today or userAlert:
            userAlert = True
            print("Alert ON")
        elif userAlert is False:
            print("Alert OFF")
        else:
            print("ERROR")
        
        
        if userAlert is False:
            return

        # uid = "494382047943589889"  # 나
        uid = "322640826356203520"  # 고기고기고기고기
        user = await client.fetch_user(uid)
        
        TITLE, DESC, TIME = getContent()

        embed = discord.Embed(
            title=f"{TITLE} {TIME}분 전!",
            description=f"<@{uid}>! 알림 드림니다아앙\n{DESC}",
            # description=f"모험섬 가야즤? <@{uid}>\n 알림 끄려면 아래의 버튼을 야무지게 누르면 됨",
            color=discord.Colour.blue(),
        )
        await user.send(embed=embed, view=ButtonFunction())
        print("Sending Complete!")


# Execute Discord Bot
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)


cmd_test = "모험섬 알림설정"


# @tree.command(name=cmd_test, description="모험섬 알림 ON/OFF")
async def self_test(interaction: discord.Interaction):
    userid = interaction.user.id
    print(userid)
    user = await client.fetch_user(userid)

    embed = discord.Embed(
        title="Button Test", description="원하시는 버튼을 클릭해주세요", color=discord.Colour.blue()
    )

    await interaction.user.send(embed=embed, view=ButtonFunction())

    await interaction.response.send_message(embed=embed, view=ButtonFunction())


# Run Bot
client.run(TOKEN)
