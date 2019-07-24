# -*- coding: utf-8 -*-

import datetime
from enum import Enum


class DateEnum(Enum):
    year = "year",
    month = "month",
    day = "day",
    week = "week",
    hour = "hour",
    minute = "minute",
    second = "second"


# date格式类似于3 days ago
def parse_date_str(date):
    # 解析日期字符串
    datelist = date.split(' ')
    datenum = int(datelist[0])
    delta = datetime.timedelta()
    if datelist[1].find(DateEnum['day'].name) != -1:
        delta = datetime.timedelta(days=-datenum)
    elif datelist[1].find(DateEnum['month'].name) != -1:
        delta = datetime.timedelta(days=-(datenum * 30))
    elif datelist[1].find(DateEnum['year'].name) != -1:
        delta = datetime.timedelta(days=-(datenum * 365))
    elif datelist[1].find(DateEnum['week'].name) != -1:
        delta = datetime.timedelta(weeks=-datenum)
    elif datelist[1].find(DateEnum['hour'].name) != -1:
        delta = datetime.timedelta(hours=-datenum)
    elif datelist[1].find(DateEnum['minute'].name) != -1:
        delta = datetime.timedelta(minutes=-datenum)
    elif datelist[1].find(DateEnum['second'].name) != -1:
        delta = datetime.timedelta(seconds=-datenum)

    thedate = datetime.datetime.now() + delta
    datestr = thedate.strftime('%Y-%m-%d %H:%M:%S.%f')
    totalsecs = str(thedate.timestamp())
    return datestr, totalsecs

# date格式：Jan 12, 2019,  4:52pm EST
def parse_est_date_str(date):
    dt = datetime.datetime.strptime(date, "%b %d, %Y, %I:%M%p EST")
    dtformat = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    result = str(dt.timestamp())
    return result, dtformat

# date格式：Oct 12, 2016 at 8:18 AM
def parse_at_date_str(date):
    dt = datetime.datetime.strptime(date, '%b %d, %Y at %I:%M %p')
    dtformat = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    result = str(dt.timestamp())
    return result, dtformat    

def parse_split_date_str(date):
    dt = datetime.datetime.strptime(date, '%m/%d/%Y')
    dtformat = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    result = str(dt.timestamp())
    return result, dtformat

# date格式'November 15, 2018'
def parse_fullmonth_date_str(date):
    dt = datetime.datetime.strptime(date, '%B %d, %Y')
    dtformat = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    result = str(dt.timestamp())
    return result, dtformat

# date格式 '10:16 PM - 6 Jan 2019'(24小时制)
def parse_date_id(date):
    dt = datetime.datetime.strptime(date, '%H:%M %p - %d %b %Y')
    dtformat = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    return dtformat

# date格式 '10:16 PM - 6 Jan 2019'(12小时制)
def parse_12hourclock_id(date):
    dt = datetime.datetime.strptime(date, '%I:%M %p - %d %b %Y')
    dtformat = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    return dtformat

# date格式：'2019-01-14T10:35:11.000Z'
def parse_date_tz(date):
    dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')
    dtformat = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    result = str(dt.timestamp())
    return result, dtformat

# date格式：Wednesday, December 12, 2018 at 1:06 PM
def parse_date_week_str(date):
    dt = datetime.datetime.strptime(date, '%A, %B %d, %Y at %H:%M %p')
    dtformat = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
    result = str(dt.timestamp())
    return result, dtformat