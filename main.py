import requests

def main() -> None:
    seats = get_seats_summary()
    messages = check_remaining_seats(seats['summary'])
    send_message(messages)

def get_seats_summary() -> None:
    url = "https://ticket.melon.com/tktapi/product/block/summary.json?v=1" 
   
    body = {
        'prodId': '210629',
        'pocCode': 'SC0002',
        'scheduleNo': '100001',
        'perfDate': '',
        'seatGradeNo': '',
        'corpCodeNo': ''
    }

    header = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Content-Length': '76',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'PCID=17351846072172531225115; _fwb=101589zbHZOiisQJu60NpBp.1735184607391; TKT_POC_ID=MP15; PC_PCID=17351846072172531225115; MAC=QsRJhbHtBNWlff+Q4A/g2xdxnCgO3l/MSoJgNfQfj0VFstYedJhJH0VWJSBbPkzV; MLCP=MTIzODM4MTAlM0Jyb3poZWtla2VrJTNCJTNCMCUzQmV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnBjM01pT2lKdFpXMWlaWEl1YldWc2IyNHVZMjl0SWl3aWMzVmlJam9pYldWc2IyNHRhbmQwSWl3aWFXRjBJam94TnpNMU1UZzBOakV4TENKdFpXMWlaWEpMWlhraU9pSXhNak00TXpneE1DSXNJbUYxZEc5TWIyZHBibGxPSWpvaVRpSjkuMkk0U0NIbGl0RzMtM0s2MmZhLWxqQVZELTgzSUJlU1ZIQjZ6SC1ZYUszTSUzQiUzQjIwMjQxMjI2MTI0MzMxJTNCRW1hRGFtJTNCMSUzQmxkeTkwMzclNDBuYXZlci5jb20lM0IyJTNC; MUS=-890363835; keyCookie=12383810; MTR=MTR; NetFunnel_ID=WP15; store_melon_cupn_check=12383810; JSESSIONID=1FAB90F897334646B07FCDB5381A12AF; wcs_bt=s_585b06516861:1735185039',
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
    message = ""
    message += seat['seatGradeName'] + ", " if seat['seatGradeName'] else ""
    message += seat['floorNo'] if seat['floorNo'] else ""
    message += seat['floorName'] +  " " if seat['floorName'] else ""
    message += seat['areaNo'] if seat['areaNo'] else ""
    message += seat['areaName'] if seat['areaName'] else ""
    message += "에 잔여좌석 " + str(seat['realSeatCntlk']) + "개 발생! "
    return message

main()