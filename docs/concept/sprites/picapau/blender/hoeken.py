"""Driekwart-varianten: lijfdraai x camerakanteling. Draaien: python3.11 hoeken.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import picapau
os.makedirs('hoeken', exist_ok=True)
for lijf in (20, 30, 40):
    for kantel in (8, 18):
        picapau.render(os.path.abspath(f'hoeken/l{lijf}_k{kantel}.png'), lijf=lijf, kantel=kantel)
