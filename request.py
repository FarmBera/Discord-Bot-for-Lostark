import requests
import json
from datetime import datetime, timedelta

# import csv
# from MainList import pict_dir
from TOKEN import TOKEN_API
from Variables import Base_URL
from Variables import send_log_request; 
send_log = send_log_request; 

class RequestObj:
    response = None
    res_arr:list = []
    FILENAME:str = None
    LOG_TYPE:str = None
    
    ReqURL:str = None
    to_send_items:list = []
    to_send_DESC:str = None
    
    
    def __init__(self, 
        ReqURL, FILENAME, LOG_TYPE
    ):
        self.ReqURL = ReqURL
        self.FILENAME = FILENAME
        self.LOG_TYPE = LOG_TYPE
    
    
    # Request to bring Data
    def RequestURL(self):
        # print("request_url")
        try:
            # global response, ReqURL, LOG_TYPE
            URL = f"{Base_URL}{self.ReqURL}"
            headers = {
                "accept": "application/json",
                "authorization": f"bearer {TOKEN_API}",
            }
            response = requests.get(URL, headers=headers)
            # check response code
            RESPONSE_CODE = self.ResCodeCheck(response.status_code)
            send_log(type="Response Code Check", istrue=RESPONSE_CODE)
            if RESPONSE_CODE == "200 OK":
                self.FileSave(response)
                return True
            else:
                return RESPONSE_CODE
        except Exception as e:
            # print(e)
            send_log(self.LOG_TYPE, f"Request Error", e)
    
    
    # global FILENAME
    # save files
    def FileSave(self, response):
        try:
            with open(f"{self.FILENAME}", "w", encoding="UTF-8") as file:
                json.dump(response.json(), file, ensure_ascii=False)
            file.close()
        except Exception as e:
            send_log("Save File", "Exception", e)


    # open file
    def FileOpen(self):
        global res_arr
        try:
            file = open(self.FILENAME, "r", encoding="UTF-8")
            res_arr = json.load(file)
            file.close()
        except Exception as e:
            print(f"ERROR >> {e}")
            send_log("Open File", "Exception", e)


    # response code check
    def ResCodeCheck(CODE="null"):
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


    # get latest data from json file
    def ResGetData(INDEX=0):
        global res_title, res_date, res_link, res_type
        res_title = res_arr[INDEX]["Title"]
        res_date = datetime.fromisoformat(res_arr[INDEX]["Date"]).strftime("%Y-%m-%d %H:%M")
        res_link = res_arr[INDEX]["Link"]
        res_type = res_arr[INDEX]["Type"]


    # Custom Define Area
    def ResponseAction(self, INDEX=0):
        to_send_DESC = ""
        to_send_items = []

        # print("Successfully Runned!")
        return


    def RunRequest(self):
        self.FileOpen()
        self.ResponseAction()


# RunRequest()
