# FROM python:3
FROM alpine:latest

RUN apk update
RUN apk add --no-cache python3 python3-dev py3-pip bash curl

COPY VERSION /
COPY SUMMARY /
COPY app.py /
COPY fx.py /
COPY snakebot.py /
COPY discord.py /

COPY requirements.txt /
RUN pip3 install -r requirements.txt

EXPOSE 3000/tcp

CMD ["python3", "app.py"]
