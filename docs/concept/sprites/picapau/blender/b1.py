"""Gekozen stand B1 (Jordi, 5 nov): lijf 30, kantel 8. Draaien: python3.11 b1.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import picapau
os.makedirs('B1', exist_ok=True)
picapau.render(os.path.abspath('B1/b1.png'), lijf=30, kantel=8)
