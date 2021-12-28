import logging

def setup_logger(logger, logfile, log_level):
  logger.setLevel(log_level)
  file_handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='a')
  file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
  logger.addHandler(file_handler)
  return logger

def setup_discord_logger(logfile):
  return setup_logger(logging.getLogger('discord'), logfile, logging.INFO)

