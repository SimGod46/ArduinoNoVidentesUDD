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
            statement= f'{result[0]}, detectado. Numero de pines = {result[1]}, {result[2]}. uso = {result[3]}'
            return statement
        except Exception as e:
            print(e)
            return 'ERROR'