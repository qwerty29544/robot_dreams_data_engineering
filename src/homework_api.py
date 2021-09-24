import requests
import json
from config_rd import RdConnecter


def run():
    cfg = RdConnecter("config.yaml")
    cfg.get_data()


if __name__ == '__main__':
    run()