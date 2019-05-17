import logging
import logging.config

logging.config.fileConfig(fname='file.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)
