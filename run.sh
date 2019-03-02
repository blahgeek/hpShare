#!/bin/sh

run_purge_storage () {
    sleep 3600
    while true; do
        echo "Purging storage..."
        python manage.py purge_storage &
        sleep 3600
    done
}

python manage.py collectstatic --noinput
python manage.py syncdb --noinput

run_purge_storage &

uwsgi --module=hpurl.wsgi:application --master --socket=0.0.0.0:8000 --processes=2
