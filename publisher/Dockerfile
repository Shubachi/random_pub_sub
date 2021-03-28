FROM python:3.9.2-slim-buster

WORKDIR /app

COPY publisher.py publisher.py 
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD [ "python", "-u", "publisher.py" ]