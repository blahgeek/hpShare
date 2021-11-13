FROM python:2.7

RUN apt-get update && apt-get install -y --no-install-recommends nginx

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app
RUN cp /app/nginx.conf /etc/nginx/sites-available/default

ENV DJANGO_SECRET_KEY changeme
ENV DJANGO_ALLOWED_HOST "*"

ENV DB_PATH /data/db.sqlite3
ENV ADMIN_USER root
ENV ADMIN_EMAIL root@localhost
ENV ADMIN_PASSWD password

RUN mkdir /data
CMD ./run.sh

EXPOSE 80
