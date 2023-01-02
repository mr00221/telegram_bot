FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD telegram_bot.py /

CMD [ "python3", "./telegram_bot.py"]