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
        'Cookie': '',
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