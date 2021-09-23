import json
import os
import requests
from config import Config
from datetime import date
from requests.exceptions import HTTPError

# exchangerateapi.io


def app(config):

    today = date.today()
    dir_path = os.path.join('..', config['directory'], str(today))
    os.makedirs(dir_path, exist_ok=True)

    for symbol in config['symbols']:
        params = {'access_key': config['access_key'], 'symbols': symbol}
        try:
            r = requests.get(url=config['url'],
                             params=params,
                             allow_redirects=True,
                             timeout=10)
            r.raise_for_status()
            data = r.json()

            with open(os.path.join(dir_path, symbol + ".json"), 'w') as json_file:
                json.dump(data, json_file)
        except HTTPError:
            print(f"Error with requesting {symbol} currency")


if __name__ == "__main__":
    config = Config("config.yaml")
    app(config.get_config('currency_app'))
