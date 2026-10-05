#!/usr/bin/env python3
"""Project Grounded: samples voor Battle! Neo Team Plasma (np_*).
v8 (Jordi over v7: 'koppel de sporen aan de juiste instrumenten uit het GBA-soundfont'): lead, akkoorden, stoten en
arpeggio's gebruiken nu GBA-samples zelf (sc88pro_square_wave, de trompet-keysplit, sc88pro_organ2); daarvoor zijn
np_lead_pulse, np_pulse_bass, np_stab en np_brass_full(_lo) weg. Nieuw: np_synth_bass = sc88pro_synth_bass byte voor
byte, een octaaf hoger gelabeld (de bas klinkt een octaaf onder de MIDI-noten, zoals in v5-v7). Blijven: np_sine en
het orgel (np_organ_sharp, ongewijzigd sinds v5). Hieronder de geschiedenis van de oude samples.
v7 (Jordi over v6: 'te kaal, dun en los zand'; lagen à la GBA-componisten):
- lead op de bronhoogte: pulse-lead (25% + 50% ontstemd) gelabeld op C5 met een vaste lowpass van 3,6 kHz, zodat
  de hoge ligging niet schel wordt (de laag een octaaf lager speelt op het PSG-vierkant: geen sample nodig);
- np_stab: korte, punchy synth-brass-stoot (zaagtand + blok, filterstoot) voor de off-beat-akkoorden;
- np_sine: zachte sinus (met een vleugje 2e harmonische) voor de oude 8-bit-sinuspartij, die het PSG-golfkanaal
  afstaat aan de sub-bas.
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
import os, struct, sys, wave
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


def organ():
    f0 = 523.25                                           # C5
    amps = [0] * 6
    for k, a in ((1, 1.0), (2, 0.8), (3, 0.7), (4, 0.6), (5, 0.25), (6, 0.45)):
        amps[k - 1] = a
    bright = [0, 0, 0.0, 0.9, 0, 0.6]                     # klik (percussie 2' en 1 1/3')
    return additive(f0, 32, amps, 64, attack=0.05, bright=bright)


def gba_copy(name, shift):
    """Een sample uit het GBA-soundfont (sound/direct_sound_samples/<name>.wav), byte voor byte gelijk, alleen
    `shift` halve tonen hoger gelabeld (klinkt dan zoveel lager)."""
    w = wave.open('sound/direct_sound_samples/%s.wav' % name)
    assert w.getsampwidth() == 1
    a = (np.frombuffer(w.readframes(w.getnframes()), np.uint8).astype(float) - 128) / 127
    d = open('sound/direct_sound_samples/%s.wav' % name, 'rb').read()
    i = d.index(b'smpl')
    sm = struct.unpack('<9I', d[i + 8:i + 44])
    loop = None
    if sm[7]:
        lp = struct.unpack('<6I', d[i + 44:i + 68])
        loop = (lp[2], lp[3] + 1)
    return a, w.getframerate(), loop, sm[3] + shift


def sine():
    f0, per = 523.25, 32
    return additive(f0, per, [1.0, 0.08], 64)


SAMPLES = {
    # naam: (functie, label-noot); label = noot waarop de sample in de MIDI 'thuis' is (None: de functie geeft hem)
    'np_sine': (sine, 72),
    'np_organ_sharp': (organ, 72),
    # v8: de GBA-synth bass (sc88pro_synth_bass), een octaaf hoger gelabeld: de MIDI-noten van de bron (Eb2-Ab4)
    # klinken een octaaf lager, zonder noten onder E1 in de MIDI (zoals np_pulse_bass in v5-v7)
    'np_synth_bass': (lambda: gba_copy('sc88pro_synth_bass', 12), None),
}


def main():
    inc = open(DATA).read()
    # oude np_-samples (alleen door Neo Plasma gebruikt) eruit; bestaande labels blijven op hun plek
    blocks = inc.split('\n\n')
    inc = '\n\n'.join(b for b in blocks if 'DirectSoundWaveData_np_' not in b
                       or any('DirectSoundWaveData_%s::' % k in b for k in SAMPLES)).rstrip('\n') + '\n'
    for f in os.listdir(OUT):
        if f.startswith('np_') and f[:-4] not in SAMPLES:
            os.remove(os.path.join(OUT, f))
    for name, (fn, key) in SAMPLES.items():
        a, rate, loop, *k = fn()
        write_wav(OUT + name + '.wav', a, rate, k[0] if key is None else key, loop)
        if 'DirectSoundWaveData_%s::' % name not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\nDirectSoundWaveData_%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (name, name)
        print('%-18s %6d samples @ %5d Hz, loop %s' % (name, len(a), rate, loop))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
