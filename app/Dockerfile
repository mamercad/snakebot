FROM python:3

COPY VERSION /
COPY app.py /
COPY snakebot.py /

COPY requirements.txt /
# RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 3000/tcp

CMD ["python3", "app.py"]
