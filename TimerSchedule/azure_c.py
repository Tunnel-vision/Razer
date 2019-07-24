from scrapyd_api import ScrapydAPI
import threading
import time
import platform
import redis
import os

rtemp = redis.from_url('redis://:liusha4439@218.90.186.70')
r = redis.from_url('redis://:liusha4439@121.43.160.214')

scrapyd_azure_spider = ScrapydAPI('http://127.0.0.1:6800')

azure_spider_dict_jobs = {}
azure_spider_job_list = []


def del_logs_dir():
    try:
        import os
        import shutil
        rootdir = r'C:\Users\hrsystem\logs'
        filelist = os.listdir(rootdir)
        for f in filelist:
            filepath = os.path.join(rootdir, f)
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)
        shutil.rmtree(rootdir, True)
        print('Remove Success')
    except:
        print('Remove Exception')


def clear():
    try:
        if platform.platform().startswith('Windows'):
            # kill google-chrome进程和chromedriver
            print(os.popen('tasklist'))
            os.system('taskkill /IM chrome.exe /F')
            os.system('taskkill /IM chromedriver.exe /F')

            # 删除日志文件夹
            del_logs_dir()

            # 清除redis队列
            if rtemp.exists('amazondetail:start_urls'):
                rtemp.delete('amazondetail:start_urls')

            if r.exists('amazondetail:start_urls'):
                r.delete('amazondetail:start_urls')
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


def func_azure_spider_timer():
    cancel_azure_spider_jobs()
    start_azure_spider_jobs()
    global azure_spider_timer
    azure_spider_timer = threading.Timer(3 * 60 * 60, func_azure_spider_timer)
    azure_spider_timer.start()


if __name__ == '__main__':
    azure_spider_timer = threading.Timer(1, func_azure_spider_timer)
    azure_spider_timer.start()
