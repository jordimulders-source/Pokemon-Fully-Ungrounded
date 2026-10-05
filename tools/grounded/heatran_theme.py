#!/usr/bin/env python3
"""Project Grounded: "Battle! Heatran", een eigen compositie in stoner metal / desert rock à la Kyuss ('Green Machine',
'Gardenia', 'Thumb', 'One Inch Man'): laaggestemde fuzzgitaren, een fuzzbas die de riff verdubbelt, groovende drums
die net achter de tel zitten. Hitte, woestijn, lava.

116 bpm, D (drop D: de gitaarriff staat op D2 = de lage open snaar), D-mineur-pentatonisch + blue note Ab.
  maat 0-1   intro: feedback-zwelling (powerchord D + hoge fuzztoon die aanzwelt, vibrato), lava-rommel op de floor tom
  maat 2-3   de riff, alleen gitaar + bas + kick; snarefill naar de loop
Loop (32 maten, ±66 s):
  A     4-11   de hook-riff (2 maten) x4, open hihat in achtsten, de 4e keer een chromatische klim G-Ab-A
  B    12-19   tweede riff op G (rijdend, 'Gardenia'), ride; de leadgitaar zingt een 'zang'-melodie erboven
  H    20-23   loom halftempo: zware powerchords, snare op 3, crash elke maat, kreunende feedback erboven
  Break 24-27  alleen bas en drums (bas speelt de riff + een bluesy loopje), feedback zwelt aan in maat 27
  Solo 28-35   de riff komt terug, bluesy pentatonische gitaarsolo met bends; laatste maat = de klim -> terug naar A
Gitaren: één sample = een complete fuzz-powerchord (G2+D3+G3 samen door de fuzz uit FluidR3, zoals een echte
versterker: de intermodulatie zit erin) = 1 kanaal per akkoord; twee sporen links/rechts, de rechter +9 cent
(dubbele opname). Losse riffnoten op een eigen fuzzsample. Fuzzbas = picked bass met eigen tanh-overdrive.
Drums: eigen kit (drumsets/heatran.inc) uit FluidR3: kick, snare, open hihat, ride, floor tom, crash; alles
DirectSound, geen PSG-piepjes. Samples: tools/grounded/gm_samples.py (heatran_*).

Gebruikt tools/grounded/musiclib.py. Zie tools/grounded/MUZIEK.md. Gebruik: python3 tools/grounded/heatran_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks

OUT = 'sound/songs/midi/mus_grounded_vs_heatran.mid'
VG = 'grounded_heatran'
TPB, BPM = 96, 116
S = TPB // 4                   # een 16e
BAR = TPB * 4
LAY = 4                        # snare iets achter de tel (1 m4a-tick = 4 MIDI-ticks bij 96 tpb)
SINGLE, POWER, LEAD, BASS, DRUMS = 29, 30, 31, 34, 127
# eigen drumkit (drumsets/heatran.inc, vanaf noot 36)
KICK, SNARE, OHH, RIDE, FTOM, MTOM, CRASH, CRASH2 = range(36, 44)
DRUM_REL = {KICK: 0, SNARE: 0, OHH: 200, RIDE: 210, FTOM: 0, MTOM: 0, CRASH: 220, CRASH2: 220}
DRUM_LEN = {KICK: TPB // 2, SNARE: TPB * 3 // 4, OHH: TPB // 2 - 6, RIDE: TPB, FTOM: TPB // 2, MTOM: TPB // 2,
            CRASH: TPB * 2, CRASH2: TPB * 2}

A0, B0, H0, K0, SO, END = 4, 12, 20, 24, 28, 36      # secties (maat); loop = maat 4-36

N = {'C': 0, 'C#': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def p(name):
    """'D2' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- riffs: (16e, lengte in 16en, 'P' powerchord | 'N' losse noot, grondtoon) -------------------------------------
RIFF_1 = [(0, 3, 'P', 'D2'), (3, 1, 'N', 'D2'), (4, 1, 'N', 'F2'), (5, 1, 'N', 'D2'), (6, 2, 'P', 'F2'),
          (8, 3, 'P', 'G2'), (11, 1, 'N', 'Ab2'), (12, 2, 'P', 'G2'), (14, 1, 'N', 'F2'), (15, 1, 'N', 'D2')]
RIFF_2 = [(0, 6, 'P', 'D2'), (6, 1, 'N', 'D2'), (7, 1, 'N', 'F2'), (8, 3, 'P', 'C3'), (11, 3, 'P', 'Bb2'),
          (14, 1, 'N', 'G2'), (15, 1, 'N', 'F2')]
RIFF_2X = [(0, 6, 'P', 'D2'), (6, 1, 'N', 'D2'), (7, 1, 'N', 'F2'), (8, 2, 'P', 'G2'), (10, 2, 'P', 'Ab2'),
           (12, 4, 'P', 'A2')]                                         # de klim naar de volgende sectie
VERSE_1 = [(0, 2, 'P', 'G2'), (2, 1, 'N', 'G2'), (3, 1, 'N', 'G2'), (4, 2, 'P', 'G2'), (6, 1, 'N', 'Bb2'),
           (7, 1, 'N', 'G2'), (8, 2, 'P', 'F2'), (10, 1, 'N', 'F2'), (11, 1, 'N', 'F2'), (12, 4, 'P', 'D2')]
VERSE_2 = [(0, 2, 'P', 'G2'), (2, 1, 'N', 'G2'), (3, 1, 'N', 'G2'), (4, 2, 'P', 'G2'), (6, 1, 'N', 'Bb2'),
           (7, 1, 'N', 'C3'), (8, 3, 'P', 'C3'), (11, 3, 'P', 'Bb2'), (14, 2, 'P', 'A2')]
HALF = [[(0, 12, 'P', 'D2'), (12, 2, 'N', 'F2'), (14, 2, 'N', 'Ab2')],
        [(0, 8, 'P', 'G2'), (8, 8, 'P', 'F2')],
        [(0, 12, 'P', 'D2'), (12, 2, 'N', 'F2'), (14, 2, 'N', 'D2')],
        [(0, 8, 'P', 'Bb2'), (8, 8, 'P', 'C3')]]
BASS_WALK = [[(0, 3, 'D2'), (3, 1, 'D2'), (4, 2, 'F2'), (6, 2, 'G2'), (8, 1, 'Ab2'), (9, 1, 'G2'), (10, 2, 'F2'),
              (12, 2, 'D2'), (14, 2, 'C2')],
             [(0, 4, 'D2'), (4, 2, 'D2'), (6, 2, 'F2'), (8, 2, 'G2'), (10, 2, 'Ab2'), (12, 4, 'A2')]]

# ---- leadgitaar: (16e, lengte, noot, extra) ; extra: 'b' = bend van 2 halve tonen eronder, 'v' = vibrato ----------
SING = [   # B: de 'zang'-melodie (John Garcia) op de leadgitaar
    [(2, 2, 'A4', ''), (4, 6, 'C5', 'v'), (10, 2, 'A4', ''), (12, 4, 'G4', '')],
    [(0, 8, 'A4', 'bv'), (10, 2, 'F4', ''), (12, 4, 'D4', '')],
    [(2, 2, 'A4', ''), (4, 6, 'C5', 'v'), (10, 2, 'D5', ''), (12, 4, 'C5', '')],
    [(0, 12, 'A4', 'v')],
    [(2, 2, 'D5', ''), (4, 6, 'F5', 'v'), (10, 2, 'D5', ''), (12, 4, 'C5', '')],
    [(0, 8, 'D5', 'bv'), (8, 4, 'C5', ''), (12, 4, 'A4', '')],
    [(2, 2, 'G4', ''), (4, 4, 'A4', ''), (8, 4, 'C5', ''), (12, 4, 'D5', '')],
    [(0, 6, 'A4', 'v'), (6, 2, 'G4', ''), (8, 8, 'D4', 'v')],
]
SOLO = [
    [(0, 2, 'A4', ''), (2, 2, 'C5', ''), (4, 4, 'D5', 'b'), (8, 2, 'C5', ''), (10, 2, 'A4', ''), (12, 4, 'G4', 'v')],
    [(0, 2, 'A4', ''), (2, 1, 'G4', ''), (3, 1, 'F4', ''), (4, 4, 'D4', 'v'), (10, 2, 'F4', ''), (12, 2, 'G4', ''),
     (14, 2, 'Ab4', '')],
    [(0, 6, 'A4', 'bv'), (6, 2, 'C5', ''), (8, 2, 'D5', ''), (10, 2, 'F5', ''), (12, 4, 'D5', 'v')],
    [(0, 2, 'C5', ''), (2, 2, 'A4', ''), (4, 2, 'C5', ''), (6, 2, 'A4', ''), (8, 8, 'G4', 'v')],
    [(0, 1, 'D5', ''), (1, 1, 'C5', ''), (2, 1, 'A4', ''), (3, 1, 'G4', ''), (4, 1, 'A4', ''), (5, 1, 'C5', ''),
     (6, 1, 'D5', ''), (7, 1, 'F5', ''), (8, 4, 'G5', 'bv'), (12, 2, 'F5', ''), (14, 2, 'D5', '')],
    [(0, 1, 'F5', ''), (1, 1, 'D5', ''), (2, 1, 'C5', ''), (3, 1, 'D5', ''), (4, 1, 'F5', ''), (5, 1, 'D5', ''),
     (6, 1, 'C5', ''), (7, 1, 'A4', ''), (8, 4, 'C5', ''), (12, 4, 'A4', 'v')],
    [(0, 8, 'D5', 'bv'), (8, 2, 'F5', ''), (10, 2, 'G5', ''), (12, 4, 'A5', 'b')],
    [(0, 6, 'D5', 'v'), (6, 2, 'C5', ''), (8, 2, 'A4', ''), (10, 2, 'Ab4', ''), (12, 4, 'A4', 'v')],
]


def bass_note(n):
    """Bas in E1-A2: zelfde toonklasse als de riff, zo laag mogelijk (nooit onder E1 = 28)."""
    while n > 45:
        n -= 12
    while n < 33:
        n += 12
    return n


class Parts:
    def __init__(self):
        self.n = {k: [] for k in ('pwrL', 'pwrR', 'sglL', 'sglR', 'bass', 'lead', 'fb', 'kick', 'snare', 'hat',
                                  'ride', 'tom', 'crash')}
        self.lead_fx = []         # (tick, soort, waarde) voor de leadgitaar
        self.fb_fx = []           # volume-zwellingen van de feedbackpartij
        self.pwr_fx = []          # volume-zwelling van de powerchords in de intro
        self.fills = []           # (start, eind) van tomfills: daar geen groove-snare/hihat/ride

    def add(self, part, start, length, note, vel):
        self.n[part].append([int(start), int(start + length), note, vel])


def riff(P, bar, pattern, vel=112, guitars=True, bass=True, right=True):
    for st, ln, kind, nm in pattern:
        s = bar * BAR + st * S
        acc = 10 if st in (0, 8) else (0 if kind == 'P' else -14)
        if guitars:
            if kind == 'P':
                P.add('pwrL', s, ln * S, p(nm), vel + acc)
                if right:
                    P.add('pwrR', s, ln * S, p(nm), vel + acc - 6)
            else:
                P.add('sglL', s, ln * S, p(nm), vel + acc)
                if right:
                    P.add('sglR', s, ln * S, p(nm), vel + acc - 6)
        if bass:
            P.add('bass', s, ln * S, bass_note(p(nm)), 116 + (6 if st in (0, 8) else 0))


def lead(P, bar, phrase, vel=118, part='lead'):
    for st, ln, nm, fx in phrase:
        s = bar * BAR + st * S
        n = p(nm)
        if 'b' in fx:                                       # bend: begin 2 halve tonen lager, in een 16e omhoog
            P.add(part, s, ln * S, n - 2, vel)
            for k in range(1, 7):
                P.lead_fx.append((s + k * S // 6, 'bend', min(8191, int(8192 * k / 6))))
        else:
            P.add(part, s, ln * S, n, vel)
        if 'v' in fx and ln >= 4:                           # vertraagd vibrato (na een 8e)
            P.lead_fx.append((s + 2 * S, 'mod', 9))


def drums_groove(P, bar, kind, kicks=(0, 6, 8, 14)):
    b = bar * BAR
    for k in kicks:
        P.add('kick', b + k * S, DRUM_LEN[KICK], KICK, 118 if k in (0, 8) else 104)
    if kind == 'half':
        P.add('snare', b + 8 * S + LAY, DRUM_LEN[SNARE], SNARE, 124)
        for q in range(4):
            P.add('ride', b + q * TPB, DRUM_LEN[RIDE], RIDE, 96 if q else 70)
        return
    for q in (4, 12):
        P.add('snare', b + q * S + LAY, DRUM_LEN[SNARE], SNARE, 122)
    if kind == 'hat':
        for e in range(8):
            P.add('hat', b + e * 2 * S, DRUM_LEN[OHH], OHH, 100 if e % 2 else 78)
    elif kind == 'ride':
        for e in range(8):
            P.add('ride', b + e * 2 * S, DRUM_LEN[RIDE] // 2, RIDE, 100 if e % 2 == 0 else 74)


def fill(P, bar, start16=12, end_crash=True):
    """Tomfill op tel 4 (snare + toms in 16en), naar een crash op de volgende maat."""
    b = bar * BAR
    P.fills.append((b + start16 * S, b + BAR))
    seq = [SNARE, SNARE, MTOM, MTOM, FTOM, FTOM, FTOM, SNARE][-(16 - start16):]
    for i, nt in enumerate(seq):
        s = b + (start16 + i) * S
        part = 'snare' if nt == SNARE else 'tom'
        P.add(part, s, S, nt, 96 + i * 4)


def crash(P, bar, note=CRASH, vel=120):
    P.add('crash', bar * BAR, DRUM_LEN[note], note, vel)
    P.add('kick', bar * BAR, DRUM_LEN[KICK], KICK, 124)


def build():
    P = Parts()

    # ---- intro: feedback-zwelling --------------------------------------------------------------------------------
    P.add('pwrL', 0, 2 * BAR - S, p('D2'), 110)
    P.add('pwrR', 0, 2 * BAR - S, p('D2'), 104)
    for k in range(33):                                     # powerchord zwelt in 2 maten aan (CC7 0 -> 100%)
        P.pwr_fx.append((k * 2 * BAR // 32, int(((k / 32) ** 1.6) * 100)))
    P.add('fb', BAR // 2, BAR + BAR // 2 - S, p('D5'), 110)      # hoge feedbacktoon zwelt mee
    for k in range(25):
        P.fb_fx.append((BAR // 2 + k * (BAR + BAR // 2) // 24, 'vol', int(((k / 24) ** 1.3) * 100)))
    P.fb_fx += [(BAR, 'mod', 4), (BAR + BAR // 2, 'mod', 10)]
    for k in range(16):                                     # lava-rommel op de floor tom in maat 1
        P.add('tom', BAR + k * S, S, FTOM, 50 + k * 4)
    crash(P, 2)
    riff(P, 2, RIFF_1, guitars=True)
    riff(P, 3, RIFF_2X)
    for k in (0, 6, 8, 14):
        P.add('kick', 2 * BAR + k * S, DRUM_LEN[KICK], KICK, 110)
    for k in (0, 8, 10, 12):
        P.add('kick', 3 * BAR + k * S, DRUM_LEN[KICK], KICK, 110)
    fill(P, 3, 8)

    # ---- A: de hook ----------------------------------------------------------------------------------------------
    for i in range(8):
        b = A0 + i
        pat = RIFF_1 if i % 2 == 0 else (RIFF_2X if i == 7 else RIFF_2)
        riff(P, b, pat)
        drums_groove(P, b, 'hat', (0, 6, 8, 14) if i % 2 == 0 else (0, 7, 8, 11))
    crash(P, A0)
    crash(P, A0 + 4, CRASH2, 110)
    fill(P, B0 - 1)

    # ---- B: tweede riff + zang -----------------------------------------------------------------------------------
    for i in range(8):
        b = B0 + i
        riff(P, b, VERSE_1 if i % 2 == 0 else VERSE_2, vel=108)
        drums_groove(P, b, 'ride', (0, 3, 8, 10) if i % 2 == 0 else (0, 3, 8, 11, 14))
        lead(P, b, SING[i], 112)
    crash(P, B0)
    crash(P, B0 + 4, CRASH2, 110)
    fill(P, H0 - 1)

    # ---- H: loom halftempo ---------------------------------------------------------------------------------------
    for i in range(4):
        b = H0 + i
        riff(P, b, HALF[i], vel=116)
        drums_groove(P, b, 'half', (0, 10) if i % 2 == 0 else (0, 6, 10))
        crash(P, b, CRASH if i % 2 == 0 else CRASH2, 116)
    for k, nm in ((0, 'D5'), (2, 'C5')):                     # kreunende feedback, 2 x 2 maten
        s = (H0 + k) * BAR
        P.add('fb', s, 2 * BAR - S, p(nm), 104)
        for j in range(13):
            P.fb_fx.append((s + j * BAR // 6, 'vol', int(40 + 60 * min(1, j / 8))))
        P.fb_fx += [(s, 'mod', 0), (s + BAR, 'mod', 10)]
    fill(P, K0 - 1, 12)

    # ---- break: bas + drums --------------------------------------------------------------------------------------
    riff(P, K0, RIFF_1, guitars=False)
    riff(P, K0 + 1, RIFF_2, guitars=False)
    for i, walk in enumerate(BASS_WALK):
        for st, ln, nm in walk:
            P.add('bass', (K0 + 2 + i) * BAR + st * S, ln * S, bass_note(p(nm)), 118 + (6 if st in (0, 8) else 0))
    for i in range(4):
        drums_groove(P, K0 + i, 'ride', (0, 6, 8, 14) if i % 2 == 0 else (0, 7, 8, 11))
    crash(P, K0, CRASH2, 112)
    s = (K0 + 3) * BAR                                      # feedback zwelt aan in maat 27: de riff komt terug
    P.add('fb', s, BAR - S, p('A4'), 110)
    for j in range(17):
        P.fb_fx.append((s + j * BAR // 16, 'vol', int(((j / 16) ** 1.5) * 100)))
    P.fb_fx += [(s, 'mod', 0), (s + BAR // 2, 'mod', 8)]
    fill(P, K0 + 3, 8)

    # ---- solo: de riff terug + bluesy leadgitaar ------------------------------------------------------------------
    for i in range(8):
        b = SO + i
        pat = RIFF_1 if i % 2 == 0 else (RIFF_2X if i == 7 else RIFF_2)
        riff(P, b, pat, right=False)                        # rechtergitaar zwijgt: daar staat de solo
        drums_groove(P, b, 'hat', (0, 6, 8, 14) if i % 2 == 0 else (0, 7, 8, 11))
        lead(P, b, SOLO[i], 120)
    crash(P, SO)
    crash(P, SO + 4, CRASH2, 112)
    fill(P, END - 1)

    for k in ('hat', 'ride'):
        P.n[k] = [x for x in P.n[k] if not any(a <= x[0] < b for a, b in P.fills)]
    P.n['snare'] = [x for x in P.n['snare'] if x[0] % S == 0 or not any(a <= x[0] < b for a, b in P.fills)]
    for k in P.n:
        P.n[k] = dedupe(P.n[k])
    return P


def write_voicegroup():
    """grounded_gm + 29 fuzz (losse noten), 30 fuzz-powerchord, 31 fuzz-lead, 34 fuzzbas, 127 stoner-drumkit."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Heatran (stoner metal). Gegenereerd door tools/grounded/heatran_theme.py.'
    lines[1] = '@ 29 = fuzzgitaar (losse noten), 30 = fuzz-powerchord (1 sample = 1 kanaal), 31 = fuzz-lead, 34 = fuzzbas, 127 = drumkit.'
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 29': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_fuzz_low, 255, 0, 255, 165  @ 29',
        '@ 30': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_fuzz_power, 255, 0, 255, 165  @ 30',
        '@ 31': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_fuzz_lead, 255, 0, 255, 200  @ 31',
        '@ 34': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_fuzz_bass, 255, 0, 255, 160  @ 34',
        '@ 127': '\tvoice_keysplit_all voicegroup_heatran_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [   # vanaf noot 36; alles DirectSound
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_heatran_kick, 255, 0, 255, %d' % DRUM_REL[KICK],
        'voice_directsound_no_resample 60, 60, DirectSoundWaveData_heatran_snare, 255, 0, 255, %d' % DRUM_REL[SNARE],
        'voice_directsound_no_resample 60, 84, DirectSoundWaveData_heatran_open_hat, 255, 0, 255, %d' % DRUM_REL[OHH],
        'voice_directsound_no_resample 60, 44, DirectSoundWaveData_heatran_ride, 255, 0, 255, %d' % DRUM_REL[RIDE],
        'voice_directsound 60, 40, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, %d' % DRUM_REL[FTOM],
        'voice_directsound 66, 80, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, %d' % DRUM_REL[MTOM],
        'voice_directsound_no_resample 60, 36, DirectSoundWaveData_heatran_crash, 255, 0, 255, %d' % DRUM_REL[CRASH],
        'voice_directsound 57, 92, DirectSoundWaveData_heatran_crash, 255, 0, 255, %d' % DRUM_REL[CRASH2],
    ]
    open('sound/voicegroups/drumsets/heatran.inc', 'w').write(
        '@ Project Grounded: stoner-drumkit voor Battle! Heatran (heatran_theme.py), samples uit FluidR3 (gm_samples.py):\n'
        '@ 36 kick, 37 snare, 38 open hihat, 39 ride, 40 floor tom, 41 middentom, 42 crash (links), 43 crash (rechts, lager).\n'
        'voice_group heatran_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


def save(P, path):
    """MIDI wegschrijven, met volume-zwellingen (CC7), vibrato (CC1) en bends (pitchwheel) per spoor."""
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    cond.append(mido.MetaMessage('set_tempo', tempo=int(60e6 / BPM), time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=A0 * BAR))
    cond.append(mido.MetaMessage('marker', text=']', time=(END - A0) * BAR))
    out.tracks.append(cond)

    def fx_lead(fx, notes):
        """bend/mod terugzetten op het begin van de volgende noot (niet bij de note-off: dan zakt de uitklinktijd)."""
        starts = sorted(set(n[0] for n in notes))
        ev = []
        for t, kind, v in fx:
            ev.append((t, kind, v))
            nxt = next((s for s in starts if s > t), None)
            if nxt is not None:
                ev.append((nxt, kind, 0))
        # per tijdstip/soort: een terugzetting mag een nieuwe waarde op hetzelfde moment niet overschrijven
        best = {}
        for t, kind, v in ev:
            if (t, kind) not in best or v:
                best[(t, kind)] = v if (t, kind) not in best else max(best[(t, kind)], v)
        return [(t, k, v) for (t, k), v in best.items()]

    layout = [  # naam, programma, volume, kanaal, pan, extra
        ('pwrL', POWER, 100, 0, 20, [(t, 'vol', v) for t, v in P.pwr_fx]),
        ('pwrR', POWER, 96, 1, 108, [(0, 'bend', 3 * 128)] + [(t, 'vol', v * 96 // 100) for t, v in P.pwr_fx]),
        ('sglL', SINGLE, 100, 2, 28, []),
        ('sglR', SINGLE, 96, 3, 100, [(0, 'bend', 3 * 128)]),
        ('bass', BASS, 54, 4, 64, []),
        ('lead', LEAD, 112, 5, 80, fx_lead(P.lead_fx, P.n['lead'])),
        ('fb', LEAD, 100, 6, 52, P.fb_fx),
    ]
    for name, prog, vol, ch, pan, fx in layout:
        add_track(out, P.n[name], prog, vol, ch, pan, fx)
    drums = ('kick', 'snare', 'hat', 'ride', 'tom', 'crash')
    add_track(out, sorted(sum((P.n[k] for k in drums), [])), DRUMS, 127, 9, 64, [])
    written = {k for k, *_ in layout} | set(drums)
    assert not [k for k in P.n if P.n[k] and k not in written], 'partij niet weggeschreven'
    out.save(path)


def add_track(out, notes, prog, vol, ch, pan, fx):
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    ev = []
    for tk, kind, v in fx:     # volgorde op één tick: controllers vóór note-off vóór note-on
        if kind == 'vol':
            ev.append((tk, 0, mido.Message('control_change', channel=ch, control=7, value=max(0, min(127, v * vol // 100)))))
        elif kind == 'mod':
            ev.append((tk, 0, mido.Message('control_change', channel=ch, control=1, value=v)))
        elif kind == 'bend':
            ev.append((tk, 0, mido.Message('pitchwheel', channel=ch, pitch=v)))
    for s, e, n, v in notes:
        ev.append((e, 1, mido.Message('note_off', channel=ch, note=n, velocity=0)))
        ev.append((s, 2, mido.Message('note_on', channel=ch, note=n, velocity=max(1, min(127, int(v))))))
    last = 0
    for tk, _, m in sorted(ev, key=lambda x: (x[0], x[1])):
        t.append(m.copy(time=tk - last))
        last = tk
    out.tracks.append(t)


def main():
    P = build()
    write_voicegroup()
    rel = releases(VG)
    progs = {'pwrL': POWER, 'pwrR': POWER, 'sglL': SINGLE, 'sglR': SINGLE, 'bass': BASS, 'lead': LEAD, 'fb': LEAD}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    for k, nt in (('kick', KICK), ('snare', SNARE), ('hat', OHH), ('ride', RIDE), ('tom', FTOM), ('crash', CRASH)):
        tail[k] = release_ticks(DRUM_REL[nt] or None, TPB, BPM) if DRUM_REL[nt] else 0
    for k in ('pwrL', 'pwrR', 'sglL', 'sglR', 'bass', 'lead', 'fb'):
        P.n[k] = detach(P.n[k], tail[k])
    # een powerchord en een losse noot op dezelfde gitaar overlappen nooit: samen één partij voor de detach
    for side in 'LR':
        both = detach(sorted(P.n['pwr' + side] + P.n['sgl' + side]), tail['pwr' + side])
        pw = {(s, n) for s, e, n, v in P.n['pwr' + side]}
        P.n['pwr' + side] = [x for x in both if (x[0], x[2]) in pw]
        P.n['sgl' + side] = [x for x in both if (x[0], x[2]) not in pw]
    order = ['lead', 'pwrL', 'sglL', 'kick', 'snare', 'bass', 'crash', 'fb', 'tom', 'hat', 'ride', 'pwrR', 'sglR']
    kept = allocate({k: P.n[k] for k in order}, order, tail, max_voices=11)
    print('tail (ticks):', tail)
    for k in order:
        n = len(P.n[k])
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        P.n[k] = kept[k]
    save(P, OUT)
    print(OUT, '%.1f s intro, %.1f s loop' % (A0 * 4 * 60 / BPM, (END - A0) * 4 * 60 / BPM))


if __name__ == '__main__':
    main()
