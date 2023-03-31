import logging
from config.config import Configuration
from executor import Executor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
config = Configuration()

logging.debug(config.env_obj.slack_oauth_token)

# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
from slack_bolt import App
app = App(token=config.env_obj.slack_oauth_token)
executor = Executor()

# Add functionality here

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()

@app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)
    say("What's up?")

@app.event("message")
def ack_the_rest_of_message_events(body, say, logger):
    logger.info(body)
    logger.info(body['event'])
    r = executor.execute(body['event']['text'])
    say(r)


@app.event("app_home_opened")
def handle_app_home_opened(body, say, logger):
    logger.info(body)
    say("Hi")


if __name__ == "__main__":
    app.start(3000)  # POST http://localhost:3000/slack/events
