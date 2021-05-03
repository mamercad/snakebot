#!/usr/bin/env python3

import os
import logging
from flask import Flask
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter
import fx as fx

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(
    os.environ.get("SLACK_SIGNING_SECRET"), "/slack/events", app
)

slack_web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    channel = event.get("channel")
    user = event.get("user")
    text = event.get("text")

    if text and text.lower() == "hello":
        return fx.hello(user, channel)

    if text and text.lower() == "yo":
        return fx.yo(user, channel)

    if text and text.startswith("weather"):
        return fx.weather(user, channel, text)

    if text and text.lower() == "version":
        return fx.version(user, channel)

    if text and text.startswith("parrot "):
        return fx.parrot(user, channel, text)

    if text and text.startswith("random"):
        return fx.rand(user, channel, text)

    if text and text.lower() == "commit":
        return fx.commit(user, channel)

    if text and text.lower() == "joke":
        return fx.joke(user, channel)

    if text and text.lower() == "guid":
        return fx.guid(user, channel)

    if text and text.lower() == "help":
        return fx.help(user, channel)

    if text and text.lower() == "talons":
        return fx.talons(user, channel)

    if text and text.lower() == "shanti":
        return fx.shanti(user, channel)

    if text and text.startswith("shell "):
        return fx.shell(user, channel, text)

    if text and text.startswith("discord "):
        return fx.disc(user, channel, text)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/discord")
def discord():
    fx.discord.post_message("Hello, World.")
    return "boom"


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host="0.0.0.0", port=3000, debug=True)
