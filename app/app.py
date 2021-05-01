import re
import os
import random
import logging
import subprocess
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


def help(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Hello, World",
    }
    with open("/VERSION") as f:
        version = f.readline().strip()
        help = """>*help*: This message
> *version*: The version
> *weather* [zip]: The weather
> *commit*: Commit message
> *joke*: Tell a joke
> *guid*: Random guid
> *random* [low] [high]: Random number
> *talons*: In memoriam
> *shanti*: You know it
> *shell* https://some.script: Run it
        """
        message["text"] = help
    response = slack_web_client.chat_postMessage(**message)
    bot.timestamp = response["ts"]


@slack_events_adapter.on("hello")
def version(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Hello, World",
    }
    with open("/VERSION") as f:
        version = f.readline().strip()
        message["text"] = f"```Version: {version}```"
    response = slack_web_client.chat_postMessage(**message)
    bot.timestamp = response["ts"]


def talons(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Hello, World",
    }
    message["text"] = f"> Wings of the Raptor"
    response = slack_web_client.chat_postMessage(**message)
    bot.timestamp = response["ts"]


def shanti(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Hello, World",
    }
    sayings = [
        "WB: Wrong Bread",
        "The so-called `grep`",
        "I brought all the books but not our textbook",
        "Abe Lincoln",
    ]
    pick = sayings[random.randint(0, len(sayings) - 1)]
    message["text"] = f"> {pick}"
    response = slack_web_client.chat_postMessage(**message)
    bot.timestamp = response["ts"]


def parrot(user_id: str, channel: str, said: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Hello, World",
    }
    message["text"] = "Did you say '{0}'?".format(said)
    response = slack_web_client.chat_postMessage(**message)
    bot.timestamp = response["ts"]


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


def commit(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Yo!",
    }

    try:
        r = requests.get("http://whatthecommit.com/index.txt")
        if r.status_code == requests.codes.ok:
            msg = r.text.strip()
            message["text"] = f'```$ git commit -am "{msg}" && git push```'
            response = slack_web_client.chat_postMessage(**message)
        else:
            message["text"] = "```HTTP {0}```".format(r.status_code)
            response = slack_web_client.chat_postMessage(**message)
    except Exception as e:
        message["text"] = "```Exception: {0}```".format(str(e))
        response = slack_web_client.chat_postMessage(**message)

    bot.timestamp = response["ts"]


def shell(user_id: str, channel: str, said: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Yo!",
    }

    try:
        said = " ".join(said.split(" ")[1:])
        # message["text"] = f"Debug:\n```{said}```"
        # response = slack_web_client.chat_postMessage(**message)

        parts = said.encode("ascii", "ignore").decode().strip()
        parts = parts.replace("dot", ".")
        parts = parts.replace("slash", "/")
        parts = parts.replace("colon", ":")
        parts = parts.replace(" ", "")

        # message["text"] = f"Debug:\n```{parts}```"
        # response = slack_web_client.chat_postMessage(**message)

        r = requests.get(parts)
        if r.status_code == requests.codes.ok:
            with open("/tmp/shell.sh", "w") as f:
                f.write(r.text)
            p = subprocess.run(
                ["/bin/bash", "/tmp/shell.sh"],
                capture_output=True,
                text=True,
                check=True,
            )
            if p.stdout:
                print(p.stdout)
                message["text"] = f"```{p.stdout}```"
                response = slack_web_client.chat_postMessage(**message)
            if p.stderr:
                print(p.stderr)
                message["text"] = f"```(stderr)\n{p.stderr}```"
                response = slack_web_client.chat_postMessage(**message)
    except Exception as e:
        message["text"] = "```Exception: {0}```".format(str(e))
        response = slack_web_client.chat_postMessage(**message)

    bot.timestamp = response["ts"]


def joke(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Yo!",
    }

    try:
        r = requests.get(
            "https://icanhazdadjoke.com", headers={"User-agent": "curl/7.64.1"}
        )
        if r.status_code == requests.codes.ok:
            msg = r.text.strip()
            message["text"] = f"> {msg}"
            response = slack_web_client.chat_postMessage(**message)
        else:
            message["text"] = "```HTTP {0}```".format(r.status_code)
            response = slack_web_client.chat_postMessage(**message)
    except Exception as e:
        message["text"] = "```Exception: {0}```".format(str(e))
        response = slack_web_client.chat_postMessage(**message)

    bot.timestamp = response["ts"]


def guid(user_id: str, channel: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Yo!",
    }

    try:
        r = requests.get("http://givemeguid.com", headers={"User-agent": "curl/7.64.1"})
        if r.status_code == requests.codes.ok:
            msg = r.text.strip()
            message["text"] = f"```{msg}```"
            response = slack_web_client.chat_postMessage(**message)
        else:
            message["text"] = "```HTTP {0}```".format(r.status_code)
            response = slack_web_client.chat_postMessage(**message)
    except Exception as e:
        message["text"] = "```Exception: {0}```".format(str(e))
        response = slack_web_client.chat_postMessage(**message)

    bot.timestamp = response["ts"]


def rand(user_id: str, channel: str, said: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Yo!",
    }

    try:
        said = said.split(" ")[1:]
        # message["text"] = "```Debug: {0}```".format(str(said))
        # response = slack_web_client.chat_postMessage(**message)
        if len(said) == 0:
            message["text"] = "```{0}```".format(str(random.randint(1, 100)))
        elif len(said) == 1:
            message["text"] = "```{0}```".format(str(random.randint(1, int(said[0]))))
        elif len(said) >= 2:
            message["text"] = "```{0}```".format(
                str(random.randint(int(said[0]), int(said[1])))
            )
        response = slack_web_client.chat_postMessage(**message)
    except Exception as e:
        message["text"] = "```Exception: {0}```".format(str(e))
        response = slack_web_client.chat_postMessage(**message)

    bot.timestamp = response["ts"]


def weather(user_id: str, channel: str, said: str):
    bot = SnakeBot(channel)
    message = bot.get_message_payload()
    message = {
        "ts": bot.timestamp,
        "channel": bot.channel,
        "username": bot.username,
        "icon_emoji": bot.icon_emoji,
        "text": "Hello, World",
    }

    try:
        said = " ".join(said.split(" ", 1)[1:])
        # message["text"] = "```Debug: {0}```".format(said)
        # response = slack_web_client.chat_postMessage(**message)
        if len(said):
            r = requests.get("http://wttr.in/{0}?format=3".format(said))
        else:
            r = requests.get("http://wttr.in/48439?format=3")
        if r.status_code == requests.codes.ok:
            message["text"] = f"> {r.text}"
            response = slack_web_client.chat_postMessage(**message)
        else:
            message["text"] = "```HTTP {0}```".format(r.status_code)
            response = slack_web_client.chat_postMessage(**message)
    except Exception as e:
        message["text"] = "```Exception: {0}```".format(str(e))
        response = slack_web_client.chat_postMessage(**message)

    bot.timestamp = response["ts"]


@slack_events_adapter.on("message")
# @slack_events_adapter.on("message.app_home")
def message(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "hello":
        return hello(user_id, channel_id)

    if text and text.lower() == "yo":
        return yo(user_id, channel_id)

    if text and text.startswith("weather"):
        return weather(user_id, channel_id, text)

    if text and text.lower() == "version":
        return version(user_id, channel_id)

    if text and text.startswith("parrot "):
        return parrot(user_id, channel_id, text)

    if text and text.startswith("random"):
        return rand(user_id, channel_id, text)

    if text and text.lower() == "commit":
        return commit(user_id, channel_id)

    if text and text.lower() == "joke":
        return joke(user_id, channel_id)

    if text and text.lower() == "guid":
        return guid(user_id, channel_id)

    if text and text.lower() == "help":
        return help(user_id, channel_id)

    if text and text.lower() == "talons":
        return talons(user_id, channel_id)

    if text and text.lower() == "shanti":
        return shanti(user_id, channel_id)

    if text and text.startswith("shell "):
        return shell(user_id, channel_id, text)


@app.route("/ping")
def ping():
    return "pong"


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host="0.0.0.0", port=3000, debug=True)
