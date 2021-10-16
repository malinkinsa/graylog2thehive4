import httpx
import json
import uuid

from main import url, api_key
from app import logger


class TheHive4:
    def __init__(self):
        self.url = f'{url}/api/alert'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

    async def create_alert(self, eventdefinition):

        alert_artifacts = []
        graylog_fields = eventdefinition.event.fields

        for key in graylog_fields.keys():
            if key == 'ip':
                alert_artifacts.append({"dataType": "ip", "data": graylog_fields[key]})
            elif key == 'mail':
                alert_artifacts.append({"dataType": "mail", "data": graylog_fields[key]})
            elif key == 'fqdn':
                alert_artifacts.append({"dataType": "fqdn", "data": graylog_fields[key]})
            elif key == 'url':
                alert_artifacts.append({"dataType": "url", "data": graylog_fields[key]})
            else:
                alert_artifacts.append({"dataType": "other", "data": graylog_fields[key]})

        alert = {
            'title': eventdefinition.event_definition_title,
            'description': eventdefinition.event_definition_description,
            'type': 'external',
            'source': 'Graylog',
            'sourceRef': str(uuid.uuid4())[0:6],
            'severity': eventdefinition.event.priority,
            'artifacts': alert_artifacts,
        }

        async with httpx.AsyncClient() as client:
            request = await client.post(self.url, data=json.dumps(alert), headers=self.headers)

        logger.logging(request.text)
