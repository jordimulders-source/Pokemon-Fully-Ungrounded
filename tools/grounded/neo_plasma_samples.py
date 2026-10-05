#!/usr/bin/env python3
"""Project Grounded: samples voor Battle! Neo Team Plasma v4 (np_*), gekozen door het origineel (BW2-mp3) te meten
(zie neo_plasma_theme.py): het 'gitaar'-spoor van de bron-MIDI is in het origineel een aanhoudende synth brass,
de bas is Slap Bass 2 (een octaaf lager dan de MIDI), het orgel een percussief (rock)orgel i.p.v. kerkorgel, en de
kick een grote, laag gestemde elektronische kick (pitch-sweep, ±250 ms) i.p.v. een droge rock-kick.

Hergebruikt de render-/loop-/wav-functies van heatran_samples.py (FluidR3 via fluidsynth). Drums uit een andere
GM-kit: programma ('kit', n, noot) = kanaal 10 met programmawissel n (16 = Power, 24 = Electronic, 25 = TR-808).
Gebruik: python3 tools/grounded/neo_plasma_samples.py"""
import os, sys, subprocess, tempfile, wave
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from heatran_samples import SF2, OUT, DATA, resample, auto_loop, write_wav, render

# naam: (GM-programma, noot, lengte in s, samplerate, loop)
SAMPLES = {
    'np_synth_brass':    (62, 60, 2.0, 22050, 'auto'),     # GM 62 Synth Brass 1, voor E3 en hoger
    'np_synth_brass_lo': (62, 43, 2.0, 16000, 'auto'),     # zelfde, op G2 voor de lage partij (niet 2 oct. omlaag)
    'np_slap_bass':      (37, 40, 1.4, 16000, None),       # GM 37 Slap Bass 2 (beste match met de bas-stem)
    'np_organ':          (17, 72, 1.6, 22050, 'auto'),     # GM 17 Percussive Organ (beste match in de orgelsectie)
    'np_hat_closed':     (('kit', 24, 42), 60, 0.25, 22050, None),
    'np_hat_open':       (('kit', 24, 46), 60, 0.6, 22050, None),
    'np_snare':          (('kit', 16, 38), 60, 0.45, 22050, None),
}


def render_kit(kit, note, dur):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    t.append(mido.Message('program_change', channel=9, program=kit, time=0))
    t.append(mido.Message('note_on', channel=9, note=note, velocity=110, time=0))
    t.append(mido.Message('note_off', channel=9, note=note, velocity=0, time=int(dur * 960)))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', '44100', '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


def kick(rate=16000, dur=0.32):
    """Elektronische kick zoals in het origineel: sinus die van ±180 Hz naar 62 Hz (C2) zakt, uitklinken ±200 ms, klikje."""
    t = np.arange(int(rate * dur)) / rate
    f = 62 + 120 * np.exp(-t / 0.025)
    ph = 2 * np.pi * np.cumsum(f) / rate
    a = np.sin(ph) * np.exp(-t / 0.085) * np.minimum(1, t / 0.002)
    a += 0.25 * np.tanh(3 * np.sin(ph)) * np.exp(-t / 0.05)        # wat boventonen in de aanzet (hoorbaar op kleine speakers)
    a[:int(rate * 0.004)] += np.random.default_rng(7).uniform(-0.3, 0.3, int(rate * 0.004))
    fade = int(rate * 0.04)
    a[-fade:] *= np.linspace(1, 0, fade)
    return a / np.abs(a).max() * 0.97


def add_label(inc, name):
    label = 'DirectSoundWaveData_' + name
    if label + '::' not in inc:
        inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
    return inc


def main():
    inc = open(DATA).read()
    for name, (prog, note, dur, rate, loop) in SAMPLES.items():
        a = render_kit(prog[1], prog[2], dur) if isinstance(prog, tuple) else render(prog, note, dur)
        start = np.argmax(np.abs(a) > 0.002)
        a = resample(a[start:start + int(dur * 44100)], 44100, rate, antialias=True)
        a = a / max(1e-6, np.abs(a).max()) * 0.97
        if loop == 'auto':
            a, loop = auto_loop(a, rate)
        else:
            fade = int(rate * 0.05)
            a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, rate, note, loop)
        inc = add_label(inc, name)
        print('%-18s %s noot %s, %d samples @ %d Hz' % (name, prog, note, len(a), rate))
    a = kick()
    write_wav(OUT + 'np_kick.wav', a, 16000, 60, None)
    inc = add_label(inc, 'np_kick')
    print('np_kick            synth, %d samples' % len(a))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
