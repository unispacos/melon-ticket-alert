# Melon 티켓 자동 알림 스크립트

Python으로 멜론 콘서트 자리 발생시 자동으로 알림을 받습니다.

준비
- Python3
- Crontab

# 사용법 (MacOS 기준)
## 멜론에서 남은 좌석 정보를 제공할 경우

1. `count_remain_seat.py`에 알림을 받고자하는 콘서트 API 정보를 입력합니다. 괄호 표시된 부분만 확인해서 변경해주세요.
```python
...

def get_seats_summary() -> None:
    url = "https://ticket.melon.com/tktapi/product/block/summary.json?v=1" 
   
    # 확인 후 필요한 정보만 채워줍니다. 
    body = {
        'prodId': '',
        'pocCode': '',
        'scheduleNo': '',
        'perfDate': '',
        'seatGradeNo': '',
        'corpCodeNo': ''
    }

    # Cookie만 변경해주세요.
    header = {
        ...
        'Cookie': '',
        ...
    }

    response = requests.post(url,headers=header,data=body)
    return response.json()

...
```
2. `main.py`에 Slack Webhook URL도 추가해줍니다.
```python
...

def send_message(messages: list) -> None: 
    slack_webhook_url = ""
    
    for message in messages:
        response = requests.post(slack_webhook_url, json={'text' : message})

...
```
3. 가상환경을 생성 후 활성화합니다.
```sh
$ python3 -m venv .venv
$ . .venv/bin/activate
```

4. 라이브러리를 설치합니다.
```sh
$ pip install -r requirements.txt
```

5. Crontab을 설정합니다. (아래는 1분 기준 설정방법)
```sh
$ crontab -e
# <python path>에는 실제 Python 경로를 입력해주세요. 전체 경로를 입력해야합니다.
# <main.py path>에는 main.py의 전체 경로를 입력해주세요.
* * * * * <python path>/python3 <count_remain_seat.py path>/count_remain_seat.py
```
 
## 멜론에서 남은 좌석 정보를 제공하지 않을 경우

1. `check_map_seat.py`에 알림을 받고자하는 콘서트 API 정보를 입력합니다. 최상단에 주석으로 표시된 부분만 확인해서 변경해주세요.
```python
...

#######################################################
########### 아래 값 채워준 뒤 실행해주시면 됩니다. #############
#######################################################
prodId = ""
pocCode = ""
scheduleNo = ""
cookie = ""
slack_webhook_url = ""
#######################################################
#######################################################

...
```
3. 가상환경을 생성 후 활성화합니다.
```sh
$ python3 -m venv .venv
$ . .venv/bin/activate
```

4. 라이브러리를 설치합니다.
```sh
$ pip install -r requirements.txt
```

5. Crontab을 설정합니다. (아래는 1분 기준 설정방법)
```sh
$ crontab -e
# <python path>에는 실제 Python 경로를 입력해주세요. 전체 경로를 입력해야합니다.
# <main.py path>에는 main.py의 전체 경로를 입력해주세요.
* * * * * <python path>/python3 <check_map_seat.py path>/check_map_seat.py
```
 
