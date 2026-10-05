#!/usr/bin/env python3
"""Project Grounded: samples voor Battle! Neo Team Plasma v6 (np_*).
v6 (Jordi over v5: 'te kale, schelle 8-bit sound, hoge tonen snijden, mist dynamiek en gelaagdheid'):
- lead: warme, volle pulse-lead als DirectSound-sample i.p.v. de PSG-blokgolf: twee licht ontstemde pulsen (25% en
  50%) gemengd, lowpass (24 dB/oct, ±3 kHz op C4; meeschuivend met de toonhoogte zoals een key-tracked filter),
  met een iets helderdere aanzet (filter dat kort opengaat) voor de articulatie;
- synth brass: vollere zaagtand-brass (twee ontstemde zaagtanden, lowpass ±2,5 kHz) met een filterstoot in de eerste
  ±60 ms = body + punch; aparte sample op C2 voor de lage partij.
v5 (naar Jordi's feedback op v4):
- bas: diepe, strakke pulse-bas (25%-pulsgolf, iets afgerond), gelabeld een octaaf hoger dan hij klinkt, zodat de
  MIDI-noten van de bron (Eb2-Ab4) een octaaf lager klinken zonder noten onder E1 in de MIDI;
- 'gitaar'-spoor: heldere synth brass met een zeer snelle, felle aanzet (eerste ±40 ms extra helder = de 'stoot'),
  twee licht ontstemde oscillatoren; een tweede sample op C2 voor de lage partij (niet 2 octaven omlaag gestemd);
- orgel: scherp drawbar-orgel (8', 4', 2 2/3', 2', 1 3/5', 1 1/3') met een klikje in de aanzet.
Alles additief gesynthetiseerd (exacte loop: samplerate = grondtoon x samples per periode). De drums komen uit de
standaard GBA-kit (rs_drumset), de lead is een PSG-blokgolf: daar zijn geen samples voor nodig.
Gebruik: python3 tools/grounded/neo_plasma_samples.py"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import write_wav

OUT = "sound/direct_sound_samples/grounded/"
DATA = "sound/direct_sound_data.inc"


def additive(f0, per, amps, n_loop, attack=0.0, bright=None, detune=0, dur_extra=0.0):
    """Periodieke golf met harmonischen `amps` (index 0 = grondtoon) op samplerate f0*per. `bright` = extra
    harmonischen die in `attack` s uitsterven (de aanzet). Met detune: tweede oscillator die per n_loop perioden
    `detune` perioden meer doet (zweving, toch een exacte loop). Geeft (golf, rate, loop)."""
    rate = int(round(f0 * per))
    f0 = rate / per
    n_att = int(np.ceil((attack + dur_extra) * f0)) * per
    n = n_att + n_loop * per
    t = np.arange(n) / rate
    a = np.zeros(n)
    for k, amp in enumerate(amps, 1):
        if amp == 0:
            continue
        a += amp * np.sin(2 * np.pi * k * f0 * t)
        if detune:
            fd = f0 * (n_loop + detune) / n_loop
            a += amp * 0.8 * np.sin(2 * np.pi * k * fd * t + 0.7 * k)
    if bright is not None and attack > 0:
        env = np.maximum(0, 1 - t / attack) ** 2         # nul vóór het loopbegin: geen klik bij de terugsprong
        for k, amp in enumerate(bright, 1):
            a += env * amp * np.sin(2 * np.pi * k * f0 * t + 0.3)
    a /= np.abs(a).max()
    a *= 0.97
    return a, rate, (n_att, n)


def pulse(k, duty):
    return 2 / (np.pi * k) * np.sin(np.pi * k * duty)


def bass():
    f0 = 65.406                                           # C2
    amps = [pulse(k, 0.25) / (1 + (k * f0 / 1400) ** 2) for k in range(1, 40)]
    bright = [0.5 * pulse(k, 0.25) * (k > 3) for k in range(1, 40)]
    return additive(f0, 256, amps, 4, attack=0.03, bright=bright)


def brass(f0, per, kmax):
    def amp(k):
        f = k * f0
        formant = 1 + 1.2 * np.exp(-((np.log2(f / 1400)) ** 2) / 0.5)      # helder koper rond 1-2 kHz
        return formant / k / (1 + (f / 5000) ** 4)
    amps = [amp(k) for k in range(1, kmax + 1)]
    bright = [0.9 * amp(k) * (k >= 4) for k in range(1, kmax + 1)]
    return additive(f0, per, amps, 128, attack=0.04, bright=bright, detune=1)


def organ():
    f0 = 523.25                                           # C5
    amps = [0] * 6
    for k, a in ((1, 1.0), (2, 0.8), (3, 0.7), (4, 0.6), (5, 0.25), (6, 0.45)):
        amps[k - 1] = a
    bright = [0, 0, 0.0, 0.9, 0, 0.6]                     # klik (percussie 2' en 1 1/3')
    return additive(f0, 32, amps, 64, attack=0.05, bright=bright)


def osc_mix(f0, per, amps2, n_loop, detune, attack=0.0, bright=None):
    """Zoals additive(), maar met een eigen harmonischenreeks voor de tweede (ontstemde) oscillator: amps2."""
    rate = int(round(f0 * per))
    f0 = rate / per
    n_att = int(np.ceil(attack * f0)) * per
    n = n_att + n_loop * per
    t = np.arange(n) / rate
    a = np.zeros(n)
    fd = f0 * (n_loop + detune) / n_loop
    for (amp1, amp2), k in zip(amps2, range(1, len(amps2) + 1)):
        a += amp1 * np.sin(2 * np.pi * k * f0 * t)
        a += amp2 * np.sin(2 * np.pi * k * fd * t + 0.9 * k)
    if bright is not None and attack > 0:
        env = np.maximum(0, 1 - t / attack) ** 2
        for k, amp in enumerate(bright, 1):
            a += env * amp * np.sin(2 * np.pi * k * f0 * t)
    a /= np.abs(a).max()
    a *= 0.97
    return a, rate, (n_att, n)


def lp(f, fc, order=4):
    return 1 / np.sqrt(1 + (f / fc) ** order)


def lead_warm():
    """Warme pulse-lead op C4: puls 25% + puls 50% (licht ontstemd: zweving ±1,6 Hz op C4), lowpass 3 kHz."""
    f0, per, kmax = 261.63, 64, 30
    amps = []
    for k in range(1, kmax + 1):
        g = lp(k * f0, 3000) * (1.25 if k == 1 else 1.0)          # iets meer grondtoon = voller
        amps.append((0.6 * pulse(k, 0.25) * g, 0.5 * pulse(k, 0.5) * g))
    bright = [0.35 * pulse(k, 0.25) * lp(k * f0, 4500) * (k >= 3) for k in range(1, kmax + 1)]
    return osc_mix(f0, per, amps, 160, 1, attack=0.035, bright=bright)


def saw_brass(f0, per, kmax, fc):
    amps = []
    for k in range(1, kmax + 1):
        g = lp(k * f0, fc) / k * (1 + 0.6 * np.exp(-((np.log2(k * f0 / 900)) ** 2) / 0.6))   # body rond 0,5-1,5 kHz
        amps.append((g, 0.85 * g))
    bright = [0.8 / k * lp(k * f0, fc * 2.2) * (k >= 3) for k in range(1, kmax + 1)]
    return osc_mix(f0, per, amps, 128, 1, attack=0.06, bright=bright)


SAMPLES = {
    # naam: (functie, label-noot); label = noot waarop de sample in de MIDI 'thuis' is
    'np_pulse_bass': (bass, 48),        # klinkt C2, gelabeld C3: alles een octaaf lager dan geschreven
    'np_lead_warm': (lead_warm, 60),
    'np_brass_full': (lambda: saw_brass(261.63, 64, 30, 2500), 60),
    'np_brass_full_lo': (lambda: saw_brass(65.406, 256, 110, 2000), 36),
    'np_organ_sharp': (organ, 72),
}


def main():
    inc = open(DATA).read()
    # v4-samples (alleen door Neo Plasma gebruikt) eruit
    blocks = inc.split('\n\n')
    inc = '\n\n'.join(b for b in blocks if 'DirectSoundWaveData_np_' not in b).rstrip('\n') + '\n'
    for f in os.listdir(OUT):
        if f.startswith('np_') and f[:-4] not in SAMPLES:
            os.remove(os.path.join(OUT, f))
    for name, (fn, key) in SAMPLES.items():
        a, rate, loop = fn()
        write_wav(OUT + name + '.wav', a, rate, key, loop)
        inc = inc.rstrip('\n') + '\n\n\t.align 2\nDirectSoundWaveData_%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (name, name)
        print('%-18s %6d samples @ %5d Hz, loop %s' % (name, len(a), rate, loop))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
