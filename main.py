import requests

def main() -> None:
    seats = get_seats_summary()
    messages = check_remaining_seats(seats['summary'])
    send_message(messages)

def get_seats_summary() -> None:
    url = "https://ticket.melon.com/tktapi/product/block/summary.json?v=1" 
   
    body = {
        'prodId': '209371',
        'pocCode': 'SC0002',
        'scheduleNo': '100002',
        'perfDate': '',
        'seatGradeNo': '',
        'corpCodeNo': ''
    }

    header = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Content-Length': '76',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_fwb=120RAdMRLtaNAcBDwlkVQHp.1709000898290; PCID=17090008984974937153609; PC_PCID=17090008984974937153609; _fwb=224JcDun9YUttLVHUEG4hU2.1709002132450; _T_ANO=nVKUYQCJkj5di2eZO8oxsnJr1eUKjuYIqnWBe5FF+VWL9v70SfaheLeu8nH0pLtD9VeDM0jk2qnrKlNoiY4y4cOabW6co6Z2dkZ/bd7ew/j8d9NdTxuWxof0xMbY+V0px6GYN+ximQ5jmH8MnenUkcdbPmUlaz9Pk7Q+kXDg8KkyotMONl0ZTs0zD+RIeSRs2rflau6lyu5Hl3eW+WX6zXI3DyTPmsvxG+Az5zmpME2Q63l8HKXsaVDUdrIWMQ9RBLoR44+ZuMNr6A2uKC0dCsmV8LQT8me8OL44WXIsiOvhviYHQPey19GLxzzblaJ9zaCYEKAR0k4Jj4XF8LrDww==; performance_layer_alert=%2C209371; TKT_POC_ID=MP15; NetFunnel_ID=WP15; MAC=QsRJhbHtBNWlff+Q4A/g2xYAPa4qFeAMvmSigmRVVfRO65jVG49VMfEIZxkrumjf; MLCP=MTIzODM4MTAlM0Jyb3poZWtla2VrJTNCJTNCMCUzQmV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnBjM01pT2lKdFpXMWlaWEl1YldWc2IyNHVZMjl0SWl3aWMzVmlJam9pYldWc2IyNHRhbmQwSWl3aWFXRjBJam94TnpBNU1qVTVNekkzTENKdFpXMWlaWEpMWlhraU9pSXhNak00TXpneE1DSXNJbUYxZEc5TWIyZHBibGxPSWpvaVRpSjkubS1XdFpZalk5ZFZnUE9iMHdaWHlzTFFIb3FjblJqNndab1FSYjNrcnI5ZyUzQiUzQjIwMjQwMzAxMTExNTI3JTNCRW1hRGFtJTNCMSUzQmxkeTkwMzclNDBuYXZlci5jb20lM0IyJTNC; MUS=-45161989; keyCookie=12383810; store_melon_cupn_check=12383810; JSESSIONID=D851047DEE23B8024D8AEFA23B327BB4; wcs_bt=s_585b06516861:1709298536',
        'Host': 'ticket.melon.com',
        'Referer': 'https://ticket.melon.com/reservation/popup/stepBlock.htm',
        'User-Agent': 'X'
    }

    response = requests.post(url,headers=header,data=body)
    return response.json()

def check_remaining_seats(seats: list) -> list:
    result = []
    
    for seat in seats:
        if seat['realSeatCntlk'] > 0:
            result.append(generate_message(seat))

    return result

def send_message(messages: list) -> None:
    slack_webhook_url = ""
    for message in messages:
        response = requests.post(slack_webhook_url, json={'text' : message})
   
def generate_message(seat: dict) -> str: 
    return seat['seatGradeName'] + ", " + seat['floorNo'] + seat['floorName'] + " " + seat['areaNo'] + seat['areaName'] + "에 잔여좌석 " + str(seat['realSeatCntlk']) + "개 발생! "

main()