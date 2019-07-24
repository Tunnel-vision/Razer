# -*- coding: utf-8 -*-

# Scrapy settings for BoardReader project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BoardReader'

SPIDER_MODULES = ['BoardReader.spiders']
NEWSPIDER_MODULE = 'BoardReader.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'BoardReader (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'BoardReader.middlewares.BoardreaderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'BoardReader.middlewares.SeleniumMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'BoardReader.pipelines.KeywordFilterPipeline': 300,
    'BoardReader.pipelines.MysqlPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
SELENIUM_TIMEOUT = 30

KEYWORDS = ["Razer issue", "Synapse issue", "Razer problem", "Razer break", "Razer not working", "Razer Error",
            "Razer stop working", "Razer Synapse", "Razer Software", "Razer Surround", "Razer Comms", "Razer Cortex",
            "Razer game booster", "Razer Chroma", "Razer Chroma Apps", "Chroma SDK", "Razer Stats and Heatmaps",
            "Razer Products", "Razer Gaming Systems", "Razer Systems", "Razer Blade", "Razer Core", "Razer Keyboards",
            "Razer Keypads", "Razer Mouse", "Razer Mousemat", "Razer Audio", "Razer Headset", "Razer Speaker",
            "Razer Earphone", "Razer Gaming Controller", "Razer Console", "Razer Microphone",
            "Razer Webcam", "Razer Capture Card", "Razer Bluetooth", "Razer Customer Support",
            "Razer Technical Support",
            "Razer Warranty", "Razer Lancehead", "Razer Lancehead TE", "Razer Synapse 3", "Synapse 3 Beta",
            "Synapse 3 pro", "Chroma HDK", "Razer Jugan", "Razer Madison", "Synapse X", "Razer Synapse for Xbox",
            "Razer Wolverine"]

MYSQL_HOST = '218.90.186.70'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'razer'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '1qaz@WSX'
