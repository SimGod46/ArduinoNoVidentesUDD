import pymysql
class data_manager:
    def __init__(self):
        db = pymysql.connect(host="dev.factoriaccp.cl", 
        user="factoriaccp", 
        passwd="Factor1a+", 
        database="factoria_dev",port=3306)
        self.cursor = db.cursor()
    def query_module(self, key):
        try:
            self.cursor.execute(f"SELECT * from ArduinoNoVidente where Modulo='{''.join(key.split())}'")
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(e)
            return 'ERROR'
    def query_all(self):
        try:
            self.cursor.execute(f"SELECT * from ArduinoNoVidente")
            result = self.cursor.fetchall()
            modulesDict = {}
            for module in result:
                modulesDict[module[0]]=module
            return modulesDict
        except Exception as e:
            print(e)
            return 'ERROR'