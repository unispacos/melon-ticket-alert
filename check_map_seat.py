import requests
import json

header = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Content-Length': '75',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '_fwb=157FfrvzGd8P9TaeVuTlmji.1732505114404; PCID=17325051145380684711937; PC_PCID=17325051145380684711937; _T_ANO=LdxO3meWcccuTMykzynf5Ou3ih7+bBk+LXsOne5hgFM1pfyGdzvZ7ycQLYM3424quILz2LMOUnAqIv3x/PXtIuLxXK8Is7h6jK693iG73AhtvjQXL2t9fiVDN6ZoA0A2A/tZco9e8ugZ4pdRMdtAu9Vz00SxNbNFTWpZ5+p96NbuuyqBa5bWkL6ENUToJPsFqOlqeZ8KhjTTG7Zy3l3pZJFnYmRnOFEukF4TZowAgUou4/SQU6a4LNxPfM9/L3yvuWSUMsQVRTMRkAjjchL7fVeM3GGRXX4Z4/PRXerslQxb7ZJTTQeWzSbnUjXlbOPFRV32ZqXmVkNvs7ShjNw/sQ==; TKT_POC_ID=MP15; cbo=0; MAC=QsRJhbHtBNWlff+Q4A/g20lB7Vmq4to4r3SWlKRjSweZkCdz+xRTweSm4jslZuKy; MLCP=MTIzODM4MTAlM0Jyb3poZWtla2VrJTNCJTNCMCUzQmV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnBjM01pT2lKdFpXMWlaWEl1YldWc2IyNHVZMjl0SWl3aWMzVmlJam9pYldWc2IyNHRhbmQwSWl3aWFXRjBJam94TnpNMU9EYzFNemc0TENKdFpXMWlaWEpMWlhraU9pSXhNak00TXpneE1DSXNJbUYxZEc5TWIyZHBibGxPSWpvaVRpSjkuQURGMmEtS2QtQ09mUC1jUmhLWG42U1F4QVp5QlJaV1dJT1lLbjBJMndhNCUzQiUzQjIwMjUwMTAzMTIzNjI4JTNCRW1hRGFtJTNCMSUzQmxkeTkwMzclNDBuYXZlci5jb20lM0IyJTNC; MUS=727328307; keyCookie=12383810; hide_banner=true; NetFunnel_ID=WP15; store_melon_cupn_check=12383810; wcs_bt=s_585b06516861:1735875409; JSESSIONID=5ED05E970FDBF842EA7D969DE3FA57D8',
    'Host': 'ticket.melon.com',
    'Referer': 'https://ticket.melon.com/reservation/popup/stepBlock.htm',
    'User-Agent': 'X'
}

def get_block_list() -> list:
    url = "https://ticket.melon.com/tktapi/product/getAreaMap.json?v=1&callback=getBlockGradeSeatMapCallBack" 
    
    body = {
        'prodId': '210629',
        'pocCode': 'SC0002',
        'scheduleNo': '100001'
    }
    
    response = requests.post(url,headers=header,data=body)
    block_datas = json.loads(response.text.replace("/**/getBlockGradeSeatMapCallBack(","").replace(");", "")) 
            
    for st in block_datas['seatData']['st']:
        print(st['sbid'])
            
    return block_datas['seatData']['st']
    

def get_remain_seat_in_block(block_id) -> int:
    url = "https://ticket.melon.com/tktapi/product/seat/seatMapList.json?v=1&callback=getSeatListCallBack" 
   
    body = {
        'prodId': '210629',
        'pocCode': 'SC0002',
        'scheduleNo': '100001',
        'blockId': block_id, #getAreaMap.json > seatData > st > sbid
        'corpCodeNo': ''
    }

    response = requests.post(url,headers=header,data=body)
    map_datas = json.loads(response.text.replace("/**/getSeatListCallBack(","").replace(");", ""))
    count = 0

    for st in map_datas['seatData']['st'][0]['ss']:
        if st['sid'] != None: 
            count += 1 
            
    return count

get_block_list()