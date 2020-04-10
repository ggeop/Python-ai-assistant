#!/usr/bin/env bash
# --------------------------------
# Start Mongo Server
# --------------------------------
sudo service mongod start

# --------------------------------
# Start Jarvis service with virtualenv
# --------------------------------
jarvis_virtualenv/bin/python ./src/jarvis/start.py