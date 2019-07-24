from scrapyd_api import ScrapydAPI
import threading
import time
import platform
import redis
import os

rtemp = redis.from_url('redis://:liusha4439@218.90.186.70')
r = redis.from_url('redis://:liusha4439@121.43.160.214')

scrapyd_google = ScrapydAPI('http://104.196.235.86:6800')
scrapyd_azure_c = ScrapydAPI('http://137.135.19.85:6800')
scrapyd_azure_spider = ScrapydAPI('http://168.63.205.135:6800')

dict_jobs = {}
job_list = []

azure_spider_dict_jobs = {}
azure_spider_job_list = []

azure_c_dict_jobs = {}
azure_c_job_instagram_list = []
azure_c_job_reddit_list = []


def start_azure_c_jobs():
    global azure_c_dict_jobs
    global azure_c_job_instagram_list
    global azure_c_job_reddit_list

    azure_c_dict_jobs.clear()
    azure_c_job_instagram_list = []
    azure_c_job_reddit_list = []

    insider_job_id = scrapyd_azure_c.schedule('Insider', 'insider')
    azure_c_dict_jobs['Insider'] = insider_job_id
    time.sleep(5)

    instagram_job_id = scrapyd_azure_c.schedule('Instagram', 'instagram')
    azure_c_job_instagram_list.append(instagram_job_id)
    time.sleep(5)

    instagramminliangtan_job_id = scrapyd_azure_c.schedule('Instagram', 'instagramminliangtan')
    azure_c_job_instagram_list.append(instagramminliangtan_job_id)
    time.sleep(5)
    azure_c_dict_jobs['Instagram'] = azure_c_job_instagram_list

    instagramdetail_job_id = scrapyd_azure_c.schedule('InstagramDetail', 'instagramdetail')
    azure_c_dict_jobs['InstagramDetail'] = instagramdetail_job_id
    time.sleep(5)

    microsoft_job_id = scrapyd_azure_c.schedule('Microsoft', 'microsoft')
    azure_c_dict_jobs['Microsoft'] = microsoft_job_id
    time.sleep(5)

    reddit_job_id = scrapyd_azure_c.schedule('Reddit', 'reddit')
    azure_c_job_reddit_list.append(reddit_job_id)
    time.sleep(5)

    redditpcmasterrace_job_id = scrapyd_azure_c.schedule('Reddit', 'redditpcmasterrace')
    azure_c_job_reddit_list.append(redditpcmasterrace_job_id)
    time.sleep(5)

    reddittechsupport_job_id = scrapyd_azure_c.schedule('Reddit', 'reddittechsupport')
    azure_c_job_reddit_list.append(reddittechsupport_job_id)
    time.sleep(5)

    azure_c_dict_jobs['Reddit'] = azure_c_job_reddit_list

    redditdetail_job_id = scrapyd_azure_c.schedule('RedditDetail', 'redditdetail')
    azure_c_dict_jobs['RedditDetail'] = redditdetail_job_id

    print('**********************************************')
    print(azure_c_dict_jobs)
    print('**********************************************')


def cancel_azure_c_jobs():
    global azure_c_dict_jobs
    global azure_c_job_instagram_list
    global azure_c_job_reddit_list

    try:
        for key, value in azure_c_dict_jobs.items():
            try:
                if isinstance(value, list):
                    for li in value:
                        scrapyd_azure_c.cancel(key, li)
                else:
                    scrapyd_azure_c.cancel(key, value)
            except:
                print('>>>>>>>>>>>>cancel_azure_c_jobs exception<<<<<<<<<<<<<')
                continue
    finally:
        azure_c_dict_jobs.clear()
        azure_c_job_instagram_list = []
        azure_c_job_reddit_list = []
        clear()


def clear():
    try:
        if platform.platform().startswith('Windows'):
            # kill google-chrome进程和chromedriver
            print(os.popen('tasklist'))
            os.system('taskkill /IM chrome.exe /F')
            os.system('taskkill /IM chromedriver.exe /F')

            # 删除日志文件夹


        else:
            # kill google-chrome进程和chromedriver
            os.system(r"ps -ef | fgrep  google-chrome | awk '{print $2}'| xargs kill -9")
            os.system(r"ps -ef | fgrep  chromedriver | awk '{print $2}'| xargs kill -9")

            # 删除日志文件夹
            os.system('sudo rm -rf /root/logs')

            # 清理内存
            os.system('echo 1 > /proc/sys/vm/drop_caches')

        # 清除所有redis队列
        rtemp.flushdb()
        r.flushdb()
    except:
        pass


def start_azure_spider_jobs():
    global azure_spider_dict_jobs
    global azure_spider_job_list

    azure_spider_dict_jobs.clear()
    azure_spider_job_list = []

    amazon_job_id = scrapyd_azure_spider.schedule('Amazon', 'amazon')
    azure_spider_dict_jobs['Amazon'] = amazon_job_id
    time.sleep(5)

    amazondetail_job_id = scrapyd_azure_spider.schedule('AmazonDetail', 'amazondetail')
    azure_spider_dict_jobs['AmazonDetail'] = amazondetail_job_id
    time.sleep(5)

    boardreader_job_id = scrapyd_azure_spider.schedule('BoardReader', 'boardreader')
    azure_spider_dict_jobs['BoardReader'] = boardreader_job_id
    time.sleep(5)

    facebook_job_id = scrapyd_azure_spider.schedule('Facebook', 'facebook')
    azure_spider_job_list.append(facebook_job_id)
    time.sleep(5)

    facebookminliangtan_job_id = scrapyd_azure_spider.schedule('Facebook', 'facebookminliangtan')
    azure_spider_job_list.append(facebookminliangtan_job_id)
    time.sleep(5)

    facebookopensourcevr_job_id = scrapyd_azure_spider.schedule('Facebook', 'facebookopensourcevr')
    azure_spider_job_list.append(facebookopensourcevr_job_id)
    time.sleep(5)

    facebookteamrazer_job_id = scrapyd_azure_spider.schedule('Facebook', 'facebookteamrazer')
    azure_spider_job_list.append(facebookteamrazer_job_id)
    azure_spider_dict_jobs['Facebook'] = azure_spider_job_list
    time.sleep(5)

    notebookreview_job_id = scrapyd_azure_spider.schedule('NotebookReview', 'notebookreview')
    azure_spider_dict_jobs['NotebookReview'] = notebookreview_job_id

    print('**********************************************')
    print(azure_spider_dict_jobs)
    print('**********************************************')


def cancel_azure_spider_jobs():
    global azure_spider_dict_jobs
    global azure_spider_job_list

    try:
        for key, value in azure_spider_dict_jobs.items():
            try:
                if isinstance(value, list):
                    for li in value:
                        scrapyd_azure_spider.cancel(key, li)
                else:
                    scrapyd_azure_spider.cancel(key, value)
            except:
                print('>>>>>>>>>>>>cancel_azure_spider_jobs exception<<<<<<<<<<<<<')
                continue
    finally:
        azure_spider_dict_jobs.clear()
        azure_spider_job_list = []
        clear()


def start_google_jobs():
    global dict_jobs
    global job_list
    dict_jobs.clear()
    job_list = []
    theverge_job_id = scrapyd_google.schedule('Theverge', 'theverge')
    dict_jobs['Theverge'] = theverge_job_id
    twitter_job_id = scrapyd_google.schedule('Twitter', 'twitter')
    dict_jobs['Twitter'] = twitter_job_id
    time.sleep(5)

    youtube_job_id = scrapyd_google.schedule('Youtube', 'youtube')
    dict_jobs['Youtube'] = youtube_job_id
    time.sleep(5)

    youtubedetail_job_id = scrapyd_google.schedule('YoutubeDetail', 'youtubedetail')
    dict_jobs['YoutubeDetail'] = youtubedetail_job_id
    time.sleep(5)

    youtuberazer_job_id = scrapyd_google.schedule('YoutubeRazer', 'youtuberazer')
    dict_jobs['YoutubeRazer'] = youtuberazer_job_id
    time.sleep(5)

    youtuberazerdetail_job_id = scrapyd_google.schedule('YoutubeRazerDetail', 'youtuberazerdetail')
    dict_jobs['YoutubeRazerDetail'] = youtuberazerdetail_job_id
    time.sleep(5)

    twitterdetail_job_id = scrapyd_google.schedule('TwitterDetail', 'twitterdetail')
    dict_jobs['TwitterDetail'] = twitterdetail_job_id
    time.sleep(5)

    socialmention_job_id = scrapyd_google.schedule('SocialMention', 'socialmention')
    dict_jobs['SocialMention'] = socialmention_job_id
    time.sleep(5)

    socialmentiondetail_job_id = scrapyd_google.schedule('SocialMentionDetail', 'socialmentiondetail')
    dict_jobs['SocialMentionDetail'] = socialmentiondetail_job_id
    time.sleep(5)

    twitterminliangtan_job_id = scrapyd_google.schedule('TwitterSource', 'twitterminliangtan')
    job_list.append(twitterminliangtan_job_id)
    time.sleep(5)

    twitteropensourcevr_job_id = scrapyd_google.schedule('TwitterSource', 'twitteropensourcevr')
    job_list.append(twitteropensourcevr_job_id)
    time.sleep(5)

    twittersource_job_id = scrapyd_google.schedule('TwitterSource', 'twittersource')
    job_list.append(twittersource_job_id)
    time.sleep(5)

    twitterteamrazer_job_id = scrapyd_google.schedule('TwitterSource', 'twitterteamrazer')
    job_list.append(twitterteamrazer_job_id)
    dict_jobs['TwitterSource'] = job_list
    print('**********************************************')
    print(dict_jobs)
    print('**********************************************')


def cancel_googel_jobs():
    global dict_jobs
    global job_list
    try:
        for key, value in dict_jobs.items():
            try:
                if isinstance(value, list):
                    for li in value:
                        scrapyd_google.cancel(key, li)
                else:
                    scrapyd_google.cancel(key, value)
            except:
                print('>>>>>>>>>>>>cancel_spider_jobs exception<<<<<<<<<<<<<')
                continue
    finally:
        dict_jobs.clear()
        job_list = []
        clear()


def func_google_timer():
    cancel_googel_jobs()
    start_google_jobs()
    global google_timer
    google_timer = threading.Timer(3 * 60 * 60, func_google_timer)
    google_timer.start()


def func_azure_spider_timer():
    cancel_azure_spider_jobs()
    start_azure_spider_jobs()
    global azure_spider_timer
    azure_spider_timer = threading.Timer(3 * 60 * 60, func_azure_spider_timer)
    azure_spider_timer.start()

def func_azure_c_timer():
    cancel_azure_c_jobs()
    start_azure_c_jobs()
    global azure_c_timer
    azure_c_timer = threading.Timer(3 * 60 * 60, func_azure_c_timer)
    azure_c_timer.start()


if __name__ == '__main__':
    google_timer = threading.Timer(1, func_google_timer)
    google_timer.start()

    azure_spider_timer = threading.Timer(1, func_azure_spider_timer)
    azure_spider_timer.start()

    azure_c_timer = threading.Timer(1, func_azure_c_timer)
    azure_c_timer.start()
