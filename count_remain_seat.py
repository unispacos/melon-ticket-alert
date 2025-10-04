import requests
import time
import os

#######################################################
########### 아래 값 채워준 뒤 실행해주시면 됩니다. #############
#######################################################
prodId = "211782"
pocCode = "SC0002"
scheduleNo = "100003"
cookie = "PCID=17556875702275130360238; _fwb=223VZG4pADhVnhHFOH5fTws.1755687570228; PC_PCID=17556875702275130360238; POC=MP10; _T_ANO=iUnLJuzpqG92Ns8dTM2b8TMLrM8TJ9SNN8ExIU128d5PZnAO1NUfmwKtmir8KOpR9O6AqxQSUmDvLmubDhP7jmgQ1zFMw0HGILB3F3E0ehvr+8eKSqRrPXNCv3CH6/msy0xdEuJVMA91zdPhU+KavSJCgGNlDmbOqSLeX6/wzzjz7YO4QiWgpTVRCI/hq1Kiz3qwYoarND5pQ1C62mVCRcUi2pJQ6grubFTj8IcedR4sD6zEZE3yMS0Hd+WNe5N3lJf876afbE2dOnxGaGSC+WzSd9esCLtyB/u7pnwVKzpAcbCCDoUTW8QM/S5UCmwsotOZKsLJtUnsG2Bove6xtg==; TKT_POC_ID=MP15; hide_banner=true; cbo=0; MAC=G86hhkkWECwD3+XzKKBtL17ZQpPpEPxEXUhvMNKQjg8vIbEgDAmK2wrC3fpz6s0W; MLCP=MjU2MTcyOTQlM0J3aGl0ZXl1cmltJTNCJTNCMCUzQmV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnBjM01pT2lKdFpXMWlaWEl1YldWc2IyNHVZMjl0SWl3aWMzVmlJam9pYldWc2IyNHRhbmQwSWl3aWFXRjBJam94TnpVNU5Ua3dPVGczTENKdFpXMWlaWEpMWlhraU9pSXlOVFl4TnpJNU5DSXNJbUYxZEc5TWIyZHBibGxPSWpvaVRpSjkuaXg5LTZTYmVhYmU4UDNBcGZicVBrdmQ0Z2tuQlU1b05VcG5OeGdMRk4zTSUzQiUzQjIwMjUxMDA1MDAxNjI3JTNCbXlteXZydnIlM0IxJTNCeXVyaW15aSU0MG5hdmVyLmNvbSUzQjIlM0I=; MUS=1291887357; keyCookie=25617294; NetFunnel_ID=WP15; store_melon_cupn_check=25617294; performance_layer_alert=%2C211782; wcs_bt=s_585b06516861:1759593391; JSESSIONID=E1227ECEA3102070F12A21F7F1013F4B"
slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]


def main() -> None:
    for i in range(30):
        seats = get_seats_summary()
        messages = check_remaining_seats(seats['summary'])
        send_message(messages)
        time.sleep(2)
        
def get_seats_summary() -> None:
    url = "https://ticket.melon.com/tktapi/product/summary.json?v=1" 
   
    body = {
        'prodId': prodId,
        'pocCode': pocCode,
        'scheduleNo': scheduleNo
    }

    header = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Content-Length': '76',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
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
    for message in messages:
        response = requests.post(slack_webhook_url, json={'text' : message})
   
def generate_message(seat: dict) -> str: 
    message = ""
    message += seat['seatGradeName'] + ", " if 'seatGradeName' in seat else ""
    message += seat['floorNo'] if 'floorNo' in seat else ""
    message += seat['floorName'] +  " " if 'floorName' in seat else ""
    message += seat['areaNo'] if 'areaNo' in seat else ""
    message += seat['areaName'] if 'areaName' in seat else ""
    message += "에 잔여좌석 " + str(seat['realSeatCntlk']) + "개 발생! "
    return message

main()
