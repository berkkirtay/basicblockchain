# Copyright (c) 2022 Berk Kırtay

from cmath import log
import logging
import json
import sys

def initializeLogger():
    logger_level = logging.CRITICAL
    # with open("logger_config.json", 'r') as f:
    #   config = json.load(f)

   # if config["logging"] == 1:
    logger_level = logging.INFO

    logging.basicConfig(filename='blockchain.log',
                        encoding='utf-8',
                        level=logger_level,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')  # %(filename)s:%(lineno)s

   # if config["log_cli"] == 1:
    #    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    logging.info("-------New logging session is initialized-------\n")
