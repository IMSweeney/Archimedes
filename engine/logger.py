import logging


class Logger():
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt='%(asctime)s %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        self.logger.addHandler(stream)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    _logger = Logger(__name__)
