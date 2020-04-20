#!/usr/bin/env bash
export PYTHONPATH="${PYTHONPATH}:./src/jarvis"
source jarvis_virtualenv/bin/activate
sudo service mongod start
python -m unittest discover -s ./src -p "*tests.py"
sudo service mongod stop