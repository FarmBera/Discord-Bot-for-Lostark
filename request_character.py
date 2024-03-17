import requests
import json
import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# import csv
# from MainList import pict_dir
from TOKEN import TOKEN_API as TOKEN
from Variables import Base_URL
from Variables import send_log_request
from Variables import TESTEST

send_log = send_log_request
log_file_char_csv: str = "logfile_character.csv"

response = None
response_e = None
# res_arr: list = []
FILENAME: str = "RequestResult_character.json"
FILENAME2: str = "RequestResult_char_exp.json"
LOG_TYPE: str = "request Character"  # for logfile

to_send_items:list = []
to_send_DESC:str = ""  # Type: String

PROFILE: dict = {}


# Request to bring Data
def request_url(characterName: str):
    try:
        if characterName == None or "":
            return "No Character Name Input!"
        global response
        # start request
        URL = f"{Base_URL}/armories/characters/{characterName}"
        headers = {
            "accept": "application/json",
            "authorization": f"bearer {TOKEN}",
        }
        response = requests.get(URL, headers=headers)
        # check response code
        RESPONSE_CODE = res_code_check(response.status_code)
        send_log(type="check res code: character", istrue=RESPONSE_CODE)
        if RESPONSE_CODE == "200 OK":
            save_file(response)
            return True
        else:
            return RESPONSE_CODE
    except Exception as e:
        # print(e)
        send_log(LOG_TYPE, f"Request Error", e)


# Requets to bring Expedition Data
def request_url_expedition(characterName: str):
    try:
        if characterName == None or "":
            return "No Character Name Input!"
        global response_e
        # start request
        URL = f"{Base_URL}/characters/{characterName}/siblings"
        headers = {
            "accept": "application/json",
            "authorization": f"bearer {TOKEN}",
        }
        response_e = requests.get(URL, headers=headers)
        # check response_e code
        RESPONSE_CODE = res_code_check(response_e.status_code)
        send_log(type="check res code: character", istrue=RESPONSE_CODE)
        if RESPONSE_CODE == "200 OK":
            save_file(response=response_e, fname=FILENAME2)
            return True
        else:
            return RESPONSE_CODE
    except Exception as e:
        # print(e)
        send_log(LOG_TYPE, f"Request Error", e)


# save files
def save_file(response, fname=FILENAME):
    try:
        with open(f"{fname}", "w", encoding="UTF-8") as file:
            json.dump(response.json(), file, ensure_ascii=False)
        file.close()
    except Exception as e:
        send_log("Save File", "Exception", e)


# open file
def open_file(fname=FILENAME):
    try:
        file = open(fname, "r", encoding="UTF-8")
        res_arr = json.load(file)
        file.close()
        return res_arr
    except Exception as e:
        print(f"ERROR >> {e}")
        send_log("Open File", "Exception", e)


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


# Reset Objects
def reset_object():
    global PROFILE
    PROFILE = {
        "ArmoryProfile": {
            "CharacterImage": None,  # 캐릭터 이미지
            "ExpeditionLevel": None,  # 원정대 레벨
            "PvpGradeName": None,  # 현재 PVP 등급
            "TownLevel": None,  # 영지 레벨
            "TownName": None,  # 영지 이름
            "Title": None,  # 칭호
            "GuildMemberGrade": None,  # 길드 멤버 등급
            "GuildName": None,  # 소속 길드 이름
            "UsingSkillPoint": None,  # 사용중인 스킬 포인터
            "TotalSkillPoint": None,  # 전체 스킬 포인터
            "ServerName": None,  # 서버
            "CharacterName": None,  # 캐릭터 닉네임
            "CharacterLevel": None,  # 전투 레벨
            "CharacterClassName": None,  # 캐릭터 클래스
            "ItemAvgLevel": None,  # 아이템레벨 평균
            "ItemMaxLevel": None,  # 최대 달성 레벨????
        },
        "Stats": {
            "치명": 0,
            "특화": 0,
            "제압": 0,
            "신속": 0,
            "인내": 0,
            "숙련": 0,
            "최대 생명력": 0,
            "공격력": 0,
        },
        # "Stats+10%": {
        #     "치명": 0,
        #     "특화": 0,
        #     "제압": 0,
        #     "신속": 0,
        #     "인내": 0,
        #     "숙련": 0,
        #     "최대 생명력": 0,
        #     "공격력": 0
        # },
        "Tendencies": {
            "지성": 0,
            "담력": 0,
            "매력": 0,
            "친절": 0,
        },
        "ArmoryEquipment": {
            "무기": "0강",
            "투구": "0강",
            "상의": "0강",
            "하의": "0강",
            "장갑": "0강",
            "어깨": "0강",
            "어빌리티 스톤": "No Info",  # AbilityStone Object 들어감
        },
        "ArmoryAvatars": [],
        "Engravings": [],
        "EngravingsLev": "",
        "Cards": {
            "CardSet": "No Cards",  # 카드 세트
            "TotalLevel": "",  # 총 각성 레벨
            "Cards": {},  # 장착 카드 리스트
            "Effects": [],  # 장착 효과
        },
        "GemsCountNeed": 11,  # 필요 보석 개수
        "Gems": {
            "GemsList": [],
            "GemsLevel": [],
            "GemsCount": 0,  # 장착 보석 개수
            "GemsEffect": [],
        },
        "Collectibles": {},
        "ExpeditionCharacters": {},
    }


# Check & Extract items
def calculate_character(nickname: str):
    global to_send_DESC
    # to_send_DESC = ""

    LOG_TYPE = "get_character_info"

    # TODO: !!!!! Uncomment Before Commit
    # req = request_url(nickname)  # request character info
    # if req != True: # 요쳥 결과 정상이 아닐 때
    #     to_send_DESC = ""
    #     send_log(LOG_TYPE, req)
    #     return

    req = open_file()


    # Default Profiles
    ARMPF = "ArmoryProfile"
    PROFILE["ArmoryProfile"]["CharacterImage"] = str(req[ARMPF]["CharacterImage"])
    PROFILE["ArmoryProfile"]["ExpeditionLevel"] = req[ARMPF]["ExpeditionLevel"]
    PROFILE["ArmoryProfile"]["PvpGradeName"] = req[ARMPF]["PvpGradeName"]
    PROFILE["ArmoryProfile"]["TownLevel"] = req[ARMPF]["TownLevel"]
    PROFILE["ArmoryProfile"]["TownName"] = req[ARMPF]["TownName"]
    PROFILE["ArmoryProfile"]["Title"] = req[ARMPF]["Title"]
    PROFILE["ArmoryProfile"]["GuildMemberGrade"] = req[ARMPF]["GuildMemberGrade"]
    PROFILE["ArmoryProfile"]["GuildName"] = req[ARMPF]["GuildName"]
    PROFILE["ArmoryProfile"]["UsingSkillPoint"] = req[ARMPF]["UsingSkillPoint"]
    PROFILE["ArmoryProfile"]["TotalSkillPoint"] = req[ARMPF]["TotalSkillPoint"]
    PROFILE["ArmoryProfile"]["ServerName"] = req[ARMPF]["ServerName"]
    PROFILE["ArmoryProfile"]["CharacterName"] = req[ARMPF]["CharacterName"]
    PROFILE["ArmoryProfile"]["CharacterLevel"] = req[ARMPF]["CharacterLevel"]
    PROFILE["ArmoryProfile"]["CharacterClassName"] = req[ARMPF]["CharacterClassName"]
    PROFILE["ArmoryProfile"]["ItemAvgLevel"] = req[ARMPF]["ItemAvgLevel"]
    PROFILE["ArmoryProfile"]["ItemMaxLevel"] = req[ARMPF]["ItemMaxLevel"]
    # print(PROFILE["ArmoryProfile"])

    # Stats
    temp = req["ArmoryProfile"]["Stats"]
    for item in temp:
        PROFILE["Stats"][item["Type"]] = item["Value"]
    
    # # Stats+10%
    # temp = PROFILE["Stats"]
    # # print(temp)
    # for key, value in temp.items():
    #     print(key, value)
    #     PROFILE["Stats+10%"][key] = int(float(value) * 1.1)

    # Tendencies
    temp = req["ArmoryProfile"]["Tendencies"]
    for item in temp:
        PROFILE["Tendencies"][item["Type"]] = item["Point"]

    # Equipped Armory
    temp = req["ArmoryEquipment"]
    try:
        for i in range(6):
            t1 = (temp[i]["Name"])[0:3]
            t2 = temp[i]["Grade"]
            t = json.loads(temp[i]["Tooltip"])
            t3 = t["Element_001"]["value"]["qualityValue"]
            tres = f"{t2} {t1}강 / 품질{t3}"
            PROFILE["ArmoryEquipment"][temp[i]["Type"]] = tres
    except:
        PROFILE["ArmoryEquipment"] = "Nothing Equipped Armory"

    AbilityStone = {
        "Name": "No Info",  # 스톤 이름
        "Grade": "No Info",  # 스톤 등급
        "Tear": "No Info",  # 티어
        "Icon": "No Info",  # 사진 링크
        "Engrav1": "No Info",  # 각인 1
        "Engrav2": "No Info",  # 각인 2
        "EngravDeb": "No Info",  # 디버프 각인
        # "": "No Info",
    }
    try: 
        temp = json.loads(temp[11]["Tooltip"])
        # print(temp)
        AbilityStone["Name"] = BeautifulSoup(
            temp["Element_000"]["value"], features="lxml"
        ).get_text()
        AbilityStone["Grade"] = BeautifulSoup(
            temp["Element_001"]["value"]["leftStr0"], features="lxml"
        ).get_text()
        AbilityStone["Tear"] = BeautifulSoup(
            temp["Element_001"]["value"]["leftStr2"], features="lxml"
        ).get_text()
        AbilityStone["Icon"] = temp["Element_001"]["value"]["slotData"]["iconPath"]
    except:
        # AbilityStone = "No AbilityStone Equipped"
        pass
    
    # todo_done: Fix Error with bringing AbilityStone data
    # 어빌리티 스톤 총 세공합 14 미만인 항목 구분 처리 (JSON 형식 다름)
    # Element_006
    try: 
        AbilityStone["Engrav1"] = (
            BeautifulSoup(
                temp["Element_006"]["value"]["Element_000"]["contentStr"]["Element_000"]["contentStr"],
                features="lxml",
            )
            .get_text()
            .replace("[", "")
            .replace("]", "|")
        )
        AbilityStone["Engrav2"] = (
            BeautifulSoup(
                temp["Element_006"]["value"]["Element_000"]["contentStr"]["Element_001"]["contentStr"],
                features="lxml",
            )
            .get_text()
            .replace("[", "")
            .replace("]", " |")
        )
        AbilityStone["EngravDeb"] = (
            BeautifulSoup(
                temp["Element_006"]["value"]["Element_000"]["contentStr"]["Element_002"]["contentStr"],
                features="lxml",
            )
            .get_text()
            .replace("[", "")
            .replace("]", "|")
        )
        PROFILE["ArmoryEquipment"]["어빌리티 스톤"] = AbilityStone
    except:
        pass
    
    # Element_005
    try: 
        AbilityStone["Engrav1"] = (
            BeautifulSoup(
                temp["Element_005"]["value"]["Element_000"]["contentStr"]["Element_000"]["contentStr"],
                features="lxml",
            )
            .get_text()
            .replace("[", "")
            .replace("]", "|")
        )
        AbilityStone["Engrav2"] = (
            BeautifulSoup(
                temp["Element_005"]["value"]["Element_000"]["contentStr"]["Element_001"]["contentStr"],
                features="lxml",
            )
            .get_text()
            .replace("[", "")
            .replace("]", " |")
        )
        AbilityStone["EngravDeb"] = (
            BeautifulSoup(
                temp["Element_005"]["value"]["Element_000"]["contentStr"]["Element_002"]["contentStr"],
                features="lxml",
            )
            .get_text()
            .replace("[", "")
            .replace("]", "|")
        )
        PROFILE["ArmoryEquipment"]["어빌리티 스톤"] = AbilityStone
    except:
        pass
        # PROFILE["ArmoryEquipment"]["어빌리티 스톤"] = "Nothing Equipped"


    # Avatars
    temp = req["ArmoryAvatars"]
    # 장비를 아무것도 안입고 있을 때 대비
    try: 
        for i in range(len(temp)):
            object = {
                "Type": temp[i]["Type"],
                "Name": temp[i]["Name"],
                "Icon": temp[i]["Icon"],
                "Grade": temp[i]["Grade"],
            }
            PROFILE["ArmoryAvatars"].append(object)
    except Exception:
        PROFILE["ArmoryAvatars"] = "Nothing Equipped Avatars"
    
    # Skills
    # TODO: 스킬 출력하는 메서드 생성
    # temp = req["ArmorySkills"]
    # TESTEST(temp)
    # for i in range(len(temp)):
        # for key, value in temp[i].items():
            # print(key, value)
            # if key == "Rune" and value["Name"] != "null":
            #     print(key, value["Name"])
                # print(key["Name"])
            # object = {
            #     temp.key()
            # }
            # temp["Name"]


    # Engraving
    # global EngravingsLev
    try: 
        for item in req["ArmoryEngraving"]["Effects"]:
            if item == None or "":
                PROFILE["Engravings"].append("No Info")
                break
            PROFILE["EngravingsLev"] += (item["Name"])[-1]
            PROFILE["Engravings"].append(item["Name"])
    except:
        PROFILE["Engravings"] = "Engravings is Empty"
        PROFILE["EngravingsLev"] = 0

    # Cards
    # TODO: 여러개의 카드 효과가 장착되었을 때 대비
    try: 
        temp = req["ArmoryCard"]["Cards"]
        awaken_total = 0
        for i in range(len(temp)):
            if item == None or "":
                break
            awaken_cal = temp[i]["AwakeCount"]
            object = {
                "Icon": temp[i]["Icon"],
                "AwakeTotal": awaken_cal,
                "Grade": temp[i]["Grade"],
            }
            awaken_total += awaken_cal
            PROFILE["Cards"]["Cards"][temp[i]["Name"]] = object
        PROFILE["Cards"]["TotalLevel"] = awaken_total
        
        temp = req["ArmoryCard"]["Effects"]  # [0]["Items"]
        for i in range(len(temp)):
            temp2 = temp[i]["Items"]
            for j in range(len(temp2)):
                object = {temp[i]["Items"][j]["Name"]: temp[i]["Items"][j]["Description"]}
                PROFILE["Cards"]["Effects"].append(object)
        PROFILE["Cards"]["CardSet"] = list(PROFILE["Cards"]["Effects"][-1].keys())[0]
    except:
        PROFILE["Cards"]["TotalLevel"] = 0
        PROFILE["Cards"]["CardSet"] = "Nothing Equipped Card"


    # TODO_undefined: 카드 효과 다시
    # print(Cards)
    # Cards = {
    #     "CardSet": [],  # 카드 세트
    #     "TotalLevel": "",
    #     "Cards": {},  # 장착 카드 리스트
    #     "Effects": [],  # 장착 효과
    # }

    # # 카드 세트 효과, 각성 합
    # temp = req["ArmoryCard"]["Effects"][-1]["Items"]
    # for item in temp:
    #     print(item["Name"])
    # # print(temp)
    
    
    # Gems
    # GemsObj = {
    #     "Gems": [],
    #     "GemsList": [],
    #     "GemsLevel": [],
    #     "GemsCount": 0,  # 장착 보석 개수
    #     "GemsEffect": {},
    # }
    try: 
        temp = req["ArmoryGem"]["Gems"]
        for i in range(len(temp)):
            t = BeautifulSoup(
                temp[i]["Name"],
                features="lxml",
            ).get_text()
            PROFILE["Gems"]["GemsList"].append(t)
            
            # TODO: 숫자만 나오게 변경 (10레벨 보석 대비)
            for i in range((len(t))):
                try:
                    temp2 = int(t[i])
                    PROFILE["Gems"]["GemsLevel"].append(temp2)
                except:
                    break;
            # 기존 코드
            # PROFILE["Gems"]["GemsLevel"].append(t[0:1])
        PROFILE["Gems"]["GemsList"].sort()
        PROFILE["Gems"]["GemsLevel"].sort()
        PROFILE["Gems"]["GemsCount"] = len(PROFILE["Gems"]["GemsList"])
        # print(GemsLevel)
        # print(GemsCount)

        # 보석 효과
        temp = req["ArmoryGem"]["Effects"]
        for i in range(len(temp)):
            tn = temp[i]["Name"]
            PROFILE["Gems"]["GemsEffect"].append(
                f'{temp[i]["Name"]} > {temp[i]["Description"]}'
            )
        # print(GemsEffect)
    except:
        PROFILE["Gems"]["GemsList"] = "No Equipped Gems"
        PROFILE["Gems"]["GemsLevel"] = "No Equipped Gems"
        PROFILE["Gems"]["GemsCount"] = "No Equipped Gems"
        PROFILE["Gems"]["GemsEffect"] = "No Equipped Gems"

    # TODO: 보석 만족 조건 생성
    """
    - 보석 모두 장착 되어 있는가 (11개 모두)
    - 7레벨 이상의 보석이 담겨 있는가
        - 숫자가 7 이상인지 확인하는 함수
    - [보류] 멸화, 홍염 분배가 잘 되어 있는가 
    """
    # print(Gems)
    

    # Collelctibles 
    ## Collectibles Summary
    temp = req["Collectibles"]
    for i in range(len(temp)):
        object = {
            "Point": temp[i]["Point"],
            "MaxPoint": temp[i]["MaxPoint"],
        }
        PROFILE["Collectibles"][temp[i]["Type"]] = object
    
    
    # todo_done: 원정대 정보 저장하기
    # Expedition Characters
    req = request_url_expedition(nickname)  # request expedition character infos
    if req != True: # 요쳥 결과 정상이 아닐 때
        to_send_DESC = ""
        send_log(LOG_TYPE, req)
        return
    req = open_file(FILENAME2)

    object = []
    for item in req:
        object.append(
            {item["ItemMaxLevel"]: f'({item["ServerName"]}) {item["CharacterClassName"]} {item["CharacterLevel"]} {item["CharacterName"]}' }
        )
        # temp = f'({item["ServerName"]}) {item["CharacterName"]} {item["ItemMaxLevel"]} {item["CharacterClassName"]} {item["CharacterLevel"]}'
        # print(temp)
        # object.append(temp)
        # object.sort()
    object = sorted(object, key=lambda x: float(list(x.keys())[0].replace(',', '')), reverse=True)
    # object = sorted(object, key=lambda x: float(list(x.values())[0].split()[0].replace(',', '')))
    PROFILE["ExpeditionCharacters"] = object
    
    TESTEST(PROFILE)
    send_log(LOG_TYPE, "Read Character Info")
    # print("Successfully Runned!")
    return


def get_user_info_forraid():
    print("get_user_info_forraid")
    # global to_send_DESC
    # for key, value in PROFILE["ArmoryProfile"].items():
    #     print(f'{key}: {value}')


def get_user_info_all_text():
    print("get_user_info_all")
    global to_send_DESC
    LBK = "\n"
    to_send_DESC = f"{LBK}"
    to_send_DESC += (
        f'{LBK}>>{PROFILE["ArmoryProfile"]["CharacterName"]} CHARACTER_SEARCH_RESULT'
    )
    to_send_DESC += f'{LBK}원정대 {PROFILE["ArmoryProfile"]["ExpeditionLevel"]}'
    to_send_DESC += f'{LBK}전투레벨 {PROFILE["ArmoryProfile"]["ExpeditionLevel"]}'
    to_send_DESC += f'아이템레벨: {PROFILE["ArmoryProfile"]["ItemAvgLevel"]}'
    # for key, value in PROFILE["ArmoryProfile"].items():
    #     print(f'{key}: {value}')

    # to_send_DESC=PROFILE["ArmoryProfile"]["ExpeditionLevel"]
    print(to_send_DESC)


# 유저 정보 모두 가져와서 csv 파일로 저장
def get_user_info_all_csv():
    # print("get_user_info_all_csv")
    log_f = open(log_file_char_csv, "a", encoding="utf-8", newline="")
    # TIME = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") # 로컬 서버에서 돌릴 때
    TIME = (datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
    # with open(log_file_char_csv, "a", encoding="utf-8") as f:
    #     writer = csv.writer(f)
    #     for key, value in PROFILE.items():
    #         writer.writerow([TIME, key, value])
    # print(type(TIME))
    wr = csv.writer(log_f)
    wr.writerow([
        TIME, 
        [value for value in PROFILE["ArmoryProfile"].values()], 
        [stat for stat in PROFILE["Stats"].values()], 
        [tenden for tenden in PROFILE["Tendencies"].values()],
        [armor for armor in PROFILE["ArmoryEquipment"].values()], 
        # [stone for stone in PROFILE["ArmoryEquipment"]["어빌리티 스톤"].values()], 
        [avatar for avatar in PROFILE["ArmoryAvatars"]], 
        [engrav for engrav in PROFILE["Engravings"]], 
        PROFILE["EngravingsLev"], 
        [card for card in PROFILE["Cards"].values()],
        PROFILE["GemsCountNeed"],
        [gems for gems in PROFILE["Gems"].values()], 
        [expedition for expedition in PROFILE["ExpeditionCharacters"]],
    ])
    log_f.close()


def RunRequest(nickname: str):
    if nickname == None or "":
        print(f"nickname is Empty! >> '{nickname}'")
        send_log(type=LOG_TYPE, istrue=nickname, var1='nickname is None or ""')
        return
    # try:
    # print(f'nickname >> "{nickname}"')
    reset_object()
    calculate_character(nickname)
    # get_user_info_forraid()
    # get_user_info_all_text()
    # get_user_info_all_csv()


def RunRequestSave(nickname: str):
    if nickname == None or "":
        send_log(type=LOG_TYPE, istrue=nickname, var1='nickname is None or ""')
        return
    reset_object()
    calculate_character()
    get_user_info_all_csv()

RunRequest("FarmBeraC")