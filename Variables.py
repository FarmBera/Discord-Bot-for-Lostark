from datetime import datetime, timedelta
import csv
import json

# bot name
BOT_NAME: str = "로아스티커 봇"

# API request base url
Base_URL: str = "https://developer-lostark.game.onstove.com"

# game activity name
BOT_GAME: str = "/로아콘도움"


SPREADSHEET_URL: str = "https://docs.google.com/spreadsheets/d/..."


# bot notice
BOT_NOTICE: str = f"""
- 현재 공개 베타 테스트 버전입니다. (v1.0.0-rc2)
* \*요청량이 많다면 일부 기능이 불안정 할 수 있습니다.  

> **버그 제보**는 id "farmbera" DM
> 건의사항, 개선점, 피드백 환영합니다 !!!

# 공지사항
- **로아 공지 알림은 테스트 기능입니다. 빈 텍스트가 전송되는 등 버그가 있을 수 있습니다. **
"""


# bot patch note
BOT_PATCHNOTE_TITLE: str = "Patch Note v1.0.0-rc2"
BOT_PATCHNOTE: str = f"""
## 기존 기능 개선 및 버그 수정

- 이모티콘 전송 시, 닉네임 뒤 보기 안좋은 조사 **"(이)가"** 를 제거, 닉네임에 맞는 조사를 붙여줄 수 있도록 수정하였습니다.
- 로스트아크에 새로운 공지가 올라오면 알려주는 기능의 버그 수정이 완료되었습니다.
    - 공지 알림 기능을 원하신다면, 봇 관리자에게 문의 바랍니다.

## 새로운 기능이 추가되었습니다!

- 이제 '/' 명령어를 이용하여 이모티콘을 전송할 수 있습니다!
    - 사용 명령어: **/로아콘**
    - 이모티콘 이름은 채팅창에 보내는 명령어와 동일합니다. ('[' 기호만 제외)
- 개인정보 처리 방침 내용과 관련 명령어를 추가하였습니다.
    - 아직은 베타 버전으로, 핵심 내용만 적었습니다.
    - 보다 자세한 내용은 추후 가이드라인을 참고하여 작성할 예정입니다.
- 오늘 등장하는 캘린더 컨텐츠를 조회할 수 있는 기능을 추가하였습니다.
    - **/캘린더** 명령어 이용하여 사용 가능합니다.
"""


PrivacyPolicy = f"""
### LoaStickers 봇
# 개인정보 처리 방침
본 디스코드 봇 사용 시, 아래의 정보가 수집될 수 있습니다.
- 사용자의 디스코드 ID 또는 닉네임
- 명령어 (이모티콘 명령어, '/' 명령어 등)
- 명령어가 전송된 서버 이름과 채팅 채널 이름

## 수집의 이유
- 오류 발생 시 대응

## 정보의 저장 및 파기
- 위 정보는 생성일로부터 최대 1년 동안 보관될 수 있습니다.
- 수집된 정보는 암호화되어 안전하게 저장됩니다. 

> 추후 개인정보 처리 방침 가이드라인에 따라 다시 작성 예정
"""


# 로아콘 공지 전송을 위한
ch_list: list = [
    # 여기에 채팅방 ID 삽입
    # ...
]
ch_list_test: list = [
    # 개발용 채팅 채널
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
