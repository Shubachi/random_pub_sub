FROM python:3.9.2-slim-buster

WORKDIR /app

COPY subscriber_sum.py subscriber_sum.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD [ "python", "-u", "subscriber_sum.py" ]