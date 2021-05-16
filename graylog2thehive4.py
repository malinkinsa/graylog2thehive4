import ssl
import sys
import requests
import json
import uuid
import logging
import argparse
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper
from flask import Flask, Response, render_template, request, flash, redirect, url_for

app = Flask(__name__)

arg = argparse.ArgumentParser()
arg.add_argument('--thehive_url', help='Configure TheHive URL | Example http://127.0.0.1:9000')
arg.add_argument('--api_key', help='Configure API Key for organisation user, this user will be the author of all alerts')
arg.add_argument('--graylog_url', help='Configure Graylog URL')

args = vars(arg.parse_args())
thehive_url = args["thehive_url"]
api_key = args["api_key"]
graylog_url = args["graylog_url"]

api = TheHiveApi(thehive_url, api_key)

graylog_url = graylog_url

# Webhook to process Graylog HTTP Notification
@app.route('/webhook', methods=['POST'])
def webhook():

    # Get request JSON contents
    content = request.get_json()

    # Add logging
    logging.basicConfig(filename='/var/log/graylog2thehive4.log', filemode='a', format='%(asctime)s - graylog2thehive - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info(json.dumps(content))

    event = content['event']

    # Fields
    fields = event['fields']

    # Configure Alert tags
    tags = ['Graylog']

    # Configure Alert title
    title = event['message']

    # Configure Alert description
    description = "**Graylog event definition:** "+content['event_definition_title']
    if content['backlog']:
        description = description+'\n\n**Matching messages:**\n\n'
        for message in content['backlog']:
            description = description+"\n\n---\n\n**Graylog URL:** "+graylog_url+"/messages/"+message['index']+"/"+message['id']+"\n\n"
            description = description+'\n\n**Raw Message:** \n\n```\n'+json.dumps(message)+'\n```\n---\n'

    # Configure Alert severity
    severity = event['priority']

    # Extract fields from Graylog event and configure it as an Alert artifact in thehive4 alert
    artifacts = []

    for key in fields.keys():
        if key == 'src_ip':
            artifacts.append(AlertArtifact(dataType='src_ip', data=fields[key]))
        elif key == 'dst_ip':
            artifacts.append(AlertArtifact(dataType='dst_ip', data=fields[key]))
        elif key == 'username':
            artifacts.append(AlertArtifact(dataType='username', data=fields[key]))
        elif key == 'email':
            artifacts.append(AlertArtifact(dataType='email', data=fields[key]))
        elif key == 'hostname':
            artifacts.append(AlertArtifact(dataType='hostname', data=fields[key]))
        elif key == 'timestamp':
            artifacts.append(AlertArtifact(dataType='timestamp', data=fields[key]))
        elif key == 'fqdn':
            artifacts.append(AlertArtifact(dataType='fqdn', data=fields[key]))
        elif key == 'url':
            artifacts.append(AlertArtifact(dataType='url', data=fields[key]))


    # Prepare the Alert
    sourceRef = str(uuid.uuid4())[0:6]
    alert = Alert(title=title,
                  tlp=2,
                  tags=tags,
                  description=description,
                  severity=severity,
                  artifacts=artifacts,
                  type='external',
                  source='Graylog',
                  sourceRef=sourceRef)


    # Create the Alert
    print('Creating alert for: '+title)
    response = api.create_alert(alert)
    if response.status_code == 201:
        logging.info(json.dumps(response.json(), indent=4, sort_keys=True))
        print('Alert created successfully for: '+title)
    else:
        print('Error while creating alert for: '+title)
        sys.exit(0)
    return content['event_definition_title']

if __name__ == '__main__':
    context = ssl.SSLContext()
    context.load_cert_chain('fullchain.pem', 'privkey.pem')
    app.run(host='0.0.0.0', ssl_context=context, debug=False)