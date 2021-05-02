import os
import random
import requests
import subprocess
from slack_sdk.web import WebClient
import discord as discord

slack_web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

msg = {
    "ts": "",
    "channel": "",
    "username": "snakebot",
    "icon_emoji": ":snake:",
    "text": "Hello, World",
}


def commit(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    try:
        r = requests.get("http://whatthecommit.com/index.txt")
        if r.status_code == requests.codes.ok:
            msg = r.text.strip()
            msg["text"] = f'```$ git commit -am "{msg}" && git push```'
            slack_web_client.chat_postMessage(**msg)
        else:
            msg["text"] = "```HTTP {0}```".format(r.status_code)
            slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def disc(user_id: str, channel: str, said: str):
    global msg
    msg["channel"] = channel
    try:
        said = " ".join(said.split(" ", 1)[1:])
        discord.post_message(said)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def help(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    try:
        with open("/VERSION") as f:
            version = f.readline().strip()
            help = f"""<https://github.com/mamercad/snakebot|*SnakeBot* Version {version}>
> *help*: This message
> *version*: The version
> *weather* [zip]: The weather
> *commit*: Commit message
> *joke*: Tell a joke
> *guid*: Random guid
> *random* [low] [high]: Random number
> *talons*: In memoriam
> *shanti*: You know it
> *shell* https://some.script: Run it
> *discord* message: Send to Discord
        """
        msg["text"] = help
        slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def guid(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    try:
        r = requests.get(
            "http://givemeguid.com",
            headers={"User-agent": "curl/7.64.1"},
        )
        if r.status_code == requests.codes.ok:
            m = r.text.strip()
            msg["text"] = f"```{m}```"
            slack_web_client.chat_postMessage(**msg)
        else:
            msg["text"] = "```HTTP {0}```".format(r.status_code)
            slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def hello(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    try:
        msg["text"] = "Hello, World."
        slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def joke(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    try:
        r = requests.get(
            "https://icanhazdadjoke.com",
            headers={"User-agent": "curl/7.64.1"},
        )
        if r.status_code == requests.codes.ok:
            msg = r.text.strip()
            msg["text"] = f"> {msg}"
            slack_web_client.chat_postMessage(**msg)
        else:
            msg["text"] = "```HTTP {0}```".format(r.status_code)
            slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def parrot(user_id: str, channel: str, said: str):
    global msg
    msg["channel"] = channel
    msg["text"] = "Did you say '{0}'?".format(said)
    slack_web_client.chat_postMessage(**msg)


def rand(user_id: str, channel: str, said: str):
    global msg
    msg["channel"] = channel
    try:
        said = said.split(" ")[1:]
        if len(said) == 0:
            msg["text"] = "```{0}```".format(str(random.randint(1, 100)))
        elif len(said) == 1:
            msg["text"] = "```{0}```".format(
                str(random.randint(1, int(said[0])))
            )  # noqa E501
        elif len(said) >= 2:
            msg["text"] = "```{0}```".format(
                str(random.randint(int(said[0]), int(said[1])))
            )
        slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def shanti(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    try:
        sayings = [
            "WB: Wrong Bread",
            "The so-called `grep`",
            "I brought all the books but not our textbook",
            "Abe Lincoln",
        ]
        pick = sayings[random.randint(0, len(sayings) - 1)]
        msg["text"] = f"> {pick}"
        slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def shell(user_id: str, channel: str, said: str):
    global msg
    msg["channel"] = channel
    try:
        said = " ".join(said.split(" ")[1:])
        parts = said.encode("ascii", "ignore").decode().strip()
        parts = parts.replace("dot", ".")
        parts = parts.replace("slash", "/")
        parts = parts.replace("colon", ":")
        parts = parts.replace(" ", "")
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
                msg["text"] = f"```{p.stdout}```"
                slack_web_client.chat_postMessage(**msg)
            if p.stderr:
                msg["text"] = f"```(stderr)\n{p.stderr}```"
                slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)


def talons(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    msg["text"] = "> Wings of the Raptor :eagle:"
    slack_web_client.chat_postMessage(**msg)


def yo(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    msg["text"] = "Yo!"
    slack_web_client.chat_postMessage(**msg)


def version(user_id: str, channel: str):
    global msg
    msg["channel"] = channel
    with open("/VERSION") as f:
        version = f.readline().strip()
    msg["text"] = f"```Version: {version}```"
    slack_web_client.chat_postMessage(**msg)


def weather(user_id: str, channel: str, said: str):
    global msg
    msg["channel"] = channel
    try:
        said = " ".join(said.split(" ", 1)[1:])
        if len(said):
            r = requests.get("http://wttr.in/{0}?format=3".format(said))
        else:
            r = requests.get("http://wttr.in/48439?format=3")
        if r.status_code == requests.codes.ok:
            msg["text"] = f"> {r.text}"
            slack_web_client.chat_postMessage(**msg)
        else:
            msg["text"] = "```HTTP {0}```".format(r.status_code)
            slack_web_client.chat_postMessage(**msg)
    except Exception as e:
        msg["text"] = "```Exception: {0}```".format(str(e))
        slack_web_client.chat_postMessage(**msg)
