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
v10: np_bass_fat (sc88pro_synth_bass + zijn grondtoon: grondtoon 17% -> 49% van de energie, RMS +33%), np_gbrass_lo/hi
(synth brass voor de glissando-intro). Zie neo_plasma_theme.py.
v9 (Jordi over v8: 'de iconische eerste seconden: de stijgende opening-run moet een vette, agressieve GBA Synth
Brass / Pulse Lead zijn'): np_lead_fat (C5) en np_lead_fat_lo (C3), gelaagd uit de GBA-samples zelf (zie fat_lead()).
Gebruik: python3 tools/grounded/neo_plasma_samples.py"""
import os, struct, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, auto_loop, write_wav

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


def gba_tone(name, note, R, dur, cents=0.0):
    """v9: een GBA-sample (klinkt C4 op zijn eigen samplerate, gemeten) als toon `note` (+cents) op samplerate R,
    `dur` s lang; de sustain via de loop van de sample zelf."""
    a, r, loop, key = gba_copy(name, 0)
    eff = r * 2 ** ((note - key + cents / 100) / 12)      # samples per seconde waarmee deze toon klinkt
    need = int(dur * eff) + 8
    if loop and len(a) < need:
        reps = (need - loop[0]) // (loop[1] - loop[0]) + 1
        a = np.concatenate([a[:loop[0]]] + [a[loop[0]:loop[1]]] * reps)
    out = resample(a[:need], eff, R)[:int(dur * R)]
    return np.pad(out, (0, int(dur * R) - len(out)))


def fat_lead(lo=False):
    """v9 (Jordi: 'de stijgende opening-run moet een vette, agressieve GBA Synth Brass / Pulse Lead zijn, snelle attack,
    veel volume, niet dun of tokkelend'): de GBA-blokgolf (sc88pro_square_wave) twee keer, ±12 cent uit elkaar
    (zweving = breed), plus de GBA-synth brass (sc88pro_trumpet_72) in unisono, in één sample = 1 kanaal. Aanzet: de
    eerste 35 ms 1,6x zo luid (de 'knal'), dan in 60 ms naar de sustain; verzadigd (tanh x2,2: vetter, lagere
    crest, de sustain ±+2 dB t.o.v. de kale blokgolf).
    lo: op C3 voor de lage noten (< C4) zónder trompet (koper niet onder C3: 'puuup'), met de blokgolf een octaaf
    hoger erbij voor de helderheid."""
    R, dur = 13379, 0.9
    note = 48 if lo else 72
    a = gba_tone('sc88pro_square_wave', note, R, dur) + 0.75 * gba_tone('sc88pro_square_wave', note, R, dur, 12)
    if lo:
        a += 0.5 * gba_tone('sc88pro_square_wave', note + 12, R, dur, -7)
    else:
        a += 0.9 * gba_tone('sc88pro_trumpet_72', note, R, dur)
    t = np.arange(len(a)) / R
    a /= np.abs(a[int(0.2 * R):]).max()                    # sustain op 1
    a *= 1 + 0.6 * np.clip(1 - np.maximum(0, t - 0.035) / 0.06, 0, 1)
    a = np.tanh(2.2 * a)
    a, loop = auto_loop(a / np.abs(a).max() * 0.97, R)
    return a, R, loop


def bass_fat():
    """v10 (Jordi/Gemini over de brug: 'de bas klinkt als een zacht, hol piepje in het middenregister'): gemeten had
    sc88pro_synth_bass maar 17% energie op de grondtoon en 46% op de 2e harmonische, dus je hoort hem een octaaf hoger
    dan hij speelt. Hier dezelfde GBA-sample + zijn eigen grondtoon als sinus (fase gelijk aan die van de sample, exact
    16 perioden per loop = naadloos), licht verzadigd: grondtoon 49% van de energie (was 17%), RMS +33%, piek even hoog -> dikker en voller, zelfde
    toonhoogte (label 72, zoals np_synth_bass)."""
    a, r, loop, key = gba_copy('sc88pro_synth_bass', 12)
    s, e = loop
    L = e - s
    per = 16
    f0 = per * r / L
    seg = a[s:e]
    X = np.fft.rfft(seg)
    ph = np.angle(X[per])
    amp1 = 2 * np.abs(X[per]) / L
    n = np.arange(len(a))
    env = np.ones(len(a))
    att = int(0.006 * r)
    env[:att] = np.linspace(0, 1, att)
    sub = np.cos(2 * np.pi * f0 * (n - s) / r + ph)
    out = a + 0.9 * amp1 * env * sub
    out = np.tanh(1.4 * out / np.abs(out).max())
    out = out / np.abs(out).max() * 0.97
    return out, r, loop, key


def gliss_brass(root):
    """v10 (Jordi/Gemini: 'de intro-run: dikke, brede synth brass met een continue pitch bend van laag naar hoog,
    harde aanslag'): synth brass zoals een GBA-synth: twee ontstemde zaagtanden (zweving, exacte loop), een
    filterstoot (bovenharmonischen die in 80 ms wegzakken) en een octaaf-onder-blok voor de dikte. Harmonischen
    begrensd tot 3,6 kHz bij +14 halve tonen (de bend gaat tot ±14 halve tonen van de wortel): geen schelle top."""
    f0 = 440 * 2 ** ((root - 69) / 12)
    per = 128 if root < 60 else 32
    nmax = max(4, int(3600 / (f0 * 2.25)))
    amps = [(1 / k) * (1 if k < 6 else 0.8 ** (k - 5)) for k in range(1, nmax + 1)]
    bright = [0] * 2 + [0.5 / k for k in range(3, nmax + 1)]
    a, rate, loop = additive(f0, per, amps, 32, attack=0.08, bright=bright, detune=1)
    return a, rate, loop


def _bandlimited(f0, per, amps, lp_hz, order=2):
    """Eén periode (per samples) met harmonischen amps (index 0 = grondtoon), gedempt door een lowpass van `order`
    (x 6 dB/oct) op lp_hz; geen detune, dus exact periodiek (geen zweving)."""
    x = np.arange(per) / per
    y = np.zeros(per)
    for k, a in enumerate(amps, 1):
        if a == 0 or k >= per // 2:
            continue
        g = 1 / np.sqrt(1 + (k * f0 / lp_hz) ** (2 * order))
        y += a * g * np.sin(2 * np.pi * k * x)
    return y


def pulse_lead(root):
    """v11 (Jordi/Gemini over v10: 'theremin / ijle fluittoon met vibrato die zweeft; moet een strakke, fel aangeslagen
    GBA pulse/square-lead zijn'). Gemeten: sc88pro_square_wave (en np_lead_fat, dat eruit is opgebouwd) is zelf een
    ontstemde/gechorusde blokgolf: in de sustain 8-10 dB tremolo op 1,7-5 Hz en het spectrale zwaartepunt schommelt 28%
    = precies 'zwevend vibrato'. Hier één zuivere pulsgolf (25%) + een vleugje 50% in fase, exact periodiek (geen
    zweving: 0 dB tremolo, 0 cent), lowpass 2e orde op 4,5 kHz (niet schel), licht verzadigd (tanh x1,8: even luid als
    de oude lead), en een felle aanslag: de eerste 25 ms 1,35x zo luid met de volle bovenharmonischen (filter dicht in
    60 ms)."""
    f0 = 440 * 2 ** ((root - 69) / 12)
    per = 32 if root >= 60 else 128
    rate = int(round(f0 * per))
    f0 = rate / per
    nh = per // 2 - 1
    pulse = [np.sin(np.pi * k * 0.25) / k for k in range(1, nh + 1)]
    sq = [(1 / k if k % 2 else 0) for k in range(1, nh + 1)]
    amps = [p + 0.35 * s for p, s in zip(pulse, sq)]
    body = _bandlimited(f0, per, amps, 4500)
    bright = _bandlimited(f0, per, amps, 9000, order=1)
    n_att = int(np.ceil(0.09 * f0)) * per                    # aanslag: hele perioden, dan de loop (16 perioden)
    n = n_att + 16 * per
    t = np.arange(n) / rate
    w = np.clip(1 - t / 0.06, 0, 1) ** 2                     # helderheid: in 60 ms dicht
    g = 1 + 0.35 * np.clip(1 - np.maximum(0, t - 0.025) / 0.04, 0, 1)  # knal: 25 ms 1,35x, in 40 ms terug
    idx = np.arange(n) % per
    pk = np.abs(body).max()
    a = np.tanh(1.8 * g * ((1 - w) * body[idx] + w * bright[idx]) / pk)    # verzadigd: lage crest = luid
    a[n_att:] = np.tanh(1.8 * body[idx[n_att:]] / pk)
    a = a / np.abs(a).max() * 0.97
    return a, rate, (n_att, n)


def bass_buzz():
    """v11 (Jordi/Gemini over v10: 'zacht, dof, houtachtig tikkend; moet een zware, blikkerige staccato synth-bass
    zijn die de track doordrukt, 25% luider'). Gemeten: np_bass_fat speelde de 16en als noten van 27 ticks (24 ms;
    detach met de v7-release) = een tik, geen toon, en de sample zelf is hol (sc88pro_synth_bass). De basstem van het
    origineel (Spleeter, maat 13-42): energie < 150 Hz 49%, 150-600 30%, 600-2k 12%, > 2 kHz 9%, en de toon houdt de
    hele 16e aan (2e helft/1e helft 0,88). Nieuw: zaagtand + 25%-puls met twee resonanties (±1 kHz = 'blikkerig',
    ±330 Hz = body; amplitude x4 / x2,5), lowpass 1e orde op 5 kHz, verzadigd (tanh x2: lage crest = luid), exact
    periodiek (geen zweving). Aanslag: de eerste 30 ms helderder (filter open) voor de punch. Klinkt op C2 en is op 48
    gelabeld (zoals np_bass_fat: de MIDI-noten klinken een octaaf lager, Eb1-Ab3)."""
    root = 36
    f0 = 440 * 2 ** ((root - 69) / 12)
    per = 256
    rate = int(round(f0 * per))
    f0 = rate / per
    nh = per // 2 - 1
    bump = lambda fk, fc, w: np.exp(-0.5 * (np.log2(fk / fc) / w) ** 2)
    amps = [(1 / k + 0.8 * np.sin(np.pi * k * 0.25) / k) * (1 + 3 * bump(k * f0, 1000, 0.6) + 1.5 * bump(k * f0, 330, 0.5))
            for k in range(1, nh + 1)]
    body = _bandlimited(f0, per, amps, 5000, order=1)
    bright = _bandlimited(f0, per, amps, 12000, order=1)
    n_att = int(np.ceil(0.05 * f0)) * per
    n = n_att + 8 * per
    t = np.arange(n) / rate
    idx = np.arange(n) % per
    w = np.clip(1 - t / 0.03, 0, 1) ** 2
    a = (1 - w) * body[idx] + w * bright[idx]
    pk = np.abs(a).max()
    a = np.tanh(2.0 * a / pk)
    a[n_att:] = np.tanh(2.0 * body[idx[n_att:]] / pk)
    a = a / np.abs(a).max() * 0.97
    return a, rate, (n_att, n)


def sine():
    f0, per = 523.25, 32
    return additive(f0, per, [1.0, 0.08], 64)


SAMPLES = {
    # naam: (functie, label-noot); label = noot waarop de sample in de MIDI 'thuis' is (None: de functie geeft hem)
    'np_sine': (sine, 72),
    'np_organ_sharp': (organ, 72),
    # (v8 np_synth_bass en v10 np_bass_fat: sinds v11 ongebruikt, weg; bass_fat() blijft als geschiedenis)
    # v9: vette lead voor de opening-run en het loopbegin (GBA-blokgolf x2 + GBA-synth brass)
    'np_lead_fat': (fat_lead, 72),
    'np_lead_fat_lo': (lambda: fat_lead(lo=True), 48),
    # v10: synth brass voor de glissando-intro
    'np_gbrass_lo': (lambda: gliss_brass(48), 48),
    'np_gbrass_hi': (lambda: gliss_brass(72), 72),
    # v11: zuivere pulse-lead (geen zweving) en blikkerige synth-bass
    'np_plead_hi': (lambda: pulse_lead(72), 72),
    'np_plead_lo': (lambda: pulse_lead(48), 48),
    'np_bass_buzz': (bass_buzz, 48),
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
