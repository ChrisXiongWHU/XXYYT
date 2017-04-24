#coding:utf-8

from qqbot import QQBot
from TrainSpider import TrainSpider
import time


if __name__ == '__main__':
    myqqbot = QQBot(qq='2389111521')
    myqqbot.Login()

    spider = TrainSpider()
    interVal = 30
    while True:
        ret = spider.query('2017-02-26','庐山','武汉')
        if ret is not None:
            myqqbot.Send('buddy',qq='1050358918',content=ret)
        time.sleep(interVal)







