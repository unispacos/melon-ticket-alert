import requests
import json
import time
import os

#######################################################
########### 아래 값 채워준 뒤 실행해주시면 됩니다. #############
#######################################################
prodId = os.environ["PRODID"]
pocCode = os.environ["POCCODE"]
scheduleNo = os.environ["SCHEDULENO"]
cookie = os.environ["COOKIE"]
slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#######################################################
#######################################################

header = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Content-Length': '75',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': cookie,
    'Host': 'ticket.melon.com',
    'Referer': 'https://ticket.melon.com/reservation/popup/stepBlock.htm',
    'User-Agent': 'X'
}

def get_block_list() -> list:
    url = "https://ticket.melon.com/tktapi/product/getAreaMap.json?v=1&callback=getBlockGradeSeatMapCallBack" 
    
    body = {
        'prodId': prodId,
        'pocCode': pocCode,
        'scheduleNo': scheduleNo
    }
    
    response = requests.post(url,headers=header,data=body)
    block_datas = json.loads(response.text.replace("/**/getBlockGradeSeatMapCallBack(","").replace(");", "")) 
            
    return block_datas['seatData']['da']['sb']
    

def get_remain_seat_in_block(block) -> int:
    url = "https://ticket.melon.com/tktapi/product/seat/seatMapList.json?v=1&callback=getSeatListCallBack" 
   
    body = {
        'prodId': prodId,
        'pocCode': pocCode,
        'scheduleNo': scheduleNo,
        'blockId': block['sbid'], #getAreaMap.json > seatData > st > sbid
        'corpCodeNo': ''
    }

    response = requests.post(url,headers=header,data=body)
    map_datas = json.loads(response.text.replace("/**/getSeatListCallBack(","").replace(");", ""))
    count = 0
    
    if "seatData" in map_datas:
        for st in map_datas['seatData']['st'][0]['ss']:
            if st['sid'] != None: 
                count += 1    
    
    return count

def send_message(message: str) -> None:
    response = requests.post(slack_webhook_url, json={'text' : message})

def main() -> None:
    for i in range(30):
        blocks = get_block_list()
        for block in blocks:
            count = get_remain_seat_in_block(block)
            if count > 0:
                send_message(block['sntv']['a'] + "구역에 잔여좌석 " + str(count) + "개 발생!")
        time.sleep(2)
        
main()
