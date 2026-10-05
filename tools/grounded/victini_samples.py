#!/usr/bin/env python3
"""Project Grounded: samples voor Battle! Victini (victini_theme.py), anime-rock-fanfare.

- victini_power: een powerchord (A2 + E3 + A3) op FluidR3 Distortion Guitar (GM 30), samen gerenderd = één kanaal per
  akkoord, met een gecrossfade loop in het sustain (aangehouden akkoorden) en kort gespeeld als chug in achtsten.
- victini_mute:  dezelfde powerchord palm-muted (FluidR3 GM 28, kort, geen loop) voor de gedempte strofe-chugs.
Gelabeld op A2 (45); het thema speelt grondtonen E2-D#3 (-5..+6 halve tonen).

Rendert met fluidsynth (apt-get install fluidsynth fluid-soundfont-gm); hulpjes uit sample_utils.py.
Gebruik: python3 tools/grounded/victini_samples.py"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, auto_loop, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
FS = 44100
RATE = 18000

# naam: (GM-programma, noten, lengte in s, loop, label-toets)
SAMPLES = {
    'victini_power': (30, (45, 52, 57), 1.2, True, 45),
    'victini_mute':  (28, (45, 52, 57), 0.35, False, 45),
}


def render(prog, notes, dur, vel=118):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    t.append(mido.Message('program_change', program=prog, time=0))
    for n in notes:
        t.append(mido.Message('note_on', note=n, velocity=vel, time=0))
    for i, n in enumerate(notes):
        t.append(mido.Message('note_off', note=n, velocity=0, time=int(dur * 960) if i == 0 else 0))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(FS), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for name, (prog, notes, dur, loop, key) in SAMPLES.items():
        a = render(prog, notes, dur)
        start = int(np.argmax(np.abs(a) > 0.002))
        a = a[start:start + int(dur * FS)]
        a = resample(a, FS, RATE)
        a = a / max(1e-6, np.abs(a).max()) * 0.97
        lp = None
        if loop:
            a, lp = auto_loop(a, RATE)
        else:
            fade = int(RATE * 0.05)
            a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, RATE, key, lp)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-14s GM %d %s, %d samples @ %d Hz, loop %s' % (name, prog, notes, len(a), RATE, lp))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
