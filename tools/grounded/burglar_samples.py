#!/usr/bin/env python3
"""Project Grounded: samples voor "Battle! Burglar" (burglar_theme.py): noir-jazz-heist. Alles met het voorvoegsel bg_.

Rendert noten uit de GM-soundfont FluidR3 (fluidsynth), knipt, resamplet en schrijft een 8-bit WAV met smpl-chunk
(grondtoon + eventuele loop); make zet die via wav2agb om in een .bin. De vingerknip is gesynthetiseerd (GM heeft er
geen). Gedeelde hulpjes uit sample_utils.py (niet uit een ander thema).
Gebruik: python3 tools/grounded/burglar_samples.py [naam ...]"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, auto_loop, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'

# naam: ([(programma, noot), ...], lengte s, samplerate, loop, lowpass Hz of None, grondtoon voor de smpl-chunk)
# programma ('kit', n) = GM-drumkanaal met drumkit n (FluidR3: 0 Standard, 32 Jazz, 40 Brush); grondtoon 60.
# loop: None = uitklinkend, 'auto' = aanhoudend (auto_loop).
SAMPLES = {
    'bg_upright':   ([(32, 43)], 1.3, 16000, None, 5000, 43),                    # contrabas (G2)
    'bg_mtpt':      ([(59, 69)], 1.0, 22050, 'auto', 3800, 69),                  # gedempte trompet (harmon-zoem eraf)
    'bg_bari':      ([(67, 50)], 1.0, 16000, 'auto', 4500, 50),                  # baritonsax (D3)
    'bg_vibes':     ([(11, 67)], 1.5, 22050, None, 6000, 67),                    # vibrafoon (G4)
    # alarmstoot: één sample per voicing (D3 bari + D4/Ab4/C#5 koper) = 1 kanaal; tritonus + grote septiem
    'bg_stab':      ([(67, 50), (61, 62), (61, 68), (61, 73)], 0.55, 16000, None, 4500, 62),
    'bg_kick':      ([(('kit', 32), 36)], 0.35, 16000, None, 6000, 60),
    'bg_brush_tap': ([(('kit', 40), 38)], 0.30, 16000, None, 7000, 60),
    'bg_brush_slap': ([(('kit', 40), 39)], 0.40, 16000, None, 7000, 60),
    'bg_ride':      ([(('kit', 32), 51)], 0.9, 22050, None, 9000, 60),
    'bg_hat':       ([(('kit', 32), 42)], 0.12, 22050, None, 9000, 60),
    'bg_hat_pedal': ([(('kit', 32), 44)], 0.15, 22050, None, 9000, 60),
    'bg_hat_open':  ([(('kit', 32), 46)], 0.45, 22050, None, 9000, 60),
    'bg_snare':     ([(('kit', 16), 38)], 0.35, 16000, None, 7000, 60),         # Power-kit: snare met crack (achtervolging)
    'bg_rim':       ([(('kit', 32), 37)], 0.15, 16000, None, 7000, 60),         # side stick ('tik-tak' van de kluis)
    'bg_crash':     ([(('kit', 32), 49)], 1.4, 16000, None, 7000, 60),
    'bg_tom_lo':    ([(('kit', 32), 45)], 0.45, 16000, None, 6000, 60),
    'bg_tom_hi':    ([(('kit', 32), 48)], 0.40, 16000, None, 6000, 60),
}


def render(voices, dur, vel=110):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    for i, (prog, note) in enumerate(voices):
        ch = 9 if isinstance(prog, tuple) else i
        t.append(mido.Message('program_change', channel=ch, program=prog[1] if isinstance(prog, tuple) else prog, time=0))
    for i, (prog, note) in enumerate(voices):
        ch = 9 if isinstance(prog, tuple) else i
        t.append(mido.Message('note_on', channel=ch, note=note, velocity=vel, time=0))
    for i, (prog, note) in enumerate(voices):
        ch = 9 if isinstance(prog, tuple) else i
        t.append(mido.Message('note_off', channel=ch, note=note, velocity=0, time=int(dur * 960) if i == 0 else 0))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', '44100', '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


def lowpass(a, rate, hz, poles=2):
    k = np.exp(-2 * np.pi * hz / rate)
    for _ in range(poles):
        out, y = np.empty_like(a), 0.0
        for i, x in enumerate(a):
            y = (1 - k) * x + k * y
            out[i] = y
        a = out
    return a


def snap(rate=16000):
    """Vingerknip: korte ruisstoot door een resonant bandfilter rond 2,3 kHz + een tik, verval ±45 ms."""
    rng = np.random.default_rng(7)
    n = int(rate * 0.12)
    t = np.arange(n) / rate
    x = rng.standard_normal(n) * np.exp(-t / 0.018)
    # tweede-orde bandpass (resonantie 2300 Hz, Q 3)
    w0, q = 2 * np.pi * 2300 / rate, 3.0
    al = np.sin(w0) / (2 * q)
    b0, b2, a0, a1, a2 = al, -al, 1 + al, -2 * np.cos(w0), 1 - al
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b0 * x[i] + b2 * (x[i - 2] if i > 1 else 0) - a1 * (y[i - 1] if i else 0)
                - a2 * (y[i - 2] if i > 1 else 0)) / a0
    y[:int(rate * 0.002)] += np.linspace(1, 0, int(rate * 0.002)) * 0.8     # tik van de aanslag
    y *= np.exp(-t / 0.035)
    return y / np.abs(y).max() * 0.97


def add_label(inc, name):
    label = 'DirectSoundWaveData_' + name
    if label + '::' not in inc:
        inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
    return inc


def main(only=()):
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for name, (voices, dur, rate, loop, lp, key) in SAMPLES.items():
        if only and name not in only:
            continue
        a = render(voices, dur, 118 if name in ('bg_stab', 'bg_mtpt') else 110)
        start = np.argmax(np.abs(a) > 0.002)
        a = a[start:start + int(dur * 44100)]
        if lp:
            a = lowpass(a, 44100, lp)
        if name == 'bg_stab':
            a = np.tanh(a / np.abs(a).max() * 2.2)              # rauw, niet glanzend
            t = np.arange(len(a)) / 44100                        # stoot: hard erin, snel weg (koper zwelt anders aan)
            a *= np.minimum(1, t / 0.008) * np.exp(-np.maximum(0, t - 0.03) / 0.16)
        a = resample(a, 44100, rate)
        a = a / max(1e-6, np.abs(a).max()) * 0.97
        if loop == 'auto':
            a, loop = auto_loop(a, rate)
        else:
            fade = int(rate * (0.02 if key == 60 else 0.06))
            a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, rate, key, loop)
        inc = add_label(inc, name)
        print('%-14s %d samples @ %d Hz, grondtoon %d%s' % (name, len(a), rate, key, ', loop' if loop else ''))
    if not only or 'bg_snap' in only:
        write_wav(OUT + 'bg_snap.wav', snap(), 16000, 60, None)
        inc = add_label(inc, 'bg_snap')
        print('bg_snap        gesynthetiseerd')
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main(sys.argv[1:])
