#!/usr/bin/env bash
# --------------------------------
# Activate Python virtual env
# --------------------------------
export PYTHONPATH="${PYTHONPATH}:./src/jarvis"
source jarvis_virtualenv/bin/activate

# --------------------------------
# Start MongoDB service
# --------------------------------
sudo systemctl start mongodb

# --------------------------------
# Run unittests
# --------------------------------
python -m unittest discover -s ./src -p "*tests.py"
exit_code=($?)

# --------------------------------
# Stop MongoDB service
# --------------------------------
sudo systemctl stop mongodb

exit $exit_code