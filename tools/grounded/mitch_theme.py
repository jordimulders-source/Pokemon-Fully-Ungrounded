#!/usr/bin/env python3
"""Project Grounded: Battle! Mitch, een eigen compositie in Drum & Bass (Jordi: "Mitch in Victory Road is gebaseerd
op een maat van mij en die is helemaal gek op Drum & Bass, dus daar moeten we een heel vet Drum & Bass battle theme
voor bouwen"). Richting: Pendulum ('Slam', 'Blood Sugar'), Netsky/Sub Focus-energie, wat neurofunk-gegrom.

174 bpm, F-klein. 1 tel = 20,7 frames, 1 maat = 1,38 s. Akkoorden van de drop (8 maten): Fm Fm Db Eb Fm Fm Db C.
Hook = de reese-riff (maat a: F1 lang, 'grom' op de 7e zestiende, Ab1, F1, C2) met per noot een andere klankkleur
(dicht/half/open filter, grom) = de 'pratende' bas; in de tweede helft van elke drop een zaagtandlead erboven.

Intro (8 maten, 11,0 s)
  0-3   pad (Fm Fm Db Eb), PSG-arpeggio, sub; vanaf maat 2 hihats; stoot + crash op de eerste tel
  4-6   de break valt in (two-step zonder ghosts), reese-hook met dicht filter (teaser)
  7     opbouw: snareroffel 8sten -> 16den, ruisriser, sirene, reverse crash, laatste achtste stil
Loop (48 maten, 66,2 s; maat 55 = maat 7, dus de terugsprong klinkt als intro -> drop)
  8-23  DROP 1: break met ghost notes en amen-chops, reese-hook, sub, synthstoten; 16-23 + lead, ride, hoornstoten
  24-27 breakdown: pad (Db Ab Eb C), 'aah'-koor, arpeggio, sub
  28-31 opbouw: koor, kick in kwarten -> snareroffel, riser, sirene, reverse crash
  32-33 valse drop: de hook voluit ...
  34    ... DJ-REWIND (de plaat wordt teruggetrokken), stilte
  35    luchthoorn (BWAP BWAP BWAAAP) + roffel
  36-43 DROP 2a: halftime, wobble-bas (filter-LFO in de sample: kwarten/achtsten/16den/triolen), hoorn + clap
  44-51 DROP 2b: terug naar dubbeltempo, amen-break, reese met meer grom, lead + hoornstoten, ride
  52-54 alleen break + reese (terug naar drop 1)
  55    = maat 7 (opbouw), loop terug naar maat 8
Max. 10 DirectSound-noten (gewone trainer): de stemverdeler houdt bas en drums voorop. PSG (kost niets): sub
(golfkanaal), hihats/riser (ruis), arpeggio (vierkant 2), sirene (vierkant 1).
Voicegroup grounded_mitch = grounded_gm + eigen samples (mitch_samples.py) + eigen drumkit (drumsets/mitch.inc,
alles DirectSound). Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/mitch_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_mitch.mid'
VG = 'grounded_mitch'
TPB, BPM = 96, 174
S = TPB // 4                 # zestiende
E = TPB // 2                 # achtste
BAR = TPB * 4
MAX_VOICES = 10              # gewone trainer

# programma's (voicegroup grounded_mitch)
REESE = {'dark': 32, 'mid': 33, 'bright': 34, 'growl': 35}
WOB = {29: 36, 32: 37, 36: 38, 37: 39, 39: 40}          # grondtoon -> wobble-sample
LEAD, STAB_MIN, STAB_MAJ, HORN_MIN, HORN_MAJ, PAD_MIN, PAD_MAJ, AAH = 92, 90, 91, 61, 62, 88, 89, 52
SIREN, ARP, SUB, HATS, RISER, DRUMS = 80, 81, 84, 120, 121, 127
# drumkit (drumsets/mitch.inc, vanaf 36): noot -> (sample, release)
KIT = [
    ('KICK', 'mitch_kick', 190),
    ('SNARE', 'mitch_snare', 200),
    ('GHOST', 'mitch_ghost', 150),
    ('RIDE', 'mitch_ride', 210),
    ('CRASH', 'trinity_cymbal_crash', None),
    ('REVCYM', 'mitch_revcym', 120),
    ('REWIND', 'mitch_rewind', 160),
    ('HORN', 'mitch_airhorn', 190),
    ('CLAP', 'sc88pro_tr909_hand_clap', 180),
    ('ROLL', 'mitch_snare', 140),
]
for i, (nm, _, _) in enumerate(KIT):
    globals()[nm] = 36 + i

INTRO = 8
LOOP_START, LOOP_END = INTRO * BAR, 56 * BAR
NOTE = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def n(name):
    """'F1' -> 29, 'Ab4' -> 68"""
    return NOTE[name[:-1]] + 12 * (int(name[-1]) + 1)


CHORDS = {'Fm': ('F', 'min'), 'Db': ('Db', 'maj'), 'Eb': ('Eb', 'maj'), 'C': ('C', 'maj'), 'Ab': ('Ab', 'maj')}
DROP_CH = ['Fm', 'Fm', 'Db', 'Eb', 'Fm', 'Fm', 'Db', 'C']
INTRO_CH = ['Fm', 'Fm', 'Db', 'Eb', 'Fm', 'Fm', 'Db', 'C']
BREAK_CH = ['Db', 'Ab', 'Eb', 'C']


def chord_root(ch, lo):
    """grondtoon van een akkoord, de eerste >= lo"""
    r = NOTE[CHORDS[ch][0]]
    while r < lo:
        r += 12
    return r


def t(bar, pos=0):
    return bar * BAR + pos * S


# ---- de reese-hook: per maat (16de, lengte, noot, klank) ----
HOOK = {
    'a':  [(0, 6, 'F1', 'mid'), (6, 2, 'F1', 'growl'), (8, 3, 'Ab1', 'bright'), (11, 3, 'F1', 'mid'), (14, 2, 'C2', 'growl')],
    'b':  [(0, 3, 'F2', 'bright'), (3, 3, 'Eb2', 'growl'), (6, 4, 'C2', 'mid'), (10, 2, 'Ab1', 'growl'), (12, 4, 'Bb1', 'bright')],
    'Db': [(0, 6, 'Db2', 'mid'), (6, 2, 'Db2', 'growl'), (8, 3, 'Ab1', 'bright'), (11, 3, 'Db2', 'mid'), (14, 2, 'Eb2', 'growl')],
    'Eb': [(0, 6, 'Eb2', 'mid'), (6, 2, 'Eb2', 'growl'), (8, 3, 'Bb1', 'bright'), (11, 3, 'G1', 'mid'), (14, 2, 'Bb1', 'growl')],
    'C':  [(0, 6, 'C2', 'mid'), (6, 2, 'C2', 'growl'), (8, 2, 'E2', 'bright'), (10, 2, 'C2', 'mid'), (12, 4, 'C2', 'rise')],
}
HOOK_ORDER = ['a', 'b', 'Db', 'Eb', 'a', 'b', 'Db', 'C']
# lead (tweede helft van de drops): per maat (16de, lengte, noot)
LEAD_MEL = [
    [(0, 3, 'C5'), (3, 3, 'Ab4'), (6, 2, 'F4'), (8, 2, 'C5'), (10, 4, 'Eb5'), (14, 2, 'C5')],
    [(0, 6, 'F5'), (6, 2, 'Eb5'), (8, 4, 'C5'), (12, 4, 'Ab4')],
    [(0, 3, 'Db5'), (3, 3, 'Ab4'), (6, 2, 'F4'), (8, 2, 'Ab4'), (10, 4, 'Db5'), (14, 2, 'C5')],
    [(0, 6, 'Bb4'), (6, 2, 'G4'), (8, 2, 'Bb4'), (10, 2, 'Eb5'), (12, 4, 'G5')],
    [(0, 3, 'C5'), (3, 3, 'Ab4'), (6, 2, 'F4'), (8, 2, 'C5'), (10, 4, 'Eb5'), (14, 2, 'C5')],
    [(0, 3, 'F5'), (3, 3, 'G5'), (6, 4, 'Ab5'), (10, 2, 'G5'), (12, 2, 'F5'), (14, 2, 'Eb5')],
    [(0, 6, 'F5'), (6, 2, 'Eb5'), (8, 4, 'Db5'), (12, 4, 'C5')],
    [(0, 6, 'C5'), (6, 2, 'Bb4'), (8, 2, 'G4'), (10, 2, 'E4'), (12, 2, 'G4'), (14, 2, 'Bb4')],
]
# drop 2b: variatie (antwoord een terts hoger in maat 2/6, slot naar boven)
LEAD_MEL2 = [LEAD_MEL[0],
             [(0, 6, 'Ab5'), (6, 2, 'G5'), (8, 4, 'F5'), (12, 4, 'C5')],
             LEAD_MEL[2], LEAD_MEL[3], LEAD_MEL[4], LEAD_MEL[5],
             [(0, 6, 'Ab5'), (6, 2, 'G5'), (8, 4, 'F5'), (12, 4, 'Eb5')],
             [(0, 3, 'E5'), (3, 3, 'G5'), (6, 4, 'C6'), (10, 6, 'Bb5')]]
# 'aah'-koor in de breakdown (per maat: 16de, lengte, noot)
AAH_MEL = [[(0, 10, 'F4'), (10, 6, 'Ab4')], [(0, 16, 'C5')], [(0, 10, 'Bb4'), (10, 6, 'G4')], [(0, 8, 'G4'), (8, 8, 'E4')]]


def build():
    P = {k: [] for k in ('kick', 'snare', 'ghost', 'ride', 'crash', 'fx', 'reese', 'lead', 'stab', 'horn', 'pad', 'aah',
                         'hats', 'sub', 'arp', 'siren')}
    reese_prog = []           # (tick, programma) voor de klankwissels van de bas
    extra = {'siren': [], 'reese': []}
    stab_prog, horn_prog, pad_prog = [], [], []

    def chord_prog(ch, mn, mj):
        return mn if CHORDS[ch][1] == 'min' else mj

    # ---------------- bouwstenen ----------------
    def drums(b, kind, ghosts=True):
        s = t(b)
        if kind == 'two':
            P['kick'] += [[s + p * S, s + p * S + E, KICK, 127] for p in (0, 10)]
            P['snare'] += [[s + p * S, s + p * S + E, SNARE, 118] for p in (4, 12)]
            if ghosts:
                P['ghost'] += [[s + p * S, s + p * S + S, GHOST, v] for p, v in ((7, 52), (9, 44), (15, 58))]
        elif kind == 'amen':          # gechopte amen: K.K.S..S.SKK.S..S
            P['kick'] += [[s + p * S, s + p * S + E, KICK, v] for p, v in ((0, 127), (2, 112), (10, 124), (11, 104))]
            P['snare'] += [[s + p * S, s + p * S + E, SNARE, 118] for p in (4, 12)]
            P['ghost'] += [[s + p * S, s + p * S + S, GHOST, v] for p, v in ((7, 70), (9, 76), (15, 82))]
        elif kind == 'half':          # halftime: kick op 1, snare op 3
            P['kick'] += [[s + p * S, s + p * S + E, KICK, v] for p, v in ((0, 127), (6, 100), (11, 108))]
            P['snare'] += [[s + 8 * S, s + 8 * S + E, SNARE, 124]]
            P['fx'] += [[s + 8 * S, s + 8 * S + E, CLAP, 96]]
            P['ghost'] += [[s + p * S, s + p * S + S, GHOST, v] for p, v in ((3, 40), (13, 48), (15, 56))]
        elif kind == 'fill':          # amen-chop-fill: de laatste tel snares in 16den
            P['kick'] += [[s + p * S, s + p * S + E, KICK, 127] for p in (0, 10)]
            P['snare'] += [[s + p * S, s + p * S + E, SNARE, 118] for p in (4, 7)]
            P['ghost'] += [[s + 9 * S, s + 10 * S, GHOST, 70]]
            P['snare'] += [[s + p * S, s + p * S + S, ROLL, 84 + 10 * (p - 12)] for p in (12, 13, 14, 15)]

    def hats(b, dens=16, vel=1.0):
        s = t(b)
        for p in range(16):
            if dens == 8 and p % 2:
                continue
            if dens == 4 and p % 4 != 2:
                continue
            off = p % 4 == 2
            P['hats'] += [[s + p * S, s + p * S + (14 if off else 4), 84 if off else 92, int((92 if off else 54) * vel)]]

    def ride(b, every=4):
        s = t(b)
        P['ride'] += [[s + p * S, s + p * S + E, RIDE, 100 if p % 8 == 0 else 86] for p in range(0, 16, every)]

    def hook(b, key, timbre=None, vel=112):
        s = t(b)
        for p, ln, nm, tb in HOOK[key]:
            st, en = s + p * S, s + (p + ln) * S
            nt = n(nm)
            if tb == 'rise':          # de bas zwiept een octaaf omhoog naar de volgende maat
                P['reese'].append([st, en, nt, vel])
                reese_prog.append((st, REESE['bright']))
                extra['reese'] += [(st + i * 6, mido.Message('pitchwheel', pitch=min(8191, int(8192 * (i / 16) ** 1.5))))
                                   for i in range(1, 17)]
                extra['reese'].append((en, mido.Message('pitchwheel', pitch=0)))
                sub_note(st, en, nt)
                continue
            P['reese'].append([st, en, nt, vel])
            reese_prog.append((st, REESE[timbre or tb] if not (timbre and tb == 'growl') else REESE['growl']))
            sub_note(st, en, nt)

    def sub_note(st, en, nt):
        while nt > n('Eb2'):
            nt -= 12
        P['sub'].append([st, en, nt, 110])

    def stabs(b, ch, pattern, which='stab', vel=100):
        s = t(b)
        r = chord_root(ch, 60)
        for p in pattern:
            P[which].append([s + p * S, s + p * S + S + 6, r, vel])
            (stab_prog if which == 'stab' else horn_prog).append(
                (s + p * S, chord_prog(ch, STAB_MIN, STAB_MAJ) if which == 'stab' else chord_prog(ch, HORN_MIN, HORN_MAJ)))

    def pad(b, ch, bars=1, vel=96):
        s = t(b)
        P['pad'].append([s, s + bars * BAR, chord_root(ch, 53), vel])
        pad_prog.append((s, chord_prog(ch, PAD_MIN, PAD_MAJ)))

    def arp(b, ch, vel=70):
        s = t(b)
        r = chord_root(ch, 65)
        tones = [r, r + (3 if CHORDS[ch][1] == 'min' else 4), r + 7, r + 12]
        seq = [0, 1, 2, 3, 2, 1, 2, 3, 0, 1, 2, 3, 2, 3, 1, 2]
        P['arp'] += [[s + p * S, s + p * S + S - 4, tones[seq[p]], vel] for p in range(16)]

    def build_bar(b):
        """De opbouwmaat (maat 7 = maat 55): roffel, riser, sirene, reverse crash; laatste achtste stil."""
        s = t(b)
        P['kick'] += [[s, s + E, KICK, 120]]
        P['snare'] += [[s + p * S, s + p * S + S, ROLL, 60 + 3 * p] for p in range(0, 8, 2)]
        P['snare'] += [[s + p * S, s + p * S + S, ROLL, 76 + 4 * p] for p in range(8, 14)]
        P['hats'] += [[s + i * E, s + i * E + E, 48 + 4 * i, 40 + 8 * i] for i in range(7)]     # riser (ruis)
        hats_prog.append((s, RISER))
        hats_prog.append((t(b + 1), HATS))
        P['siren'].append([s, s + 14 * S, n('C4'), 70])
        extra['siren'] += [(s + i * 12, mido.Message('pitchwheel', pitch=min(8191, int(8192 * i / 28)))) for i in range(1, 29)]
        extra['siren'].append((s + 14 * S, mido.Message('pitchwheel', pitch=0)))
        rev_len = 445                                   # mitch_revcym = 1,6 s; eindigt precies op de maatgrens
        P['fx'].append([t(b + 1) - rev_len, t(b + 1) - 2, REVCYM, 100])
        P['reese'].append([s, s + 12 * S, n('C2'), 100])
        reese_prog.append((s, REESE['dark']))
        P['sub'].append([s, s + 12 * S, n('C2'), 100])
        stabs(b, 'C', [0], 'stab', 96)

    hats_prog = [(0, HATS)]

    # ================= INTRO =================
    P['crash'].append([t(0), t(0) + 2 * TPB, CRASH, 100])
    stabs(0, 'Fm', [0], 'stab', 110)
    for b in range(4):
        pad(b, INTRO_CH[b], vel=88 if b else 70)
        arp(b, INTRO_CH[b], 40 + 8 * b)
        P['sub'].append([t(b), t(b + 1) - 6, chord_root(INTRO_CH[b], 29) if INTRO_CH[b] != 'Eb' else n('Eb2'), 70 + 8 * b])
        if b >= 2:
            hats(b, 8 if b == 2 else 16, 0.6 + 0.2 * (b - 2))
    P['reese'].append([t(2), t(4) - 6, n('F1'), 60])    # het grommende beest wordt wakker
    reese_prog.append((t(2), REESE['dark']))
    for i, b in enumerate(range(4, 7)):
        drums(b, 'two', ghosts=False)
        hats(b, 16, 0.8)
        hook(b, HOOK_ORDER[i], timbre='dark', vel=96 + 6 * i)
        pad(b, INTRO_CH[b], vel=72)
    P['crash'].append([t(4), t(4) + 2 * TPB, CRASH, 96])
    build_bar(7)

    # ================= LOOP =================
    def drop_bar(b, k, kind, second_half, lead_mel=LEAD_MEL, horn=False, hookvel=112):
        ch = DROP_CH[k % 8]
        drums(b, kind)
        hats(b, 16)
        hook(b, HOOK_ORDER[k % 8], vel=hookvel)
        if k % 8 == 0:
            P['crash'].append([t(b), t(b) + 2 * TPB, CRASH, 110])
        if second_half:
            ride(b)
            for p, ln, nm in lead_mel[k % 8]:
                P['lead'].append([t(b, p), t(b, p + ln), n(nm), 104])
        pat = [3, 6] if k % 2 == 0 else [0, 3, 6, 11]
        if horn:
            stabs(b, ch, pat, 'horn', 104)
        else:
            stabs(b, ch, pat, 'stab', 100)

    # DROP 1 (8-23)
    for k in range(16):
        b = 8 + k
        kind = 'fill' if k in (7, 15) else ('amen' if k % 4 == 3 else 'two')
        drop_bar(b, k, kind, k >= 8, horn=k >= 8 and k % 2 == 1)
    # BREAKDOWN (24-27) + OPBOUW (28-31)
    P['crash'].append([t(24), t(24) + 2 * TPB, CRASH, 100])
    P['kick'].append([t(24), t(24) + E, KICK, 127])
    for i in range(8):
        b = 24 + i
        ch = BREAK_CH[i % 4]
        pad(b, ch, vel=92)
        arp(b, ch, 56 + (8 if i >= 4 else 0))
        P['sub'].append([t(b), t(b + 1) - 6, chord_root(ch, 29) if chord_root(ch, 29) <= n('Eb2') else chord_root(ch, 29) - 12, 96])
        for p, ln, nm in AAH_MEL[i % 4]:
            P['aah'].append([t(b, p), t(b, p + ln) - 6, n(nm) + (12 if i >= 4 and i < 7 else 0), 100 if i < 4 else 108])
    for b in (28, 29):
        P['kick'] += [[t(b, p), t(b, p) + E, KICK, 110 + 4 * (b - 28)] for p in (0, 4, 8, 12)]
        hats(b, 4 if b == 28 else 8, 0.7)
    P['snare'] += [[t(29, p), t(29, p) + E, SNARE, 90] for p in (4, 12)]
    P['snare'] += [[t(30, p), t(30, p) + S, ROLL, 70 + 2 * p] for p in range(0, 16, 2)]
    P['kick'] += [[t(30, p), t(30, p) + E, KICK, 118] for p in (0, 8)]
    P['snare'] += [[t(31, p), t(31, p) + S, ROLL, 80 + 3 * p] for p in range(14)]
    P['kick'].append([t(31), t(31) + E, KICK, 124])
    P['hats'] += [[t(30) + i * E, t(30) + i * E + E, 44 + 2 * i, 36 + 4 * i] for i in range(15)]     # riser
    hats_prog += [(t(30), RISER), (t(32), HATS)]
    P['siren'].append([t(30), t(31, 14), n('C4'), 72])
    extra['siren'] += [(t(30) + i * 24, mido.Message('pitchwheel', pitch=min(8191, int(8192 * (i / 30) ** 1.4))))
                       for i in range(1, 31)]
    extra['siren'].append((t(31, 14), mido.Message('pitchwheel', pitch=0)))
    P['fx'].append([t(32) - 445, t(32) - 2, REVCYM, 100])
    P['reese'] += [[t(28 + i), t(29 + i) - 6, chord_root(c, 29) if chord_root(c, 29) <= 39 else chord_root(c, 29) - 12, 70 + 8 * i]
                   for i, c in enumerate(BREAK_CH)]
    reese_prog.append((t(28), REESE['dark']))
    reese_prog.append((t(30), REESE['mid']))
    # VALSE DROP (32-33) + REWIND (34) + LUCHTHOORN (35)
    drop_bar(32, 0, 'two', False)
    drop_bar(33, 1, 'amen', False)
    P['fx'].append([t(34), t(34, 12), REWIND, 120])
    P['fx'] += [[t(35, p), t(35, p + ln), HORN, 112] for p, ln in ((0, 2), (3, 2), (6, 5))]
    P['snare'] += [[t(35, p), t(35, p) + S, ROLL, 70 + 4 * (p - 8)] for p in range(8, 16)]
    P['kick'] += [[t(35, p), t(35, p) + E, KICK, 120] for p in (0, 3, 6)]
    P['hats'] += [[t(35) + i * S, t(35) + i * S + S, 60 + 2 * i, 50 + 4 * i] for i in range(8, 15)]
    hats_prog += [(t(35, 8), RISER), (t(36), HATS)]
    # DROP 2a (36-43): halftime + wobble
    WOB_ROOTS = [('F1', 'Fm'), ('Db2', 'Db'), ('Ab1', 'Ab'), ('C2', 'C')]
    for i, (rt, ch) in enumerate(WOB_ROOTS):
        b = 36 + 2 * i
        for j in range(2):
            drums(b + j, 'half')
            hats(b + j, 8)
        nt = n(rt)
        last = i == 3
        P['reese'].append([t(b), t(b + 2) - (S if not last else 0), nt, 118])
        reese_prog.append((t(b), WOB[nt]))
        sub_note(t(b), t(b + 2) - S, nt)
        P['crash'].append([t(b), t(b) + 2 * TPB, CRASH, 104])
        stabs(b, ch, [0], 'horn', 112)
        stabs(b + 1, ch, [0, 3], 'horn', 104)
        stabs(b + 1, ch, [8, 11, 14], 'stab', 92)
    # DROP 2b (44-51)
    for k in range(8):
        b = 44 + k
        kind = 'fill' if k == 7 else ('amen' if k % 2 else 'two')
        drop_bar(b, k, kind, True, lead_mel=LEAD_MEL2, horn=k % 2 == 0, hookvel=116)
        if k % 2:
            ride(b, 2)
    # TERUG (52-54) + OPBOUW (55 = 7)
    for k in range(3):
        b = 52 + k
        drums(b, 'two')
        hats(b, 16, 0.9)
        hook(b, HOOK_ORDER[k], vel=108)
    P['crash'].append([t(52), t(52) + 2 * TPB, CRASH, 96])
    build_bar(55)
    return P, reese_prog, extra, stab_prog, horn_prog, pad_prog, hats_prog


def clip_loop(notes):
    out = []
    for a, b, nt, v in notes:
        for g in (LOOP_START, LOOP_END):
            if a < g < b:
                b = g
        if a < LOOP_END:
            out.append([a, b, nt, v])
    return dedupe(out)


def main():
    P, reese_prog, extra, stab_prog, horn_prog, pad_prog, hats_prog = build()
    for k in P:
        P[k] = clip_loop(P[k])
    # het golfkanaal speelt een golf van één periode een octaaf lager dan genoteerd (en niet onder ±32,7 Hz):
    # de sub een octaaf hoger noteren, dan klinkt hij op de bedoelde hoogte (F1 = 43,7 Hz)
    P['sub'] = [[a, b, nt + 12, v] for a, b, nt, v in P['sub']]
    write_voicegroup()
    rel = {'reese': 170, 'lead': 190, 'stab': 170, 'horn': 190, 'pad': 200, 'aah': 165}
    tail = {k: release_ticks(r, TPB, BPM) for k, r in rel.items()}
    kitrel = {36 + i: r for i, (_, _, r) in enumerate(KIT)}
    for k in ('kick', 'snare', 'ghost', 'ride', 'fx'):
        tail[k] = max(release_ticks(kitrel[nt], TPB, BPM) if kitrel[nt] else 0 for _, _, nt, _ in P[k]) if P[k] else 0
    tail['crash'] = 0
    P['crash'] = [[a, min(b, a + 2 * TPB), nt, v] for a, b, nt, v in P['crash']]
    P['kick'] = [[a, b, nt, int(v * 0.8)] for a, b, nt, v in P['kick']]       # kick iets onder de snare (gemeten)
    for k in ('reese', 'lead', 'pad', 'aah'):
        P[k] = detach(P[k], tail[k])
    order = ['reese', 'kick', 'snare', 'fx', 'lead', 'ghost', 'stab', 'horn', 'crash', 'ride', 'aah', 'pad']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAX_VOICES)
    for k in order:
        tot = len(ds[k])
        if tot and len(kept[k]) < tot:
            print('  %-6s %3d van %4d noten vallen weg (%.1f%%)' % (k, tot - len(kept[k]), tot, 100 * (tot - len(kept[k])) / tot))
        P[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (LOOP_START, LOOP_END)

    def progs(lst, at_loop=True):
        """programmawissels; op het loopbegin het programma dat daar hoort nog eens zetten (de sprong terug)."""
        lst = sorted(set(lst))
        out = [(tk, 'prog', p) for tk, p in lst if tk < LOOP_END]
        if at_loop:
            cur = [p for tk, p in lst if tk <= LOOP_START]
            if cur and not any(tk == LOOP_START for tk, _ in lst):
                out.append((LOOP_START, 'prog', cur[-1]))
        return out
    # pitchwheel-berichten binnen de loop houden + BENDR 12 aan het begin
    bendr = [(0, mido.Message('control_change', control=20, value=12))]
    ex = {k: bendr + [(tk, m) for tk, m in v if tk < LOOP_END] for k, v in extra.items()}
    layout = [  # naam, programma, volume, kanaal, pan, ccs, extra
        ('drums', DRUMS, 112, 9, 64, (), ()),
        ('cym', DRUMS, 112, 10, 76, (), ()),
        ('fx', DRUMS, 96, 11, 64, (), ()),
        ('reese', REESE['mid'], 100, 0, 64, progs(reese_prog), ex['reese']),
        ('lead', LEAD, 72, 1, 58, (), ()),
        ('stab', STAB_MIN, 74, 2, 70, progs(stab_prog), ()),
        ('horn', HORN_MIN, 82, 3, 54, progs(horn_prog), ()),
        ('pad', PAD_MIN, 62, 4, 64, progs(pad_prog), ()),
        ('aah', AAH, 80, 5, 64, (), ()),
        ('hats', HATS, 90, 12, 72, progs(hats_prog), ()),
        ('sub', SUB, 48, 13, 64, (), ()),
        ('arp', ARP, 30, 14, 84, (), ()),
        ('siren', SIREN, 34, 15, 44, (), ex['siren']),
    ]
    tracks = {'drums': sorted(P['kick'] + P['snare'] + P['ghost']), 'cym': sorted(P['ride'] + P['crash'])}
    for name, prog, vol, ch, pan, ccs, extr in layout:
        song.add(tracks.get(name, P.get(name, [])), prog, vol, ch, pan, extra=extr, ccs=ccs)
    written = {'kick', 'snare', 'ghost', 'ride', 'crash'} | {nm for nm, *_ in layout}
    assert not [k for k in P if P[k] and k not in written], 'partij niet weggeschreven'
    assert len(layout) <= 16
    song.save(OUT, LOOP_END)
    sec = lambda tk: tk / TPB * 60 / BPM
    print(OUT, '%d sporen, intro %.1f s, loop %.1f s, totaal %.1f s' % (len(layout), sec(LOOP_START),
                                                                      sec(LOOP_END - LOOP_START), sec(LOOP_END)))
    for nm, b in (('drop 1', 8), ('breakdown', 24), ('opbouw', 28), ('valse drop', 32), ('rewind', 34),
                  ('drop 2a', 36), ('drop 2b', 44), ('terug', 52), ('opbouw', 55)):
        print('  %-10s maat %2d  %5.1f s' % (nm, b, sec(t(b))))


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + Drum & Bass-samples (mitch_samples.py) en een eigen drumkit voor Battle! Mitch.'
    lines[1] = '@ Gegenereerd door tools/grounded/mitch_theme.py.'
    lines[2] = 'voice_group %s' % VG
    ds = lambda smp, rel, key=60, att=255, dec=0, sus=255: \
        '\tvoice_directsound %d, 0, DirectSoundWaveData_%s, %d, %d, %d, %d' % (key, smp, att, dec, sus, rel)
    rep = {
        32: ds('mitch_reese_dark', 170), 33: ds('mitch_reese_mid', 170), 34: ds('mitch_reese_bright', 170),
        35: ds('mitch_growl', 170),
        36: ds('mitch_wob_f1', 170), 37: ds('mitch_wob_ab1', 170), 38: ds('mitch_wob_c2', 170),
        39: ds('mitch_wob_db2', 170), 40: ds('mitch_wob_eb2', 170),
        61: ds('mitch_horn_min', 190), 62: ds('mitch_horn_maj', 190),
        80: '\tvoice_square_1 60, 0, 0, 2, 0, 0, 15, 2',
        81: '\tvoice_square_2 60, 0, 1, 0, 2, 4, 1',
        84: '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_8, 0, 7, 15, 1',
        88: ds('mitch_pad_min', 200, att=40), 89: ds('mitch_pad_maj', 200, att=40),
        90: ds('mitch_stab_min', 170), 91: ds('mitch_stab_maj', 170), 92: ds('mitch_lead', 190),
        120: '\tvoice_noise_alt 60, 0, 0, 0, 0, 15, 1',
        121: '\tvoice_noise_alt 60, 0, 0, 3, 0, 15, 2',
        127: '\tvoice_keysplit_all voicegroup_mitch_drumset',
    }
    out = []
    for l in lines:
        tag = l.rstrip().rsplit('@ ', 1)[-1] if '@ ' in l and l.startswith('\t') else None
        if tag is not None and tag.isdigit() and int(tag) in rep:
            out.append('%s  @ %s' % (rep[int(tag)], tag))
        else:
            out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = []
    for nm, smp, r in KIT:
        if smp == 'trinity_cymbal_crash':
            kit.append('voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165')
        else:
            kit.append('voice_directsound_no_resample 60, 64, DirectSoundWaveData_%s, 255, 0, 255, %d' % (smp, r))
    open('sound/voicegroups/drumsets/mitch.inc', 'w').write(
        '@ Project Grounded: Drum & Bass-kit voor Battle! Mitch (mitch_theme.py), alles DirectSound:\n'
        '@ ' + ', '.join('%d %s' % (36 + i, nm.lower()) for i, (nm, _, _) in enumerate(KIT)) + '.\n'
        'voice_group mitch_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    main()
