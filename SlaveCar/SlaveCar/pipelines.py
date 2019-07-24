# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors
import pymssql
from twisted.enterprise import adbapi
# 存到slave的Mysql
class MySQLPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='192.168.4.31',
            port=3306,
            user='root',
            passwd='root',
            db='db_cars',
            charset='utf8'
        )
    def process_item(self, item, spider):
        try:
            print('*************************************写入开始*************************************');
            self.connect.cursor().execute('insert into T_CarsInfo (Url,Post_Time,Car_Type_Title,youdian,quedian'
                                          ',waiguan,neishi,kongjian,peizhi,dongli,chaokong,youhao,shushi,comments'
                                          ',CreatedName,CreatedTime) values(%s,%s,%s,''%s'',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())',
                       (item['Url'], item['Post_Time'], item['Car_Type_Title'], item['youdian'],
                        item['quedian'], item['waiguan'], item['neishi'], item['kongjian'],
                        item['peizhi'], item['dongli'], item['chaokong'], item['youhao']
                        ,item['shushi'],item['comments'],'Slave1'))
            self.connect.commit()
            print("*************************************写入成功*************************************")
        except Exception as e:
            print("*************************************写入失败*************************************.")
            print(e);
        return item

class SQLServerPipeline(object):
    def __init__(self):
        self.connect = pymssql.connect(
            host='192.168.4.241:1433',
            user='PUser',
            password='sa123456',
            database='DB_Cars',
            charset='utf8'
        )

    def process_item(self, item, spider):
        try:
            print('*************************************写入开始*************************************');
            # 数据插入到汽车信息表
            self.connect.cursor().execute('insert into T_CarsInfo (Url,Post_Time,Car_Type,Car_Type_Title,youdian,quedian'
                                          ',waiguan,neishi,kongjian,peizhi,dongli,chaokong,youhao,shushi,comments'
                                          ',CreatedTime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, convert(varchar(19),SYSDATETIME()))',
                                          (item['Url'], item['Post_Time'],item['Car_Type'], item['Car_Type_Title'], item['youdian'],
                                           item['quedian'], item['waiguan'], item['neishi'], item['kongjian'],
                                           item['peizhi'], item['dongli'], item['chaokong'], item['youhao']
                                           , item['shushi'], item['comments']))

            CarsID = self.connect.cursor().lastrowid;
            # 评论的情态特性插入
            self.connect.cursor().execute(
                'insert into T_Cars_Senstive1 (CarsID,CarsType,Post_Time,SenW,SenN,SenK,SenP,SenD'
                ',SenC,SenY,SenS,CreatedTime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,convert(varchar(19),SYSDATETIME()))',
                (CarsID,item['Post_Time'],item['Car_Type'], item['SenW'], item['SenN'], item['SenK'], item['SenP'],
                 item['SenD'], item['SenC'], item['SenY'], item['SenS']))

            # 数据插入到log表
            self.connect.cursor().execute( 'insert into T_CarsInfo_Log (Url,Post_Time,Car_Type,Car_Type_Title,youdian,quedian'
                                        ',waiguan,neishi,kongjian,peizhi,dongli,chaokong,youhao,shushi,comments'
                                        ',CreatedTime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, convert(varchar(19),SYSDATETIME()))',
                                        (item['Url'], item['Post_Time'], item['Car_Type'], item['Car_Type_Title'], item['youdian'],
                                         item['quedian'], item['waiguan'], item['neishi'], item['kongjian'],
                                         item['peizhi'], item['dongli'], item['chaokong'], item['youhao']
                                         , item['shushi'], item['comments']))

            self.connect.commit()
            print("*************************************写入成功*************************************")
        except Exception as e:
            print("*************************************写入失败*************************************.")
            print(e);
        return item