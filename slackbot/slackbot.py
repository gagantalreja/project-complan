import base64
import requests
import json
import os
from urllib.parse import parse_qsl

from dotenv import load_dotenv
from auth import authorize

load_dotenv()


def send_on_slack(message, channel_id):
    slack_token = os.getenv("SLACK_TOKEN")
    block = [{"type": "section", "text": {"type": "mrkdwn", "text": message}}]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {slack_token}"
    }

    data = {
        "channel": channel_id,
        "blocks": block
    }
    result = requests.post(
        "https://slack.com/api/chat.postMessage", headers=headers, json=data)
    print(result.json())


def lambda_handler(event, context):
    print(event)
    slack_signature = event["headers"]["x-slack-signature"]
    slack_time = event["headers"]["x-slack-request-timestamp"]

    # decoding body from base64
    b64_decoded = event.get("body")
    if event["isBase64Encoded"]:
        b64_decoded = base64.b64decode(b64_decoded).decode("utf-8")

    # parsing query string to dict
    params = json.loads(b64_decoded)
    print(params)

    # authenticating
    if not authorize(b64_decoded, slack_time, slack_signature):
        return {"code": 403, "body": "Request to infrabot is unauthorized!"}

    print("Request Authorized..")
    if params["type"] == "url_verification":
        return params.get("challenge")

    if params["event"]["type"] == "app_home_opened":
        text = f"Hey <@{params['event']['user']}>"
        channel_id = params["event"]["channel"]
        send_on_slack(text, channel_id)
    
    if params["event"]["type"] == "app_mention":
        text = f"Hey <@{params['event']['user']}>, How can i help you today?"
        channel_id = params["event"]["channel"]
        send_on_slack(text, channel_id)
    
    return True
