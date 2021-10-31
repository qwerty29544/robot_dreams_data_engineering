import requests
import json
import yaml
import os


def get_json_data(**kwargs):
    # TODO: есть проблема с тем, что называется, кривые пути, решается ли это КОЛЕСО-файлом?
    config_path = os.path.join(os.getcwd(), 'airflow/dags/common/config.yaml')
    print(config_path)
    with open(config_path, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    # читаю токен из пулла
    xcom_token = json.loads(kwargs['ti'].xcom_pull(task_ids='get_auth_token_via_http_post'))['access_token']
    # дата выполнения таски из context
    execution_date = kwargs['ds']

    # TODO: нужен ли здесь вообще try? Я что-то думаю, что airflow сам по себе умеет хорошо логгировать ошибки
    try:
        request = requests.get(url=config['API']['url'] + config['API']['endpoint'],
                               data=json.dumps({"date": execution_date}),
                               headers={"content-type": "application/json", "Authorization": f"JWT {xcom_token}"})
        request.raise_for_status()
        data = request.json()
        # папка с выгрузкой из конфигурации
        with open(config['API']['dir path'] + f'{execution_date}.json', "w") as data_json:
            json.dump(data, data_json)
        print("All was ok, data passed")
        return True

    except requests.exceptions.HTTPError:
        print("All was'n ok? HTTP ERROR")
        return False