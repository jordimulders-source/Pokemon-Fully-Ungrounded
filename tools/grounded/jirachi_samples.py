#!/usr/bin/env python3
"""Project Grounded: de trance-samples voor Battle! Jirachi v2 (jirachi_theme.py, de euforische climax).
Alles gesynthetiseerd (geen soundfont nodig), met een exacte loop:
  jirachi_supersaw_dark / _mid / _bright : 'supersaw' = 7 licht ontstemde zaagtanden in één sample (1 kanaal per
      akkoordnoot). Drie helderheden ('filter' dicht -> open): in de opbouw wisselt het spoor per maat van sample,
      zo klinkt het alsof het filter opengaat.
  jirachi_supersaw_lead : dezelfde supersaw op C5 (32 samples per periode) voor de lead in de hoge ligging.
  jirachi_sawbass : twee ontstemde zaagtanden + sub-octaaf (sinus), rond gefilterd, voor de off-beat trancebas.
  jirachi_kick    : trancekick (sinus met toonhoogtesweep 150 -> 45 Hz, klik, zachte saturatie), eenmalig.
  jirachi_vox     : (v3) de lang uitgerekte 'aaah'-vocal van het trance-tussenstuk: FluidR3 GM 52 (Choir Aahs) +
      53 (Voice Oohs) op C5, plus een kopie +7 cent (breedte, twee lagen in één kanaal); de luidheid na de aanzet
      geëgaliseerd (het FluidR3-koor pulseert). Loop van ±1,1 s (de eigen
      ademlus van het FluidR3-koor, gezocht met autocorrelatie, 35% gecrossfade); lowpass 4,5 kHz (tegen aliasing tot D6).
Exacte loop: de loop is M perioden van de grondtoon (per samples per periode); zaagtand k heeft precies M + k
trillingen per loop, dus elke stem loopt naadloos rond (de zweving zit in de sample: M = 128 -> 13,5 cent per stap).
Labels achteraan sound/direct_sound_data.inc (na .align 2). gm_samples.py blijft ongemoeid (alleen write_wav).
Gebruik: python3 tools/grounded/jirachi_samples.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gm_samples import write_wav, render, resample

OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
C4 = 261.6256


def supersaw(note, per, M, detune, fc, top, sub=0.0, seed=1, knee=0.5):
    """detune: [(k, amplitude)], fc = filterfrequentie in harmonischen (None = open), top = hoogste harmonische
    (zacht afgerond vanaf knee x top: de GBA transponeert zonder filter, dus weinig hoge harmonischen = weinig aliasing)."""
    f0 = C4 * 2 ** ((note - 60) / 12)
    rate = int(round(f0 * per))
    n = per * M
    x = np.arange(n) / n * 2 * np.pi            # één loop = 2 pi
    rng = np.random.default_rng(seed)
    a = np.zeros(n)
    nyq = 0.42 * n                              # trillingen per loop; ruim onder Nyquist
    for k, amp in detune:
        cyc = M + k
        ph = rng.uniform(0, 2 * np.pi)
        for h in range(1, top + 1):
            if h * cyc >= nyq:
                break
            g = 1.0 if fc is None else 1 / np.sqrt(1 + (h / fc) ** 4)
            roll = 1.0 if h <= top * knee else np.cos((h - top * knee) / (top * (1 - knee)) * np.pi / 2) ** 2
            a += amp * g * roll * np.sin(h * (cyc * x) + h * ph) / h
    if sub:
        a += sub * np.sin(M // 2 * x)            # sub-octaaf: M/2 trillingen per loop
    return a / np.abs(a).max() * 0.97, rate


SAW7 = [(0, 1.0), (-1, 0.8), (1, 0.8), (-2, 0.62), (2, 0.62), (-3, 0.45), (3, 0.45)]


def kick(rate=16000, dur=0.34):
    t = np.arange(int(rate * dur)) / rate
    f = 45 + 105 * np.exp(-t / 0.028)
    ph = 2 * np.pi * np.cumsum(f) / rate
    a = np.sin(ph) * np.exp(-t / 0.16)
    a += 0.5 * np.random.default_rng(3).uniform(-1, 1, len(t)) * np.exp(-t / 0.0025)     # klik
    a = np.tanh(2.2 * a)
    a[-int(rate * 0.02):] *= np.linspace(1, 0, int(rate * 0.02))
    return a / np.abs(a).max() * 0.97, rate


def vox(rate=14000, key=72):
    """Koor-'aaah' met een lange, ademende loop (zie docstring)."""
    from scipy.signal import butter, sosfiltfilt
    lay = []
    for prog, g in ((52, 0.6), (53, 0.6)):
        a = render(prog, key, 3.4)
        a = a[np.argmax(np.abs(a) > 0.002):]
        lay.append(g * a / np.sqrt(np.mean(a[44100:] ** 2)))
    n = min(len(x) for x in lay)
    a = lay[0][:n] + lay[1][:n]
    b = resample(a, 44100 * 2 ** (7 / 1200), 44100)                             # tweede laag +7 cent
    a = a[:len(b)] + 0.35 * b
    a = sosfiltfilt(butter(6, 4500, fs=44100, output='sos'), a)
    a = resample(a, 44100, rate)
    # het FluidR3-koor 'pulseert' (Aahs: luidheid x0,6-x2 per 50 ms): na de aanzet egaliseren (omhullende 60 ms)
    win = int(0.06 * rate)
    env = np.sqrt(np.convolve(a ** 2, np.ones(win) / win, 'same')) + 1e-4
    ref = np.median(env[int(0.5 * rate):int(2.5 * rate)])
    x = np.clip((np.arange(len(a)) / rate - 0.2) / 0.15, 0, 1)                   # vanaf 0,2 s geleidelijk egaliseren
    a = a * ((1 - x) + x * np.clip(ref / env, 0.5, 2.0))
    s0, want, w = int(1.0 * rate), int(1.1 * rate), int(0.08 * rate)
    L = max(range(int(want * 0.85), int(want * 1.15)),
            key=lambda L: np.dot(a[s0:s0 + w], a[s0 + L:s0 + L + w]) / (np.linalg.norm(a[s0 + L:s0 + L + w]) + 1e-9))
    e, f = s0 + L, int(L * 0.35)
    x = np.linspace(0, 1, f)
    a = a[:e].copy()
    a[e - f:e] = a[e - f:e] * (1 - x) + a[s0 - f:s0] * x                       # loopeinde vloeit over in het begin
    # de crossfade dooft deels uit (fasen): de loop rondom (cyclisch) nog eens egaliseren
    body = a[s0:e]
    ext = np.concatenate([body, body, body])
    env = np.sqrt(np.convolve(ext ** 2, np.ones(win) / win, 'same'))[len(body):2 * len(body)] + 1e-4
    a[s0:e] = body * np.clip(ref / env, 0.5, 2.5)
    return a / np.abs(a).max() * 0.97, (s0, e)


def main():
    inc = open(DATA).read()
    jobs = {
        'jirachi_supersaw_dark':   supersaw(60, 64, 128, SAW7, 2.2, 18),
        'jirachi_supersaw_mid':    supersaw(60, 64, 128, SAW7, 5.0, 18),
        'jirachi_supersaw_bright': supersaw(60, 64, 128, SAW7, None, 18),
        'jirachi_supersaw_lead':   supersaw(72, 32, 128, SAW7, None, 13, knee=0.7, seed=4),   # lead: grondtoon C5
        'jirachi_sawbass':         supersaw(48, 64, 128, [(-1, 1.0), (1, 1.0)], 7.0, 26, sub=1.2, seed=2),
    }
    for name, (a, rate) in jobs.items():
        write_wav(OUT + name + '.wav', a, rate, 72 if name.endswith('lead') else 60 if 'super' in name else 48, (0, len(a)))
        print('%-24s loop %d samples @ %d Hz' % (name, len(a), rate))
    a, rate = kick()
    write_wav(OUT + 'jirachi_kick.wav', a, rate, 60, None)
    print('%-24s %d samples @ %d Hz' % ('jirachi_kick', len(a), rate))
    a, loop = vox()
    write_wav(OUT + 'jirachi_vox.wav', a, 14000, 72, loop)
    print('%-24s %d samples, loop %s @ 14000 Hz' % ('jirachi_vox', len(a), loop))
    for name in list(jobs) + ['jirachi_kick', 'jirachi_vox']:
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
