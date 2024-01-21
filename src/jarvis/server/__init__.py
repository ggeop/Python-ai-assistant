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

from logging import config

import server.settings
from server.settings import ROOT_LOG_CONF
from server.utils.mongoDB import db
from server.utils.startup import configure_MongoDB

# ----------------------------------------------------------------------------------------------------------------------
# Create a Console & Rotating file logger
# ----------------------------------------------------------------------------------------------------------------------
config.dictConfig(ROOT_LOG_CONF)

# ----------------------------------------------------------------------------------------------------------------------
# Clear log file in each assistant fresh start
# ----------------------------------------------------------------------------------------------------------------------
with open(ROOT_LOG_CONF['handlers']['file']['filename'], 'w') as f:
    f.close()

# ----------------------------------------------------------------------------------------------------------------------
# Configuare MongoDB, load skills and settings
# ----------------------------------------------------------------------------------------------------------------------
configure_MongoDB(db, settings)

# ----------------------------------------------------------------------------------------------------------------------
# Get assistant settings
# ----------------------------------------------------------------------------------------------------------------------
input_mode = db.get_documents(collection='general_settings')[0]['input_mode']
response_in_speech = db.get_documents(collection='general_settings')[0]['response_in_speech']
assistant_name = db.get_documents(collection='general_settings')[0]['assistant_name']

# ----------------------------------------------------------------------------------------------------------------------
# Create assistant input and output engine instances
# ----------------------------------------------------------------------------------------------------------------------
#input_engine = engines.STTEngine() if input_mode == InputMode.VOICE.value else engines.TTTEngine()
#output_engine = engines.TTSEngine() if response_in_speech else engines.TTTEngine()
