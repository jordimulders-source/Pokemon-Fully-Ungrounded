#!/bin/sh
set -e
python3 kop.py ${ROZE:-0.35} > /dev/null
python3 r2.py; python3 lijnen.py; python3 gezicht2.py
