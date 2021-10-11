#!/usr/bin/env bash
# --------------------------------
# Activate Python virtual env
# --------------------------------
export PYTHONPATH="${PYTHONPATH}:./src/jarvis"

# --------------------------------
# Start MongoDB service
# --------------------------------
sudo systemctl start mongodb

# --------------------------------
# Run unittests
# --------------------------------
python -m unittest discover -s ./src -p "*tests.py"

# --------------------------------
# Stop MongoDB service
# --------------------------------
sudo systemctl stop mongodb