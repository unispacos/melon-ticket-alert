import requests

def get_map_seats() -> None:
    url = "https://ticket.melon.com/tktapi/product/seat/seatMapList.json?v=1&callback=getSeatListCallBack" 
   
    body = {
        'prodId': '210629',
        'pocCode': 'SC0002',
        'scheduleNo': '100001',
        'blockId': '2099',
        'corpCodeNo': ''
    }

    header = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Content-Length': '71',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '',
        'Host': 'ticket.melon.com',
        'Referer': 'https://ticket.melon.com/reservation/popup/stepBlock.htm',
        'User-Agent': 'X'
    }

    response = requests.post(url,headers=header,data=body)
    return response

get_map_seats()