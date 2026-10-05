#!/usr/bin/env python3
"""Project Grounded: extra samples voor Battle! Shaymin v2 (shaymin_theme.py, gevechtsversie): contrabas (getokkeld)
voor de bas-ostinato en een lichte ritmesectie (zachte bassdrum, twee toms) uit FluidR3. De v1-samples (shaymin_harp,
celesta, nylon, flute, clarinet) komen uit gm_samples.py en blijven ongemoeid.
Gebruikt de render-/schrijffuncties van keccles_samples.py (zelfde werkwijze, zie MUZIEK.md).
Gebruik: python3 tools/grounded/shaymin_samples.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keccles_samples import render, resample, write_wav, OUT, DATA

# naam: (GM-programma of 'drum', noot, lengte in s, samplerate, velocity)
SAMPLES = {
    'shaymin_upright':  (32, 43, 0.9, 16000, 118),     # acoustic bass (G2), getokkeld
    'shaymin_kick':     ('drum', 35, 0.35, 16000, 100), # acoustic bass drum: rond en zacht, geen rockkick
    'shaymin_tom_lo':   ('drum', 43, 0.5, 16000, 105),  # high floor tom
    'shaymin_tom_hi':   ('drum', 48, 0.4, 16000, 105),  # hi-mid tom
}


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for name, (prog, note, dur, rate, vel) in SAMPLES.items():
        a = render(prog, note, dur, vel)
        start = np.argmax(np.abs(a) > 0.002)
        a = resample(a[start:start + int(dur * 44100)], 44100, rate)
        a = a / max(1e-6, np.abs(a).max()) * 0.97
        fade = int(rate * (0.03 if prog == 'drum' else 0.08))
        a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, rate, 60 if prog == 'drum' else note, None)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-16s GM %4s noot %d, %d samples @ %d Hz' % (name, prog, note, len(a), rate))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
