# Python Flask Mail API

This tool comes handy when you want to deploy mail API.


![Exapmle contact form](https://raw.githubusercontent.com/p3t3r67x0/mail_api/master/img/contact_form_example.png)


## Example

```bash
curl -X POST https://example.com/api/v1/mail -d '{"first_name":"Jane","last_name":"Doe","message":"Hey how are you doing?","email":"me@example.com"}' -H "Content-Type: application/json"
```


## Prerequisites

Create a `.config` file in the `/api` folder

```config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = 'super_secure_password'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'me@example.com'
```


## Build Setup

```bash
# install build dependencies
sudo apt install virtualenv python3.7 python3.7-dev

# create a virtualenv
virtualenv -p /usr/bin/python3.7 venv

# activate virtualenv
. venv/bin/activate

# install dependencies
pip3 install -r requirements.txt

# serve at 127.0.0.1:5000
gunicorn --bind 127.0.0.1:5000 wsgi:app --access-logfile - --error-logfile - --log-level info
```


## Systemd Setup

Create a file `/etc/systemd/system/mailapi.service` with following content

```bash
[Unit]
Description=Gunicorn instance to serve mailapi
After=network.target

[Service]
User=<user>
Group=www-data
WorkingDirectory=/home/<user>/git/mail_api/api
Environment="PATH=/home/<user>/git/mail_api/venv/bin"
ExecStart=/home/<user>/git/mail_api/venv/bin/gunicorn --bind 127.0.0.1:5000 wsgi:app --workers 4 --threads 2 --access-logfile /var/log/mailapi/access.log --error-logfile /var/log/mailapi/error.log --log-level INFO
Restart=on-failure
RestartSec=2s

[Install]
WantedBy=multi-user.target
```


Start the service and enable the service

```bash
sudo systemctl start mailapi
sudo systemctl enable mailapi
```


## Setup Nginx with SSL

Install dependencies from Ubuntu repository

```bash
sudo apt install nginx-full certbot python-certbot-nginx
```


Setup nginx config file in `/etc/nginx/sites-enabled/api_example_com`

```cfg
server {
    server_name api.example.com;

    location / {
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' 'https://example.com' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;

            # Custom headers and headers various browsers *should* be OK with but aren't
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;

            # Tell client that this pre-flight info is valid for 20 days
            add_header 'Access-Control-Max-Age' 1728000 always;
            add_header 'Content-Type' 'text/plain; charset=utf-8' always;
            add_header 'Content-Length' 0 always;
            return 204;
        }

        if ($request_method = 'POST') {
            add_header 'Access-Control-Allow-Origin' 'https://example.com' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        }

        if ($request_method = 'GET') {
            add_header 'Access-Control-Allow-Origin' 'https://example.com' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        }

        if ($request_method = 'PUT') {
            add_header 'Access-Control-Allow-Origin' 'https://example.com' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        }

        if ($request_method = 'DELETE') {
            add_header 'Access-Control-Allow-Origin' 'https://example.com' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        }

        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Port $server_port;
    }
}
```
