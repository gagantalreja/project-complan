import logging
from slack_bolt import App
from config.config import Configuration
from executor import Executor
from dotenv import load_dotenv

load_dotenv()

LOG_FORMAT = '%(clientip)-15s - - [%(asctime)s] %(user)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
config = Configuration()

logging.debug(config.env_obj.slack_oauth_token)

app = App(token=config.env_obj.slack_oauth_token)
executor = Executor()

@app.middleware
def log_request(logger, body, next):
    logger.debug(body)
    return next()

@app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)
    say("What's up?")

@app.event("message")
def ack_the_rest_of_message_events(body, say, logger):
    logger.info(body['event'])
    response = executor.execute(body['event']['text'])
    say(response)

@app.event("app_home_opened")
def handle_app_home_opened(body, say, logger):
    logger.info(body)
    say("Hi <@{user}>".format(user=body['event']['user']))


if __name__ == "__main__":
    app.start(3000)
