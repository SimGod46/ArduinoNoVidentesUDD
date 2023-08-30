import pymysql


class DataManager:
    def __init__(self):
        db = pymysql.connect(host="dev.factoriaccp.cl", 
        user="factoriaccp",
        passwd="Factor1a+", 
        database="factoria_dev", port=3306)
        self.cursor = db.cursor()

    def query_status(self, key):
        try:
            self.cursor.execute(f"SELECT * from ArduinoNoVidente where StatusCode = {key}")
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(e)
            return 'ERROR'

    def query_all(self):
        try:
            self.cursor.execute(f"SELECT * from ArduinoNoVidente")
            result = self.cursor.fetchall()
            modules_dict = {}
            for module in result:
                modules_dict[module[0]] = module
            return modules_dict
        except Exception as e:
            print(e)
            return 'ERROR'
