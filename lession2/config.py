import yaml
# pydantic

class Config:
    def __init__(self, path):
        with open(path, 'r') as cfg_file:
            self.config = yaml.safe_load(cfg_file)

    def get_config(self, app='app1'):
        return self.config[app]