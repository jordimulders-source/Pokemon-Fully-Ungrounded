#!/usr/bin/env python3
"""Project Grounded: twee eigen samples voor Battle! Ultra Beast (ub_theme.py), voorvoegsel ub_*.

Beide direct op 11.025 Hz gesynthetiseerd (MUZIEK.md: eigen samples max. 11 kHz), geen FluidR3, geen audio van
andere thema's.
  ub_glass  glazen FM-lead: twee FM-stemmen (draaggolf C5, modulator x1,412 = niet-harmonisch: glas/metaal i.p.v.
            een 'instrument'), +13 cent uit elkaar (zweving ±4 Hz = het glinsteren). Aanzet met hoge modulatie-index
            (klank van een tik op glas) die zakt naar een zachte, toonvaste kern. Loop = een heel aantal perioden van
            álle vier de oscillatoren (131/185 en 132/186 cycli in 2760 samples) = exact, geen zoem.
  ub_swell  'omgekeerde' zwelling: een lange niet-harmonische FM-klok (x1,4, x2,76) achterstevoren, zodat hij uit
            het niets aanzwelt en hard afbreekt. Voor de overgangen (scheur in de ruimte).
Gebruik: python3 tools/grounded/ub_samples.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import write_wav

OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
RATE = 11025


def glass():
    L = 2760                                   # 131 cycli = 523,3 Hz (C5)
    A = int(0.09 * RATE)                       # aanzet vóór de loop
    n = A + L
    t = np.arange(n)
    env_i = 0.9 + 2.2 * np.exp(-t / (0.035 * RATE))           # modulatie-index: tik -> zachte kern
    x = np.zeros(n)
    for c, m, amp in ((131, 185, 1.0), (132, 186, 0.8)):
        ph_c = 2 * np.pi * c * t / L
        ph_m = 2 * np.pi * m * t / L
        x += amp * np.sin(ph_c + env_i * np.sin(ph_m))
    # in de loop is de index constant (0,9 + een verwaarloosbare rest): forceer exact constant vanaf A
    x[A:] = sum(amp * np.sin(2 * np.pi * c * t[A:] / L + 0.9 * np.sin(2 * np.pi * m * t[A:] / L))
                for c, m, amp in ((131, 185, 1.0), (132, 186, 0.8)))
    # crossfade over 120 samples tussen aanzet en kern (de index sprong is klein, toch geen klik)
    f = 120
    w = np.linspace(0, 1, f)
    full = sum(amp * np.sin(2 * np.pi * c * t[A - f:A] / L + env_i[A - f:A] * np.sin(2 * np.pi * m * t[A - f:A] / L))
               for c, m, amp in ((131, 185, 1.0), (132, 186, 0.8)))
    core = sum(amp * np.sin(2 * np.pi * c * t[A - f:A] / L + 0.9 * np.sin(2 * np.pi * m * t[A - f:A] / L))
               for c, m, amp in ((131, 185, 1.0), (132, 186, 0.8)))
    x[A - f:A] = full * (1 - w) + core * w
    x *= np.minimum(1, t / 20.0)
    x = x / np.abs(x).max() * 0.97
    return x, 72, (A, n)


def swell():
    n = int(1.15 * RATE)
    t = np.arange(n) / RATE
    f0 = 261.63
    x = np.zeros(n)
    for ratio, idx, amp, dec in ((1.4, 2.6, 1.0, 0.45), (2.76, 1.4, 0.55, 0.30), (0.5, 0.0, 0.5, 0.7)):
        env = np.exp(-t / dec)
        x += amp * env * np.sin(2 * np.pi * f0 * (1 + 0.004 * (ratio > 1)) * t
                                + idx * env * np.sin(2 * np.pi * f0 * ratio * t))
    x = x[::-1].copy()                          # achterstevoren: zwelt aan en breekt af
    x *= np.minimum(1, (n - np.arange(n)) / 60.0)   # geen klik aan het eind
    x = x / np.abs(x).max() * 0.97
    return x, 60, None


SAMPLES = {'ub_glass': glass, 'ub_swell': swell}


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    total = 0
    for name, fn in SAMPLES.items():
        a, key, lp = fn()
        write_wav(OUT + name + '.wav', a, RATE, key, lp)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        total += len(a)
        print('%-9s %5d samples @ %d Hz (%.2f s), grondtoon %d%s' % (name, len(a), RATE, len(a) / RATE, key,
                                                                    ', loop %d-%d' % lp if lp else ''))
    open(DATA, 'w').write(inc)
    print('totaal %.1f KB' % (total / 1024))


if __name__ == '__main__':
    main()
