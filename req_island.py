import requests
import json
from datetime import datetime, timedelta
# from MainList import pict_dir
from TOKEN import TOKEN_API
from Variables import Base_URL
from Variables import send_log_request
send_log = send_log_request
from Variables import TESTEST


response = None
res_arr:list = []
FILENAME:str = "RequestCalendar.json"
log_file_path:str = "LogFile_Request.txt"
LOG_TYPE:str = "request Island"  # for logfile

to_send_items:list = []
to_send_DESC:str = ""


# Request to Bring Data
def request_url():
    try:
        global response
        URL = f"{Base_URL}/gamecontents/calendar"
        headers = {
            "accept": "application/json",
            "authorization": f"bearer {TOKEN_API}",
        }
        response = requests.get(URL, headers=headers)
        # check response code
        RESPONSE_CODE = res_code_check(response.status_code)
        if RESPONSE_CODE == "200 OK":
            save_file(response)
            # send_log(LOG_TYPE, RESPONSE_CODE)
            return True
        else: 
            send_log(LOG_TYPE, RESPONSE_CODE)
    except Exception as e:
        print(e)
        send_log(LOG_TYPE, f"Request Error >> {e}")


def save_file(response):
    try:
        with open(FILENAME, "w", encoding="UTF-8") as file:
            json.dump(response.json(), file, ensure_ascii=False)
        file.close()
    except Exception as e:
        send_log(LOG_TYPE, f"Save File Error >> {e}")


def open_file():
    global res_arr
    try:
        file = open(FILENAME, "r", encoding="UTF-8")
        res_arr = json.load(file)
        file.close()
        return res_arr
    except Exception as e:
        print(f"ERROR >> {e}")
        return None


# response code check
def res_code_check(CODE=""):
    if CODE == 200: return f"{CODE} OK"
    elif CODE == 401: return f"{CODE} Unauthorized"
    elif CODE == 403: return f"{CODE} Forbidden"
    elif CODE == 404: return f"{CODE} Not Found"
    elif CODE == 415: return f"{CODE} Unsupported Media Type"
    elif CODE == 429: return f"{CODE} Rate Limit Exceeded"
    elif CODE == 500: return f"{CODE} Internal Server Error"
    elif CODE == 502: return f"{CODE} Bad Gateway"
    elif CODE == 503: return f"{CODE} Service Unavailable"
    elif CODE == 504: return f"{CODE} Gateway Timeout"
    else: return f"Unknown ERR >> {CODE}"


def TESTEST(varname):
    with open(f"TESTEST.json", "w", encoding="UTF-8") as file:
        json.dump(varname, file, ensure_ascii=False)
    file.close()


# check new data from server
def check_new_cal_content(INDEX=0):
    global to_send_DESC
    to_send_DESC = ""

    req = request_url()  # request new content
    if req != True:
        to_send_DESC = None
        send_log(LOG_TYPE, "request Exception")
        return
    req = open_file()

    # "CategoryName"이 "모험섬" 인 항목 필터링
    filtered_items = [item for item in req if item["CategoryName"] == "모험 섬"]
    with open("RequestCalendar_island.json", "w", encoding="UTF-8") as file:
        json.dump(filtered_items, file, ensure_ascii=False)
    file.close()

    # 모든 컨텐츠 목록 출력
    list_all_contents = [item["ContentsName"] for item in req]
    # print(island_list)

    # Calculate date today
    time_str = datetime.now()
    target_date = datetime.strptime(str(time_str), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
    
    # Load from files
    # data_list = []
    file = open("RequestCalendar_island.json", "r", encoding="UTF-8")
    data_list = json.load(file)
    file.close()

    list_all = [
        "잔혹한 장난감 성",
        "스노우팡 아일랜드",
        "몬테섬",
        "고요한 안식의 섬",
        "포르페",
        "블루홀 섬",
        "우거진 갈대의 섬",
        "죽음의 협곡",
        "쿵덕쿵 아일랜드",
        "환영 나비 섬",
        "하모니 섬",
        "수라도",
        "볼라르 섬",
        "기회의 섬",
        "메데이아",
        "라일라이 아일랜드",
    ]
    list_pvp = ["우거진 갈대의 섬", "수라도", "메데이아"]
    list_notIslandHeart = ["라일라이 아일랜드"]
    list_notAdventurePaper = ["죽음의 협곡"]
    list_reward_all = [
        "갈대 숲의 보물 상자",
        "강태공의 주머니",
        "고요한 안식의 섬의 마음",
        "골드",
        "기회의 섬의 마음",
        "달콤살벌 마리오네트 변장도구",
        "대양의 주화 상자",
        "라일라이 아일랜드 섬의 마음",
        "라일라이 아일랜드 축제 기념 상자",
        "메데이아 섬의 마음",
        "메데이아의 선물",
        "모험물 : 의문의 상자",
        "모험물 : 죽은자의 눈",
        "모험물 : 환영 나비",
        "몬테 섬의 마음",
        "몬테섬 참가상",
        "미로 정원 두근두근 상자",
        "변신 : 레몬색 아기 피냐타",
        "변신 : 설탕색 아기 피냐타",
        "변신 : 황금색 아기 피냐타",
        "볼라르 섬의 마음",
        "볼라르의 비밀 상자",
        "블루홀 섬의 마음",
        "비밀지도",
        "선혈의 조각",
        "설치물 : 늠름한 신수상",
        "설치물 : 우아한 신수상",
        "설치물 : 위엄있는 신수상",
        "수라도 섬의 마음",
        "수신 아포라스 카드",
        "수호",
        "스노우팡 아일랜드 섬의 마음",
        "실링",
        "아드린느 카드",
        "영혼의 잎사귀",
        "우거진 갈대의 섬의 마음",
        "인연의 돌",
        "잔혹한 장난감 성 섬의 마음",
        "전설 ~ 고급 카드 팩 III",
        "정령의 선물",
        "조사용 토끼발 망치",
        "조화로운 소리의 상자",
        "죽음의 협곡 섬의 마음",
        "즐거운 눈싸움 기념 주머니",
        "천상의 하모니",
        "쿵덕쿵 아일랜드 섬의 마음",
        "크림스네일의 동전",
        "탈 것 : 길들인 붉은 야생 늑대",
        "탈 것 : 붉은 갈기 늑대",
        "투명한 소리의 상자",
        "포르페 섬의 마음",
        "풍요",
        "하모니 섬의 마음",
        "해적 주화",
        "향기로운 소리의 상자",
        "환영 나비 섬의 마음",
        "황혼의 레퀴엠",
    ]
    list_reward = [
        "골드",
        "대양의 주화 상자",
        "라일라이 아일랜드 축제 기념 상자",
        "모험물 : 죽은자의 눈",
        "실링",
        "전설 ~ 고급 카드 팩 III",
        "조사용 토끼발 망치",
        # "달콤살벌 마리오네트 변장도구",
    ]

    # Extract today island list
    list_island_today = []
    for i in range(len(data_list)):
        t = data_list[i]["StartTimes"]
        if t == None: continue
        for j in range(len(t)):
            x = data_list[i]["StartTimes"][j]
            x = datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
            if x == target_date:
                list_island_today.append(data_list[i]["ContentsName"])
    list_island_today = set(list_island_today)
    list_island_today = list(list_island_today)
    list_island_today.sort()
    
    # Extract dates
    to_send_items = []
    to_send_dates = []
    test = []
    # todo_delay: 주말에 보상 중복되면 안나타나는 버그 해결할 것
    for island in data_list:
        if island["ContentsName"] not in list_island_today:
            continue
        test.append(island)
        for reward in island["RewardItems"]:
            if reward["Name"] not in list_reward or reward["StartTimes"] == None:
                continue
            # if reward["StartTimes"] == None: continue
            t = reward["StartTimes"]
            for i in t:
                x = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                if x != target_date:
                    continue
                item = {
                    # island['ContentsName']: reward['Name'] # previous
                    "name": island["ContentsName"],
                    "reward": reward["Name"],
                    "time": [],
                }
                if item in to_send_items:
                    continue
                else:
                    to_send_items.append(item)
                # print(f"{island['ContentsName']}: {reward['Name']}")
            for st_times in t:
                date_add = datetime.strptime(st_times, "%Y-%m-%dT%H:%M:%S").strftime(
                    "%H:%M"
                )
                date_verify = datetime.strptime(st_times, "%Y-%m-%dT%H:%M:%S").strftime(
                    "%Y-%m-%d"
                )
                # if date_verify == target_date:
                #     # print(date_verify)
                #     temp_list.append(TOADD)
                for content in to_send_items:
                    if (
                        content["name"] == island["ContentsName"]
                        and date_verify == target_date
                    ):
                        # 찾은 항목에 새로운 시간 추가
                        content["time"].append(date_add)
            # to_send_items[island["ContentsName"]]["time"].extend(temp_list)

            for i in t:
                x = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
                appear_date = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").strftime(
                    "%H:%M"
                )
                if x == target_date:
                    to_send_dates.append(appear_date)
    to_send_dates = set(to_send_dates)
    to_send_dates = list(to_send_dates)
    to_send_dates.sort()

    # Output Text
    target_weekday = time_str.weekday()
    # print(type(target_weekday), target_weekday)
    to_send_DESC = ""
    if 5 <= target_weekday <= 6:
        # print("주말")
        AM = ["09:00", "11:00", "13:00"]
        PM = ["19:00", "21:00", "23:00"]
        temp_am = []
        temp_pm = []
        for item in to_send_items:
            if item["time"] == AM:
                temp_desc = ""
                # temp_desc += f'# 오전  '
                temp_desc += f'\n### {item["name"]}'
                temp_desc += f'\n- 보상: {item["reward"]}'
                # temp_desc += f'\n- 등장시간: {item["time"]}'
                # temp_desc += f'\n'
                temp_am.append(temp_desc)
            elif item["time"] == PM:
                temp_desc = ""
                # temp_desc += f'# 오후  '
                temp_desc += f'\n### {item["name"]}'
                temp_desc += f'\n- 보상: {item["reward"]}'
                # temp_desc += f'\n- 등장시간: {item["time"]}'
                # temp_desc += f'\n'
                temp_pm.append(temp_desc)
        to_send_DESC += f"# 오전\n"
        for item in temp_am:
            to_send_DESC += f"{item}\n"
        to_send_DESC += f"\n# 오후\n"
        for item in temp_pm:
            to_send_DESC += f"{item}\n"
    else:
        # to_send_DESC += f"\n### 오늘의 모험섬"
        # print("평일")
        TESTEST(to_send_items)
        for item in to_send_items:
            to_send_DESC += f"### {item['name']}"
            to_send_DESC += f"\n- 보상: {item['reward']}"
            to_send_DESC += f"\n"
            # for key, value in item.items():
                # to_send_DESC += f"### {key}"
                # to_send_DESC += f"\n- 보상: {value}"
                # to_send_DESC += f"\n"
        to_send_DESC += f"\n### 등장 시간  \n"
        for item in to_send_dates:
            to_send_DESC += f"{item}  "

    # 모든 모험섬 보상 꺼내기
    # itemMainList = []
    # temperList = []
    # for i in range(len(data_list)):
    #     x = data_list[i]["RewardItems"]
    #     if (t == None): continue
    #     for j in range(len(t)):
    #         # x = data_list[i]["RewardItems"]
    #         # print(x)
    #         for k in range(len(x)):
    #             y = x[k]["Name"]
    #             # print(y)
    #             temperList.append(y)
    #         # x = datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
    #         # print(type(x))
    #         # print(type(target_date), "Target Date")
    #         # if x == target_date:
    #         #     # print(data_list[i]["ContentsName"])
    #         #     temperList.append(data_list[i]["ContentsName"])
    #     # t = datetime.strptime(data_list[i]["StartTimes"], "%Y-%m-%dT%H:%M:%S")
    #     # t = t.strftime("%Y-%m-%d")
    # temperList = set(temperList)
    # temperList = list(temperList)
    # temperList.sort()
    # with open(f'TESTEST.json', 'w', encoding="UTF-8") as file:
    #     json.dump(temperList, file, ensure_ascii = False)
    # file.close()

    # 이름이 "모험 섬" 인 목록들 출력
    # filtered_contents_names = [item["ContentsName"] for item in req if item["CategoryName"] == "모험 섬"]
    # print(filtered_contents_names)

    # # 날짜 문자열 변환
    # prev_date_str = "2023-11-11T19:00:00"
    # input_datetime = datetime.strptime(prev_date_str, "%Y-%m-%dT%H:%M:%S") # 날짜 객체로 변환
    # formatted_date_str = input_datetime.strftime("%Y-%m-%d %H:%M") # 날짜 포멧 변경
    # print(formatted_date_str)

    send_log(LOG_TYPE, "오늘의 모험섬 컨텐츠 가져오기")
    # print("Successfully Runned!")
    return


def RunRequest():
    open_file()
    check_new_cal_content()


# RunRequest()
