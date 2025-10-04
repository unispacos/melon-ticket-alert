import requests
import json
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
