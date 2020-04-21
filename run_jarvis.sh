#!/usr/bin/env bash
# --------------------------------
# Start MongoDB service
# --------------------------------
sudo service mongod start

# --------------------------------
# Start Jarvis service with virtualenv
# --------------------------------
./jarvis_virtualenv/bin/python ./src/jarvis/start.py

# --------------------------------
# Stop MongoDB service
# --------------------------------
sudo service mongod stop