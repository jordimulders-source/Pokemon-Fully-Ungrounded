#!/usr/bin/env python3
"""Project Grounded: samples voor het Ashfrost-thema (ashfrost_theme.py, wintervariant van Fallarbor):
sleebellen (FluidR3 GM-drum 83 'Jingle Bell' = een schudbos belletjes) en een warme pad (GM 89 'Warm Pad') met een
gecrossfade loop. Celesta, speeldoos, klarinet en contrabas bestaan al (jirachi_*, shaymin_*) en worden hergebruikt.
Gebruikt de render-/schrijffuncties van keccles_samples.py (zie MUZIEK.md); bewerkt gm_samples.py niet.
Gebruik: python3 tools/grounded/ashfrost_samples.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keccles_samples import render, resample, write_wav, auto_loop, OUT, DATA

# naam: (GM-programma of 'drum', noot, lengte in s, samplerate, velocity, loop)
SAMPLES = {
    'ashfrost_sleigh':    ('drum', 83, 0.55, 22050, 110, None),   # sleebellen: één schudslag
    'ashfrost_warm_pad':  (89, 60, 2.2, 16000, 100, 'auto'),      # warme pad (C4), loop in het sustaindeel
    # zachte houten lead voor het A-deel: blokfluit (GM 74) op D5, in de ligging van de melodie (Bb4-D6).
    # De FluidR3-klarinet viel af: 87% van zijn energie zit in de 3e boventoon (2-4 kHz) = schel in de GBA-mix.
    'ashfrost_recorder':  (74, 74, 1.2, 22050, 100, 'auto'),
}
LOWPASS = {'ashfrost_recorder': 4000}   # Hz, 2x eenpolig: blaasruis eraf (de 8-bit-mix maakt hoog extra hard)


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for name, (prog, note, dur, rate, vel, loop) in SAMPLES.items():
        a = render(prog, note, dur, vel)
        if name in LOWPASS:
            k = np.exp(-2 * np.pi * LOWPASS[name] / 44100)
            for _ in range(2):
                y, out = 0.0, np.empty_like(a)
                for j, x in enumerate(a):
                    y = (1 - k) * x + k * y
                    out[j] = y
                a = out
        start = np.argmax(np.abs(a) > 0.002)                       # stilte vooraan weg
        a = resample(a[start:start + int(dur * 44100)], 44100, rate)
        a = a / max(1e-6, np.abs(a).max()) * 0.97                  # 8 bit: volle schaal
        if loop == 'auto':
            # een pad zweeft (chorus): lange loop (0,4 s) met een lange crossfade, ná de aanzet van de sample
            a, loop = (auto_loop(a, rate, note, at=1.4, length=0.4, xfade=0.15) if name.endswith('pad')
                       else auto_loop(a, rate, note, at=0.5, length=0.15, xfade=0.04))
            a = a / max(1e-6, np.abs(a).max()) * 0.97
        else:
            fade = int(rate * 0.04)
            a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, rate, 60 if prog == 'drum' else note, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s GM %4s noot %d, %d samples @ %d Hz, loop %s' % (name, prog, note, len(a), rate, loop))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
