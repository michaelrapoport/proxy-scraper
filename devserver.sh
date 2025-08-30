#!/bin/sh
source .venv/bin/activate
pip install -r requirements.txt
python -m flask --app src/app run -p $PORT --debug
