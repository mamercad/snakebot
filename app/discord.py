#!/usr/bin/env python3

import os
import requests

discord_info = {
    "webhook": os.environ.get("DISCORD_WEBHOOK"),
    "username": "SnakeBot",
    "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/768px-Python-logo-notext.svg.png",  # noqa E501
}

headers = {
    "Content-type": "application/json",
}

payload = {
    "username": discord_info["username"],
    "avatar_url": discord_info["avatar_url"],
    "content": "",
    "embeds": [],
}


def post_message(msg: str):
    global discord_info, headers, payload
    try:
        payload["content"] = msg
        r = requests.post(
            discord_info["webhook"], headers=headers, json=payload
        )  # noqa E501
        if r.status_code == requests.codes.ok:
            pass
        else:
            pass
    except Exception:
        # raise e
        pass
