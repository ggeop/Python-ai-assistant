#!/usr/bin/env bash
export PYTHONPATH="${PYTHONPATH}:./src/jarvis"
source jarvis_virtualenv/bin/activate
python -m unittest discover -s ./src -p "*tests.py"