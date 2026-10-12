#!/usr/bin/env python3
"""Project Grounded: "Battle! Burglar" (SIMON de inbreker, v0.9.3), eigen compositie: noir-jazz-heist.

Idee: op je tenen door een donker huis (swingende sluipmuziek: contrabas, vingerknippen, brushes, gedempte trompet,
baritonsax-stoten, vibrafoon), de kluis tikt, dan gaat het alarm af en wordt het een opgejaagde achtervolging
(sneller, recht, drums vol, alarmstoten), een halve toon hoger als climax, en daarna 'kwijt': terug op de tenen.
Eigen melodie (geen Pink Panther/Mission Impossible). Anti-kermis (MUZIEK.md, gymleiders ronde 3): geen blazers in
tertsen boven de melodie (de bari verdubbelt in octaven eronder), geen hoempa-bas (de bas springt nooit omhoog op de
'en'), geen PSG-tegenlijnen boven de melodie (PSG alleen: sirene in de twee alarmmaten, sinus-sub onder de bas).

D-klein. Tempo: 150 bpm (swing) -> accelerando -> 176 bpm (recht) -> ritardando -> 150.
  0-1    intro (3,2 s): alarmstoot + crash, vibrafoon-akkoord, knippen, sluipend basloopje naar de loop
Loop (maat 2-54, ±77 s):
  A  2-17   sluipen (swing): walking bass, knippen op 2 en 4, de melodie op de gedempte trompet (tiptoe-staccato,
            chromatisch kruipen, blue note Ab), bari antwoordt; tweede helft ride erbij en bari twee octaven lager mee
  B 18-25   de kluis: tik-tak (side stick), bas + bari unisono 'kraak'-riff (D D F Ab A C), trompet houdt de
            spanning vast; maat 24-25 ALARM: accelerando, tweetonige alarmstoten, PSG-sirene, roffel
  C 26-41   achtervolging (176, recht): drums vol, bas in achtsten (+ sinus-sub), melodie verkort en recht, bari
            een octaaf lager unisono, alarmstoten aan het eind van elke frase, tomfills
  C2 42-49  climax: hetzelfde een halve toon hoger (Es-klein), 16e-hats, extra kick
  D 50-53   kwijt: alleen hats + tiptoe-bas, trompetfragment, ritardando, knippen terug -> A
Voicegroup grounded_burglar (gegenereerd) = grounded_gm met eigen samples (burglar_samples.py): 11 vibrafoon,
32 contrabas, 59 gedempte trompet, 62 alarmstoot, 67 baritonsax, 80 sirene (PSG-vierkant), 81 sinus-sub (PSG-golf),
127 = drumkit drumsets/burglar.inc. Gebruik: python3 tools/grounded/burglar_theme.py [--render <map>]"""
import os, subprocess, sys, tempfile
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_burglar.mid'
VG = 'grounded_burglar'
TPB = 48
E = TPB // 2
BAR = TPB * 4
BPM_SLOW, BPM_FAST = 150, 176
VIBES, BASS, TPT, STAB, BARI, SIREN, SUB, DRUMS = 11, 32, 59, 62, 67, 80, 81, 127
# drumkit (drumsets/burglar.inc, vanaf 36)
KICK, BTAP, BSLAP, SNAP, RIDE, HAT, PHAT, OHAT, SNARE, RIM, CRASH, TOML, TOMH = range(36, 49)

INTRO, A0, B0, AL0, C0, C20, D0, END = 0, 2, 18, 24, 26, 42, 50, 54

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
     'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


CH = {'Dm': [2, 5, 9, 0], 'Gm': [7, 10, 2, 5], 'Bb7': [10, 2, 5, 8], 'A7': [9, 1, 4, 7], 'Eb7': [3, 7, 10, 1],
      'Bb': [10, 2, 5, 9]}
PROG = (['Dm', 'A7']
        + ['Dm', 'Dm', 'Gm', 'Gm', 'Bb7', 'A7', 'Dm', 'A7', 'Dm', 'Dm', 'Gm', 'Gm', 'Eb7', 'A7', 'Dm', 'Dm']   # A
        + ['Dm', 'Dm', 'Dm', 'Dm', 'Bb7', 'Bb7', 'A7', 'A7']                                               # B
        + ['Dm', 'Dm', 'Bb', 'A7', 'Dm', 'Dm', 'Gm', 'A7', 'Dm', 'Dm', 'Bb', 'A7', 'Dm', 'Dm', 'Eb7', 'Bb7']  # C
        + ['Dm', 'Dm', 'Bb', 'A7', 'Dm', 'Dm', 'Gm', 'A7']                                                 # C2 (+1)
        + ['Dm', 'Dm', 'Eb7', 'A7'])                                                                       # D
assert len(PROG) == END
SHIFT = [1 if C20 <= b < D0 + 2 else 0 for b in range(END)]          # C2 en het begin van D in Es-klein


def swing(b):
    return b < C0 - 2 or b >= D0 + 2                                  # intro, A, B swingen; alarm/C/C2/D-begin recht


def tick(b, pos):
    """achtste-positie (0-7, mag .5 = 16e) in maat b -> tick; swing: de 'en' op 2/3 van de tel."""
    beat, frac = divmod(pos, 2)
    t = b * BAR + int(beat) * TPB
    if swing(b) and frac:
        return t + (32 if frac == 1 else int(frac * TPB))
    return t + int(frac * E)


def section(b):
    for name, s in (('D', D0), ('C2', C20), ('C', C0), ('AL', AL0), ('B', B0), ('A2', A0 + 8), ('A1', A0), ('I', 0)):
        if b >= s:
            return name


# ---- melodie (gedempte trompet): (achtste, lengte in achtsten, noot); lengte 1 = staccato ------------------------------
M = {
    'M1': [(1, 1, 'D5'), (2, 1, 'C#5'), (3, 1, 'D5'), (4, 2, 'F5'), (6, 1, 'E5'), (7, 1, 'Eb5')],
    'M2': [(0, 3, 'D5'), (5, 1, 'A4'), (6, 1, 'Bb4'), (7, 1, 'B4')],
    'M3': [(0, 1, 'D5'), (1, 2, 'G5'), (3, 1, 'F5'), (4, 1, 'D5'), (5, 2, 'Bb4'), (7, 1, 'A4')],
    'M4': [(0, 4, 'G4'), (6, 1, 'G4'), (7, 1, 'Ab4')],
    'M5': [(0, 2, 'Ab4'), (2, 1, 'F4'), (3, 1, 'Ab4'), (4, 2, 'Bb4'), (6, 1, 'D5'), (7, 1, 'F5')],
    'M6': [(0, 1, 'G5'), (1, 1, 'F5'), (2, 1, 'E5'), (3, 2, 'C#5'), (5, 1, 'Bb4'), (6, 2, 'A4')],
    'M7': [(0, 2, 'D5'), (3, 1, 'F5'), (4, 1, 'A5'), (5, 1, 'Ab5'), (6, 1, 'G5'), (7, 1, 'F5')],
    'M8': [(0, 2, 'E5'), (2, 1, 'C#5'), (3, 3, 'A4')],
    'M5b': [(0, 2, 'Db5'), (2, 1, 'Bb4'), (3, 1, 'G4'), (4, 2, 'Eb5'), (6, 1, 'Db5'), (7, 1, 'C5')],
    'M6b': [(0, 1, 'Bb4'), (1, 1, 'A4'), (2, 1, 'C#5'), (3, 1, 'E5'), (4, 2, 'G5'), (6, 1, 'F5'), (7, 1, 'E5')],
    'M7b': [(0, 3, 'D5'), (3, 1, 'A4'), (4, 1, 'D5')],
    # B: de kluis (spanning vasthouden)
    'B2': [(0, 4, 'A4'), (4, 4, 'Bb4')],
    'B3': [(0, 6, 'A4')],
    'B4': [(4, 2, 'D5'), (6, 2, 'F5')],
    'B5': [(0, 3, 'Ab5'), (3, 1, 'F5'), (4, 4, 'D5')],
    'B6': [(0, 2, 'F5'), (2, 2, 'Ab5'), (4, 3, 'Bb5')],
    # C: achtervolging (recht, verkort motief)
    'C1': [(0, 1, 'D5'), (1, 1, 'C#5'), (2, 1, 'D5'), (3, 1, 'F5'), (4, 2, 'A5'), (6, 1, 'Ab5'), (7, 1, 'G5')],
    'C2': [(0, 1, 'F5'), (1, 1, 'E5'), (2, 2, 'D5'), (5, 1, 'A4'), (6, 1, 'C5'), (7, 1, 'D5')],
    'C3': [(0, 2, 'F5'), (2, 1, 'D5'), (3, 1, 'F5'), (4, 2, 'Bb5'), (6, 1, 'A5'), (7, 1, 'F5')],
    'C4': [(0, 2, 'E5'), (2, 1, 'C#5'), (3, 1, 'E5'), (4, 2, 'G5')],
    'C6': [(0, 1, 'F5'), (1, 1, 'E5'), (2, 1, 'D5'), (3, 1, 'C5'), (4, 2, 'A4'), (6, 1, 'Bb4'), (7, 1, 'C5')],
    'C7': [(0, 2, 'D5'), (2, 2, 'G5'), (4, 1, 'F5'), (5, 1, 'D5'), (6, 1, 'Bb4'), (7, 1, 'G4')],
    'C8': [(0, 1, 'A4'), (1, 1, 'C#5'), (2, 1, 'E5'), (3, 1, 'G5'), (4, 3, 'Bb5'), (7, 1, 'A5')],
    'C7b': [(0, 2, 'Eb5'), (2, 1, 'G5'), (3, 1, 'Bb5'), (4, 2, 'Ab5'), (6, 1, 'G5'), (7, 1, 'F5')],
    'C8b': [(0, 1, 'F5'), (1, 1, 'Gb5'), (2, 1, 'F5'), (3, 1, 'D5'), (4, 4, 'F5')],      # Bb7 -> Es-klein
    # D: kwijt
    'D1': [(1, 1, 'D5'), (2, 1, 'C#5'), (3, 1, 'D5'), (4, 2, 'F5')],                      # (+1 door SHIFT)
    'D2': [(0, 4, 'D5')],
    'D4': [(5, 1, 'A4'), (6, 1, 'C#5'), (7, 1, 'E5')],
}
MEL = {}
for i, k in enumerate(['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M1', 'M2', 'M3', 'M4', 'M5b', 'M6b', 'M7b', None]):
    MEL[A0 + i] = k
for i, k in enumerate([None, 'B2', 'B3', 'B4', 'B5', 'B6', None, None]):
    MEL[B0 + i] = k
CPH = ['C1', 'C2', 'C3', 'C4', 'C1', 'C6', 'C7', 'C8']
for i, k in enumerate(CPH + ['C1', 'C2', 'C3', 'C4', 'C1', 'C6', 'C7b', 'C8b']):
    MEL[C0 + i] = k
for i, k in enumerate(CPH):
    MEL[C20 + i] = k
for i, k in enumerate(['D1', 'D2', None, 'D4']):
    MEL[D0 + i] = k


def melody():
    out = []
    for b in range(END):
        k = MEL.get(b)
        if not k:
            continue
        fast = b >= AL0 and not swing(b)
        for pos, ln, nm in M[k]:
            s = tick(b, pos)
            if ln == 1:
                e = s + (14 if fast else 13)
            else:
                e = tick(b, pos + ln) if pos + ln < 8 else (b + 1) * BAR
                e -= 6
            acc = 10 if pos in (0, 4) or ln > 1 else 0
            out.append([s, e, p(nm) + SHIFT[b], 100 + acc])
    return out


# ---- bas ---------------------------------------------------------------------------------------------------------
def root(b, lo=33, hi=45):
    n = lo + (CH[PROG[b]][0] + SHIFT[b] - lo) % 12
    return n if n <= hi else n - 12


def walking(b):
    """4 kwarten: grondtoon, akkoordtonen, chromatische nadering van de volgende grondtoon (swing, kort aangezet)."""
    r = root(b, 36, 47)
    pcs = CH[PROG[b]]
    third = r + (pcs[1] - pcs[0]) % 12
    fifth = r + (pcs[2] - pcs[0]) % 12
    nxt = root(b + 1, 36, 47) if b + 1 < END else root(A0, 36, 47)
    appr = nxt + (1 if (b % 2) else -1)
    line = [r, third if b % 2 else fifth, fifth if b % 2 else r + 12 if r + 12 <= 50 else third, appr]
    return [(i * 2, n) for i, n in enumerate(line)]


def bass():
    out = []
    for b in range(END):
        sec = section(b)
        if b == 0:
            out += [[tick(b, 0), tick(b, 0) + 40, 38, 112]]                        # D2 onder de stoot
            continue
        if b == 1:                                                                  # sluipend loopje naar de loop
            for pos, n in ((3, 'A1'), (4, 'Bb1'), (5, 'B1'), (6, 'C2'), (7, 'C#2')):
                s = tick(b, pos)
                out.append([s, s + 14, p(n), 100])
            continue
        if sec in ('A1', 'A2') or b >= D0 + 2:
            for pos, n in walking(b):
                s = tick(b, pos)
                out.append([s, s + 34, n, 112 if pos == 0 else 104])
        elif sec == 'B':
            r = 38 if PROG[b] == 'Dm' else 34                                       # D2 / Bb1
            for pos, iv in ((0, 0), (2, 0), (3, 3), (5, 6), (6, 7), (7, 10)):
                s = tick(b, pos)
                out.append([s, s + 14, r + iv, 116 if pos == 0 else 106])
        elif sec == 'AL':                                                           # alarm: achtsten op A, dan omhoog
            seq = [33] * 8 if b == AL0 else [33, 33, 34, 34, 35, 35, 36, 37]
            for pos, n in enumerate(seq):
                s = tick(b, pos)
                out.append([s, s + 16, n, 110 + (6 if pos % 2 == 0 else 0)])
        elif sec in ('C', 'C2'):
            r = root(b, 33, 44)
            nxt = root(b + 1, 33, 44) if b + 1 < D0 else root(b, 33, 44)
            appr = nxt - 1 if nxt - 1 != r + 7 else nxt + 1
            line = [r, r, r + 12, r + 10, r, r, r + 7, appr]
            for pos, n in enumerate(line):
                s = tick(b, pos)
                out.append([s, s + 16, n, 118 if pos in (0, 4) else 104])
        elif sec == 'D':                                                            # kwijt: tiptoe
            r = root(b, 36, 47)
            for pos, n in ((0, r), (3, r), (6, r + 1)):
                s = tick(b, pos)
                out.append([s, s + 14, n, 100])
    return out


def sub(bass_notes):
    """Sinus-sub (PSG-golf, ProgrammableWaveData_1 = op toonhoogte) in de achtervolging: grondtoon per kwart, >= C2."""
    out = []
    for b in range(C0, D0):
        r = root(b, 36, 47)
        for q in range(4):
            s = b * BAR + q * TPB
            out.append([s, s + TPB - 6, r, 100])
    return out


# ---- bari (onder de melodie: antwoorden, unisono-riff, octaafverdubbeling) -----------------------------------------
BARI_ANS = {A0 + 3: [(3, 1, 'G2'), (4, 2, 'Bb2')], A0 + 7: [(5, 1, 'A2'), (6, 1, 'C3'), (7, 1, 'C#3')],
            A0 + 15: [(0, 1, 'D3'), (2, 1, 'F3'), (3, 1, 'Ab3'), (4, 2, 'A3'), (7, 1, 'A2')]}


def bari(mel, bass_notes):
    out = []
    for b, pat in BARI_ANS.items():
        for pos, ln, nm in pat:
            s = tick(b, pos)
            e = s + 13 if ln == 1 else tick(b, pos + ln) - 6
            out.append([s, e, p(nm), 104])
    for s, e, n, v in mel:
        b = s // BAR
        if A0 + 8 <= b < A0 + 14:
            out.append([s, e, n - 24, v - 8])                                       # twee octaven lager mee
        elif C0 <= b < D0:
            out.append([s, e, n - 12, v - 6])                                       # unisono een octaaf lager
    for s, e, n, v in bass_notes:                                                   # kraak-riff unisono met de bas
        if section(s // BAR) == 'B':
            out.append([s, e, n + 12, v - 4])
    return dedupe(out)


# ---- alarmstoten (1 sample per voicing; noot 62 = D3+D4/Ab4/C#5) --------------------------------------------------
def stabs():
    out = []

    def hit(b, pos, ln, key, v=112):
        s = tick(b, pos)
        out.append([s, s + ln * E - 4, key + SHIFT[b], v])
    hit(0, 0, 3, 62, 120)                                                           # intro: betrapt!
    for b in (AL0, AL0 + 1):                                                        # het alarm: tweetonig
        pats = [(0, 2), (2, 2), (4, 2), (6, 2)] if b == AL0 else [(0, 2), (2, 2), (4, 1), (5, 1), (6, 1), (7, 1)]
        for i, (pos, ln) in enumerate(pats):
            hit(b, pos, ln, 61 if i % 2 == 0 else 63)
    for b in range(C0, D0):
        i = (b - C0) % 8
        k = 61 if PROG[b] == 'A7' else 62
        if i == 3:
            hit(b, 6, 1, k); hit(b, 7, 1, k)
        if i == 7:
            hit(b, 4, 2, k, 116); hit(b, 6, 2, k + 2 if PROG[b] == 'A7' else k, 116)
    return out


def siren():
    """PSG-sirene in de twee alarmmaten: één noot A4 met een pitch-bend-golf (0 -> +5 halve tonen -> 0 per 2 tellen)."""
    s, e = AL0 * BAR, (AL0 + 2) * BAR - 6
    ev = [(0, mido.Message('control_change', control=20, value=12)), (0, mido.Message('pitchwheel', pitch=0))]
    for t in range(s, e, 4):
        ph = ((t - s) % (2 * TPB)) / (2 * TPB)
        semis = 5 * (ph * 2 if ph < 0.5 else 2 - ph * 2)
        ev.append((t, mido.Message('pitchwheel', pitch=min(8191, round(8192 * semis / 12)))))
    ev.append((e + 2, mido.Message('pitchwheel', pitch=0)))
    return [[s, e, 69, 100]], ev


# ---- vibrafoon (shells onder de melodie) --------------------------------------------------------------------------
def vibes(mel):
    out = []

    def place(pc, lo=55, hi=66):
        n = lo + (pc - lo) % 12
        return n if n <= hi else n - 12
    for b in range(END):
        sec = section(b)
        pcs = [(x + SHIFT[b]) % 12 for x in CH[PROG[b]]]
        shell = sorted({place(pcs[1]), place(pcs[3])})
        if b == 0:
            hits = [(4, 4)]
            shell = sorted({place(pcs[0]), place(pcs[1]), place(pcs[2]), place(1)})   # Dm(maj7): de 'noir'-klank
        elif sec in ('A1', 'A2'):
            hits = [(0, 2), (3, 1)] if (b - A0) % 2 == 0 else [(1, 1), (3, 2)]       # charleston / antwoord
            if b < A0 + 2:
                hits = [(0, 3)]
        elif sec == 'B' and b < AL0:
            hits = [(0, 6)] if (b - B0) % 2 == 0 else []
        elif sec == 'D':
            hits = [(0, 6)] if b < D0 + 2 else [(0, 2), (3, 1)]
        else:
            hits = []
        for pos, ln in hits:
            s = tick(b, pos)
            e = (tick(b, pos + ln) if pos + ln < 8 else (b + 1) * BAR) - 6
            low = min([n for ms, me, n, _ in mel if ms < e and me > s] or [127])
            for n in shell:
                if n < low - 1:
                    out.append([s, e, n, 84 if ln == 1 else 78])
    return out


# ---- drums --------------------------------------------------------------------------------------------------------
def drums():
    d = {k: [] for k in ('kick', 'snare', 'cym', 'crash', 'perc')}

    def hit(part, b, pos, note, vel, ln=None):
        s = tick(b, pos)
        L = ln if ln is not None else {KICK: 20, BTAP: 16, BSLAP: 20, SNAP: 8, RIDE: 24, HAT: 6, PHAT: 8, OHAT: 24,
                                       SNARE: 20, RIM: 8, CRASH: 96, TOML: 18, TOMH: 18}[note]
        d[part].append([s, s + L, note, vel])
    for b in range(END):
        sec = section(b)
        k8 = (b - C0) % 8 if sec in ('C', 'C2') else None
        if b == 0:
            hit('crash', b, 0, CRASH, 110); hit('kick', b, 0, KICK, 120)
            hit('perc', b, 4, BSLAP, 70)
        elif b == 1:
            for pos in (2, 6):
                hit('perc', b, pos, SNAP, 110)
            hit('kick', b, 7, KICK, 70)
        elif sec in ('A1', 'A2') or b >= D0 + 2:
            for pos in (2, 6):
                hit('perc', b, pos, SNAP, 112)
                hit('cym', b, pos, PHAT, 70)
            hit('kick', b, 0, KICK, 78)
            if sec == 'A2' or b >= D0 + 2:
                for pos, v in ((0, 84), (2, 92), (3, 66), (4, 84), (6, 92), (7, 66)):
                    hit('cym', b, pos, RIDE, v)
                hit('kick', b, 4, KICK, 66)
            else:
                hit('snare', b, 7, BTAP, 64)
            if (b - A0) % 8 == 7:
                hit('snare', b, 6, BSLAP, 96); hit('snare', b, 7, BTAP, 80)
            if b == A0 + 8:
                hit('crash', b, 0, CRASH, 80)
        elif sec == 'B':
            for pos in (0, 2, 4, 6):
                hit('perc', b, pos, RIM, 100 if pos % 4 == 0 else 84)                # tik-tak van de kluis
            hit('kick', b, 0, KICK, 104); hit('kick', b, 5, KICK, 84)
            for pos in (2, 6):
                hit('cym', b, pos, PHAT, 72)
            if b in (B0 + 3, B0 + 5):
                hit('snare', b, 6, BSLAP, 104); hit('snare', b, 7, BSLAP, 92)
            if b == B0 + 4:
                hit('crash', b, 0, CRASH, 84)
        elif sec == 'AL':
            if b == AL0:
                hit('crash', b, 0, CRASH, 116)
            for q in range(4):
                hit('kick', b, q * 2, KICK, 110)
            if b == AL0:                                                            # roffel: 8en -> 16en -> 32sten
                for i in range(8):
                    hit('snare', b, i, SNARE, 64 + i * 3, 20)
            else:
                for i in range(8):
                    hit('snare', b, i * 0.5, SNARE, 84 + i * 2, 11)
                for i in range(8):
                    hit('snare', b, 4 + i * 0.25, SNARE, 100 + i * 3, 5)
                hit('snare', b, 6, SNARE, 120, 5)
        elif sec in ('C', 'C2'):
            if k8 in (0, 4):
                hit('crash', b, 0, CRASH, 112 if k8 == 0 else 96)
            kicks = (0, 3, 4) if sec == 'C' else (0, 3, 4, 7)
            fill = k8 == 7
            for pos in kicks:
                if not (fill and pos > 4):
                    hit('kick', b, pos, KICK, 124 if pos in (0, 4) else 108)
            for pos in (2, 6):
                if not (fill and pos == 6):
                    hit('snare', b, pos, SNARE, 120)
            hats = [x * 0.5 for x in range(16)] if sec == 'C2' else list(range(8))
            for pos in hats:
                if fill and pos >= 4:
                    continue
                if k8 == 0 and pos == 0:
                    continue
                v = 96 if pos % 2 == 0 else (72 if pos % 1 == 0 else 58)
                if pos == 7 and k8 == 3:
                    hit('cym', b, pos, OHAT, 88)
                else:
                    hit('cym', b, pos, HAT, v)
            if fill:                                                                # tomfill in de laatste 2 tellen
                for i, (pos, n) in enumerate(((4, SNARE), (4.5, SNARE), (5, TOMH), (5.5, TOMH), (6, TOML), (6.5, TOML),
                                              (7, SNARE), (7.5, SNARE))):
                    hit('perc', b, pos, n, 100 + i * 3, 11)
        elif sec == 'D':
            for pos in range(8):
                hit('cym', b, pos, HAT, 80 if pos % 2 == 0 else 60)
            hit('kick', b, 0, KICK, 96)
    return {k: dedupe(v) for k, v in d.items()}


# ---- dynamiek -----------------------------------------------------------------------------------------------------
TRACKS = [   # naam, programma, basisvolume, pan
    ('tpt', TPT, 112, 70), ('bass', BASS, 112, 64), ('kick', DRUMS, 112, 64), ('snare', DRUMS, 100, 60),
    ('stab', STAB, 104, 64), ('bari', BARI, 96, 54), ('crash', DRUMS, 78, 76), ('cym', DRUMS, 74, 78),
    ('perc', DRUMS, 90, 50), ('vibes', VIBES, 74, 84), ('siren', SIREN, 44, 64), ('sub', SUB, 64, 64),
]
GAIN = {'I': 1.0, 'A1': .84, 'A2': .90, 'B': .92, 'AL': 1.0, 'C': 1.0, 'C2': 1.0, 'D': .86}
GAIN_OVR = {('bass', 'A1'): 1.0, ('bass', 'A2'): 1.0, ('bass', 'B'): 1.0, ('perc', 'A1'): 1.0, ('vibes', 'D'): 1.0}


def tempo_map(song):
    song.tempo(0, BPM_SLOW / 120)
    song.tempo(A0 * BAR, BPM_SLOW / 120)                       # op de looptick zelf (MUZIEK.md, Heatran v5)
    acc = [152, 154, 158, 160, 164, 166, 170, 174]             # accelerando in de alarmmaten, per tel
    for i, bpm in enumerate(acc):
        song.tempo(AL0 * BAR + i * TPB, bpm / 120)
    song.tempo(C0 * BAR, BPM_FAST / 120)
    rit = [172, 168, 164, 162, 158, 156, 154, 152]             # ritardando in de laatste twee maten van D
    for i, bpm in enumerate(rit):
        song.tempo((D0 + 2) * BAR + i * TPB, bpm / 120)


def build(render_dir=None):
    write_voicegroup()
    rel = releases(VG)
    kitrel = kit_releases()
    mel = melody()
    bs = bass()
    parts = {'tpt': mel, 'bass': bs, 'bari': bari(mel, bs), 'stab': stabs(), 'vibes': vibes(mel)}
    parts.update(drums())
    sn, siren_ev = siren()
    parts['siren'] = sn
    parts['sub'] = sub(bs)
    melodic = {'tpt': TPT, 'bass': BASS, 'bari': BARI, 'stab': STAB, 'vibes': VIBES}
    # uitklinktijden met het snelste tempo (meeste ticks per frame) + 2 ticks marge (MUZIEK.md, Victini)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM_FAST) + 2 for k, pr in melodic.items()}
    for k in ('kick', 'snare', 'cym', 'crash', 'perc'):
        tail[k] = max(release_ticks(r, TPB, BPM_FAST) for r in kitrel.values()) // 2
    for k in ('tpt', 'bass', 'bari', 'vibes', 'stab'):
        parts[k] = detach(parts[k], tail[k])
    order = ['tpt', 'bass', 'kick', 'snare', 'crash', 'stab', 'bari', 'perc', 'cym', 'vibes']
    kept = allocate({k: parts[k] for k in order}, order, tail)
    print('uitklinktijd (ticks):', tail)
    for k in order:
        n = len(parts[k])
        gone = sorted({e[0] // BAR for e in parts[k] if e not in kept[k]})
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1),
                                                             ' maten %s' % gone if gone else ''))
        parts[k] = kept[k]
    anti_kermis(parts)

    song = Song(TPB, 500000)
    tempo_map(song)
    song.loop = (A0 * BAR, END * BAR)
    for ch, (k, prog, vol, pan) in enumerate(TRACKS):
        ccs, lastv = [], None
        for b in range(END):
            sec = section(b)
            v = round(vol * GAIN_OVR.get((k, sec), GAIN[sec]))
            if v != lastv or b == A0:
                ccs.append((b * BAR, 7, v))
                lastv = v
        extra = siren_ev if k == 'siren' else ()
        song.add(parts[k], prog, ccs[0][2], ch, pan, extra=extra, ccs=[c for c in ccs if c[0] > 0])
    song.save(OUT, END * BAR)
    secs = lambda b0, b1, bpm: (b1 - b0) * 4 * 60 / bpm
    print(OUT, 'intro %.1f s, loop ±%.1f s' % (secs(0, A0, BPM_SLOW), secs(A0, C0, BPM_SLOW) + secs(C0, END, BPM_FAST) + 1.5))
    if render_dir:
        render_gm(parts, render_dir)


def anti_kermis(parts):
    """Controles uit de kermis-lessen: geen begeleiding boven de melodie, geen hoempa-sprongen in de bas."""
    mel = parts['tpt']
    above = 0
    for k in ('bari', 'vibes', 'stab', 'siren'):
        for s, e, n, v in parts[k]:
            top = n + (11 if k == 'stab' else 0)                       # stoot: bovenste toon C#5 boven de sample-toets
            if k == 'siren':
                continue                                                # sirene: alleen in de alarmmaten (melodie rust)
            for ms, me, mn, _ in mel:
                if ms < e and me > s and top > mn:
                    above += 1
                    print('  boven de melodie: %s maat %d noot %d (melodie %d)' % (k, s // BAR, n, mn))
                    break
    hoempa = 0
    bs = sorted(parts['bass'])
    for a, b2 in zip(bs, bs[1:]):
        if (b2[0] % TPB) and b2[2] - a[2] >= 5:                        # sprong omhoog op een 'en'
            hoempa += 1
    sir_overlap = sum(1 for s, e, *_ in parts['siren'] for ms, me, *_ in mel if ms < e and me > s)
    print('anti-kermis: begeleiding boven de melodie %d, hoempa-sprongen %d, sirene tijdens melodie %d'
          % (above, hoempa, sir_overlap))
    assert above == 0 and hoempa <= len(bs) * 0.02 and sir_overlap == 0, 'kermis!'


def kit_releases():
    return {i: int(l.split(',')[-1]) for i, l in enumerate(KIT)}


KIT = [   # vanaf noot 36; alles DirectSound
    'voice_directsound 60, 0, DirectSoundWaveData_bg_kick, 255, 0, 255, 160',        # 36 kick
    'voice_directsound 60, 0, DirectSoundWaveData_bg_brush_tap, 255, 0, 255, 150',   # 37 brush tap
    'voice_directsound 60, 0, DirectSoundWaveData_bg_brush_slap, 255, 0, 255, 160',  # 38 brush slap
    'voice_directsound 60, 0, DirectSoundWaveData_bg_snap, 255, 0, 255, 100',        # 39 vingerknip
    'voice_directsound 60, 0, DirectSoundWaveData_bg_ride, 255, 0, 255, 190',        # 40 ride
    'voice_directsound 60, 0, DirectSoundWaveData_bg_hat, 255, 0, 255, 100',         # 41 hihat dicht
    'voice_directsound 60, 0, DirectSoundWaveData_bg_hat_pedal, 255, 0, 255, 110',   # 42 hihat pedaal
    'voice_directsound 60, 0, DirectSoundWaveData_bg_hat_open, 255, 0, 255, 150',    # 43 hihat open
    'voice_directsound 60, 0, DirectSoundWaveData_bg_snare, 255, 0, 255, 160',       # 44 snare
    'voice_directsound 60, 0, DirectSoundWaveData_bg_rim, 255, 0, 255, 100',         # 45 side stick
    'voice_directsound 60, 0, DirectSoundWaveData_bg_crash, 255, 0, 255, 200',       # 46 crash
    'voice_directsound 60, 0, DirectSoundWaveData_bg_tom_lo, 255, 0, 255, 160',      # 47 tom laag
    'voice_directsound 60, 0, DirectSoundWaveData_bg_tom_hi, 255, 0, 255, 160',      # 48 tom hoog
]


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Burglar (noir-jazz-heist). Gegenereerd door tools/grounded/burglar_theme.py.'
    lines[1] = ('@ 11 vibrafoon, 32 contrabas, 59 gedempte trompet, 62 alarmstoot, 67 baritonsax (bg_*, burglar_samples.py), '
                '80 sirene (PSG), 81 sinus-sub (PSG-golf), 127 = drumkit burglar.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 11': '\tvoice_directsound 60, 0, DirectSoundWaveData_bg_vibes, 255, 0, 255, 200  @ 11',
        '@ 32': '\tvoice_directsound 60, 0, DirectSoundWaveData_bg_upright, 255, 0, 255, 170  @ 32',
        '@ 59': '\tvoice_directsound 60, 0, DirectSoundWaveData_bg_mtpt, 255, 0, 255, 165  @ 59',
        '@ 62': '\tvoice_directsound 60, 0, DirectSoundWaveData_bg_stab, 255, 0, 255, 150  @ 62',
        '@ 67': '\tvoice_directsound 60, 0, DirectSoundWaveData_bg_bari, 255, 0, 255, 160  @ 67',
        '@ 80': '\tvoice_square_1 60, 0, 0, 2, 0, 0, 15, 2  @ 80',
        '@ 81': '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 1  @ 81',
        '@ 127': '\tvoice_keysplit_all voicegroup_burglar_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/drumsets/burglar.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Burglar (burglar_theme.py): 36 kick, 37/38 brushes (tap/slap), 39 knip,\n'
        '@ 40 ride, 41-43 hihat (dicht/pedaal/open), 44 snare, 45 side stick, 46 crash, 47/48 toms. bg_* = burglar_samples.py.\n'
        'voice_group burglar_drumset, 36\n' + ''.join('\t%s\n' % k for k in KIT) + '\n')


# ---- offline-render (FluidR3 GM; benadering: andere klanken dan de GBA, wel noten/vorm/tempo) ----------------------
GM_DRUM = {KICK: 36, BTAP: 38, BSLAP: 38, SNAP: 39, RIDE: 51, HAT: 42, PHAT: 44, OHAT: 46, SNARE: 40, RIM: 37,
           CRASH: 49, TOML: 45, TOMH: 48}
GM_DRUM_VEL = {BTAP: .55, BSLAP: .7, SNAP: .6}


def render_gm(parts, outdir):
    m = mido.MidiFile(OUT)
    gm = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    gm.tracks.append(m.tracks[0])
    progs = {'tpt': 59, 'bass': 32, 'stab': 61, 'bari': 67, 'vibes': 11, 'siren': 80, 'sub': 38}
    free = [c for c in range(16) if c != 9]
    for i, (k, prog, vol, pan) in enumerate(TRACKS):
        src = m.tracks[i + 1]
        drum = prog == DRUMS
        ch = 9 if drum else free.pop(0)
        t = mido.MidiTrack()
        for x in src:
            if x.type == 'program_change':
                x = x.copy(channel=ch, program=32 if drum else progs[k])
            elif x.type in ('note_on', 'note_off'):
                if drum:
                    vel = int(x.velocity * GM_DRUM_VEL.get(x.note, 1)) if x.velocity else 0
                    x = x.copy(channel=ch, note=GM_DRUM[x.note], velocity=max(1, vel) if x.velocity else 0)
                else:
                    x = x.copy(channel=ch)
            elif hasattr(x, 'channel'):
                x = x.copy(channel=ch)
            t.append(x)
        gm.tracks.append(t)
    os.makedirs(outdir, exist_ok=True)
    mid = os.path.join(outdir, 'burglar_gm.mid')
    gm.save(mid)
    wav = os.path.join(outdir, 'burglar_fluidr3.wav')
    subprocess.run(['fluidsynth', '-ni', '-g', '0.6', '-r', '44100', '-F', wav, '/usr/share/sounds/sf2/FluidR3_GM.sf2', mid],
                   check=True, capture_output=True)
    mp3 = os.path.join(outdir, 'burglar_fluidr3.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-b:a', '160k', mp3], check=True)
    os.remove(wav)
    print('render:', mp3)


if __name__ == '__main__':
    rd = sys.argv[sys.argv.index('--render') + 1] if '--render' in sys.argv else None
    build(rd)
