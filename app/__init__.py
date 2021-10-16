from fastapi import FastAPI


webhook = FastAPI()

try:
    from app.modules.logger import Logger
    logger = Logger()

    from app.modules.thehive4 import TheHive4
    thehive4 = TheHive4()

except Exception as exc:
    print('Error loading module: {}'.format(exc))
