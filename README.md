# Deprecated. New version available [here](https://github.com/malinkinsa/graylog-alert-gateway).

# Graylog2TheHive4

Simple app to create TheHive4 alerts from Graylog Event event definition.

## Environment

This app has been tested with the following versions:
- CentOS 7.9.2009 (Core)
- Graylog 4.1.6
- TheHive4 4.1

This app should be installed on the host where TheHive4 is installed.
## Setup
## Setup Graylog2TheHive4 application

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

- Configure `TheHive4 URL as url`, `TheHive4 API key as api_key`, `Ip where application will be work` and `Port where application will be work (optional)` in graylog2thehive4.service:

```
vim /etc/systemd/system/graylog2thehive4.service
systemctl daemon-reload
```

- Launch application as a service and add to autostart:

```
systemctl start graylog2thehive4.service
systemctl enable graylog2thehive4.service
```

- Launch application from command line with specified `TheHive4 URL`, `API key`, `Ip where application will be work` and `Port where application will be work (optional)`:

```
cd /opt/graylog2thehive4/
python3 main.py --thehive_url= --api_key= --graylog_url= --ip= --port=
```

## Setup Graylog Notification

Create new `Notification` with  in `Alerts -> Notifications`:

- Specify: `Title`;
- Notification Type: `HTTP Notification`;
- URL: `http{s}://TheHive4:Port/webhook`; For example: `http://192.168.0.1:5000/webhook`
- Add this URL to Graylog whitelist or disable whitelist in `System -> Configurations`;

## Adding artifacts to TheHive4 alert

- In Graylog | Add fields in `Event Definitions -> Fields -> Add Custom Field` | For example: Name of this field is *`ip`*
- Add this dataType in `thehive4.py` | For example:

```
if key == 'ip':
            alert_artifacts.append({"dataType": "ip", "data": graylog_fields[key]})
```

## Logging

For debug you can use log with message from graylog and message that sending to thehive4. It located in `./log/graylog2thehive4.log`