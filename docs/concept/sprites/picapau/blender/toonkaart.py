"""Toonkaart voor B1: model met alle kleuren wit gerenderd, verkleind naar 64, 4 tonen (schaduwgids voor de maker).
Draaien: python3.11 toonkaart.py  (daarna python3 toonkaart_tonen.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import picapau
for k in list(picapau.KLEUR): picapau.KLEUR[k] = (0.9, 0.9, 0.9)
os.makedirs('B1', exist_ok=True)
picapau.render(os.path.abspath('B1/wit.png'), lijf=30, kantel=8)
