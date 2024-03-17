import requests
import json
from datetime import datetime, timedelta

# import csv
# from MainList import pict_dir
from TOKEN import TOKEN_API
from Variables import Base_URL
from Variables import send_log_request
send_log = send_log_request


response = None
res_arr = []
FILENAME = "RequestResult.json"
LOG_TYPE = "request Notice"  # for logfile

to_send_items = []
to_send_DESC = None
# res_title: str = None
# res_date: str = None
# res_link: str = None
# res_type: str = None
# res_TYPES = {"공지", "점검", "상점", "이벤트"}
# res_THING = ("Title", "Date", "Link", "Type")


# Request to bring Data
def request_url():
    try:
        global response
        URL = f"{Base_URL}/news/notices"
        headers = {
            "accept": "application/json",
            "authorization": f"bearer {TOKEN_API}",
        }
        response = requests.get(URL, headers=headers)
        # check response code
        RESPONSE_CODE = res_code_check(response.status_code)
        # send_log(type="Response Code Check", istrue=RESPONSE_CODE)
        if RESPONSE_CODE == "200 OK":
            save_file(response)
            return True
        else:
            send_log(type=f"Request Response Exception >> {RESPONSE_CODE}", istrue="False")
            return RESPONSE_CODE
    except Exception as e:
        # print(e)
        send_log(LOG_TYPE, f"Request Error", e)
        return False


# save files
def save_file(response):
    try:
        with open(f"{FILENAME}", "w", encoding="UTF-8") as file:
            json.dump(response.json(), file, ensure_ascii=False)
        file.close()
    except Exception as e:
        send_log(type="Save File", istrue="Exception", var1=e)


# open file
def open_file():
    global res_arr
    try:
        file = open(FILENAME, "r", encoding="UTF-8")
        res_arr = json.load(file)
        file.close()
        return res_arr
    except Exception as e:
        print(f"ERROR >> {e}")
        send_log(type="Open File", istrue="Exception", var1=e)


# response code check
def res_code_check(CODE="null"):
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
    else: return f"Code ERR >> {CODE}"
    # return f"ERR"


## get latest data from json file
# def get_all_res_data(INDEX=0):
#     global res_title, res_date, res_link, res_type
#     res_title = res_arr[INDEX]["Title"]
#     res_date = datetime.fromisoformat(res_arr[INDEX]["Date"]).strftime("%Y-%m-%d %H:%M")
#     res_link = res_arr[INDEX]["Link"]
#     res_type = res_arr[INDEX]["Type"]


# check new data from server
def check_new_article(INDEX=0):
    LOG_TYPE = "check_new_article"
    global to_send_DESC
    to_send_DESC = ""
    to_send_items = []
    
    pre_one = open_file()  # save previous content
    req = request_url()  # save new content

    if req != True:  # 요쳥 결과 정상이 아닐 때
        to_send_DESC = None
        send_log(type=LOG_TYPE, istrue=req, var1="Request result is not True")
        return

    new_one = open_file()
    
    # 새로운 공지가 없다면 (새로 불러온 결과가 이전과 같다면)
    if new_one == pre_one:
        # print(f"Not Changed")
        to_send_DESC = None
        # send_log(type=LOG_TYPE, istrue="There's No New Notice")
        return

    # new_one에는 있지만 pre_one에는 없는 데이터 찾기
    missing_in_pre_one = [item for item in new_one if item not in pre_one]
    for item in missing_in_pre_one:
        to_send_items.append(item)

    if to_send_items == []:
        to_send_DESC = None
        # print(f'Empty List >> {to_send_items}')
        return
    
    for item in to_send_items:
        to_send_DESC += f"\n### [{item['Title']}]({item['Link']})"
        time = datetime.strptime(item['Date'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M")
        to_send_DESC += f"\n- Posted at {time}"

    # print(to_send_DESC)
    send_log(
        type=LOG_TYPE, 
        istrue="New Notice", 
        var1=to_send_items, 
        var2=to_send_DESC.replace("\n", "  "))
    # print("New Notice Sent!")
    return


def RunRequest():
    # open_file()
    check_new_article()
    # print(f'>{to_send_DESC}<')


# RunRequest()
