FROM python:2.7

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV SECRET_KEY changeme
ENV DB_FILE /app/db.sqlite3

CMD uwsgi --module=hpurl.wsgi:application --master --socket=0.0.0.0:8000 --processes=2

EXPOSE 8000
