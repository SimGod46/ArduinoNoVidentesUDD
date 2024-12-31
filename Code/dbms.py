import requests, json

class DataManager:
    def __init__(self):
        self.api_url = "https://blinduino.cl/jsonData"

    def parse_json(self, json_data):
        modules_dict = {}            
        if len(json_data) > 0:
            for item in json_data:
                module = list(item.values())
                modules_dict[module[0]] = module                
        return modules_dict

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
            if response.status_code != 200:
                raise AssertionError
            
            json_data = response.json()

            with open('blinduinoData.json', 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

            return self.parse_json(json_data)
        
        except Exception as e:
            print(e)
            with open('blinduinoData.json', 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                return self.parse_json(json_data)   
            return 'ERROR'