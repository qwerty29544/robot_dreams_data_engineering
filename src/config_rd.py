import yaml
import requests
import json
import os
from datetime import datetime


# TODO: Нужно добавить общие логи и инициализацию директорий на уровне инициализации класса
class RdConnecter:
    def __init__(self, config_path):
        with open(config_path, 'r') as yaml_file:
            self.config = yaml.safe_load(yaml_file)
        self.last_token = ""

    def get_AUTH(self):
        return self.config['AUTH']

    def get_API(self):
        return self.config['API']

    def post_token(self):
        auth_cfg = self.get_AUTH()
        token = auth_cfg['expected output']
        token_key = list(token.keys())[0]
        # TODO: Вообще тут нужно добавить проверку возвращаемого от API ключа
        # output_token_base = auth_cfg['output type']

        try:
            request = requests.post(url=auth_cfg['url'] + auth_cfg['endpoint'],
                                    data=json.dumps(auth_cfg['payload']),
                                    headers=auth_cfg['headers'])
            request.raise_for_status()
            if not token_key == list(request.json().keys())[0]:
                pass
            else:
                token[token_key] = request.json()[token_key]

            output_token = token[token_key]
            self.last_token = output_token
            return output_token
        except requests.exceptions.HTTPError:
            print("Response error")
            return None

    def get_data(self):
        api_cfg = self.get_API()
        jwt_token = self.post_token()
        if jwt_token is None:
            print("Bad request")
            return None

        token_base = api_cfg['headers']['Authorization'].split(" ")
        token_base[1] = jwt_token
        api_cfg['headers']['Authorization'] = " ".join(token_base)

        dir_path = api_cfg['dir path']
        if dir_path is None or not os.path.isdir(dir_path):
            dir_path = os.path.dirname(os.getcwd())

        path_data = os.path.join(dir_path, "data")
        path_logs = os.path.join(dir_path, "logs")

        os.makedirs(path_data, exist_ok=True)
        os.makedirs(path_logs, exist_ok=True)

        # TODO: проверить не лежит ли в config.yaml по payload список и итерироваться по списку дат
        today_data_path = os.path.join(path_data, api_cfg['payload']['date'] + ".json")
        today_logs_path = os.path.join(path_logs, api_cfg['payload']['date'] + ".json")

        try:
            request = requests.get(url=api_cfg['url'] + api_cfg['endpoint'],
                                   data=json.dumps(api_cfg['payload']),
                                   headers=api_cfg['headers'])
            request.raise_for_status()
            data = request.json()
            with open(today_data_path, "w") as data_json:
                json.dump(data, data_json)
            with open(today_logs_path, 'w') as logs_json:
                comment = {"date": api_cfg['payload']['date'],
                           "time": datetime.ctime(datetime.now()).split(" ")[3],
                           "result": "correct data read"}
                json.dump(comment, logs_json)
            return True

        except requests.exceptions.HTTPError:
            with open(today_logs_path, 'w') as logs_json:
                comment = {"date": api_cfg['payload']['date'],
                           "time": datetime.ctime(datetime.now()).split(" ")[3],
                           "result": "bad data requesting"}
                json.dump(comment, logs_json)
            return None


