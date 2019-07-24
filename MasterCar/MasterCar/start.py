from multiprocessing import Process
from scrapy import cmdline
import time

# 配置参数即可, 爬虫名称，运行频率
confs = [
    {
        "spider_name": "master",
        "frequency": 2,
    },
]

def start_spider(spider_name, frequency):
    args = ["scrapy", "crawl", spider_name]
    while True:
        start = time.time()
        p = Process(target=cmdline.execute, args=(args,))
        p.start()
        p.join()
        time.sleep(frequency)


if __name__ == '__main__':
    for conf in confs:
        process = Process(target=start_spider,
                          args=(conf["spider_name"], conf["frequency"]))
        process.start()
        time.sleep(1800)
