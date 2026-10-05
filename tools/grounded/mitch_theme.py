#!/usr/bin/env python3
"""Project Grounded: Battle! Mitch v2, een eigen compositie: episch Pokémon-baasgevecht x Chase & Status-Drum & Bass.

Jordi over v1: 'het idee van een Pokémon battle theme is er al, maar ik wil een ECHTE HYBRIDE: de drumbeat klinkt te
recht/langzaam en mist de agressieve DnB-fundering; laat de wandelende baslijn vallen, rauwe reese met slides en een
wobbly sub ('Baddadan', 'No Problem'); heldere Pokémon-koperleads + chiptune-plucks, opzwepende mineurmelodie; klassieke
battle-intro met snelle chromatische loopjes, build-up met versnellende snareroffel, en dan de drop.'

Diagnose v1 (gemeten in de opname, drop 1, aanslag per 16e): het patroon wás two-step, maar je hoorde het niet. De
hihats (PSG-ruis) zaten 14 dB onder de kick en de 16den waren onhoorbaar (alleen de achtste 'en' kwam door: een
8sten-gevoel); de snare-aanslag was 2-3x zwakker dan de aanslagen van de reese in het middengebied (een kamer-snare
zonder crack), de ghost notes verdwenen in de ruisvloer, en de bas speelde lange noten óp de kicks. Wat je hoorde was
'boem ... (bas) ... boem': de groove van de bas op halve snelheid = recht en langzaam. Drop 2 was bovendien halftime.

v2: 174 bpm, F-klein. 1 tel = 20,7 frames, 1 maat = 1,38 s.
  Drums (eigen kit, alles DirectSound): punchy kick (sinus 190 -> 52 Hz + klik), snare met crack (FluidR3 + ruisstoot
  1,8-6,5 kHz), ghost/roffel, échte hihats in 16den (DirectSound, accent op de achtsten, open hihat op de laatste 'en'),
  two-step K . . . S . . g . g K . S . . g, om de 4 maten een amen-variant, om de 8 een rollende fill.
  Bas: rauwe reese (5 ontstemde zaagtanden, tanh-fuzz, lowpass ±2,5 kHz; mitch_samples.py) + PSG-sub; 'bad-da-DAN'-
  stoten (twee 16den + een lange op de kick van 3-en), pitch-bend-dives en -scoops, opstijgende bas in de laatste maat
  vóór elke drop; in drop 2 een stotterende variant en vier maten wobble (filter-LFO in de sample) op vol tempo.
  Lead: de Pokémon-trompet (sc88pro-trompet-keysplit van de GBA zelf) met een PSG-blokgolf unisono (Gen 3-klank),
  PSG-arpeggio's in 16den eronder.

Intro (8 maten, 11,0 s)
  0     battle-stinger: chromatische 16den-loopjes omlaag (in groepjes van 4, elk een halve toon lager)
  1     loopje omhoog (harmonisch mineur) en drie stoten E-G-C ('ta-ta-TAA') op de C-majeur
  2-5   dreigend ostinato (trompet-16den), kick + hihats, donkere reese, sub, arpeggio
  6-7   build-up: snareroffel 8sten -> 16den -> 32sten, sirene + reese die een octaaf opstijgen, ruisriser,
        reverse crash, de laatste achtste stil
Loop (48 maten, 66,2 s; maat 54-55 = 6-7, dus de terugsprong klinkt als build-up -> drop)
  8-23  DROP 1: two-step, reese-stoten, sub, melodie A (16 maten, de tweede 8 met een crash en ride)
  24-27 breakdown: pad, 'aah'-koor, arpeggio, shaker (geen stilstand: de 16den lopen door)
  28-31 build-up: kick in kwarten -> 8sten, versnellende roffel, sirene, riser, reverse crash
  32-33 valse drop ... 34 DJ-REWIND ... 35 luchthoorn (BWAP BWAP BWAAAP) + roffel (de grap uit v1)
  36-43 DROP 2a: melodie B (16den-loopjes), stotterbas, amen-variaties
  44-47 wobble op vol tempo (two-step blijft), het thema keert terug (A 1-4)
  48-51 climax: A 5-8, stotterbas, crashes
  52-53 de stinger van de intro over drums + bas
  54-55 = 6-7 (build-up), terug naar maat 8
Max. 10 DirectSound-noten (gewone trainer): lead > kick > snare > bas > hihats > ... PSG (kost niets): sub (golf),
arpeggio (vierkant 2), lead-verdubbeling/sirene (vierkant 1), shaker/riser (ruis).
Voicegroup grounded_mitch = grounded_gm + eigen samples (mitch_samples.py) + eigen drumkit (drumsets/mitch.inc).
Zie tools/grounded/MUZIEK.md.
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
REESE = {'dark': 32, 'mid': 33, 'bright': 34, 'growl': 35, 'raw': 41, 'rawdark': 42}
WOB = {29: 36, 32: 37, 36: 38, 37: 39, 39: 40}          # grondtoon -> wobble-sample
LEAD = 56                                                # trompet-keysplit (sc88pro, de Pokémon-trompet)
LEAD2 = 92                                               # mitch_lead: twee ontstemde zaagtanden, unisono
STAB_MIN, STAB_MAJ, HORN_MIN, HORN_MAJ, PAD_MIN, PAD_MAJ, AAH = 90, 91, 61, 62, 88, 89, 52
SIREN, ARP, LEADSQ, SUB, SHAKER, RISER, DRUMS = 80, 81, 82, 84, 120, 121, 127
# drumkit (drumsets/mitch.inc, vanaf 36): naam, sample, release, lengte (ticks; ±de samplelengte)
KIT = [
    ('KICK', 'mitch_kick', 180, 60),
    ('SNARE', 'mitch_snare', 190, 60),
    ('GHOST', 'mitch_ghost', 140, 24),
    ('RIDE', 'mitch_ride', 170, 48),
    ('CRASH', 'trinity_cymbal_crash', None, TPB + E),
    ('REVCYM', 'mitch_revcym', 120, 440),
    ('REWIND', 'mitch_rewind', 160, 288),
    ('HORN', 'mitch_airhorn', 190, 48),
    ('CLAP', 'sc88pro_tr909_hand_clap', 180, 48),
    ('ROLL', 'mitch_ghost', 110, 12),
    ('HAT', 'mitch_hat', 110, 16),
    ('OHAT', 'mitch_ohat', 150, 72),
]
for i, (nm, *_) in enumerate(KIT):
    globals()[nm] = 36 + i
KITLEN = {36 + i: k[3] for i, k in enumerate(KIT)}

INTRO = 8
LOOP_START, LOOP_END = INTRO * BAR, 56 * BAR
NOTE = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def n(name):
    """'F1' -> 29, 'Ab4' -> 68"""
    return NOTE[name[:-1]] + 12 * (int(name[-1]) + 1)


CHORDS = {'Fm': ('F', 'min'), 'Db': ('Db', 'maj'), 'Eb': ('Eb', 'maj'), 'C': ('C', 'maj'), 'Ab': ('Ab', 'maj')}
DROP_CH = ['Fm', 'Fm', 'Db', 'Eb', 'Fm', 'Fm', 'Db', 'C']
BREAK_CH = ['Db', 'Ab', 'Eb', 'C']


def chord_root(ch, lo):
    r = NOTE[CHORDS[ch][0]]
    while r < lo:
        r += 12
    return r


def t(bar, pos=0):
    return bar * BAR + int(pos * S)


# ---------------- de Pokémon-melodie (trompet): per maat (16de, lengte, noot) ----------------
MEL_A = [
    [(0, 3, 'F5'), (3, 3, 'C5'), (6, 2, 'Ab4'), (8, 2, 'C5'), (10, 2, 'F5'), (12, 2, 'G5'), (14, 2, 'Ab5')],
    [(0, 6, 'G5'), (6, 2, 'F5'), (8, 3, 'Eb5'), (11, 3, 'F5'), (14, 2, 'C5')],
    [(0, 3, 'Db5'), (3, 3, 'F5'), (6, 2, 'Ab5'), (8, 2, 'F5'), (10, 2, 'Ab5'), (12, 2, 'Bb5'), (14, 2, 'C6')],
    [(0, 6, 'Bb5'), (6, 2, 'G5'), (8, 3, 'Eb5'), (11, 3, 'G5'), (14, 2, 'Bb5')],
    [(0, 3, 'C6'), (3, 3, 'Ab5'), (6, 2, 'F5'), (8, 2, 'Ab5'), (10, 2, 'C6'), (12, 2, 'Db6'), (14, 2, 'C6')],
    [(0, 3, 'Bb5'), (3, 3, 'Ab5'), (6, 2, 'G5'), (8, 2, 'F5'), (10, 4, 'Eb5'), (14, 2, 'F5')],
    [(0, 3, 'Db5'), (3, 1, 'Eb5'), (4, 2, 'F5'), (6, 2, 'Ab5'), (8, 3, 'Bb5'), (11, 3, 'Ab5'), (14, 2, 'F5')],
    [(0, 6, 'E5'), (6, 2, 'G5'), (8, 2, 'Bb5'), (10, 2, 'C6'), (12, 1, 'Db6'), (13, 1, 'C6'), (14, 1, 'B5'), (15, 1, 'Bb5')],
]
# melodie B (drop 2a): rivaal-energie, 16den-loopjes omhoog
MEL_B = [
    [(0, 2, 'F5'), (2, 1, 'G5'), (3, 1, 'Ab5'), (4, 2, 'C6'), (6, 2, 'Ab5'), (8, 1, 'G5'), (9, 1, 'Ab5'), (10, 2, 'G5'),
     (12, 2, 'F5'), (14, 2, 'Eb5')],
    [(0, 6, 'F5'), (6, 1, 'C5'), (7, 1, 'Db5'), (8, 1, 'Eb5'), (9, 1, 'F5'), (10, 1, 'G5'), (11, 1, 'Ab5'), (12, 4, 'C6')],
    [(0, 2, 'Db6'), (2, 2, 'C6'), (4, 2, 'Ab5'), (6, 2, 'F5'), (8, 1, 'Ab5'), (9, 1, 'Bb5'), (10, 2, 'Ab5'), (12, 2, 'F5'),
     (14, 2, 'Db5')],
    [(0, 6, 'Eb5'), (6, 1, 'Bb4'), (7, 1, 'C5'), (8, 1, 'Db5'), (9, 1, 'Eb5'), (10, 1, 'F5'), (11, 1, 'G5'), (12, 4, 'Bb5')],
    [(0, 2, 'F5'), (2, 1, 'G5'), (3, 1, 'Ab5'), (4, 2, 'C6'), (6, 2, 'Ab5'), (8, 1, 'G5'), (9, 1, 'Ab5'), (10, 2, 'Bb5'),
     (12, 2, 'C6'), (14, 2, 'Db6')],
    [(0, 6, 'C6'), (6, 2, 'Bb5'), (8, 2, 'Ab5'), (10, 2, 'G5'), (12, 4, 'F5')],
    [(0, 2, 'Db6'), (2, 2, 'C6'), (4, 2, 'Ab5'), (6, 2, 'F5'), (8, 2, 'Db5'), (10, 2, 'F5'), (12, 2, 'Ab5'), (14, 2, 'Bb5')],
    [(0, 4, 'C6'), (4, 2, 'G5'), (6, 2, 'E5'), (8, 1, 'C5'), (9, 1, 'E5'), (10, 1, 'G5'), (11, 1, 'Bb5'), (12, 4, 'C6')],
]
# stinger (maat 0 en 52): chromatisch omlaag in groepjes van 4, elk groepje een halve toon lager
STING_DOWN = [(i, 1, n('F5') - (i // 4) - (i % 4)) for i in range(16)]
# maat 1 en 53: omhoog (F harmonisch mineur) en drie stoten
STING_UP = [(i, 1, n(x)) for i, x in enumerate(['F4', 'G4', 'Ab4', 'Bb4', 'C5', 'Db5', 'E5', 'F5'])] + \
           [(8, 2, n('E5')), (11, 2, n('G5')), (14, 2, n('C6'))]
# ostinato (intro): intervallen per 16de t.o.v. de grondtoon (mineur / majeur)
OST = {'min': [0, 0, 7, 0, 0, 8, 0, 0, 7, 0, 0, 8, 7, 5, 3, 2], 'maj': [0, 0, 7, 0, 0, 9, 0, 0, 7, 0, 0, 9, 7, 5, 4, 2]}
AAH_MEL = [[(0, 10, 'F4'), (10, 6, 'Ab4')], [(0, 16, 'C5')], [(0, 10, 'Bb4'), (10, 6, 'G4')], [(0, 8, 'G4'), (8, 8, 'E4')]]

# ---------------- bas: per maat (16de, lengte, interval t.o.v. de grondtoon, klank, bend) ----------------
# bend: ('dive', h) = over de noot h halve tonen omlaag; ('up', h) = vanaf h halve tonen lager omhoog scheppen;
# ('rise', 12) = een octaaf omhoog naar de volgende maat (de drop)
# drop 1: 'No Problem'/'Baddadan': korte stoten met 'bad-da-DAN' (16de, 16de, lang op de kick van 3-en)
BASS1 = {
    'a':  [(0, 3, 0, 'raw', None), (3, 1, 0, 'growl', None), (4, 2, 0, 'raw', None), (6, 2, 3, 'raw', ('up', 2)),
           (8, 1, 0, 'growl', None), (9, 1, 0, 'growl', None), (10, 4, 7, 'raw', ('dive', 7)), (14, 2, 10, 'growl', None)],
    'b':  [(0, 6, 0, 'raw', ('dive', 1)), (6, 1, 12, 'bright', None), (7, 1, 0, 'growl', None), (8, 2, 12, 'raw', None),
           (10, 2, 10, 'raw', None), (12, 2, 7, 'growl', None), (14, 2, 3, 'raw', ('up', 3))],
    'maj': [(0, 3, 0, 'raw', None), (3, 1, 0, 'growl', None), (4, 2, 0, 'raw', None), (6, 2, -5, 'raw', None),
            (8, 1, 0, 'growl', None), (9, 1, 0, 'growl', None), (10, 4, -5, 'raw', ('dive', 5)), (14, 2, 2, 'growl', None)],
    'C':  [(0, 3, 0, 'raw', None), (3, 1, 0, 'growl', None), (4, 2, 0, 'raw', None), (6, 2, 4, 'raw', None),
           (8, 1, 0, 'growl', None), (9, 1, 0, 'growl', None), (10, 6, 0, 'raw', ('rise', 12))],
}
BASS1_ORDER = ['a', 'b', 'maj', 'maj', 'a', 'b', 'maj', 'C']
# drop 2: stotterend (meer grom, meer 16den)
BASS2 = [(0, 2, 0, 'raw', None), (2, 1, 0, 'growl', None), (3, 1, 0, 'growl', None), (4, 2, 12, 'bright', None),
         (6, 1, 0, 'growl', None), (7, 1, 0, 'growl', None), (8, 2, 0, 'raw', None), (10, 2, 3, 'raw', None),
         (12, 1, 7, 'growl', None), (13, 1, 7, 'growl', None), (14, 2, 10, 'raw', ('dive', 3))]
BASS_ROOT = {'Fm': 'F1', 'Db': 'Db2', 'Eb': 'Eb2', 'C': 'C2', 'Ab': 'Ab1'}


def build():
    P = {k: [] for k in ('kick', 'snare', 'ghost', 'clap', 'hat', 'ride', 'crash', 'fx', 'reese', 'lead', 'lead2', 'stab',
                         'horn', 'pad', 'aah', 'noise', 'sub', 'arp', 'sq1')}
    reese_prog, stab_prog, horn_prog, pad_prog = [], [], [], []
    noise_prog, sq1_prog = [(0, SHAKER)], [(0, LEADSQ)]
    extra = {'reese': [], 'sq1': []}

    def chord_prog(ch, mn, mj):
        return mn if CHORDS[ch][1] == 'min' else mj

    def bend(track, st, en, kind, h):
        """pitch bend (BENDR 12: 64 stappen = 12 halve tonen); terugzetten gebeurt bij de volgende noot."""
        ev = extra[track]
        steps = 8
        if kind == 'dive':                       # over de tweede helft van de noot omlaag
            a = st + (en - st) // 2
            ev += [(a + (en - a) * i // steps, mido.Message('pitchwheel', pitch=-int(8192 * h / 12 * (i / steps) ** 1.6)))
                   for i in range(1, steps + 1)]
        elif kind == 'up':                       # scheppen: begin h lager, in een 16de omhoog
            ev.append((st, mido.Message('pitchwheel', pitch=-int(8192 * h / 12))))
            ev += [(st + S * i // 4, mido.Message('pitchwheel', pitch=-int(8192 * h / 12 * (1 - i / 4)))) for i in range(1, 5)]
        elif kind == 'rise':
            ev += [(st + (en - st) * i // 16, mido.Message('pitchwheel', pitch=min(8191, int(8192 * h / 12 * (i / 16) ** 1.5))))
                   for i in range(1, 17)]
        ev.append((en, 'reset'))

    # ---------------- drums ----------------
    def drums(b, kind):
        s = t(b)
        K = lambda p, v=127: P['kick'].append([s + int(p * S), s + int(p * S) + KITLEN[KICK], KICK, v])
        SN = lambda p, v=124: P['snare'].append([s + int(p * S), s + int(p * S) + KITLEN[SNARE], SNARE, v])
        G = lambda p, v: P['ghost'].append([s + int(p * S), s + int(p * S) + KITLEN[GHOST], GHOST, v])
        if kind == 'two':             # K . . . S . . g . g K . S . . g
            K(0); SN(4); K(10); SN(12)
            G(7, 72); G(9, 58); G(15, 78)
        elif kind == 'two_b':         # variant: extra kick op de 'a' van 3 (stuwend), ghost op 1-en
            K(0); SN(4); K(10); K(11, 104); SN(12)
            G(2, 56); G(7, 72); G(14, 66)
        elif kind == 'amen':          # amen-achtig: K . K . S . . g . g K K . g S g
            K(0); K(2, 112); SN(4); G(7, 80); G(9, 70); K(10, 120); K(11, 104); G(13, 76); SN(14, 118); G(15, 84)
        elif kind == 'fill':          # rollende amen-fill: laatste twee tellen snares/ghosts in 16den
            K(0); SN(4); G(7, 72); K(8, 118); G(9, 80); SN(10, 108); G(11, 86); SN(12, 116); SN(13, 112); G(14, 96); SN(15, 124)
        elif kind == 'intro':         # intro: kick + zachte snare (nog geen crack: die bewaren we voor de drop)
            K(0, 118); G(4, 84); K(10, 112); G(12, 90); G(15, 60)

    def hats(b, vel=1.0, open_last=False, dens=16):
        s = t(b)
        acc = [127, 84, 108, 88]       # 1 e en a: accent op de tel, half accent op de 'en'
        for p in range(16):
            if dens == 8 and p % 2:
                continue
            if open_last and p == 14:
                P['hat'].append([s + p * S, s + p * S + KITLEN[OHAT], OHAT, int(110 * vel)])
                continue
            if open_last and p == 15:
                continue
            P['hat'].append([s + p * S, s + p * S + KITLEN[HAT], HAT, int(acc[p % 4] * vel)])

    def shaker(b, vel=1.0):
        s = t(b)
        P['noise'] += [[s + p * S, s + p * S + 8, 92 if p % 2 else 96, int((50 if p % 2 else 70) * vel)] for p in range(16)]

    def ride(b):
        s = t(b)
        P['ride'] += [[s + p * S, s + p * S + KITLEN[RIDE], RIDE, 96 if p % 8 == 0 else 80] for p in (0, 4, 8, 12)]

    def crash(b, v=112):
        P['crash'].append([t(b), t(b) + KITLEN[CRASH], CRASH, v])

    # ---------------- bas ----------------
    def sub_note(st, en, nt, v=112):
        while nt > n('Eb2'):
            nt -= 12
        P['sub'].append([st, en, nt, v])

    def bass_bar(b, ch, pattern, vel=116):
        s = t(b)
        root = n(BASS_ROOT[ch])
        maj = CHORDS[ch][1] == 'maj'
        for p, ln, iv, tb, bd in pattern:
            if iv == 3 and maj:
                iv = 4
            if iv == 10 and ch == 'Db':        # Cb past niet: de grote septiem (C) die naar Db terugtrekt
                iv = 11
            nt = root + iv
            while nt < n('E1'):
                nt += 12
            st, en = s + p * S, s + (p + ln) * S
            P['reese'].append([st, en, nt, vel - (10 if tb == 'growl' and ln == 1 else 0)])
            reese_prog.append((st, REESE[tb]))
            if bd:
                bend('reese', st, en, *bd)
            sub_note(st, en if not bd or bd[0] != 'dive' else st + (en - st) // 2, nt)

    def wobble(b, root, bars):
        nt = n(root)
        P['reese'].append([t(b), t(b + bars) - S, nt, 118])
        reese_prog.append((t(b), WOB[nt]))
        sub_note(t(b), t(b + bars) - S, nt)

    # ---------------- melodisch ----------------
    def lead(b, mel, vel=127, oct=0):
        for p, ln, nm in mel:
            nt = (n(nm) if isinstance(nm, str) else nm) + oct
            P['lead'].append([t(b, p), t(b, p + ln), nt, vel])
            P['lead2'].append([t(b, p), t(b, p + ln), nt, vel])     # zaagtand unisono: de trompet 'scheurt'
            P['sq1'].append([t(b, p), t(b, p + ln), nt, 100])

    def ostinato(b, ch, vel=116):
        r = chord_root(ch, n('Db4'))
        for p, iv in enumerate(OST[CHORDS[ch][1]]):
            P['lead'].append([t(b, p), t(b, p) + S - 6, r + iv, vel if p % 4 == 0 else vel - 18])
            P['sq1'].append([t(b, p), t(b, p) + S - 6, r + iv + 12, 70])

    def stabs(b, ch, pattern, which='stab', vel=100):
        r = chord_root(ch, 60)
        for p in pattern:
            P[which].append([t(b, p), t(b, p) + S + 6, r, vel])
            (stab_prog if which == 'stab' else horn_prog).append(
                (t(b, p), chord_prog(ch, STAB_MIN, STAB_MAJ) if which == 'stab' else chord_prog(ch, HORN_MIN, HORN_MAJ)))

    def pad(b, ch, vel=92):
        P['pad'].append([t(b), t(b + 1), chord_root(ch, 53), vel])
        pad_prog.append((t(b), chord_prog(ch, PAD_MIN, PAD_MAJ)))

    def arp(b, ch, vel=70, fast=False):
        r = chord_root(ch, 65)
        tones = [r, r + (3 if CHORDS[ch][1] == 'min' else 4), r + 7, r + 12, r + 15 if CHORDS[ch][1] == 'min' else r + 16]
        seq = [0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 3]
        P['arp'] += [[t(b, p), t(b, p) + S - 6, tones[seq[p]], vel if p % 4 == 0 else vel - 12] for p in range(16)]

    # ---------------- secties ----------------
    def stinger(b, with_drums=False):
        """maat b: chromatisch omlaag; maat b+1: omhoog en drie stoten (E-G-C op C-majeur)."""
        crash(b, 116)
        P['kick'].append([t(b), t(b) + KITLEN[KICK], KICK, 127])
        stabs(b, 'Fm', [0], 'horn', 118)
        lead(b, STING_DOWN, 116)
        lead(b + 1, STING_UP, 118)
        stabs(b + 1, 'C', [8, 11, 14], 'horn', 118)
        stabs(b + 1, 'C', [8, 11, 14], 'stab', 104)
        P['kick'] += [[t(b + 1, p), t(b + 1, p) + KITLEN[KICK], KICK, 124] for p in (8, 11, 14)]
        P['sub'].append([t(b), t(b + 1) - S, n('F1'), 112])
        P['reese'].append([t(b), t(b, 6), n('F1'), 112])
        reese_prog.append((t(b), REESE['rawdark']))
        P['sub'] += [[t(b + 1, p), t(b + 1, p + 2), n('C2'), 112] for p in (8, 11, 14)]
        P['reese'] += [[t(b + 1, p), t(b + 1, p + 2), n('C2'), 112] for p in (8, 11, 14)]
        reese_prog.append((t(b + 1, 8), REESE['raw']))
        if with_drums:
            drums(b, 'two')
            hats(b)
            P['snare'] += [[t(b + 1, p), t(b + 1, p) + KITLEN[SNARE], SNARE, 120] for p in (4,)]
            P['ghost'] += [[t(b + 1, p), t(b + 1, p) + KITLEN[GHOST], GHOST, 70] for p in (2, 6)]
            hats(b + 1, 0.9, dens=8)
        arp(b, 'Fm', 64)

    def build_up(b):
        """twee maten: roffel 8sten -> 16den -> 32sten, sirene + reese een octaaf omhoog, ruisriser, reverse crash,
        de laatste achtste stil. Akkoorden Db | C."""
        s = t(b)
        P['kick'].append([s, s + KITLEN[KICK], KICK, 124])
        P['kick'] += [[t(b, p), t(b, p) + KITLEN[KICK], KICK, 110] for p in (8,)]
        # roffel: maat 1 achtsten, maat 2 tel 1-2 16den, tel 3 32sten, tel 4 (tot de laatste 8ste) 32sten fortissimo
        roll = [(p, 64 + 2 * p) for p in range(0, 16, 2)]
        roll += [(16 + p, 84 + 2 * p) for p in range(8)]
        roll += [(24 + p / 2, 100 + p) for p in range(8)]
        roll += [(28 + p / 2, 112 + 3 * p) for p in range(4)]
        for p, v in roll:
            st = t(b) + int(p * S)
            P['ghost'].append([st, st + KITLEN[ROLL], ROLL, min(127, v)])
        P['snare'].append([t(b + 1, 12), t(b + 1, 12) + KITLEN[SNARE], SNARE, 124])
        # hihats: 16den die aanzwellen, de laatste tel weg
        for p in range(28):
            P['hat'].append([t(b) + p * S, t(b) + p * S + KITLEN[HAT], HAT, 50 + p * 2])
        # ruisriser (PSG)
        P['noise'] += [[t(b) + i * E, t(b) + i * E + E, 48 + i, 30 + 6 * i] for i in range(14)]
        noise_prog.extend([(t(b), RISER), (t(b + 2), SHAKER)])
        # sirene (vierkant 1) twee maten omhoog
        sq1_prog.extend([(t(b), SIREN), (t(b + 2), LEADSQ)])
        P['sq1'].append([t(b), t(b + 1, 14), n('C4'), 92])
        extra['sq1'] += [(t(b) + i * 24, mido.Message('pitchwheel', pitch=min(8191, int(8192 * (i / 30) ** 1.4))))
                         for i in range(1, 31)]
        extra['sq1'].append((t(b + 1, 14), 'reset'))
        # reese: Db dan C die een octaaf opstijgt
        P['reese'].append([t(b), t(b + 1) - 8, n('Db2'), 108])
        reese_prog.append((t(b), REESE['rawdark']))
        P['reese'].append([t(b + 1), t(b + 1, 14), n('C2'), 112])
        reese_prog.append((t(b + 1), REESE['raw']))
        bend('reese', t(b + 1), t(b + 1, 14), 'rise', 12)
        P['sub'].append([t(b), t(b + 1) - 8, n('Db2'), 104])
        P['sub'].append([t(b + 1), t(b + 1, 12), n('C2'), 108])
        arp(b, 'Db', 64)
        arp(b + 1, 'C', 74)
        stabs(b, 'Db', [0], 'stab', 100)
        stabs(b + 1, 'C', [0], 'stab', 104)
        P['fx'].append([t(b + 2) - 440, t(b + 2) - 2, REVCYM, 104])

    def drop_bar(b, k, mel, kind=None, bass='1', ridebar=False, vel=127):
        ch = DROP_CH[k % 8]
        if kind is None:
            kind = 'fill' if k % 8 == 7 else ('amen' if k % 4 == 3 else ('two_b' if k % 2 else 'two'))
        drums(b, kind)
        hats(b, open_last=k % 2 == 1 and kind != 'fill')
        if bass == '1':
            bass_bar(b, ch, BASS1[BASS1_ORDER[k % 8]])
        elif bass == '2':
            bass_bar(b, ch, BASS2 if k % 8 != 7 else BASS1['C'])
        if mel is not None:
            lead(b, mel[k % 8], vel)
        arp(b, ch, 62)
        if ridebar:
            ride(b)
        if k % 8 == 0:
            crash(b)
            stabs(b, ch, [0], 'horn', 116)

    # ================= INTRO =================
    stinger(0)
    for i, ch in enumerate(['Fm', 'Fm', 'Db', 'Eb']):
        b = 2 + i
        drums(b, 'intro')
        hats(b, 0.75 + 0.05 * i)
        ostinato(b, ch, 112 + 3 * i)
        arp(b, ch, 50 + 4 * i)
        r = n(BASS_ROOT[ch])
        P['reese'] += [[t(b), t(b, 6), r, 100], [t(b, 6), t(b, 8), r, 92], [t(b, 10), t(b, 16) - 4, r, 100]]
        reese_prog.append((t(b), REESE['rawdark']))
        sub_note(t(b), t(b, 8), r, 104)
        sub_note(t(b, 10), t(b, 16) - 4, r, 104)
        if i == 0:
            crash(b, 100)
    build_up(6)

    # ================= LOOP =================
    # DROP 1 (8-23)
    for k in range(16):
        drop_bar(8 + k, k, MEL_A, ridebar=k >= 8)
    crash(16, 112)
    # BREAKDOWN (24-27): pad, koor, arpeggio, sub, shaker (16den lopen door)
    crash(24, 100)
    P['kick'].append([t(24), t(24) + KITLEN[KICK], KICK, 127])
    for i in range(4):
        b = 24 + i
        ch = BREAK_CH[i]
        pad(b, ch, 92)
        arp(b, ch, 58)
        shaker(b, 0.8 + 0.1 * i)
        rt = chord_root(ch, 29)
        sub_note(t(b), t(b + 1) - 6, rt if rt <= n('Eb2') else rt - 12, 100)
        for p, ln, nm in AAH_MEL[i]:
            P['aah'].append([t(b, p), t(b, p + ln) - 6, n(nm), 104])
    # OPBOUW (28-31)
    for i, b in enumerate((28, 29)):
        ch = BREAK_CH[i]
        P['kick'] += [[t(b, p), t(b, p) + KITLEN[KICK], KICK, 112 + 6 * i] for p in ((0, 4, 8, 12) if i == 0 else range(0, 16, 2))]
        hats(b, 0.7 + 0.15 * i)
        pad(b, ch, 84)
        arp(b, ch, 62)
        for p, ln, nm in AAH_MEL[i]:
            P['aah'].append([t(b, p), t(b, p + ln) - 6, n(nm) + 12, 108])
        rt = chord_root(ch, 29)
        rt = rt if rt <= n('Eb2') else rt - 12
        P['reese'].append([t(b), t(b + 1) - 8, rt, 96])
        reese_prog.append((t(b), REESE['rawdark']))
        sub_note(t(b), t(b + 1) - 8, rt, 104)
    P['snare'] += [[t(29, p), t(29, p) + KITLEN[SNARE], SNARE, 100] for p in (4, 12)]
    build_up(30)
    # VALSE DROP (32-33) + REWIND (34) + LUCHTHOORN (35)
    drop_bar(32, 0, MEL_A)
    drop_bar(33, 1, MEL_A, kind='amen')
    P['fx'].append([t(34), t(34, 12), REWIND, 124])
    P['fx'] += [[t(35, p), t(35, p + ln), HORN, 116] for p, ln in ((0, 2), (3, 2), (6, 5))]
    P['kick'] += [[t(35, p), t(35, p) + KITLEN[KICK], KICK, 124] for p in (0, 3, 6)]
    roll = [(8 + p, 80 + 3 * p) for p in range(4)] + [(12 + p / 2, 96 + 4 * p) for p in range(8)]
    for p, v in roll:
        st = t(35) + int(p * S)
        P['ghost'].append([st, st + KITLEN[ROLL], ROLL, min(127, v)])
    P['noise'] += [[t(35) + i * S, t(35) + i * S + S, 60 + 2 * i, 50 + 4 * i] for i in range(8, 16)]
    noise_prog.extend([(t(35, 8), RISER), (t(36), SHAKER)])
    P['fx'].append([t(36) - 440, t(36) - 2, REVCYM, 100])
    # DROP 2a (36-43): melodie B, stotterbas
    for k in range(8):
        drop_bar(36 + k, k, MEL_B, kind='fill' if k == 7 else ('amen' if k % 2 else 'two'), bass='2')
    # WOBBLE (44-47): two-step op vol tempo, thema A 1-4
    for k, (root, bars) in enumerate((('F1', 2), (None, 0), ('Db2', 1), ('Eb2', 1))):
        b = 44 + k
        drop_bar(b, k, MEL_A, bass=None, kind='amen' if k == 3 else ('two_b' if k % 2 else 'two'))
        if root:
            wobble(b, root, bars)
    # CLIMAX (48-51): thema A 5-8, stotterbas, ride
    for k in range(4, 8):
        drop_bar(48 + k - 4, k, MEL_A, bass='2', ridebar=False, kind='fill' if k == 7 else None)
    crash(48, 116)
    crash(50, 108)
    # STINGER (52-53) over drums + bas, BUILD-UP (54-55 = 6-7)
    stinger(52, with_drums=True)
    build_up(54)
    return P, dict(reese=reese_prog, stab=stab_prog, horn=horn_prog, pad=pad_prog, noise=noise_prog, sq1=sq1_prog), extra


def clip_loop(notes):
    out = []
    for a, b, nt, v in notes:
        for g in (LOOP_START, LOOP_END):
            if a < g < b:
                b = g
        if a < LOOP_END:
            out.append([a, b, nt, v])
    return dedupe(out)


def same_pitch_overlap(notes):
    """Dezelfde toonhoogte mag in één spoor niet overlappen (de note-off van de eerste kapt de tweede af)."""
    notes = sorted(notes)
    for i, e in enumerate(notes):
        for f in notes[i + 1:]:
            if f[0] >= e[1]:
                break
            if f[2] == e[2] and f[0] > e[0]:
                e[1] = f[0]
    return notes


def main():
    P, progs_, extra = build()
    for k in P:
        P[k] = same_pitch_overlap(clip_loop(P[k]))
    # golfkanaal: een golf van één periode klinkt een octaaf lager dan genoteerd (zie MUZIEK.md)
    P['sub'] = [[a, b, nt + 12, v] for a, b, nt, v in P['sub']]
    write_voicegroup()
    rel = {'reese': 150, 'lead': 127, 'lead2': 160, 'stab': 170, 'horn': 190, 'pad': 200, 'aah': 165}
    tail = {k: release_ticks(r, TPB, BPM) for k, r in rel.items()}
    kitrel = {36 + i: k[2] for i, k in enumerate(KIT)}
    for k in ('kick', 'snare', 'ghost', 'clap', 'hat', 'ride', 'fx'):
        tail[k] = max(release_ticks(kitrel[nt], TPB, BPM) if kitrel[nt] else 0 for _, _, nt, _ in P[k]) if P[k] else 0
    tail['crash'] = 0
    P['kick'] = [[a, b, nt, int(v * 0.85)] for a, b, nt, v in P['kick']]      # kick iets onder de snare (gemeten)
    for k in ('reese', 'lead', 'lead2', 'pad', 'aah'):
        P[k] = detach(P[k], tail[k])
    order = ['lead', 'kick', 'snare', 'reese', 'crash', 'fx', 'horn', 'lead2', 'hat', 'ghost', 'clap', 'stab', 'ride', 'aah', 'pad']
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

    def progs(lst):
        """programmawissels; op het loopbegin het programma dat daar hoort nog eens zetten (de sprong terug)."""
        lst = sorted(set(lst))
        out = [(tk, 'prog', p) for tk, p in lst if tk < LOOP_END]
        cur = [p for tk, p in lst if tk <= LOOP_START]
        if cur and not any(tk == LOOP_START for tk, _ in lst):
            out.append((LOOP_START, 'prog', cur[-1]))
        return out

    def bends(track):
        """pitchwheel binnen de loop; 'reset' wordt pas bij de volgende noot gezet (niet bij de note-off: dan
        springt de uitklinkende staart omhoog). BENDR 12 aan het begin en op het loopbegin bend 0."""
        ev = [(0, mido.Message('control_change', control=20, value=12))]
        starts = sorted(set(a for a, *_ in P[track]))
        for tk, m in extra[track]:
            if tk >= LOOP_END:
                continue
            if isinstance(m, str):
                nxt = next((s for s in starts if s >= tk), None)
                if nxt is not None and nxt < LOOP_END:
                    ev.append((nxt, mido.Message('pitchwheel', pitch=0)))
            else:
                ev.append((tk, m))
        ev.append((LOOP_START, mido.Message('pitchwheel', pitch=0)))
        return ev

    layout = [  # naam, noten, programma, volume, kanaal, pan, ccs, extra
        ('drums', sorted(P['kick'] + P['snare'] + P['ghost'] + P['clap']), DRUMS, 127, 9, 64, (), ()),
        ('hats', P['hat'], DRUMS, 127, 8, 74, (), ()),
        ('cym', sorted(P['ride'] + P['crash']), DRUMS, 100, 10, 56, (), ()),
        ('fx', P['fx'], DRUMS, 96, 11, 64, (), ()),
        ('reese', P['reese'], REESE['raw'], 80, 0, 64, progs(progs_['reese']), bends('reese')),
        ('lead', P['lead'], LEAD, 127, 1, 60, (), ()),
        ('lead2', P['lead2'], LEAD2, 84, 6, 68, (), ()),
        ('stab', P['stab'], STAB_MIN, 64, 2, 70, progs(progs_['stab']), ()),
        ('horn', P['horn'], HORN_MIN, 84, 3, 54, progs(progs_['horn']), ()),
        ('pad', P['pad'], PAD_MIN, 62, 4, 64, progs(progs_['pad']), ()),
        ('aah', P['aah'], AAH, 80, 5, 64, (), ()),
        ('noise', P['noise'], SHAKER, 70, 12, 72, progs(progs_['noise']), ()),
        ('sub', P['sub'], SUB, 52, 13, 64, (), ()),
        ('arp', P['arp'], ARP, 28, 14, 84, (), ()),
        ('sq1', P['sq1'], LEADSQ, 62, 15, 52, progs(progs_['sq1']), bends('sq1')),
    ]
    for name, notes, prog, vol, ch, pan, ccs, extr in layout:
        song.add(notes, prog, vol, ch, pan, extra=extr, ccs=ccs)
    written = {'kick', 'snare', 'ghost', 'clap', 'hat', 'ride', 'crash'} | {nm for nm, *_ in layout}
    assert not [k for k in P if P[k] and k not in written], 'partij niet weggeschreven'
    assert len(layout) <= 16
    song.save(OUT, LOOP_END)
    sec = lambda tk: tk / TPB * 60 / BPM
    print(OUT, '%d sporen, intro %.1f s, loop %.1f s, totaal %.1f s' % (len(layout), sec(LOOP_START),
                                                                      sec(LOOP_END - LOOP_START), sec(LOOP_END)))
    for nm, b in (('stinger', 0), ('ostinato', 2), ('build-up', 6), ('drop 1', 8), ('breakdown', 24), ('build-up', 28),
                  ('valse drop', 32), ('rewind', 34), ('drop 2a', 36), ('wobble', 44), ('climax', 48), ('stinger', 52),
                  ('build-up', 54)):
        print('  %-10s maat %2d  %5.1f s' % (nm, b, sec(t(b))))
    # drumdichtheid (aanslagen per maat, drums + hihats) in de drops
    for nm, b0, b1 in (('drop 1', 8, 24), ('drop 2a', 36, 44), ('climax', 48, 52)):
        d = sum(1 for k in ('kick', 'snare', 'ghost') for a, *_ in P[k] if t(b0) <= a < t(b1)) / (b1 - b0)
        h = sum(1 for a, *_ in P['hat'] if t(b0) <= a < t(b1)) / (b1 - b0)
        print('  dichtheid %-8s drums %.1f + hihats %.1f per maat' % (nm, d, h))


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + Drum & Bass-samples (mitch_samples.py) en een eigen drumkit voor Battle! Mitch.'
    lines[1] = '@ Gegenereerd door tools/grounded/mitch_theme.py.'
    lines[2] = 'voice_group %s' % VG
    ds = lambda smp, rel, key=60, att=255, dec=0, sus=255: \
        '\tvoice_directsound %d, 0, DirectSoundWaveData_%s, %d, %d, %d, %d' % (key, smp, att, dec, sus, rel)
    rep = {
        32: ds('mitch_reese_dark', 150), 33: ds('mitch_reese_mid', 150), 34: ds('mitch_reese_bright', 150),
        35: ds('mitch_growl', 150),
        36: ds('mitch_wob_f1', 170), 37: ds('mitch_wob_ab1', 170), 38: ds('mitch_wob_c2', 170),
        39: ds('mitch_wob_db2', 170), 40: ds('mitch_wob_eb2', 170),
        41: ds('mitch_reese_raw', 150), 42: ds('mitch_reese_raw_dark', 150),
        61: ds('mitch_horn_min', 190), 62: ds('mitch_horn_maj', 190),
        80: '\tvoice_square_1 60, 0, 0, 2, 0, 0, 15, 2',
        81: '\tvoice_square_2 60, 0, 1, 0, 2, 4, 1',
        82: '\tvoice_square_1 60, 0, 0, 1, 0, 1, 10, 1',
        84: '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_8, 0, 7, 15, 1',
        88: ds('mitch_pad_min', 200, att=40), 89: ds('mitch_pad_maj', 200, att=40),
        90: ds('mitch_stab_min', 170), 91: ds('mitch_stab_maj', 170), 92: ds('mitch_lead', 160),
        120: '\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0',
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
    for nm, smp, r, _ in KIT:
        if smp == 'trinity_cymbal_crash':
            kit.append('voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165')
        else:
            kit.append('voice_directsound_no_resample 60, 64, DirectSoundWaveData_%s, 255, 0, 255, %d' % (smp, r))
    open('sound/voicegroups/drumsets/mitch.inc', 'w').write(
        '@ Project Grounded: Drum & Bass-kit voor Battle! Mitch (mitch_theme.py), alles DirectSound:\n'
        '@ ' + ', '.join('%d %s' % (36 + i, k[0].lower()) for i, k in enumerate(KIT)) + '.\n'
        'voice_group mitch_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    main()
