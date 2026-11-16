#!/bin/sh
# Keten r8 (vanuit deze map): basis r5 115% geel + vlamtong (vlam8.py) + ogen-probeersels a-e (ogen8.py).
# naslag_*: eerste opzet met een 2x vergroot oog, vervallen na Jordi (r5-oog houden, linkeroog leesbaar maken).
set -e
python3 ogen8.py
python3 telling8.py
python3 vel8.py
rm -rf __pycache__
