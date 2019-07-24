from scrapyd_api import ScrapydAPI
import threading
import time
import platform
import redis
import os

rtemp = redis.from_url('redis://:liusha4439@218.90.186.70')
r = redis.from_url('redis://:liusha4439@121.43.160.214')

scrapyd_azure_c = ScrapydAPI('http://127.0.0.1:6800')

azure_c_dict_jobs = {}
azure_c_job_instagram_list = []
azure_c_job_twitter_list = []


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
            # kill google-chrome process and chromedriver
            print(os.popen('tasklist'))
            os.system('taskkill /IM chrome.exe /F')
            os.system('taskkill /IM chromedriver.exe /F')

            # delete log dir
            del_logs_dir()

            # delete redis
            if rtemp.exists('instagramdetail:start_urls'):
                rtemp.delete('instagramdetail:start_urls')

            if r.exists('instagramdetail:start_urls'):
                r.delete('instagramdetail:start_urls')

            # if rtemp.exists('twitterdetail:start_urls'):
            #     rtemp.delete('twitterdetail:start_urls')
            #
            # if r.exists('twitterdetail:start_urls'):
            #     r.delete('twitterdetail:start_urls')
    except:
        pass


def start_azure_c_jobs():
    global azure_c_dict_jobs
    global azure_c_job_instagram_list
    global azure_c_job_twitter_list

    azure_c_dict_jobs.clear()
    azure_c_job_instagram_list = []
    azure_c_job_twitter_list = []

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

    # twitter_job_id = scrapyd_azure_c.schedule('Twitter', 'twitter')
    # azure_c_dict_jobs['Twitter'] = twitter_job_id
    # time.sleep(5)
    #
    # twitterdetail_job_id = scrapyd_azure_c.schedule('TwitterDetail', 'twitterdetail')
    # azure_c_dict_jobs['TwitterDetail'] = twitterdetail_job_id
    # time.sleep(5)
    #
    # twitterminliangtan_job_id = scrapyd_azure_c.schedule('TwitterSource', 'twitterminliangtan')
    # azure_c_job_twitter_list.append(twitterminliangtan_job_id)
    # time.sleep(5)
    #
    # twitteropensourcevr_job_id = scrapyd_azure_c.schedule('TwitterSource', 'twitteropensourcevr')
    # azure_c_job_twitter_list.append(twitteropensourcevr_job_id)
    # time.sleep(5)
    #
    # twittersource_job_id = scrapyd_azure_c.schedule('TwitterSource', 'twittersource')
    # azure_c_job_twitter_list.append(twittersource_job_id)
    # time.sleep(5)
    #
    # twitterteamrazer_job_id = scrapyd_azure_c.schedule('TwitterSource', 'twitterteamrazer')
    # azure_c_job_twitter_list.append(twitterteamrazer_job_id)
    # azure_c_dict_jobs['TwitterSource'] = azure_c_job_twitter_list


def cancel_azure_c_jobs():
    global azure_c_dict_jobs
    global azure_c_job_instagram_list
    global azure_c_job_twitter_list

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
        azure_c_job_twitter_list = []
        clear()


def func_azure_c_timer():
    cancel_azure_c_jobs()
    start_azure_c_jobs()
    global azure_c_timer
    azure_c_timer = threading.Timer(3 * 60 * 60, func_azure_c_timer)
    azure_c_timer.start()


if __name__ == '__main__':
    azure_c_timer = threading.Timer(1, func_azure_c_timer)
    azure_c_timer.start()
