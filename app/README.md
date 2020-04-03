# Nuxt MailAPI frontend


## Build Setup

```bash
# install dependencies
npm install

# serve with hot reload at localhost:3000
npm run dev

# build for production and launch server
npm run build
npm run start

# generate static project
npm run generate
```


## Systemd Setup

Create `/etc/systemd/system/mailapp.service` with following content

```
[Unit]
Description=Nuxtjs instance to serve mailapp
After=network.target

[Service]
User=<user>
WorkingDirectory=/home/<user>/git/mail_api/app
ExecStart=/usr/bin/node /home/<user>/git/mail_api/app/node_modules/.bin/nuxt start --port 3000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
