from datetime import datetime, timedelta
import csv
import json

BOT_NAME: str = "로아스티커 봇"

Base_URL: str = "https://developer-lostark.game.onstove.com"

BOT_NOTICE: str = f"""
# 공지사항

### 현재 로아 공지 알림에 지속적인 오류 발생으로, 해당 기능은 임시 비활성화 하였습니다. 

- 현재 공개 알파 테스트 버전입니다. (Ver 0.3)
* 요청량이 많다면 일부 기능이 불안정 할 수 있습니다.  

> **버그 제보**는 id "farmbera" DM
> 건의사항, 개선점, 피드백 환영합니다 !!!
"""
# - **로아 공지 알림은 테스트 기능입니다. 빈 텍스트가 전송되는 등 버그가 있을 수 있습니다. **
# ### **현재 로아 공지 알림에 치명적인 버그가 발생되어 해당 기능은 임시 비활성화 되었습니다**


# 로아콘 공지 전송을 위한
ch_list: list = [
    1172504236777553950,  # fb's Game Server / lostark-news
    # 1051752247496806430,  # 길드디코(였던것) / 잡담방
    # 891208473189175387,  # 달콤한집 / 자유채팅
]
ch_list_test: list = [
    1168826400111857675, # bot-test
    1172397317047984168, # bot-test-ch1
]


# Save Log Files
log_file_path: str = "logfile_request.csv"


def send_log_request(type, istrue=f"Null", var1=f"Null", var2=f"Null", var3=f"Null"):
    # log_f = open(log_file_path, "a", encoding="UTF-8")
    # TIME = (datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
    # msg = f"\n///Type: {type}>>{istrue}//at {TIME}//desc: {var1}"
    # log_f.write(msg)
    # log_f.close()
    log_f = open(log_file_path, "a", encoding="utf-8", newline="")  # 읽기모드로 파일을 연다
    TIME = (datetime.now() + timedelta(hours=9)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # on US Server
    # TIME = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") # on KR Server
    wr = csv.writer(log_f)
    wr.writerow([type, istrue, TIME, var1, var2, var3])
    log_f.close()


def TESTEST(variable):
    with open(f"TESTEST.json", "w", encoding="UTF-8") as file:
        json.dump(variable, file, ensure_ascii=False)
    file.close()