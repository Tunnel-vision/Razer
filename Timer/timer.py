# -*- coding: utf-8 -*-
import threading
import mail
import pymysql
from datetime import datetime
import requests
import os
import datetime
import time


def get_total_issues():
    db = pymysql.connect('218.90.186.70', 'root', '1qaz@WSX', 'razer', charset='utf8', port=3306)
    cursor = db.cursor()
    # dt = datetime.datetime.now().strftime('%Y-%m-%d %H%%')
    dt = datetime.datetime.now()
    delta1 = datetime.timedelta(hours=-1)
    dt1 = dt + delta1
    delta2 = datetime.timedelta(hours=-2)
    dt2 = dt + delta2
    sql = """SELECT count(*) FROM ( SELECT * FROM instagram WHERE DateofAdd >= DATE_SUB(now(), INTERVAL 3 HOUR) UNION SELECT * FROM twitter WHERE DateofComplaint >= DATE_SUB(now(), INTERVAL 3 HOUR)) tb"""
    db.ping(reconnect=True)
    cursor.execute(sql)
    num = cursor.fetchone()[0]
    if num is None:
        num = 0
    db.close()
    return num


# 每隔3小时发送一次邮件
def func_timer():
    url = 'http://192.168.4.35/TaskSet/TaskSet.ashx?action=ExportExcel'
    response = requests.get(url)
    time.sleep(5)
    # html = response.read()
    excelpath = get_result_excel(r'D:\Razer\outRazer\Files\Excel')
    num = get_total_issues()
    if num > 0:
        mail.send_email(num, excelpath)
    else:
        print('NOT FOUND NEW DATA')
    global timer
    timer = threading.Timer(3 * 60 * 60, func_timer)
    timer.start()


def get_result_excel(filepath):
    dt = datetime.datetime.now().strftime('%Y%m%d%H')
    files = os.listdir(filepath)
    for fi in files:
        temppath = ''.join([filepath, os.sep])
        fullpath = ''.join([temppath, fi])
        if dt in fullpath:
            return fullpath


if __name__ == '__main__':
    timer = threading.Timer(1, func_timer)
    timer.start()
