import requests
import json
from datetime import datetime, timedelta

# from MainList import pict_dir
from TOKEN import TOKEN_API
from Variables import Base_URL
from Variables import send_log_request; send_log = send_log_request;


response = None
res_arr: list = []
FILENAME = "RequestCalendar_contents.json"
log_file_path = "LogFile_Request.txt"
LOG_TYPE = "request Calendar"  # for logfile

to_send_items: list = []
to_send_DESC: str = ""


# # Save Log Files
# def send_log(type, istrue=f"Null", var1 = f"Null"):
#     log_f = open(log_file_path, "a", encoding="UTF-8")
#     TIME = (datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
#     msg = f"\n///Type: {type}>>{istrue}//at {TIME}//desc: {var1}"
#     log_f.write(msg)
#     log_f.close()


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
        send_log(type="check res code: calendar", istrue=RESPONSE_CODE)
        if RESPONSE_CODE == "200 OK":
            save_file(response)
            send_log(type=LOG_TYPE, istrue=RESPONSE_CODE)
            return True
    except Exception as e:
        print(e)
        send_log(LOG_TYPE, f"Request Error >> {e}")


def save_file(response):
    with open(FILENAME, "w", encoding="UTF-8") as file:
        json.dump(response.json(), file, ensure_ascii=False)
    file.close()


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
    else: return f"Code >> {CODE}"


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

    # # "CategoryName"이 "except_content" 안에 없는 항목 필터링
    # # ALL_CATEGORIES = ["항해", "카오스게이트", "로웬", "섬", "모험 섬", "필드보스", "태초의 섬"]
    # except_content = ["항해", "로웬", "섬", "모험 섬"]
    # filtered_items = [item for item in req if item["CategoryName"] not in except_content]
    # # filtered_items = [item["CategoryName"] for item in req]
    # # filtered_items = set(filtered_items)
    # # filtered_items = list(filtered_items)
    # with open("RequestCalendar_contents.json", "w", encoding="UTF-8") as file:
    #     json.dump(filtered_items, file, ensure_ascii = False)
    # file.close()

    # 모든 컨텐츠 목록 출력
    # list_all_contents = [item["ContentsName"] for item in req]
    # print(island_list)

    # Calculate date today
    time_str = datetime.now()
    target_date = datetime.strptime(str(time_str), "%Y-%m-%d %H:%M:%S.%f").strftime(
        "%Y-%m-%d"
    )
    # print(target_date)

    t_year = time_str.year
    t_month = time_str.month
    t_day = time_str.day
    start_date = datetime(
        year=t_year, month=t_month, day=t_day, hour=6, minute=10, second=0
    )
    # .strftime("%Y-%m-%dT%H:%M:%S")
    end_date = datetime(
        year=t_year, month=t_month, day=t_day + 1, hour=5, minute=50, second=0
    )
    # .strftime("%Y-%m-%dT%H:%M:%S")
    # print(type(start_date))
    # print(type(end_date))
    # print(start_date)
    # print(end_date)

    # start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    # end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    # print(start_date)
    # print(end_date)

    # Load from files
    file = open("RequestCalendar_contents.json", "r", encoding="UTF-8")
    data_list = json.load(file)
    file.close()

    # Extract today island list
    list_calendar_today = []
    except_content = ["항해", "섬", "모험 섬"]
    for i in range(len(data_list)):
        t = data_list[i]["StartTimes"]
        if t == None:
            continue
        for j in range(len(t)):
            x = data_list[i]["StartTimes"][j]
            x = datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")
            # print(type(x))
            # if (x == target_date):
            if start_date <= x or x <= end_date:
                z = data_list[i]["CategoryName"]
                if z in list_calendar_today:
                    continue
                list_calendar_today.append(z)
    # list_calendar_today = set(list_calendar_today)
    # list_calendar_today = list(list_calendar_today)
    list_calendar_today.sort()
    list_calendar_today = [
        item for item in list_calendar_today if item not in except_content
    ]

    # Extract dates
    # to_send_items = []
    # to_send_dates = []
    # for content in data_list:
    #     if content and content["ContentsName"] in filtered_items:
    #         for reward in content["RewardItems"]:
    #             if reward and reward["Name"] in filtered and reward["StartTimes"] != None:
    #                 t = reward["StartTimes"]
    #                 for i in t:
    #                     x = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
    #                     if x == target_date:
    #                         item = { content['ContentsName']: reward['Name'] }
    #                         if (item in to_send_items): continue
    #                         else: to_send_items.append(item)
    #                         # print(f"{content['ContentsName']}: {reward['Name']}")
    #                 for i in t:
    #                     x = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
    #                     appear_date = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
    #                     if x == target_date: to_send_dates.append(appear_date)
    # to_send_dates = set(to_send_dates)
    # to_send_dates = list(to_send_dates)
    # to_send_dates.sort()

    # Output Text
    # to_send_DESC = ""
    # # to_send_DESC += f"\n### 오늘의 모험섬"
    # for item in to_send_items:
    #     for key, value in item.items():
    #         to_send_DESC += f"### {key}"
    #         to_send_DESC += f"\n- 보상: {value}"
    #         to_send_DESC += f"\n"
    # to_send_DESC += f"\n### 등장 시간  \n"
    # for item in to_send_dates:
    #     to_send_DESC += f"{item}  "

    with open(f"TESTEST.json", "w", encoding="UTF-8") as file:
        json.dump(list_calendar_today, file, ensure_ascii=False)
    file.close()

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

    send_log(LOG_TYPE, "오늘의 캘린더 컨텐츠 가져오기")
    # print("Successfully Runned!")
    return


def RunRequest():
    open_file()
    check_new_cal_content()


# RunRequest()
