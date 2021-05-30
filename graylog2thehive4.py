import os
import sys
import json
import uuid
import logging
import argparse
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact
from flask import Flask, request

app = Flask(__name__)

arg = argparse.ArgumentParser()
arg.add_argument('--thehive_url', help='Configure TheHive URL | Example http://127.0.0.1:9000', required=True)
arg.add_argument('--api_key', help='Configure API Key for organisation user, this user will be the author of all alerts', required=True)
arg.add_argument('--graylog_url', help='Configure Graylog URL', required=True)
arg.add_argument('--ip', help='Configure ip where application will be launch', required=True)
arg.add_argument('--port', help='Configure port where application will be launch', default=5000)

args = vars(arg.parse_args())
thehive_url = args["thehive_url"]
api_key = args["api_key"]
graylog_url = args["graylog_url"]
ip = args["ip"]
port = args["port"]

api = TheHiveApi(thehive_url, api_key)

graylog_url = graylog_url

# Webhook to process Graylog HTTP Notification
@app.route('/webhook', methods=['POST'])
def webhook():

    # Get request JSON contents
    content = request.get_json()

    # Add logging
    log_dir = './log/'
    os.mkdir(log_dir)
    logging.basicConfig(filename='./log/graylog2thehive4.log', filemode='a', format='%(asctime)s - graylog2thehive - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info(json.dumps(content, indent=4, sort_keys=True))

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
            artifacts.append(AlertArtifact(dataType='ip', tags=['src_ip'], data=fields[key]))
        elif key == 'dst_ip':
            artifacts.append(AlertArtifact(dataType='ip', tags=['dst_ip'], data=fields[key]))
        elif key == 'ip':
            artifacts.append(AlertArtifact(dataType='ip', data=fields[key]))
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
        else:
            key == fields[key]
            artifacts.append(AlertArtifact(dataType='other', data=fields[key]))


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
    app.run(host=ip, port=port, debug=False)