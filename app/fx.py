import os
from slack_sdk.web import WebClient

slack_web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

msg = {
    "ts": "",
    "channel": "",
    "username": "snakebot",
    "icon_emoji": ":snake:",
    "text": "Hello, World",
}


def version(user_id: str, channel: str):
    msg["channel"] = channel

    with open("/VERSION") as f:
        version = f.readline().strip()
    msg["text"] = f"```Version: {version}```"

    slack_web_client.chat_postMessage(**msg)
