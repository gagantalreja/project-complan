import os

config_object = None


class Config:
    def __init__(self):
        self.open_api_key = os.environ.get("OPENAI_API_KEY", "1234XXXXX4321")
        self.slack_signing_secret = os.environ.get("SIGNING_SECRET", "XXX")
        self.slack_oauth_token = os.environ.get("SLACK_TOKEN", "XXX")


def load_config(force=True):
    if config_object and not force:
        return config_object
    else:
        return Config()


class Configuration:
    def __init__(self):
        self.env_obj = load_config(force=False)
