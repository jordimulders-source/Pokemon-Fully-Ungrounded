#!/usr/bin/env python3
"""Project Grounded: "Battle! Keccles" v2, eigen compositie in de stijl van Willie Colón (Fania-jaren: 'El Malo',
'La Murga', 'Che Che Colé', 'Calle Luna Calle Sol', 'Juanito Alimaña'). Keccles is een Kecleon met een PhD en
existentiële angst; hij vecht op harde New Yorkse salsa dura.

v1 (Jordi: 'klinkt goed, maar te eentonig, meer reguliere salsa'): de hook, het tempo en de groove blijven.
v2 voegt toe wat Colón-salsa is: brallende trombones voorop (2-3 in harmonie, eigen FluidR3-sample), trompet alleen
voor kleur, cuatro (Yomo Toro) met tremolo-fills, een coro, veel soorten percussie en echte dynamiek (CC7 per sectie).

190 bpm (4/4, 'cut time'), A-mineur, clave 2-3 (even maten = 2-kant, oneven = 3-kant).
  0-3    intro: montuno + clave + maracas, bongó/conga erbij, bloque (koperstoten), koperloop + abanico (= maat 67)
Loop (64 maten, ±81 s):
  A  4-19   de hook: eerst alleen twee trombones in tertsen (rauw), dan trompet erbovenop; maat 19 = corte (tutti
            stoot op de 3-kant, dan stilte) met een cuatro-oploopje naar de coro
  B 20-35   coro (zacht): koor 'aah' in tertsen (vraag), cuatro-tremolo antwoordt (inspiración); alleen montuno,
            bas, conga, maracas. Daarna bongó + clave, dan cascara + trombone in het koor, crescendo; het laatste
            antwoord is een koperstoot
  P 36-39   piano-montunosolo (octaven, blokakkoorden) over bas + percussie, güiro
  D 40-47   descarga: alleen bas + percussie (bongó, conga, clave, güiro, maracas); dan een cuatro-solo met
            cascara, en een trombone-swell (CC7-ramp) naar de mambo
  M 48-63   mambo: trombone-moña in tertsen + campana + bongo-bel, dan de trompetriff erbovenop (gestapeld), dan
            trompetten in tertsen, dan drie trombones; crescendo
  K 64-67   bloque-stoten, timbalesolo, koperloop -> terug naar A
Percussie (eigen drumkit drumsets/keccles.inc, alles DirectSound): bongó-martillo (in de mambo de bongo-bel), conga-
tumbao, timbales (cascara, campana, abanico, fills), clave, güiro (sample + PSG-ruis), maracas (PSG-ruis), crash.

Voicegroup grounded_keccles (gegenereerd) = grounded_gm met: 0 = piano met korte release (montuno), 24 = cuatro,
56 = trompet, 57 = trombone (FluidR3 GM 57, 2 samples), 121 = güiro (PSG-ruis), 122 = maracas (PSG-ruis),
127 = salsa-drumkit. Zie tools/grounded/MUZIEK.md. Gebruik: python3 tools/grounded/keccles_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_keccles.mid'
VG = 'grounded_keccles'
TPB, BPM = 48, 190
E = TPB // 2                   # een achtste
S16 = TPB // 4
BAR = TPB * 4
PIANO, CUATRO, CORO, TRUMPET, TROMBONE, BASS, GUIRO_PSG, MARACAS, DRUMS = 0, 24, 52, 56, 57, 33, 121, 122, 127
GUITAR = 29                    # v3: riffende elektrische gitaar (lichte overdrive)
# eigen drumkit (drumsets/keccles.inc, vanaf noot 36)
(KICK, CLAVE, CASCARA, HEMBRA, MACHO, CAMPANA, SLAP, TUMBA, CONGA_HI, CRASH, RIM,
 BONGO_HI, BONGO_LO, BELL_MOUTH, BELL_HEEL, GUIRO_L, GUIRO_S) = range(36, 53)

A0, B0, P0, D0, M0, K0, END = 4, 20, 36, 40, 48, 64, 68      # secties (maat); de loop = maat 4-68

N = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    """'A4' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


CH = {'Am': [9, 0, 4], 'Dm': [2, 5, 9], 'E7': [4, 8, 11, 2], 'Dm7': [2, 5, 9, 0], 'G7': [7, 11, 2, 5],
      'Cmaj7': [0, 4, 7, 11], 'Fmaj7': [5, 9, 0, 4], 'Bm7b5': [11, 2, 5, 9]}
PROG = (['Am', 'Dm', 'E7', 'E7']
        + ['Am', 'Am', 'Dm', 'E7'] * 4                    # A
        + ['Dm7', 'G7', 'Cmaj7', 'E7'] * 4                # B: coro-vamp
        + ['Am', 'Dm', 'E7', 'Am']                        # P
        + ['Am', 'Dm', 'E7', 'Am'] * 2                    # D
        + ['Am', 'Dm', 'E7', 'Am'] * 4                    # M
        + ['Dm', 'E7', 'E7', 'E7'])                       # K
assert len(PROG) == END

HARM = [9, 11, 0, 2, 4, 5, 8]          # A harmonisch mineur (hook, mambo)
NAT = [9, 11, 0, 2, 4, 5, 7]           # A natuurlijk mineur / C groot (coro-vamp)


def third_below(n, scale=HARM):
    """Diatonische terts onder n: de tweede stem."""
    lo = n - 1
    for d in range(1, 6):
        if (n - d) % 12 in scale:
            lo = n - d
            break
    for d in range(1, 6):
        if (lo - d) % 12 in scale:
            return lo - d
    return n - 3


def mel(pattern, bar, vel=116, shift=0, stac=0.7):
    """[(achtste, lengte in achtsten, 'A4'), ...] -> punchy koper: korte noten staccato, accent op 1 en 2+."""
    out = []
    for st, ln, nm in pattern:
        s = bar * BAR + int(st * E)
        dur = int(E * stac) if ln == 1 else int(ln * E) - 6
        out.append([s, s + dur, p(nm) + shift, vel + (6 if st in (0, 3) else 0)])
    return out


def harm(notes, scale=HARM, lo=48, vel=-12):
    """Tweede stem een diatonische terts lager (nooit onder `lo`: koper onder C3 = 'puuup')."""
    out = []
    for s, e, n, v in notes:
        t = third_below(n, scale)
        out.append([s, e, t + 12 if t < lo else t, v + vel])
    return out


# ---- melodieën -----------------------------------------------------------------------------------------------------
HOOK = [   # A: de hook (4 maten: Am Am Dm E7); de vierde maat verschilt per herhaling
    [(0, 1, 'A4'), (1, 1, 'C5'), (2, 1, 'E5'), (3, 2, 'A5'), (5, 1, 'G#5'), (6, 1, 'A5'), (7, 1, 'C6')],
    [(1, 1, 'B5'), (2, 1, 'A5'), (3, 1, 'E5'), (4, 2, 'F5'), (6, 1, 'E5')],
    [(0, 1, 'D5'), (1, 1, 'F5'), (2, 1, 'A5'), (3, 2, 'D6'), (5, 1, 'C6'), (6, 1, 'B5'), (7, 1, 'A5')],
]
HOOK_END = [[(1, 1, 'G#5'), (2, 1, 'B5'), (3, 1, 'D6'), (4, 3, 'E6')],                       # open (vraag)
            [(1, 1, 'G#5'), (2, 1, 'B5'), (3, 1, 'D6'), (4, 1, 'C6'), (5, 1, 'B5'), (6, 2, 'G#5')]]  # naar de herhaling
CORO_MEL = [   # B: de coro (vraag, 2 maten Dm7 G7), koor in tertsen
    [(1, 1, 'D5'), (2, 1, 'C5'), (3, 2, 'A4'), (5, 1, 'C5'), (6, 2, 'D5')],
    [(0, 1, 'F5'), (1, 1, 'E5'), (2, 1, 'D5'), (3, 3, 'B4'), (6, 1, 'G4'), (7, 1, 'B4')],
]
# cuatro-inspiraciones (antwoord, 2 maten Cmaj7 E7): (achtste, achtsten, noot, tremolo)
CUATRO_ANS = [
    [[(0, 2, 'E5', 1), (2, 2, 'G5', 1), (4, 1, 'E5', 0), (5, 1, 'D5', 0), (6, 1, 'C5', 0), (7, 1, 'B4', 0)],
     [(0, 2, 'G#4', 1), (2, 1, 'B4', 0), (3, 1, 'D5', 0), (4, 3, 'E5', 1)]],
    [[(0, 4, 'G5', 1), (4, 1, 'B5', 0), (5, 1, 'A5', 0), (6, 1, 'G5', 0), (7, 1, 'E5', 0)],
     [(0, 1, 'F5', 0), (1, 1, 'E5', 0), (2, 1, 'D5', 0), (3, 1, 'B4', 0), (4, 2, 'G#4', 1), (6, 1, 'B4', 0), (7, 1, 'D5', 0)]],
    [[(0, 1, 'C5', 0), (1, 1, 'E5', 0), (2, 1, 'G5', 0), (3, 3, 'B5', 1), (6, 1, 'A5', 0), (7, 1, 'G5', 0)],
     [(0, 2, 'E5', 1), (2, 1, 'D5', 0), (3, 1, 'C5', 0), (4, 1, 'B4', 0), (5, 1, 'G#4', 0), (6, 2, 'E4', 1)]],
]
BRASS_ANS = [   # laatste antwoord in de coro: koperstoot omhoog naar de pianosolo
    [(0, 1, 'E5'), (1, 1, 'G5'), (2, 1, 'B5'), (3, 2, 'C6'), (5, 1, 'B5'), (6, 2, 'G5')],
    [(0, 1, 'G#5'), (1, 1, 'B5'), (2, 1, 'D6'), (3, 2, 'E6'), (6, 1, 'E6'), (7, 1, 'E6')],
]
PIANO_SOLO = [   # P: montunosolo in octaven (Am Dm E7 Am); 'chord' = blokakkoord
    [(0, 1, 'A5'), (1, 1, 'A5'), (3, 1, 'C6'), (4, 1, 'B5'), (5, 1, 'A5'), (6, 2, 'E5')],
    [(1, 1, 'F5'), (2, 1, 'A5'), (3, 1, 'D6'), (5, 1, 'C6'), (6, 1, 'A5'), (7, 1, 'F5')],
    [(0, 1, 'G#5'), (1, 1, 'B5'), (2, 1, 'D6'), (3, 1, 'F6'), (4, 1, 'E6'), (5, 1, 'D6'), (6, 1, 'B5'), (7, 1, 'G#5')],
    [(0, 1, 'chord'), (3, 1, 'chord'), (5, 1, 'G#5'), (6, 1, 'A5'), (7, 1, 'B5')],
]
MONA = {   # mambo: trombone-moña (ostinato)
    'Am': [(1, 1, 'E4'), (2, 1, 'E4'), (3, 1, 'A4'), (5, 1, 'E4'), (6, 2, 'G4')],
    'Dm': [(0, 1, 'F4'), (1, 1, 'A4'), (3, 1, 'F4'), (4, 1, 'D4'), (6, 2, 'F4')],
    'E7': [(1, 1, 'G#4'), (2, 1, 'G#4'), (3, 1, 'B4'), (5, 1, 'G#4'), (6, 2, 'D4')],
    'Am2': [(0, 2, 'C4'), (3, 1, 'E4'), (4, 1, 'A3'), (6, 1, 'A3'), (7, 1, 'C4')],
}
MAMBO_TPT = {   # mambo: tegenriff van de trompetten in de gaten van de moña (gestapeld)
    'Am': [(0, 2, 'C6'), (3, 1, 'B5'), (4, 1, 'A5'), (6, 2, 'E5')],
    'Dm': [(0, 2, 'D6'), (3, 1, 'C6'), (4, 1, 'A5'), (6, 2, 'F5')],
    'E7': [(0, 1, 'E6'), (1, 1, 'D6'), (2, 1, 'B5'), (3, 1, 'G#5'), (4, 1, 'E5'), (5, 1, 'F5'), (6, 2, 'G#5')],
    'Am2': [(0, 3, 'A5'), (4, 1, 'C6'), (5, 1, 'B5'), (6, 1, 'A5'), (7, 1, 'E5')],
}
RUN = [(i, 1, nm) for i, nm in enumerate(['E4', 'G#4', 'B4', 'D5', 'E5', 'F5', 'G#5', 'B5'])]   # koperloop omhoog
BLOQUE = {'Dm': ('A5', 'F5', 'D4'), 'E7': ('B5', 'G#5', 'E4')}


def clave_pos(bar):
    return (2, 4) if bar % 2 == 0 else (0, 3, 6)     # 2-3: even maat = 2-kant


def section(b):
    if b < A0:
        return 'intro'
    if b < B0:
        return 'A1' if b < A0 + 8 else 'A2'
    if b < P0:
        u = (b - B0) // 4
        return 'B12' if u < 2 else 'B3' if u == 2 else 'B4'
    if b < D0:
        return 'P'
    if b < M0:
        return 'D1' if b < D0 + 4 else 'D2'
    if b < K0:
        return 'M%d' % ((b - M0) // 4 + 1)
    return 'K'


# ---- dynamiek: CC7 per spoor per sectie (Jordi: 'ik mis de dynamiek') ------------------------------------------------
TRACKS = [   # naam, programma, basisvolume (vol), pan
    ('tpt', TRUMPET, 104, 84), ('tpt2', TRUMPET, 88, 96), ('trb', TROMBONE, 118, 52), ('trb2', TROMBONE, 106, 40),
    ('trb3', TROMBONE, 96, 64), ('piano', PIANO, 90, 72), ('bass', BASS, 118, 64), ('cuatro', CUATRO, 104, 88),
    ('coro', CORO, 100, 60), ('bongo', DRUMS, 92, 84), ('conga', DRUMS, 96, 46), ('timb', DRUMS, 100, 70),
    ('clave', DRUMS, 88, 58), ('noise', GUIRO_PSG, 40, 64), ('gtr', GUITAR, 100, 80),
]
GAIN = {'intro': .92, 'A1': .84, 'A2': .90, 'B12': .50, 'B3': .64, 'B4': .80, 'P': .84, 'D1': .82, 'D2': .88,
        'M1': .88, 'M2': .93, 'M3': 1.0, 'M4': 1.0, 'K': 1.0}
GAIN_OVR = {   # sporen die in een sectie de hoofdrol hebben
    ('coro', 'B12'): .86, ('coro', 'B3'): .92, ('coro', 'B4'): 1.0, ('cuatro', 'B12'): .90, ('cuatro', 'B3'): .95,
    ('cuatro', 'D2'): 1.0, ('cuatro', 'K'): .9, ('cuatro', 'A2'): .9, ('piano', 'P'): 1.0, ('bass', 'D1'): 1.0,
    ('bass', 'D2'): 1.0, ('bass', 'B12'): .66, ('noise', 'B12'): .85, ('conga', 'D1'): .95, ('bongo', 'D1'): .95,
    ('trb', 'B4'): .9, ('gtr', 'D1'): 1.0, ('gtr', 'M1'): .96,
}

# ---- v3: riffende elektrische gitaar à la 'Vigilante' (Colón/Blades): (achtste, achtsten, noot, effect) ------------
# effect: '' gewoon, 'x' gedempte spookslag, 's' slide (van een hele toon onder), 'b' bend (een hele toon omhoog
# vanaf de geschreven noot - 2), 'v' vibrato, combinaties mogen ('bv').
GTR_DESCARGA = [   # D1 (maat 40-43, Am Dm E7 Am): de gitaar riffs over bas + percussie, tussen de bongó-repiques
    [(0.5, .5, 'A3', 'x'), (1, .5, 'A3', 'x'), (1.5, .5, 'C4', ''), (2, .5, 'D4', ''), (2.5, 1, 'E4', 's'),
     (4, .5, 'G4', ''), (4.5, 1.5, 'A4', 'bv'), (6.5, .5, 'G4', ''), (7, .5, 'E4', ''), (7.5, .5, 'D4', '')],
    [(0, 1, 'C4', ''), (1, .5, 'A3', ''), (2, .5, 'D4', 'x'), (2.5, .5, 'D4', ''), (3, .5, 'F4', ''), (3.5, .5, 'A4', ''),
     (4, 2.5, 'D5', 'bv'), (7, .5, 'C5', ''), (7.5, .5, 'A4', '')],
    [(0.5, .5, 'B3', 'x'), (1, .5, 'E4', ''), (1.5, .5, 'G#4', ''), (2, .5, 'B4', ''), (2.5, .5, 'D5', ''),
     (3, 1.5, 'E5', 'sv'), (5, .5, 'D5', ''), (5.5, .5, 'B4', ''), (6, .5, 'G#4', ''), (6.5, .5, 'F4', ''), (7, 1, 'E4', 'v')],
    [(0, .5, 'A4', ''), (0.5, .5, 'A4', 'x'), (1.5, 1, 'C5', 'b'), (2.5, .5, 'A4', 'x'), (3, .5, 'A4', ''),
     (4, .8, 'E4', ''), (5, .8, 'F#4', ''), (6, .8, 'G4', ''), (7, .8, 'G#4', '')],   # 4-7: met het basloopje mee
]
GTR_MONA = {   # M1 (maat 50-51): tegenriff in de gaten van de trombone-moña (op 1, 3 en de 16e-opmaten)
    'E7': [(0, .5, 'E5', ''), (0.5, .5, 'E5', 'x'), (4, .5, 'D5', ''), (4.5, .5, 'B4', ''), (7, .5, 'B4', ''), (7.5, .5, 'D5', '')],
    'Am2': [(1.5, .5, 'E5', ''), (2, 1, 'A5', 'b'), (5, .5, 'G5', ''), (5.5, .5, 'E5', ''), (6, .5, 'C5', 'x'),
            (6.5, .5, 'E5', ''), (7.5, .5, 'G#4', '')],
}


def build():
    parts = {k: [] for k, *_ in TRACKS}
    parts['noise_prog'] = []

    def hit(part, bar, e8, note, vel, ln=S16):
        s = bar * BAR + int(e8 * E)
        parts[part].append([s, s + ln, note, vel])

    def bloque(bar, chord, positions, vel=120):
        lead, second, low = BLOQUE[chord]
        for e8 in positions:
            hit('tpt', bar, e8, p(lead), vel, int(E * 0.7))
            hit('trb', bar, e8, p(lead) - 12, vel + 4, int(E * 0.7))
            hit('trb2', bar, e8, p(second) - 12, vel, int(E * 0.7))
            hit('trb3', bar, e8, p(low) + 12 if p(low) < 60 else p(low), vel - 4, int(E * 0.7))
            hit('bass', bar, e8, bass_root(CH[chord][0]), 120, int(E * 0.8))
            for o in (0, 12):
                hit('piano', bar, e8, p(lead) - 12 + o, 100, int(E * 0.5))
            hit('timb', bar, e8, RIM, 112)

    def run(bar):        # maat 3 = maat 67: koperloop (trombones in tertsen) + abanico, eindigt op de maatgrens
        parts['tpt'] += mel(RUN, bar, 110)
        parts['trb'] += mel(RUN, bar, 116, shift=-12)
        parts['trb2'] += harm(mel(RUN, bar, 116, shift=-12))
        hit('bass', bar, 0, bass_root(4), 118, int(E * 0.8))
        hit('bass', bar, 4, bass_root(4) + 12, 110, int(E * 0.8))
        abanico(bar)

    def abanico(bar, start=6):   # rimshot-roffel naar de 1 (de 'abanico' van de timbalero)
        for k in range(4):
            hit('timb', bar, start + k * 0.5, RIM if k % 2 else MACHO, 90 + k * 10)

    def tremolo(part, bar, figure, vel=100, shift=0):
        """cuatro: (achtste, achtsten, noot, tremolo) -> tokkel-tremolo in 16e (aanslag + zachtere terugslag)."""
        for st, ln, nm, trem in figure:
            s = bar * BAR + int(st * E)
            if trem:
                for k in range(int(ln * 2)):
                    t = s + k * S16
                    parts[part].append([t, t + S16 - 1, p(nm) + shift, vel - (14 if k % 2 else 0)])
            else:
                parts[part].append([s, s + int(E * 0.8), p(nm) + shift, vel + 6])

    # ---- intro + break -------------------------------------------------------------------------------------------
    bloque(2, 'E7', (0, 3, 6))
    bloque(K0, 'Dm', (0, 3, 6))
    bloque(K0 + 1, 'E7', (2, 4, 6, 7))
    hit('timb', K0, 0, CRASH, 112, E)
    for k in range(16):                                                 # timbalesolo (maat 66)
        nt = [MACHO, MACHO, HEMBRA, RIM][k % 4] if k < 12 else [HEMBRA, HEMBRA, MACHO, RIM][k - 12]
        hit('timb', K0 + 2, k * 0.5, nt, 74 + k * 3 + (14 if k % 4 == 0 else 0))
    run(3)
    run(END - 1)

    # ---- corte (maat 19): tutti op de 3-kant (1, 2+), dan stilte; cuatro loopt op naar de coro -------------------
    corte = A0 + 15
    for e8 in (0, 3):
        for part, nm, v in (('tpt', 'D6', 124), ('trb', 'G#4', 124), ('trb2', 'E4', 118),
                            ('trb3', 'D4', 112)):
            hit(part, corte, e8, p(nm), v, int(E * 0.75))
        hit('bass', corte, e8, bass_root(4), 124, int(E * 0.8))
        for nt in (p('G#4'), p('B4'), p('D5')):
            hit('piano', corte, e8, nt, 104, int(E * 0.5))
        hit('timb', corte, e8, RIM, 116)
        hit('conga', corte, e8, SLAP, 112, S16)
    hit('timb', corte, 0, CRASH, 116, E)
    tremolo('cuatro', corte, [(5, 1, 'E5', 1), (6, 1, 'G#5', 0), (7, 1, 'B5', 0)], 96)

    # ---- bas (tumbao), piano (montuno) ----------------------------------------------------------------------------
    for b in range(END):
        ch, nxt = PROG[b], PROG[(b + 1) if b + 1 < END else A0]
        root, nroot = CH[ch][0], CH[nxt][0]
        sec = section(b)
        rhythm = (b == 1) or (A0 <= b < K0 and b != corte)
        bv = -14 if sec == 'B12' else 0
        if rhythm:
            if b in (1, A0, B0, P0, D0, M0) or (sec.startswith('D') and b % 2 == 0):
                hit('bass', b, 0, bass_root(root), 116 + bv, 3 * E - 6)
            hit('bass', b, 3, fifth(root), 108 + bv, 3 * E - 6)
            # 4: de grondtoon van de volgende maat, doorgehouden over de maatgrens (anticipatie)
            ln = 2 * E - 6 if b + 1 in (K0, 2, corte) else 5 * E - 6
            hit('bass', b, 6, bass_root(nroot), 120 + bv, ln)
            if sec.startswith('D') and b % 4 == 3 and b + 1 < M0:          # descarga: loopje naar de volgende maat
                parts['bass'] = [n for n in parts['bass'] if not (n[0] == b * BAR + 6 * E)]
                nr = bass_root(nroot)
                for k, nt in enumerate((fifth(root), nr - 3, nr - 2, nr - 1)):   # kwint, dan chromatisch omhoog
                    hit('bass', b, 4 + k, nt + (12 if nr - 3 < 28 else 0), 112, E - 4)
        if b < 2 or (A0 <= b < P0 and b != corte):
            vel = {'intro': 92, 'A1': 86, 'A2': 90, 'B12': 76, 'B3': 80, 'B4': 86}[sec]
            montuno(parts, b, ch, nxt, vel)
        elif M0 <= b < K0:
            montuno(parts, b, ch, nxt, 88, octaves=False)               # mambo: enkele noten (ruimte voor koper)

    # ---- A: de hook ----------------------------------------------------------------------------------------------
    for i in range(16):
        b = A0 + i
        if b == corte:
            continue
        k = i % 4
        pat = HOOK[k] if k < 3 else HOOK_END[0] if i in (3, 11) else HOOK_END[1]   # vraag, antwoord
        trb = mel(pat, b, 118, shift=-12)
        parts['trb'] += trb                                             # Colón: trombones voorop, in tertsen
        parts['trb2'] += harm(trb, vel=-8)
        if i >= 8:                                                      # tweede helft: trompet erbovenop (kleur)
            parts['tpt'] += mel(pat, b, 106)
        elif k == 3:                                                    # eerste helft: trompet-antwoord op de 4
            parts['tpt'] += mel([(6, 1, 'E6'), (7, 1, 'E6')], b, 100)

    # ---- B: coro ------------------------------------------------------------------------------------------------
    for u in range(4):
        b = B0 + u * 4
        for j in range(2):                                              # koor (vraag), in tertsen
            ctop = mel(CORO_MEL[j], b + j, 92 + u * 6, stac=0.85)
            parts['coro'] += ctop + harm(ctop, NAT, lo=52, vel=-10)
            if u == 3:                                                  # laatste keer: trombone zingt mee
                parts['trb'] += mel(CORO_MEL[j], b + j, 100, shift=-12, stac=0.85)
        if u < 3:                                                       # cuatro (antwoord)
            for j in range(2):
                tremolo('cuatro', b + 2 + j, CUATRO_ANS[u][j], 98 + u * 4)
        else:                                                           # koperstoot naar de pianosolo
            for j in range(2):
                t = mel(BRASS_ANS[j], b + 2 + j, 118)
                parts['tpt'] += t
                parts['trb'] += mel(BRASS_ANS[j], b + 2 + j, 120, shift=-12)
                parts['trb2'] += harm(mel(BRASS_ANS[j], b + 2 + j, 120, shift=-12), NAT)

    # ---- P: pianosolo ---------------------------------------------------------------------------------------------
    for i, pat in enumerate(PIANO_SOLO):
        b = P0 + i
        for st, ln, nm in pat:
            s = b * BAR + st * E
            dur = 10 if ln == 1 else ln * E - 14
            if nm == 'chord':
                for nt in (p('A4'), p('C5'), p('E5')):
                    parts['piano'].append([s, s + 10, nt, 112])
            else:
                for o in (0, -12):
                    parts['piano'].append([s, s + dur, p(nm) + o, 108 + (8 if st in (0, 3) else 0)])

    # ---- D: descarga (bas + percussie), dan cuatro-solo en trombone-swell ---------------------------------------
    for i in range(4):                                                  # cuatro speelt de hook als tremolo-solo
        b = D0 + 4 + i
        pat = HOOK[i] if i < 3 else HOOK_END[0]
        tremolo('cuatro', b, [(st, ln, nm, 1 if ln > 1 else 0) for st, ln, nm in pat], 104)
    swell = (M0 - 2) * BAR + 4 * E
    for part, nm, v in (('trb', 'D4', 120), ('trb2', 'B3', 116), ('trb3', 'G#3', 112)):
        parts[part].append([swell, M0 * BAR - 4, p(nm), v])

    # ---- M: mambo ------------------------------------------------------------------------------------------------
    for i in range(16):
        b = M0 + i
        key = PROG[b] if i % 4 != 3 else 'Am2'
        trb = mel(MONA[key], b, 118 + (4 if i >= 8 else 0))
        parts['trb'] += trb
        if not 8 <= i < 12:                                             # M3: trompetten in tertsen, 1 trombone
            parts['trb2'] += harm(trb, vel=-6)
        if i >= 12:                                                     # climax: drie trombones
            parts['trb3'] += harm(harm(trb, vel=-6), vel=-6)
        if i >= 4:                                                      # gestapelde riff: trompet erbovenop
            tp = mel(MAMBO_TPT[key], b, 110 + (6 if i >= 8 else 0))
            parts['tpt'] += tp
            if 8 <= i < 12:                                             # trompetten in tertsen (max. 3 koperstemmen)
                parts['tpt2'] += harm(tp, vel=-10)

    # ---- v3: elektrische gitaar (descarga-riffs, moña-dubbel en tegenriff) -----------------
    gfx = {}

    def guitar(bar, figure, vel=104, shift=0):
        for st, ln, nm, fx in figure:
            s = bar * BAR + int(round(st * E))
            n = p(nm) + shift - (2 if ('s' in fx or 'b' in fx) else 0)
            dur = 6 if 'x' in fx else int(round(ln * E)) - (2 if ln < 1 else 4)
            v = 64 if 'x' in fx else vel + (8 if st in (0, 3, 4.5) else 0)
            parts['gtr'].append([s, s + dur, n, v])
            if fx.replace('x', ''):
                gfx[(s, n)] = fx

    for i, fig in enumerate(GTR_DESCARGA):
        guitar(D0 + i, fig, 104)
    for i in range(2):                                                  # M1, maat 48-49: moña een octaaf hoger mee
        b = M0 + i
        guitar(b, [(st, ln, nm, '') for st, ln, nm in MONA[PROG[b]]], 98, shift=12)
    guitar(M0 + 2, GTR_MONA['E7'], 100)
    guitar(M0 + 3, GTR_MONA['Am2'], 100)

    # ---- percussie -----------------------------------------------------------------------------------------------
    for b in range(END):
        sec = section(b)
        ending = b in (2, 3, corte, K0, K0 + 1, K0 + 2, K0 + 3)
        # clave (niet in de zachte coro; in de volle stukken dragen cascara en campana hem)
        if sec not in ('B12', 'A2', 'B4', 'M1', 'M2', 'M3', 'M4') and b != corte:   # volle stukken: cascara draagt de clave
            for e8 in clave_pos(b):
                hit('clave', b, e8, CLAVE, 100 if sec != 'B3' else 84)
        # conga-tumbao
        if b >= 1 and b != K0 + 2 and b != corte:
            soft = {'intro': -20, 'B12': -24, 'B3': -12}.get(sec, 0)
            for e8, nt, v in ((0, SLAP, 46), (2, SLAP, 112), (4, SLAP, 46), (6, TUMBA, 104),
                              (7, CONGA_HI if b % 2 else TUMBA, 100)):
                if ending and e8 != 2:
                    continue                                            # bloque/loop: alleen de slap
                hit('conga', b, e8, nt, v + soft, S16 + 4)
            if sec.startswith('M') or sec.startswith('D'):
                hit('conga', b, 5, CONGA_HI, 84, S16 + 4)
        # bongó: martillo; in de mambo de bongo-bel (cencerro)
        if (b in (1,) or sec in ('A1', 'A2', 'B3', 'B4', 'P', 'D1', 'D2')) and not ending:
            for e8, nt, v in ((0, BONGO_HI, 104), (1, BONGO_HI, 58), (2, BONGO_HI, 86), (3, BONGO_HI, 58),
                              (4, BONGO_HI, 100), (5, BONGO_HI, 58), (6, BONGO_LO, 108), (7, BONGO_HI, 64)):
                if v < 70 and sec in ('A2', 'B4'):
                    continue                                            # volle stukken: geen spookslagen (ruimte)
                hit('bongo', b, e8, nt, v - (10 if sec == 'B3' else 0), S16)
            if sec == 'D1' and b % 2:                                   # descarga: bongó improviseert (repiques)
                for k in range(4):
                    hit('bongo', b, 4 + k * 0.5, BONGO_HI if k % 2 == 0 else BONGO_LO, 92 + k * 4, S16 - 2)
        elif sec.startswith('M'):
            for e8, nt, v in ((0, BELL_MOUTH, 110), (2, BELL_HEEL, 82), (4, BELL_MOUTH, 106), (6, BELL_HEEL, 82),
                              (7, BELL_HEEL, 62)):
                hit('bongo', b, e8, nt, v, E - 6)
        # timbales: cascara (A, coro-opbouw, solo's), campana (mambo)
        if sec in ('intro', 'A1', 'A2', 'B4', 'P', 'D2') and not ending:
            for e8 in ((0, 2, 4, 5, 7) if b % 2 == 0 else (0, 2, 3, 5, 7)):
                v = 92 if e8 in clave_pos(b) else 64
                hit('timb', b, e8, CASCARA, v - (16 if sec == 'B4' else 0), S16)
        if sec.startswith('M'):
            for e8, v in ((0, 112), (2, 86), (3, 70), (4, 106), (6, 86), (7, 70)):
                hit('timb', b, e8, CAMPANA, v + (6 if sec in ('M3', 'M4') else 0), E - 4)
        # güiro: PSG-ruis in A en de mambo (lang-kort-kort), sample in de pianosolo/descarga
        if sec in ('A1', 'A2') or sec.startswith('M') or b in (2, 3, END - 1):
            if b != corte:
                for beat in range(4):
                    s = b * BAR + beat * TPB
                    parts['noise'] += [[s, s + 18, 76, 72], [s + E, s + E + 8, 79, 48], [s + E + S16, s + E + S16 + 8, 79, 48]]
        elif sec in ('P', 'D1', 'D2'):
            for beat in range(4):
                hit('clave', b, beat * 2, GUIRO_L, 70 if beat % 2 == 0 else 58, E - 4)
                hit('clave', b, beat * 2 + 1, GUIRO_S, 52, S16 - 2)
        # maracas (PSG-ruis): intro, coro, solo's
        if sec in ('intro', 'B12', 'B3', 'B4', 'P', 'D1', 'D2') and b not in (2, 3):
            for e8 in range(8):
                s = b * BAR + e8 * E
                parts['noise'].append([s, s + 6, 88, 70 if e8 % 2 == 0 else 46])
                parts['noise'].append([s + S16, s + S16 + 4, 91, 30])
        # fills
        rel = b - A0
        if A0 <= b < K0 and rel % 4 == 3 and b + 1 not in (B0, P0, D0, M0, K0) and b != corte \
                and sec not in ('B12', 'B3', 'D1'):
            for k, nt in enumerate((MACHO, MACHO, HEMBRA, HEMBRA)):    # kleine fill elke 4 maten
                hit('timb', b, 6 + k * 0.5, nt, 84 + k * 6)
        if b + 1 in (P0, M0, K0) or b == D0 + 3:                       # grote fill naar een nieuwe sectie
            for k in range(8):
                hit('timb', b, 4 + k * 0.5, [MACHO, HEMBRA][k // 4] if k < 7 else RIM, 80 + k * 6)
        if b in (A0, P0, M0, M0 + 8, D0 + 4) or (sec in ('M3', 'M4') and b % 2 == 0 and b != M0 + 8):
            hit('timb', b, 0, CRASH, 112 if b in (A0, M0, M0 + 8) else 96, E)
            hit('timb', b, 0, RIM, 112)
        if b in (B0 + 8, B0 + 12):
            abanico(b - 1)

    # programma's van het ruisspoor: güiro (121) of maracas (122) per sectie
    prog_cc, last = [], None
    for b in range(END):
        sec = section(b)
        pr = GUIRO_PSG if (sec in ('A1', 'A2') or sec.startswith('M') or b in (2, 3, END - 1)) else MARACAS
        if pr != last or b == A0:
            prog_cc.append((b * BAR, 'prog', pr))
            last = pr

    for k in list(parts):
        parts[k] = dedupe(parts[k])

    write_voicegroup()
    rel = releases(VG)
    melodic = {'tpt': TRUMPET, 'tpt2': TRUMPET, 'trb': TROMBONE, 'trb2': TROMBONE, 'trb3': TROMBONE, 'piano': PIANO,
               'bass': BASS, 'cuatro': CUATRO, 'coro': CORO, 'gtr': GUITAR}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in melodic.items()}
    for k in ('bongo', 'conga', 'timb', 'clave'):
        tail[k] = 2
    for k in ('tpt', 'tpt2', 'trb', 'trb2', 'trb3', 'bass', 'coro', 'cuatro', 'gtr'):
        parts[k] = detach(parts[k], tail[k])
    # stemverdeler: melodie > trombones > koor/cuatro > bas > timbales > montuno > conga/bongó > tweede stemmen
    # v3: de gitaar als laatste (laagste prioriteit): hij wijkt, de bestaande partijen blijven exact zoals in v2
    order = ['trb', 'tpt', 'coro', 'cuatro', 'bass', 'timb', 'trb2', 'piano', 'trb3', 'clave', 'conga', 'bongo', 'tpt2',
             'gtr']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail)
    print('tail (ticks):', tail)
    for k in order:
        n = len(ds[k])
        gone = sorted({e[0] // BAR for e in ds[k] if e not in kept[k]})
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1),
                                                             ' maten %s' % gone if gone else ''))
        parts[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (A0 * BAR, END * BAR)
    for ch, (k, prog, vol, pan) in enumerate(TRACKS):
        ccs, lastv = [], None
        for b in range(END):
            sec = section(b)
            g = GAIN_OVR.get((k, sec), GAIN[sec])
            if sec == 'B4':                                             # crescendo naar de pianosolo
                g *= 0.92 + 0.04 * (b - (B0 + 12))
            v = round(vol * g)
            if v != lastv or b == A0 or (b and section(b) != section(b - 1)):   # elke sectie (en het loopbegin) opnieuw
                ccs.append((b * BAR, 7, v))
                lastv = v
        if k in ('trb', 'trb2', 'trb3'):                                # swell naar de mambo (maat 46.5-47)
            ccs = [c for c in ccs if not (M0 - 2) * BAR < c[0] < M0 * BAR]
            for j in range(13):
                ccs.append((swell + j * (M0 * BAR - swell) // 13, 7, round(vol * (0.35 + 0.65 * j / 12))))
        if k == 'noise':
            ccs += prog_cc
        extra = gtr_bends(parts['gtr'], gfx) if k == 'gtr' else ()
        song.add(parts[k], prog, ccs[0][2] if ccs and ccs[0][0] == 0 else vol, ch, pan, extra=extra,
                 ccs=[c for c in ccs if c[0] > 0 or c[1] == 'prog'])
    written = {k for k, *_ in TRACKS} | {'noise_prog'}
    assert not [k for k in parts if parts[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END * BAR)
    print(OUT, '%.1f s intro, %.1f s loop' % (A0 * 4 * 60 / BPM, (END - A0) * 4 * 60 / BPM))


def gtr_bends(notes, gfx):
    """Slides/bends (pitchwheel, BENDR 2 = een hele toon) en vibrato (CC1) voor de gitaar; alleen voor noten die de
    stemverdeler liet staan. Terugzetten pas op de volgende noot (anders zakt de uitklinkende staart mee)."""
    ev = [(0, mido.Message('control_change', control=20, value=2)), (0, mido.Message('pitchwheel', pitch=0)),
          (0, mido.Message('control_change', control=21, value=40)), (0, mido.Message('control_change', control=1, value=0))]
    notes = sorted(notes)
    for i, (s, e, n, v) in enumerate(notes):
        fx = gfx.get((s, n), '')
        if not fx:
            continue
        nxt = notes[i + 1][0] if i + 1 < len(notes) else e + TPB
        if 's' in fx or 'b' in fx:
            steps = 3 if 's' in fx else 6                               # slide snel, bend langzamer
            for k in range(1, steps + 1):
                ev.append((s + k * 2, mido.Message('pitchwheel', pitch=min(8191, round(8192 * k / steps)))))
            ev.append((nxt, mido.Message('pitchwheel', pitch=0)))
        if 'v' in fx and e - s > E:
            ev.append((s + E, mido.Message('control_change', control=1, value=36)))
            ev.append((nxt, mido.Message('control_change', control=1, value=0)))
    return ev


def bass_root(pc):
    """Grondtoon tussen G1 (31) en F#2 (42)."""
    n = 24 + pc
    while n < 31:
        n += 12
    return n


def fifth(pc):
    r = bass_root(pc)
    return r + 7 if r + 7 <= 43 else r - 5


def top(pc, lo, hi):
    n = pc
    while n < lo:
        n += 12
    return n if n < hi else n - 12


def montuno(parts, b, ch, nxt, vel, octaves=True):
    """Piano-montuno in octaven: 2-maats-cel, gesyncopeerd, de laatste achtste anticipeert de volgende akkoord."""
    tones = sorted(top(pc, 64, 76) for pc in CH[ch][:3])
    ntones = sorted(top(pc, 64, 76) for pc in CH[nxt][:3])
    if b % 2 == 0:
        cell = [(0, tones[1]), (2, tones[0]), (3, tones[2]), (5, tones[1])]
    else:
        cell = [(1, tones[2]), (2, tones[1]), (4, tones[0]), (5, tones[1])]
    last = cell[-1][1]
    cell.append((7, min(ntones, key=lambda n: abs(n - last))))
    for e8, nt in cell:
        s = b * BAR + e8 * E
        for o in ((0, 12) if octaves else (12,)):
            parts['piano'].append([s, s + 10, nt + o, vel + (8 if e8 in (2, 7) else 0)])


def write_voicegroup():
    """grounded_gm + piano met korte release (0), cuatro (24), trompet (56), trombone (57), güiro/maracas (121/122),
    salsa-drumkit (127)."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Keccles (salsa dura). Gegenereerd door tools/grounded/keccles_theme.py.'
    lines[1] = ('@ 0 = piano met korte release (montuno), 24 = cuatro, 56 = trompet, 57 = trombone (FluidR3), 121/122 = '
                'güiro/maracas (ruis), 127 = salsa-drumkit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 0': '\tvoice_keysplit voicegroup_keccles_piano_keysplit, keysplit_piano  @ 0',
        '@ 24': '\tvoice_directsound 60, 0, DirectSoundWaveData_kc_cuatro, 255, 0, 255, 140  @ 24',
        '@ 29': '\tvoice_keysplit voicegroup_keccles_guitar_keysplit, keysplit_french_horn  @ 29',
        '@ 56': '\tvoice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet  @ 56',
        '@ 57': '\tvoice_keysplit voicegroup_keccles_trombone_keysplit, keysplit_french_horn  @ 57',
        '@ 121': '\tvoice_noise_alt 60, 0, 0, 0, 2, 6, 0  @ 121',
        '@ 122': '\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 122',
        '@ 127': '\tvoice_keysplit_all voicegroup_keccles_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/keysplits/keccles_piano.inc', 'w').write(
        '@ Project Grounded: piano met korte release voor de montuno van Battle! Keccles (keccles_theme.py).\n'
        'voice_group keccles_piano_keysplit\n'
        + ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_piano1_%d, 255, 250, 0, 150\n' % k
                  for k in (48, 60, 72, 84)) + '\n')
    open('sound/voicegroups/keysplits/keccles_trombone.inc', 'w').write(
        '@ Project Grounded: trombone (FluidR3 GM 57, gm_samples.py) voor Battle! Keccles; tabel keysplit_french_horn\n'
        '@ (t/m noot 66 = sample op G3, daarboven = sample op G4). Korte release: salsa-stoten.\n'
        'voice_group keccles_trombone_keysplit\n'
        '\tvoice_directsound 55, 0, DirectSoundWaveData_kc_trombone_55, 255, 0, 255, 150\n'
        '\tvoice_directsound 67, 0, DirectSoundWaveData_kc_trombone_67, 255, 0, 255, 150\n\n')
    open('sound/voicegroups/keysplits/keccles_guitar.inc', 'w').write(
        '@ Project Grounded: elektrische gitaar met lichte overdrive (FluidR3 GM 29, keccles_samples.py) voor Battle!\n'
        '@ Keccles v3; tabel keysplit_french_horn (t/m noot 66 = sample op A3, daarboven = A4). Korte release: riffs.\n'
        'voice_group keccles_guitar_keysplit\n'
        '\tvoice_directsound 57, 0, DirectSoundWaveData_kc_guitar_57, 255, 0, 255, 150\n'
        '\tvoice_directsound 69, 0, DirectSoundWaveData_kc_guitar_69, 255, 0, 255, 150\n\n')
    kit = [   # vanaf noot 36; alles DirectSound (geen PSG-piepjes)
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0',          # 36 kick
        'voice_directsound 60, 64, DirectSoundWaveData_kc_claves, 255, 0, 255, 100',                            # 37 clave
        'voice_directsound 79, 88, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 80',             # 38 cascara
        'voice_directsound 60, 54, DirectSoundWaveData_kc_timbale_lo, 255, 0, 255, 140',                        # 39 timbal hembra
        'voice_directsound 60, 82, DirectSoundWaveData_kc_timbale_hi, 255, 0, 255, 140',                        # 40 timbal macho
        'voice_directsound_no_resample 64, 72, DirectSoundWaveData_sd90_cowbell, 255, 0, 255, 120',             # 41 campana
        'voice_directsound_no_resample 64, 54, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60',   # 42 conga slap
        'voice_directsound 60, 46, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                # 43 tumbadora open
        'voice_directsound 66, 58, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                # 44 conga open
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',     # 45 crash
        'voice_directsound 72, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 100',              # 46 rimshot
        'voice_directsound 60, 90, DirectSoundWaveData_kc_bongo_hi, 255, 0, 255, 80',                           # 47 bongó macho
        'voice_directsound 60, 84, DirectSoundWaveData_kc_bongo_lo, 255, 0, 255, 80',                           # 48 bongó hembra
        'voice_directsound 54, 88, DirectSoundWaveData_kc_cowbell, 255, 0, 255, 120',                           # 49 bongo-bel (mond)
        'voice_directsound 57, 88, DirectSoundWaveData_kc_cowbell, 255, 0, 255, 100',                           # 50 bongo-bel (hiel)
        'voice_directsound 60, 40, DirectSoundWaveData_kc_guiro_long, 255, 0, 255, 160',                        # 51 güiro lang
        'voice_directsound 62, 40, DirectSoundWaveData_kc_guiro_long, 255, 0, 255, 60',                         # 52 güiro kort
    ]
    open('sound/voicegroups/drumsets/keccles.inc', 'w').write(
        '@ Project Grounded: salsa-drumkit voor Battle! Keccles (keccles_theme.py): 36 kick, 37 clave, 38 cascara,\n'
        '@ 39/40 timbales (hembra/macho), 41 campana, 42 conga slap, 43 tumbadora, 44 conga open, 45 crash, 46 rimshot,\n'
        '@ 47/48 bongó (macho/hembra), 49/50 bongo-bel (mond/hiel), 51/52 güiro (lang/kort). kc_* = FluidR3 (gm_samples.py).\n'
        'voice_group keccles_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    build()
