#!/usr/bin/env python3
"""Project Grounded: eigen sample voor Area Zero (areazero_theme.py).

az_crystal: het 'kristal'-belletje van Area Zero (sinus + zwakke boventonen, snelle aanzet, lange uitsterving).
Gesynthetiseerd (geen FluidR3 nodig), grondtoon C6, 16 kHz (resample_wav.py: grondtoon >= C6 -> 16000 Hz), geen loop
(sterft vanzelf uit). Stock-glockenspiel/unknown_bell klinken een kwarttoon vals op toets 60 (gemeten: 1361 Hz en
1227 Hz), dus voor een arpeggio dat precies moet kloppen niet bruikbaar.
Gebruik: python3 tools/grounded/areazero_samples.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import write_wav

OUT = 'sound/direct_sound_samples/grounded'


def crystal(rate=16000, key=84, dur=0.9):
    f0 = 440 * 2 ** ((key - 69) / 12)
    t = np.arange(int(rate * dur)) / rate
    x = np.zeros_like(t)
    # (verhouding, sterkte, uitsterftijd s): grondtoon draagt, octaaf + licht onharmonische glans sterven snel
    for r, a, d in ((1.0, 1.0, 0.45), (2.0, 0.30, 0.18), (3.01, 0.12, 0.09), (4.18, 0.05, 0.05)):
        x += a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / d)
    att = np.minimum(1, t / 0.004)                     # 4 ms aanzet: tik zonder klik
    x *= att
    x[-int(rate * 0.05):] *= np.linspace(1, 0, int(rate * 0.05))
    return x / np.abs(x).max() * 0.95


def main():
    os.makedirs(OUT, exist_ok=True)
    write_wav(os.path.join(OUT, 'az_crystal.wav'), crystal(), 16000, 84, None)
    print('az_crystal.wav')


if __name__ == '__main__':
    main()
