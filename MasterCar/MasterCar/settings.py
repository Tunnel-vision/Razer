# 项目名称
BOT_NAME = 'MasterCar'
# 爬虫模块
SPIDER_MODULES = ['MasterCar.spiders']
NEWSPIDER_MODULE = 'MasterCar.spiders'
# 使用scrapy-redis调度器
SCHEDULER="scrapy_redis.scheduler.Scheduler"
# 去重
DUPEFILTER_CLASS="scrapy_redis.dupefilter.RFPDupeFilter"
# 先入先出的队列
SCHEDULER_QUEUE_CLASS='scrapy_redis.queue.SpiderQueue'
#DOWNLOAD_DELAY = 1
# 指定数据库的主机IP
REDIS_HOST = "127.0.0.1"
# 指定数据库的端口号
REDIS_PORT = 6379
#REDIS_URL = 'redis://39.106.155.194:6379'
"""
Redis中的URL不会被Scrapy_redis清理掉，
这样的好处是：爬虫停止了再重新启动，
它会从上次暂停的地方开始继续爬取
"""
SCHEDULER_PERSIST=True
# 默认 Request 并发数：100
CONCURRENT_REQUESTS = 100
# 默认每个域名的并发数：10000
CONCURRENT_REQUESTS_PER_DOMAIN = 10000

IPPOOL=[
	{"ipaddr":"113.200.214.164:8080"}
]
