# Graylog2TheHive4

Simple app to create TheHive4 alerts from Graylog

# Environment

This app has been tested with the following versions:
- CentOS 7.9.2009 (Core)
- Graylog 4.0.6
- TheHive4 4.0.4-1

This app should be installed on the host where TheHive4 is installed.
# Setup
## Setup Graylog2TheHive4 application:

- Clone repo:

```
git clone git@github.com:malinkinsa/graylog2thehive4.git /opt/graylog2thehive4
```

- Install python requirements:

```
cd /opt/graylog2thehive4
pip3 install -r requirements.txt
```

- Copy init.d file:

```
cp init.d/graylog2thehive4.service /etc/systemd/system/
```

- Configure TheHive4 URL, API key and Graylog url in graylog2thehive4.service:

```
vim /etc/systemd/system/graylog2thehive4.service
systemctl daemon-reload
```

- Configure SSL, IP, PORT for application in graylog2thehive4.py:

```
    context = ssl.SSLContext()
    context.load_cert_chain('fullchain.pem', 'privkey.pem')
    app.run(host='0.0.0.0', ssl_context=context
    debug=False)
```

- Configure application log rotation:

```
cp logrotate.d/graylog2thehive /etc/logrotate.d/
```

- Launch application and add to autostart:

```
systemctl start graylog2thehive4.service
systemctl enable graylog2thehive4.service
```

## Setup Graylog Notification

Create new `Notification` with  in `Alerts -> Notifications`:

- Specify: `Title`;
- Notification Type: `HTTP Notification`;
- URL: `http{s}://TheHive4:Port/webhook`; For example: `http://192.168.0.1:5000/webhook`
- Add this URL to Graylog whitelist or disable whitelist in `System -> Configurations`;

## Adding artifacts to TheHive4 alert

- In TheHive4 | Add dataType: `Admin -> Observable types` | For example: *`src_ip`*
- In Graylog | Add fields in `Event Definitions -> Fields -> Add Custom Field` | For example: Name of this field is *`src_ip`*
- Add this dataType in `graylog2thehive4.py` | For example:

```
if key == 'src_ip':
            artifacts.append(AlertArtifact(dataType='src_ip', data=fields[key]))
```

# To-Do

- [] Create docker container;

# Credits

Based on [graylog2thehive4](https://github.com/H2Cyber/Graylog2TheHive4) 