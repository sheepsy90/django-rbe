import logging


def create_logger(file_path, logger_name=None, logger_level=20):
    """ Creates a logger for the current instance """

    if logger_name is None:
        logger_name = file_path

    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        logger.setLevel(logger_level)

        # Create file handler and set level to info ('normal' output)
        # Logs all messages to file
        file_log = logging.FileHandler(file_path, mode='a')
        file_log.setLevel(logger_level)

        # Add formatter
        file_log_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_log.setFormatter(file_log_format)

        # Add handlers to logger
        logger.addHandler(file_log)

    return logger

rbe_logger = create_logger('rbe_network.log')