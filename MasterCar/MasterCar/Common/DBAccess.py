import pymssql
class SQLServer(object):
    def __init__(self):
        self.connect = pymssql.connect(
            host='192.168.4.241:1433',
            user='PUser',
            password='sa123456',
            database='DB_Cars',
            charset='utf8'
        )

    def ClearCarsInfo(self):
        try:
            self.connect.cursor().execute('delete from T_CarsInfo');
            self.connect.cursor().execute('delete from T_Cars_Senstive');
            self.connect.commit()
        except Exception as e:
            print(e);