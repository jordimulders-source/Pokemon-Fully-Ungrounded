#!/usr/bin/env python3
"""Project Grounded: de twee eigen samples voor de trainerklasse-remixes van MUS_VS_TRAINER (trclass_theme.py).
De rest van de remixes gebruikt alleen stock-samples (die al in de ROM staan).
  trclass_steel   steel drum (GM 114, C5), calypso-lead van de SEA-remix
  trclass_vibes   vibrafoon (GM 11, C5), lounge-lead van CHIC en zwevende klokjes van MYSTIC
Allebei uitklinkend (geen loop), 11.025 Hz (MUZIEK.md: eigen samples max. 11 kHz), DPCM (sound/compressed_samples.mk).
Gebruik: python3 tools/grounded/trclass_samples.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gm_samples import render
from sample_utils import resample, write_wav

OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
RATE = 11025
# naam: (GM-programma, noot, lengte in s, uitfaden in s)
SAMPLES = {
    'trclass_steel': (114, 72, 0.75, 0.25),
    'trclass_vibes': (11, 72, 1.10, 0.35),
}


def main():
    inc = open(DATA).read()
    for name, (prog, note, dur, fade) in SAMPLES.items():
        a = render(prog, note, dur + 0.2)
        start = int(np.argmax(np.abs(a) > 0.002))
        a = a[start:start + int(dur * 44100)]
        a = resample(a, 44100, RATE)
        a = a / max(1e-6, np.abs(a).max()) * 0.97
        f = int(RATE * fade)
        a[-f:] *= np.linspace(1, 0, f) ** 2
        write_wav(OUT + name + '.wav', a, RATE, note, None)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-14s GM %3d noot %d: %d samples @ %d Hz (%.1f KB, DPCM ±%.1f KB)' % (
            name, prog, note, len(a), RATE, len(a) / 1024, len(a) / 2048))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
