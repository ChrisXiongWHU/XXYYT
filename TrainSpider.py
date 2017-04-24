#coding:utf-8

import requests
import json
from pprint import pprint
from collections import namedtuple

TrainInfo = namedtuple('TrainInfo',['code','yz','zy','ze','buy','sTime','aTime','last'])

class TrainSpider(object):
    stationMap = {'庐山':'LSG','武汉':'WHN'}
    queryUrl = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
    headers = {
            'Host':'kyfw.12306.cn',
            'If-Modified-Since':'0',
            'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
    desired = ['D3274','D2232','D3264','K1268']


    def doQuery(self,date,from_station,to_station):   
        url = TrainSpider.queryUrl.format(date,
        TrainSpider.stationMap[from_station],TrainSpider.stationMap[to_station])
        qRe = requests.get(url=url,verify=False,headers=TrainSpider.headers)         
        res = json.loads(qRe.content,encoding='utf8')
        data = res['data']
        trainInfo = []
        with(open('res.txt','w')) as f:
            for train in data:
                info = train['queryLeftNewDTO']
                pprint(info,stream=f)
                trainCode = info['station_train_code']
                if trainCode in TrainSpider.desired:
                    yz = self.parse(info['yz_num']) #硬座
                    zy = self.parse(info['zy_num']) #一等座
                    ze = self.parse(info['ze_num']) #二等座
                    canWebBuy = info['canWebBuy'] == 'Y' #是否可购买
                    aTime = info['arrive_time']
                    sTime = info['start_time']
                    last = info['lishi']
                    trainInfo.append(TrainInfo(trainCode,yz,zy,ze,canWebBuy,sTime,aTime,last))
        return trainInfo

    def parse(self,num):
        if num == '--':
            return None
        elif num == u'\u6709':
            return 1
        elif num == u'\u65e0':
            return 0
        else:
            return int(num)

    
    def check(self,info):
        if info.buy:
            for ticket in info[1:4]:
                if ticket is not None and ticket > 0:
                    return True
    
    
    def query(self,date,from_station,to_station):
        trainInfo = self.doQuery(date,from_station,to_station)
        if len(trainInfo) == 0:
            return None
        needReport = [train for train in trainInfo if self.check(train)]
        strFormat4K = '车次:{}\t开始时间:{}\t到达时间:{}\t历时:{}\t硬座:{}'
        strFormat4D = '车次{}\t开始时间:{}\t到达时间:{}\t历时:{}\t一等座:{}\t二等座:{}'
        report = []
        for train in needReport:
            if train.code[0] == 'K':
                report.append(trFormat4K.format(train.code,train.sTime,train.aTime,train.last,train.yz))
            else:
                report.append(strFormat4D.format(train.code,train.sTime,train.aTime,train.last,train.zy,train.ze))
        ret = '\n'.join(report)
        return ret
        
            
                

                
                
        
        

if __name__ == '__main__':
    t = TrainSpider()             
    r = t.query('2017-02-26','庐山','武汉')

    
