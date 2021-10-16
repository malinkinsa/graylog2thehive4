from app import webhook, thehive4, logger
from app.models import GraylogEventDefinition


@webhook.api_route("/webhook", methods=['POST'])
async def read_webhook(eventdefinition: GraylogEventDefinition):

    logger.logging(eventdefinition)
    await thehive4.create_alert(eventdefinition)
