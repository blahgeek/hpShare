# hpShare

`hpShare` is a **self-hosted** [CloudApp](http://getcloudapp.com)-like, [Droplr](http://droplr.com)-like server especially for **Chinese** users. It uses **[QiNiu](http://qiniu.com)** as storage backend instead of [Amazon S3](http://http://s3.amazonaws.com) which is slow and may be blocked someday in China.

`hpShare` is now also an URL shortener. It's a good start for your personal short domain.

`hpShare` comes with an admin portal (provided by `Django`) and several client apps (CLI, DropZone script, etc.)

`hpShare` is written in [Django](http://http://djangoproject.com).

## Demos & Screenshots & GIFs

[z1k.co/F5j7](http://z1k.co/F5j7)

[z1k.co/F5O8](http://z1k.co/F5O8)

[z1k.co/blog](http://z1k.co/blog)

![Demo](screenshots/demo.gif)

![admin](screenshots/admin.png)

## How-To

- Prepare a python2 environment, `pip install -r requirements.txt`
- Get a [QiNiu](http://qiniu.com) (free) account
- `mv config.py.sample config.py`, fill it up
- Modify `hpurl/settings.py` as you need
- Prepare Django project by running `./manage.py syncdb`, `./manage.py collectstatic`
- Run it! `uwsgi --module=hpurl.wsgi:application --master --socket=uwsgi.sock --processes=4 --daemonize=uwsgi.log`
- Modify `nginx.conf` (change `server_name` etc) and run!

## Clients

- CLI: `wget http://your.domain.com/~cli/hpshare`, alternatively see `clients/bash/hpshare.bash`
- DropZone script: see `clients/hpShare.dzbundle`, double-click it to install (you need to install `DropZone` first)

## Admin

Goto `http://your.domain.com/`

Run `./manage.py purge_storage` to delete expired files. Add it to a cron job!

