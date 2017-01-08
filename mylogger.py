# -*- coding:utf-8 -*-

import logging.config
import os

try:
    from cloghandler import ConcurrentRotatingFileHandler as RFHandler
except ImportError:
    from warnings import warn
    warn("ConcurrentLogHandler package not installed.  Using builtin log handler")
    from logging.handlers import RotatingFileHandler as RFHandler

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s - %(levelname)s] - %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'clogger': {
            'handlers': ['console',],
            'level': 'DEBUG',
        }
    }
}

LOG_PATH = "E:/logs"

class mylogger(object):
    
    @staticmethod
    def get_instance(tag="test"):
        logging.config.dictConfig(LOGGING)
        logger = logging.getLogger("clogger")
        
        if not os.path.exists(os.path.join(LOG_PATH)):
            os.makedirs(os.path.join(LOG_PATH))
        
        logfile = os.path.join(LOG_PATH) + '%s.log' % tag
        
        fh = RFHandler(logfile, maxBytes=1024 * 1024 * 100, backupCount=10, delay=0.05)
        formatter = logging.Formatter('[%(asctime)s - %(levelno)s] - %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        
        logger.addHandler(fh)
        
#         error_logfile = os.path.join(LOG_PATH) + '%s_error.log' % tag
#         efh = RFHandler(error_logfile, maxBytes=1024 * 1024 * 100, backupCount=10, delay=0.05)
#         efh.setFormatter(formatter)
#         efh.setLevel(logging.ERROR)
#         logger.addHandler(efh)
        
        return logger
    