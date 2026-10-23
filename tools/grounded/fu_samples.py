#!/usr/bin/env python3
"""Fully Ungrounded: de gedeelde instrumentenset (fu_*) voor alle nieuwe Latijns-Amerikaanse muziek.

Eén set eigen samples die elk nummer hergebruikt (zuinig met ROM, Jordi 22 okt): Andes (charango, quena, zampoña,
bombo), Afro-Peruaans/Caribisch (cajón, bongó, conga's, güiro, shaker, claves, cowbell), cumbia/tango (accordeon),
fanfare/salsa (trombone; trompet en tuba zijn de vanilla-samples), nylongitaar, reggaeton (808-bas, dembow-kick en
-snare, supersaw-stab) en samba (surdo, tamborim, caixa, agogô, cuíca, apito; cavaquinho = de charango).

Bronnen: FluidR3 (GM-soundfont, via fluidsynth) en een paar gesynthetiseerde klanken (808, kick, cajón, surdo,
tamborim, supersaw) met exacte loops. Melodische samples op 11.025 Hz (DPCM via sound/compressed_samples.mk),
slagwerk op 16.000 Hz onverpakt (DPCM is slecht voor transiënten). Alles in sound/direct_sound_samples/fu/.
De voicegroup (sound/voicegroups/fu.inc + drumsets/fu.inc + keysplits/fu_*.inc) schrijft dit script ook.

Vereist: apt-get install fluidsynth fluid-soundfont-gm; pip install mido numpy.
Gebruik: python3 tools/grounded/fu_samples.py [naam ...]   (zonder namen: alles)"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/fu/'
DATA = 'sound/direct_sound_data.inc'
MEL, DRUM = 11025, 16000
SR = 44100
RNG = np.random.default_rng(20261022)


# ---- bronnen ------------------------------------------------------------------------------------------------------
def render(prog, note, dur, vel=110):
    """Eén noot uit FluidR3 (mono, 44,1 kHz, -1..1). prog 'drum' = GM-drumkit (kanaal 10)."""
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 9 if prog == 'drum' else 0
    if ch == 0:
        t.append(mido.Message('program_change', program=prog, time=0))
    t.append(mido.Message('note_on', channel=ch, note=note, velocity=vel, time=0))
    t.append(mido.Message('note_off', channel=ch, note=note, velocity=0, time=int(dur * 960)))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(SR), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    a = a / 32768.0
    s = int(np.argmax(np.abs(a) > 0.002))
    return a[s:]


def fit(a, n):
    out = np.zeros(n)
    out[:min(n, len(a))] = a[:n]
    return out


def shift(a, cents):
    """Toonhoogte verschuiven door te herbemonsteren (korter/langer), voor dubbele snaren en musette."""
    r = 2 ** (cents / 1200)
    n = int(len(a) / r)
    return np.interp(np.arange(n) * r, np.arange(len(a)), a)


def lowpass(a, hz, rate=SR):
    k = np.exp(-2 * np.pi * hz / rate)
    out, y = np.empty_like(a), 0.0
    for i, x in enumerate(a):
        y = (1 - k) * x + k * y
        out[i] = y
    return out


def highpass(a, hz, rate=SR):
    return a - lowpass(a, hz, rate)


def env(n, attack, decay, rate=SR):
    t = np.arange(n) / rate
    e = np.exp(-t / decay)
    if attack:
        e *= np.minimum(1, t / attack)
    return e


def norm(a, peak=0.97):
    return a / max(1e-9, np.abs(a).max()) * peak


# ---- melodische instrumenten (FluidR3) --------------------------------------------------------------------------------
def charango(note):
    """Charango: kleine tokkelluit met dubbele snaren (paren, deels in octaven), helder en kort. Staalsnarige gitaar
    (GM 25) + een vleugje banjo (GM 105) voor de tik, de snaarparen als een tweede stem 7 cent hoger, en de octaafsnaar."""
    n = int(SR * 0.9)
    a = fit(render(25, note, 0.9, 112), n) + 0.30 * fit(render(105, note, 0.9, 100), n)
    a = a + 0.85 * fit(shift(a, 7), n) + 0.22 * fit(render(25, note + 12, 0.9, 96), n)
    a = highpass(a, 180)
    return a * env(n, 0, 0.45) ** 0.6


def charango_strum(root=64):
    """Rasgueo: een neerwaartse slag over vijf snaarparen in kwinten/octaven (grondtoon, kwint, octaaf, octaaf+kwint,
    twee octaven) zonder terts, dus bruikbaar onder mineur én majeur; 1 kanaal voor een heel akkoord."""
    n = int(SR * 1.0)
    out = np.zeros(n)
    for i, (iv, g) in enumerate(((0, 1.0), (7, 0.9), (12, 0.95), (19, 0.7), (24, 0.55))):
        s = int(SR * 0.011 * i)                                       # 11 ms tussen de snaren
        x = fit(render(25, root + iv, 0.9, 108), n)
        x = x + 0.8 * fit(shift(x, 6), n)
        out[s:] += g * fit(x, n - s)
    out = highpass(out, 160)
    return out * env(n, 0, 0.5) ** 0.5


def windy(note, progs, dur, breath=0.0, vib=None):
    """Blaasinstrument: mix van GM-programma's [(prog, gain)], optioneel ademruis in de aanzet (quena: houtig, veel lucht)."""
    n = int(SR * dur)
    a = sum(g * fit(render(p, note, dur, 112), n) for p, g in progs)
    if breath:
        f = 440 * 2 ** ((note - 69) / 12)
        noise = RNG.standard_normal(n)
        noise = lowpass(highpass(noise, f * 1.5), f * 4)
        e = 0.25 + 0.75 * np.exp(-np.arange(n) / (SR * 0.08))       # lucht vooral in de aanzet, daarna wat blijft
        a = a / max(1e-9, np.abs(a).max()) + breath * noise / np.abs(noise).max() * e
    return a


def accordion(note):
    """Accordeon met musette (twee rietjes, één ±12 cent hoger): GM 21 + een verschoven kopie."""
    n = int(SR * 1.4)
    a = fit(render(21, note, 1.4, 110), n)
    return a + 0.75 * fit(shift(a, 12), n)


def loop_best(a, rate, want, at=0.45, xf=0.4):
    """Loop van ±want s in het aanhoudende deel, op het punt waar het signaal het best op zichzelf lijkt, met de
    laatste xf van de loop gecrossfade met wat vóór het loopbegin staat (geen klik)."""
    s = int(len(a) * at)
    W, n = int(rate * want), int(rate * 0.04)
    best = max(range(int(W * 0.85), int(W * 1.15)),
               key=lambda L: np.dot(a[s:s + n], a[s + L:s + L + n]) / (np.linalg.norm(a[s + L:s + L + n]) + 1e-9))
    e = s + best
    f = int(best * xf)
    w = np.linspace(0, 1, f)
    a = a[:e].copy()
    a[e - f:e] = a[e - f:e] * (1 - w) + a[s - f:s] * w
    return a, (s, e)


# ---- gesynthetiseerd (exacte loops) ---------------------------------------------------------------------------------
def bass808():
    """808-bas op C2: een aanzet met een korte toonval (van +7 halve tonen) en een tik, daarna een licht verzadigde
    sinus. Loop = precies 7 perioden (1180 samples op 11.025 Hz = 65,40 Hz)."""
    rate, L, k = MEL, 1180, 7
    f = k * rate / L
    head = int(rate * 0.12)
    t = np.arange(head + 3 * L) / rate
    glide = f * (1 + (2 ** (7 / 12) - 1) * np.exp(-t / 0.018))
    ph = 2 * np.pi * np.cumsum(glide) / rate
    a = np.tanh(1.8 * np.sin(ph)) / np.tanh(1.8)
    a[:int(rate * 0.004)] += np.linspace(0.6, 0, int(rate * 0.004)) * RNG.standard_normal(int(rate * 0.004)) * 0.3
    # het loopdeel moet exact periodiek zijn: neem een schone periode-reeks met dezelfde fase als het einde
    tail = np.tanh(1.8 * np.sin(2 * np.pi * f * np.arange(L) / rate + ph[head])) / np.tanh(1.8)
    a = np.concatenate([a[:head], tail])
    return norm(a), rate, 36, (head, head + L)


def supersaw():
    """Supersaw voor stabs en leads (reggaeton): drie zaagtanden op C4 die exact 131/130/132 perioden in de loop doen
    (±13 cent), bandbegrensd. Loop = 5520 samples (0,5 s); de zweving loopt naadloos door."""
    rate, L = MEL, 5520
    t = np.arange(L) / rate
    a = np.zeros(L)
    for k, g in ((131, 1.0), (130, 0.8), (132, 0.8)):
        f = k * rate / L
        for h in range(1, int(rate / 2 / f)):
            roll = 1.0 if h * f < 3000 else max(0.0, 1 - (h * f - 3000) / 2000)
            a += g * roll * np.sin(2 * np.pi * h * f * t + 0.37 * k * h) / h
    a = norm(a, 0.9)
    head = np.tile(a, 1)[:int(rate * 0.02)] * np.linspace(0, 1, int(rate * 0.02))  # zachte aanzet (geen klik)
    full = np.concatenate([head, a])
    return full, rate, 60, (len(head), len(full))


def kick():
    """Dembow-kick: sinus 170 -> 50 Hz in ±50 ms, korte tik, licht verzadigd, 0,35 s."""
    n = int(DRUM * 0.35)
    t = np.arange(n) / DRUM
    f = 50 + 120 * np.exp(-t / 0.025)
    a = np.sin(2 * np.pi * np.cumsum(f) / DRUM) * np.exp(-t / 0.14)
    a += 0.35 * RNG.standard_normal(n) * np.exp(-t / 0.003)
    return norm(np.tanh(2.2 * a))


def cajon(kind):
    """Cajón: 'bass' = doffe houten dreun (±85 Hz) met een tik; 'slap' = rand van het slagvlak: houtige 300 Hz-body
    plus ratelende snaren (ruis 1,5-6 kHz)."""
    if kind == 'bass':
        n = int(DRUM * 0.4)
        t = np.arange(n) / DRUM
        f = 85 + 40 * np.exp(-t / 0.012)
        a = np.sin(2 * np.pi * np.cumsum(f) / DRUM) * np.exp(-t / 0.09)
        a += 0.25 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.03)
        nz = lowpass(RNG.standard_normal(n), 1800, DRUM) * np.exp(-t / 0.006)
        return norm(a + 0.6 * nz)
    n = int(DRUM * 0.3)
    t = np.arange(n) / DRUM
    body = (np.sin(2 * np.pi * 310 * t) + 0.5 * np.sin(2 * np.pi * 520 * t)) * np.exp(-t / 0.035)
    nz = RNG.standard_normal(n)
    snares = lowpass(highpass(nz, 1500, DRUM), 6000, DRUM) * np.exp(-t / 0.07)
    click = highpass(nz, 2500, DRUM) * np.exp(-t / 0.004)
    return norm(0.8 * body + 1.1 * snares / np.abs(snares).max() + 0.7 * click / np.abs(click).max())


def surdo():
    """Surdo: grote samba-trom, diep (±62 Hz) met lange nagalm, een vilten klop en een beetje vel (GM 41 eronder)."""
    n = int(DRUM * 0.9)
    t = np.arange(n) / DRUM
    f = 62 + 22 * np.exp(-t / 0.02)
    a = np.sin(2 * np.pi * np.cumsum(f) / DRUM) * np.exp(-t / 0.33)
    tom = resample(fit(shift(render('drum', 41, 0.9, 120), -700), int(SR * 0.9)), SR, DRUM)
    nz = lowpass(RNG.standard_normal(n), 900, DRUM) * np.exp(-t / 0.01)
    return norm(a + 0.45 * fit(tom, n) / max(1e-9, np.abs(tom).max()) + 0.5 * nz / np.abs(nz).max())


def tamborim():
    """Tamborim: klein trommeltje met een stokje, hoog en droog (±560 Hz + boventoon) met een tik."""
    n = int(DRUM * 0.12)
    t = np.arange(n) / DRUM
    a = (np.sin(2 * np.pi * 560 * t) + 0.6 * np.sin(2 * np.pi * 1210 * t)) * np.exp(-t / 0.028)
    nz = highpass(RNG.standard_normal(n), 2000, DRUM) * np.exp(-t / 0.004)
    return norm(a + 0.9 * nz / np.abs(nz).max())


def drum_mix(parts, dur):
    """[(GM-drumnoot, gain, cent-verschuiving)] gemengd, 44,1 kHz."""
    n = int(SR * dur)
    return sum(g * fit(shift(render('drum', k, dur + 0.2, 118), c) if c else render('drum', k, dur + 0.2, 118), n)
               for k, g, c in parts)


# ---- de lijst ------------------------------------------------------------------------------------------------------
# naam: (functie, soort) ; soort 'mel' = 11.025 Hz, grondtoon = noot; 'loop' = met loop; 'drum' = 16 kHz, toets 60
def bank():
    B = {}
    B['fu_charango_64'] = ('pluck', 64, lambda: charango(64))
    B['fu_charango_76'] = ('pluck', 76, lambda: charango(76))
    B['fu_charango_strum'] = ('pluck', 64, lambda: charango_strum(64))
    B['fu_quena_69'] = ('wind', 69, lambda: windy(69, ((73, 1.0), (77, 0.45)), 1.3, breath=0.22))
    B['fu_quena_81'] = ('wind', 81, lambda: windy(81, ((73, 1.0), (77, 0.35)), 1.3, breath=0.18))
    B['fu_zampona_67'] = ('wind', 67, lambda: windy(67, ((75, 1.0),), 1.3, breath=0.28))
    B['fu_zampona_79'] = ('wind', 79, lambda: windy(79, ((75, 1.0),), 1.3, breath=0.22))
    B['fu_accordion_60'] = ('reed', 60, lambda: accordion(60))
    B['fu_accordion_72'] = ('reed', 72, lambda: accordion(72))
    B['fu_trombone_55'] = ('brass', 55, lambda: fit(render(57, 55, 1.1, 127), int(SR * 1.1)))
    B['fu_trombone_67'] = ('brass', 67, lambda: fit(render(57, 67, 1.1, 127), int(SR * 1.1)))
    B['fu_nylon_52'] = ('pluck', 52, lambda: fit(render(24, 52, 1.2, 112), int(SR * 1.2)) * env(int(SR * 1.2), 0, 0.6) ** 0.4)
    B['fu_nylon_64'] = ('pluck', 64, lambda: fit(render(24, 64, 1.0, 112), int(SR * 1.0)) * env(int(SR * 1.0), 0, 0.5) ** 0.4)
    B['fu_cuica'] = ('pluck', 72, lambda: fit(render('drum', 79, 0.45, 118), int(SR * 0.45)))
    # slagwerk
    B['fu_kick'] = ('synth_drum', None, kick)
    B['fu_snare_rg'] = ('drum', None, lambda: drum_mix(((40, 1.0, 300), (37, 0.7, 0)), 0.25))
    B['fu_bombo'] = ('drum', None, lambda: drum_mix(((41, 1.0, -450), (35, 0.7, 0)), 0.7))
    B['fu_bombo_aro'] = ('drum', None, lambda: drum_mix(((37, 1.0, -200), (77, 0.5, -300)), 0.18))
    B['fu_cajon_bass'] = ('synth_drum', None, lambda: cajon('bass'))
    B['fu_cajon_slap'] = ('synth_drum', None, lambda: cajon('slap'))
    B['fu_bongo_hi'] = ('drum', None, lambda: drum_mix(((60, 1.0, 0),), 0.25))
    B['fu_bongo_lo'] = ('drum', None, lambda: drum_mix(((61, 1.0, 0),), 0.3))
    B['fu_conga_slap'] = ('drum', None, lambda: drum_mix(((62, 1.0, 0),), 0.2))
    B['fu_conga_open'] = ('drum', None, lambda: drum_mix(((63, 1.0, 0),), 0.35))
    B['fu_tumba'] = ('drum', None, lambda: drum_mix(((64, 1.0, 0),), 0.45))
    B['fu_guiro_long'] = ('drum', None, lambda: drum_mix(((74, 1.0, 0),), 0.4))
    B['fu_guiro_short'] = ('drum', None, lambda: drum_mix(((73, 1.0, 0),), 0.15))
    B['fu_shaker'] = ('drum', None, lambda: drum_mix(((82, 1.0, 0),), 0.15))
    B['fu_claves'] = ('drum', None, lambda: drum_mix(((75, 1.0, 0),), 0.15))
    B['fu_cowbell'] = ('drum', None, lambda: drum_mix(((56, 1.0, 0),), 0.3))
    B['fu_caixa'] = ('drum', None, lambda: drum_mix(((38, 1.0, 150), (40, 0.4, 300)), 0.25))
    B['fu_surdo'] = ('synth_drum', None, surdo)
    B['fu_tamborim'] = ('synth_drum', None, tamborim)
    B['fu_agogo_hi'] = ('drum', None, lambda: drum_mix(((67, 1.0, 0),), 0.35))
    B['fu_agogo_lo'] = ('drum', None, lambda: drum_mix(((68, 1.0, 0),), 0.35))
    B['fu_apito'] = ('drum', None, lambda: drum_mix(((71, 1.0, 0),), 0.2))
    return B


SYNTH_MEL = {'fu_808': bass808, 'fu_supersaw': supersaw}
LOOP_LEN = {'wind': 0.3, 'reed': 0.5, 'brass': 0.25}
COMPRESS_MIN = 4096          # DPCM alleen voor melodische samples vanaf 4 KB (zie compressed_samples.mk)


def make(name, kind, note, fn):
    if kind in ('drum', 'synth_drum'):
        a = fn()
        if kind == 'drum':
            a = resample(a, SR, DRUM)
        fade = int(DRUM * 0.015)
        a = norm(a)
        a[-fade:] *= np.linspace(1, 0, fade)
        return a, DRUM, 60, None
    a = resample(fn(), SR, MEL)
    a = norm(a)
    if kind in LOOP_LEN:
        a, loop = loop_best(a, MEL, LOOP_LEN[kind])
        return a, MEL, note, loop
    fade = int(MEL * 0.05)
    a[-fade:] *= np.linspace(1, 0, fade)
    return a, MEL, note, None


def pitch_of(a, rate, lo=40, hi=2000):
    """Grondtoon (Hz) via autocorrelatie over het middendeel (4x opgewaardeerd, parabolisch geïnterpoleerd): controle
    van het gelabelde basisnummer. Zoekt pas na de eerste nuldoorgang, en neemt de eerste piek die bijna zo hoog is
    als de hoogste (geen subharmonische door octaafsnaren of zweving)."""
    s = a[int(len(a) * 0.3):int(len(a) * 0.3) + int(rate * 0.2)]
    s = np.interp(np.arange(len(s) * 4) / 4, np.arange(len(s)), s - s.mean())
    r = rate * 4
    c = np.correlate(s, s, 'full')[len(s) - 1:]
    z = int(np.argmax(c < 0))
    mn, mx = max(z, int(r / hi)), int(r / lo)
    seg = c[mn:mx]
    k = mn + int(np.argmax(seg > 0.85 * seg.max()))
    while k + 1 < mx and c[k + 1] > c[k]:
        k += 1
    d = (c[k - 1] - c[k + 1]) / (2 * (c[k - 1] - 2 * c[k] + c[k + 1]))
    return r / (k + d)


def main(only=()):
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    items = [(n, k, nt, f) for n, (k, nt, f) in bank().items()] + [(n, 'synth', None, f) for n, f in SYNTH_MEL.items()]
    for name, kind, note, fn in items:
        if only and name not in only:
            continue
        if kind == 'synth':
            a, rate, key, loop = fn()
        else:
            a, rate, key, loop = make(name, kind, note, fn)
        write_wav(OUT + name + '.wav', a, rate, key, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/fu/%s.bin"\n' % (label, name)
        msg = ''
        if rate == MEL and kind not in ('pluck',) or name.startswith(('fu_nylon', 'fu_charango_6', 'fu_charango_7')):
            hz = pitch_of(a, rate)
            want = 440 * 2 ** ((key - 69) / 12)
            msg = '  grondtoon %.1f Hz (label %d = %.1f Hz, %+.0f cent)' % (hz, key, want, 1200 * np.log2(hz / want))
        print('%-18s %-10s %6d samples @ %5d Hz%s%s' % (name, kind, len(a), rate, ' loop' if loop else '', msg))
    open(DATA, 'w').write(inc)
    write_voicegroup()


# ---- voicegroup ----------------------------------------------------------------------------------------------------
# Eén voicegroup `fu` voor alle nummers. Programma's (GM-nummering waar het kan):
PROGRAMS = {
    0: '\tvoice_keysplit voicegroup_piano_keysplit, keysplit_piano',
    21: '\tvoice_keysplit voicegroup_fu_accordion_keysplit, keysplit_fu_s66',
    24: '\tvoice_keysplit voicegroup_fu_nylon_keysplit, keysplit_fu_s58',
    25: '\tvoice_keysplit voicegroup_fu_charango_keysplit, keysplit_fu_s70',
    26: '\tvoice_directsound 60, 0, DirectSoundWaveData_fu_charango_strum, 255, 0, 255, 170',
    33: '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
    38: '\tvoice_directsound 60, 0, DirectSoundWaveData_fu_808, 255, 0, 255, 200',
    56: '\tvoice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet',
    57: '\tvoice_keysplit voicegroup_fu_trombone_keysplit, keysplit_fu_s61',
    58: '\tvoice_keysplit voicegroup_tuba_keysplit, keysplit_tuba',
    73: '\tvoice_keysplit voicegroup_fu_quena_keysplit, keysplit_fu_s75',
    75: '\tvoice_keysplit voicegroup_fu_zampona_keysplit, keysplit_fu_s73',
    78: '\tvoice_directsound 60, 0, DirectSoundWaveData_fu_cuica, 255, 0, 255, 150',
    80: '\tvoice_square_1 60, 0, 0, 2, 0, 0, 15, 0',                 # PSG-lead (blokgolf 50%)
    81: '\tvoice_directsound 60, 0, DirectSoundWaveData_fu_supersaw, 255, 0, 255, 165',
    82: '\tvoice_square_2 60, 0, 2, 0, 1, 7, 1',                     # PSG-blokgolf 25%, kort
    83: '\tvoice_square_2 60, 0, 1, 0, 2, 9, 3',                     # PSG-blokgolf 12,5%, aanhoudend (zachte lead)
    121: '\tvoice_noise_alt 60, 0, 0, 0, 2, 6, 0',                    # ruis, wit: güiro/hihat
    122: '\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0',                    # ruis, kort: maracas/shaker
    123: '\tvoice_noise_alt 60, 0, 0, 5, 0, 12, 5',                   # ruis, zwellend: wind/riser
    127: '\tvoice_keysplit_all voicegroup_fu_drumset',
}
FILLER = '\tvoice_square_2 60, 0, 2, 0, 1, 7, 1'
KEYSPLITS = {   # naam: (tabel, [(sample, release)])
    'accordion': ('fu_s66', [('fu_accordion_60', 180), ('fu_accordion_72', 180)]),
    'nylon': ('fu_s58', [('fu_nylon_52', 200), ('fu_nylon_64', 200)]),
    'charango': ('fu_s70', [('fu_charango_64', 175), ('fu_charango_76', 175)]),
    'trombone': ('fu_s61', [('fu_trombone_55', 150), ('fu_trombone_67', 150)]),
    'quena': ('fu_s75', [('fu_quena_69', 190), ('fu_quena_81', 190)]),
    'zampona': ('fu_s73', [('fu_zampona_67', 185), ('fu_zampona_79', 185)]),
}
# drumkit vanaf noot 36: (sample, toets, pan, release); 'stock:' = vanilla-sample (speelt zoals in vanilla, no_resample)
DRUMKIT = [
    ('fu_kick', 60, 64, 0), ('fu_snare_rg', 60, 64, 60), ('stock:sc88pro_tr909_hand_clap', 60, 64, 60),      # 36-38
    ('fu_bombo', 60, 64, 120), ('fu_bombo_aro', 60, 64, 40),                                               # 39-40
    ('fu_cajon_bass', 60, 64, 60), ('fu_cajon_slap', 60, 64, 60),                                          # 41-42
    ('fu_bongo_hi', 60, 88, 80), ('fu_bongo_lo', 60, 84, 80),                                              # 43-44
    ('fu_conga_slap', 60, 50, 60), ('fu_conga_open', 60, 50, 60), ('fu_tumba', 60, 44, 60),                # 45-47
    ('fu_guiro_long', 60, 76, 160), ('fu_guiro_short', 60, 76, 60), ('fu_shaker', 60, 80, 40),            # 48-50
    ('fu_claves', 60, 58, 100), ('fu_cowbell', 60, 72, 120),                                               # 51-52
    ('stock:trinity_cymbal_crash', 60, 64, 165), ('fu_caixa', 60, 70, 60),                                 # 53-54
    ('stock:unknown_close_hihat', 60, 76, 40), ('stock:unknown_open_hihat', 60, 76, 120),                  # 55-56
    ('fu_surdo', 60, 60, 140), ('fu_surdo', 64, 68, 140),                                                  # 57-58
    ('fu_tamborim', 60, 86, 40), ('fu_agogo_hi', 60, 44, 100), ('fu_agogo_lo', 60, 44, 100),               # 59-61
    ('fu_apito', 60, 64, 60),                                                                              # 62
]
DRUM_NAMES = ('36 dembow-kick, 37 dembow-snare, 38 clap, 39 bombo, 40 bombo-aro (rand), 41 cajón-bas, 42 cajón-slap,\n'
              '@ 43/44 bongó hoog/laag, 45 conga slap, 46 conga open, 47 tumba, 48/49 güiro lang/kort, 50 shaker,\n'
              '@ 51 claves, 52 cowbell, 53 crash, 54 caixa (snare), 55/56 hihat dicht/open, 57/58 surdo laag/hoog,\n'
              '@ 59 tamborim, 60/61 agogô hoog/laag, 62 apito')


def write_voicegroup():
    lines = ['@ Fully Ungrounded: de gedeelde instrumentenset (gegenereerd door tools/grounded/fu_samples.py).',
             '@ 21 accordeon, 24 nylongitaar, 25 charango, 26 charango-rasgueo (kwintakkoord), 33 bas, 38 808,',
             '@ 56 trompet, 57 trombone, 58 tuba, 73 quena, 75 zampona, 78 cuica, 80/82/83 PSG-blokgolven, 81 supersaw,',
             '@ 121/122 PSG-ruis, 127 drumkit (drumsets/fu.inc).',
             'voice_group fu']
    for k in range(128):
        lines.append('%s  @ %d' % (PROGRAMS.get(k, FILLER), k))
    open('sound/voicegroups/fu.inc', 'w').write('\n'.join(lines) + '\n')
    ks = ['@ Fully Ungrounded: keysplits van de gedeelde instrumentenset (fu_samples.py); tabellen keysplit_fu_sNN',
          '@ in sound/keysplit_tables.inc (t/m noot NN = de lage sample, daarboven de hoge).']
    for name, (table, smp) in KEYSPLITS.items():
        ks.append('voice_group fu_%s_keysplit' % name)
        ks += ['\tvoice_directsound 60, 0, DirectSoundWaveData_%s, 255, 0, 255, %d' % (s_, r) for s_, r in smp]
        ks.append('')
    open('sound/voicegroups/keysplits/fu.inc', 'w').write('\n'.join(ks) + '\n')
    kit = ['@ Fully Ungrounded: drumkit van de gedeelde instrumentenset (fu_samples.py):',
           '@ ' + DRUM_NAMES, 'voice_group fu_drumset, 36']
    for smp, key, pan, rel in DRUMKIT:
        if smp.startswith('stock:'):
            kit.append('\tvoice_directsound_no_resample %d, %d, DirectSoundWaveData_%s, 255, 0, 255, %d'
                       % (key, pan, smp[6:], rel))
        else:
            kit.append('\tvoice_directsound %d, %d, DirectSoundWaveData_%s, 255, 0, 255, %d' % (key, pan, smp, rel))
    open('sound/voicegroups/drumsets/fu.inc', 'w').write('\n'.join(kit) + '\n\n')
    tables = open('sound/keysplit_tables.inc').read()
    for table, _ in KEYSPLITS.values():
        if 'keysplit %s,' % table not in tables:
            tables = tables.rstrip('\n') + '\n\nkeysplit %s, 0\n\tsplit 0, %d\n\tsplit 1, 127\n' % (table, int(table[-2:]))
    open('sound/keysplit_tables.inc', 'w').write(tables)
    # DPCM-lijst: melodische samples (niet in de drumkit) vanaf 4 KB
    drums = {d[0] for d in DRUMKIT}
    big = sorted(n for n in [os.path.basename(f)[:-4] for f in sorted(os.listdir(OUT)) if f.endswith('.wav')]
                 if n not in drums and os.path.getsize(OUT + n + '.wav') >= COMPRESS_MIN + 100)
    mk = open('sound/compressed_samples.mk').read()
    i = mk.find('\n# Fully Ungrounded: gedeelde instrumentenset')
    if i >= 0:
        mk = mk[:i] + '\n'
    mk = (mk.rstrip('\n') + '\n\n# Fully Ungrounded: gedeelde instrumentenset (fu_samples.py), melodische samples als DPCM\n'
          'FU_COMPRESSED_SAMPLES := \\\n\t' + ' '.join(big) + '\n\n'
          'FU_COMPRESSED_SAMPLE_BINS := $(patsubst %,sound/direct_sound_samples/fu/%.bin,$(FU_COMPRESSED_SAMPLES))\n'
          '$(FU_COMPRESSED_SAMPLE_BINS): sound/%.bin: sound/%.wav sound/compressed_samples.mk\n\t$(WAV2AGB) -b -c $< $@\n')
    open('sound/compressed_samples.mk', 'w').write(mk)
    vgi = open('sound/voice_groups.inc').read()
    for after, inc in (('drumsets/keccles.inc"\n', 'drumsets/fu.inc'), ('keysplits/keccles_guitar.inc"\n', 'keysplits/fu.inc')):
        if inc not in vgi:
            vgi = vgi.replace(after, after + '.include "sound/voicegroups/%s"\n' % inc)
    if 'voicegroups/fu.inc' not in vgi:
        vgi = vgi.rstrip('\n') + '\n.include "sound/voicegroups/fu.inc"\n'
    open('sound/voice_groups.inc', 'w').write(vgi)


if __name__ == '__main__':
    main(sys.argv[1:])
