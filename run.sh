#!/bin/sh

run_purge_storage () {
    sleep 3600
    while true; do
        echo "Purging storage..."
        python manage.py purge_storage &
        sleep 3600
    done
}

cp /data/config.py ./
python manage.py collectstatic --noinput
python manage.py syncdb --noinput
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.create_superuser(os.environ['ADMIN_USER'], os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWD'])
EOF

unset ADMIN_USER
unset ADMIN_EMAIL
unset ADMIN_PASSWD

run_purge_storage &

nginx
uwsgi --module=hpurl.wsgi:application --master --socket=0.0.0.0:8000 --processes=2
