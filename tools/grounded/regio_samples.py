#!/usr/bin/env python3
"""Project Grounded: eigen sample voor de regionale remixes van het Hoenn-wildthema (regio_theme.py).

Eén sample: een steel drum (GM 114 uit FluidR3) voor de waterversie; de rest zijn stock-samples.
11.025 Hz (MUZIEK.md: eigen samples max. 11 kHz), eenmalig (de steel drum klinkt vanzelf uit; lange noten
worden in regio_theme.py als roffel gespeeld), DPCM via sound/compressed_samples.mk.
  python3 tools/grounded/regio_samples.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, write_wav
from gm_samples import render            # alleen de fluidsynth-render (gm_samples zelf wordt niet aangepast)

OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
RATE = 11025
SAMPLES = {
    # naam: (GM-programma, noot, lengte in s)
    'regio_steeldrum': (114, 72, 0.75),
}


def main():
    inc = open(DATA).read()
    for name, (prog, note, dur) in SAMPLES.items():
        a = render(prog, note, dur + 0.2)
        a = a[np.argmax(np.abs(a) > 0.002):]                       # stilte vooraan weg
        a = a[:int(dur * 44100)]
        a = resample(a, 44100, RATE)
        a = a / max(1e-6, np.abs(a).max()) * 0.97                  # 8 bit: volle schaal
        fade = int(RATE * 0.08)
        a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, RATE, note, None)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (
                label, name)
        print('%-16s GM %d noot %d, %d samples @ %d Hz (%.1f KB)' % (name, prog, note, len(a), RATE, len(a) / 1024))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
