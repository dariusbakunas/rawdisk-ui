import logging.config
import os


def setup_logging(log_level=logging.INFO, formatter='standard'):
    """Setup logging configuration
    """

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format':
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': formatter,
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': log_level,
                'propagate': True
            },
        }
    }

    logging.config.dictConfig(config)
