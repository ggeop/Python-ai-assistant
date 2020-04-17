# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import time
from logging import config

from jarvis.core.processor import Processor
from jarvis import settings
from jarvis.settings import ROOT_LOG_CONF
from jarvis.utils.console import stdout_print, clear, OutputStyler, jarvis_logo, start_text
from jarvis.utils.mongoDB import db
from jarvis.utils.startup import internet_connectivity_check, configure_MongoDB

# Create a Console & Rotating file logger
config.dictConfig(ROOT_LOG_CONF)


def main():
    """
    Do initial checks, clear the console and print the assistant logo.

    STEP 1: Clear log file in each assistant fresh start
    STEP 2: Checks for internet connectivity
    STEP 3: Configuare MongoDB, load skills and settings
    STEP 4: Clear console
    """

    # STEP 1
    with open(ROOT_LOG_CONF['handlers']['file']['filename'], 'r+') as f:
        f.truncate(0)

    logging.info('=' * 48)
    logging.info('Startup ckeck')
    logging.info('=' * 48)

    # STEP 2
    if not internet_connectivity_check():
        logging.warning('Skills with internet connection will not work :-(')
        time.sleep(3)

    # STEP 3
    configure_MongoDB(db, settings)

    logging.info('APPLICATION STARTS..')

    # STEP 4
    clear()
    print(OutputStyler.CYAN + jarvis_logo + OutputStyler.ENDC)
    print(OutputStyler.HEADER + start_text + OutputStyler.ENDC)
    processor = Processor(settings, db)

    while True:
        processor.run()


if __name__ == '__main__':
    main()

