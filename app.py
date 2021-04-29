import os
import logging
from flask import Flask
import requests
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter
from snakebot import SnakeBot

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ.get("SLACK_SIGNING_SECRET"), "/slack/events", app
)
slack_web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def hello(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Hello, World",
    }
    response = slack_web_client.chat_postMessage(**message)
    bot.timestamp = response["ts"]


def yo(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Yo!",
    }
    response = slack_web_client.chat_postMessage(**message)
    bot.timestamp = response["ts"]


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "hello":
        return hello(user_id, channel_id)

    if text and text.lower() == "yo":
        return yo(user_id, channel_id)


@app.route('/ping')
def ping():
    return "pong"


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0', port=3000, debug=True)
