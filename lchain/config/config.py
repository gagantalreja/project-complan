import os
import json
from dotenv import load_dotenv

config_object = None

load_dotenv()


class Config:
    def __init__(self):
        self.open_api_key = os.environ.get("OPENAI_API_KEY")
        self.slack_signing_secret = os.environ.get("SIGNING_SECRET")
        self.slack_oauth_token = os.environ.get("SLACK_TOKEN")
        self.jira_user = os.environ.get("JIRA_USER")
        self.jira_token = os.environ.get("JIRA_TOKEN")
        with open(f"{os.getcwd()}/config/user_conf.json") as f:
            self.user_conf = json.load(f)


def load_config(force=True):
    if config_object and not force:
        return config_object
    else:
        return Config()


class Configuration:
    def __init__(self):
        self.env_obj = load_config(force=False)
