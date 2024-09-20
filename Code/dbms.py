import pymysql
import requests

class DataManager:
    def __init__(self):
        self.api_url = "https://blinduino.cmasccp.cl"


    def query_status(self, keyCode):
        try:
            allModules = self.query_all()
            for _, value in allModules.items():
                if len(value) > 2 and value[2] == str(keyCode):
                    return value
            return None

        except Exception as e:
            print(e)
            return 'ERROR'

    def query_all(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                json_data = response.json()
                modules_dict = {}
                
                if len(json_data) > 0:
                    for item in json_data:
                        module = list(item.values())
                        modules_dict[module[0]] = module
                
                return modules_dict
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            print(e)
            return 'ERROR'