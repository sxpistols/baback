#!/bin/bash

export PATH=/home/labs247/dolswork/back/venv/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/labs247/.local/bin:/home/labs247/bin

export FLASK_APP=run.py
export FLASK_DEBUG=1
export FLASK_RUN_PORT=9966
export FLASK_RUN_HOST=0.0.0.0
flask run
