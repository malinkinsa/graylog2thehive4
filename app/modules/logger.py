import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('internal_logging')
        self.logger.setLevel(logging.INFO)
        log_format = logging.Formatter('%(asctime)s - %(message)s')
        handler = logging.FileHandler(filename='./log/graylog2thehive4.log', mode='a')
        handler.setFormatter(log_format)
        self.logger.addHandler(handler)

    def logging(self, logging_message, *args):
        message = logging_message
        self.logger.info(message, *args)
