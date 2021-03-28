FROM python:3.9.2-slim-buster

WORKDIR /app

COPY subscriber_median.py subscriber_median.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD [ "python", "-u", "subscriber_median.py" ]