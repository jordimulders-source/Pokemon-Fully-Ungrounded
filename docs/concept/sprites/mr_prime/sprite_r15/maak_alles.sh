#!/bin/sh
# r15: hoed rechts op de kop laten aansluiten (Jordi bij r14). Varianten A/B, A gekozen.
set -e
python3 r15.py
cp variant_A.png mr_prime.png
python3 diff.py
python3 maak_vel.py
