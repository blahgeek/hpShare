FROM python:2.7

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV SECRET_KEY changeme
ENV DB_FILE /app/db.sqlite3

CMD ./run.sh

EXPOSE 8000
