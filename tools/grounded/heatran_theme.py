#!/usr/bin/env python3
"""Project Grounded: "Battle! Heatran" v4, eigen compositie: 100% Kyuss-desert rock (Blues for the Red Sun,
Welcome to Sky Valley; referenties Gardenia, Green Machine, Thumb).

Jordi over v1-v3: 'nog steeds veel te netjes, helder en vrolijk'. v4 volgt zijn productieregels punt voor punt:
  1. GITAAR (Josh Homme): nek-pickup + toonknop dicht -> asymmetrische fuzz -> cocked wah (800 Hz) -> SVT + kast,
     boven 4 kHz niets (heatran_samples.py). C standard (laagste noot C2). Zware, trage, repetitieve riffs in
     C-mineur-pentatonisch + b5 (Gb), lang doorklinkend; geen majeurwendingen, geen heldere leads. Elke riffnoot
     heeft een eigen sample op zijn toonhoogte (keysplit_heatran): niets wordt omhoog getransponeerd.
  2. BAS (Scott Reeder): speelt EXACT de gitaarriff (dezelfde MIDI-noten, sample een octaaf lager gelabeld), modderige
     tube-fuzz; geen eigen lijntjes. Drums: simpel, lomp, mechanisch: kick op de riffaccenten, doffe snare op 2 en 4,
     hihat in kwarten, crash alleen op een sectiebegin, geen fills (één simpele snare-8en aan het eind van de brug).
  3. 80 bpm, trage lome 'desert groove'; hypnotiserende herhaling.

  maat 0-1   intro: powerchord C zwelt aan + feedback (cocked wah), floor tom rommelt aan
  maat 2-3   de refreinriff één keer als statement (hele band)
  maat 4     de stop: akkoord hangt, feedback huilt
Loop (48 maten, 144 s):
  V1  5-12   strofe: bas + drums spelen riff A; vanaf maat 9 de gitaar zacht palm-muted links (dezelfde riff)
  R1 13-20   refrein: riff B, gitaren links/rechts + bas unisono, kick op de akkoorden
  V2 21-28   strofe 2: riff A, bas + drums, palm-mute links en rechts
  R2 29-36   refrein 2
  B  37-44   brug: hypnotische pedaalriff C (8en, gitaar + bas unisono), drums bouwen op (floor tom -> kick ->
             snare/hihat), feedback zwelt; één simpele snarefill aan het eind
  R3 45-52   refrein 3 + een donkere, kreunende wah-lead (laag, lange noten); 52 = de stop -> terug naar maat 5
Samples: tools/grounded/heatran_samples.py. Gebruikt musiclib.py; zie MUZIEK.md. Gebruik: python3 tools/grounded/heatran_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks

OUT = 'sound/songs/midi/mus_grounded_vs_heatran.mid'
VG = 'grounded_heatran'
TPB, BPM = 96, 80
S = TPB // 4                   # een 16e
E = TPB // 2                   # een 8e
BAR = TPB * 4
LAY = 3                        # snare iets achter de tel (lome groove)
MUTE, NOTE, POWER, LEAD, BASS, DRUMS = 28, 29, 30, 31, 34, 127
R_BEND = 3 * 128               # rechter gitaar ±9 cent hoger (dubbele opname)
# eigen drumkit (drumsets/heatran.inc, vanaf noot 36)
KICK, SNARE, HAT, CRASH, FTOM = range(36, 41)
DRUM_REL = {KICK: 0, SNARE: 0, HAT: 0, CRASH: 225, FTOM: 0}
DRUM_LEN = {KICK: TPB // 2, SNARE: TPB // 2, HAT: TPB // 4, CRASH: TPB * 2, FTOM: TPB // 2}
REL = {POWER: 200, NOTE: 200, MUTE: 140, LEAD: 210, BASS: 190}   # release per keysplit-instrument

INTRO_RIFF, STOP0 = 2, 4
V1, R1, V2, R2, B, R3, END = 5, 13, 21, 29, 37, 45, 53      # secties (maat); loop = maat 5-53

N = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def p(name):
    """'C2' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- riffs: (16e, lengte in 16en, soort, noot[, 's' = erin glijden]) ---------------------------------------------
# 'P' = powerchord (grondtoon + kwint + octaaf in één sample), 'N' = riffnoot (grondtoon + octaaf)
# riff A (strofe, 'Gardenia'): lange C, dan een loom pentatonisch loopje met de b5, terug naar de hangende C
RIFF_A1 = [(0, 6, 'P', 'C2'), (6, 2, 'N', 'C2'), (8, 2, 'N', 'Eb2'), (10, 2, 'N', 'C2'), (12, 3, 'N', 'F2', 's'),
           (15, 1, 'N', 'Gb2')]
RIFF_A2 = [(0, 4, 'P', 'F2'), (4, 2, 'N', 'Eb2'), (6, 2, 'N', 'C2'), (8, 8, 'P', 'C2')]
RIFF_A3 = [(0, 3, 'P', 'Gb2'), (3, 3, 'P', 'F2'), (6, 2, 'N', 'Eb2'), (8, 8, 'P', 'C2')]     # de b5 als doomkleur
# riff B (refrein, 'Green Machine'): beukende C-stoten, Eb/Gb, F die erin glijdt; dalend chromatisch naar huis
RIFF_B1 = [(0, 3, 'P', 'C2'), (3, 3, 'P', 'C2'), (6, 2, 'P', 'Eb2'), (8, 6, 'P', 'F2', 's'), (14, 2, 'N', 'Eb2')]
RIFF_B2 = [(0, 3, 'P', 'C2'), (3, 3, 'P', 'C2'), (6, 2, 'P', 'Gb2'), (8, 6, 'P', 'F2'), (14, 2, 'N', 'Eb2')]
RIFF_B4 = [(0, 4, 'P', 'G2'), (4, 4, 'P', 'Gb2'), (8, 4, 'P', 'F2'), (12, 4, 'P', 'Eb2')]
# riff C (brug, 'Thumb'): hypnotische pedaal in 8en
RIFF_C = [(0, 2, 'N', 'C2'), (2, 2, 'N', 'C2'), (4, 2, 'N', 'C3'), (6, 2, 'N', 'C2'), (8, 2, 'N', 'Bb2'),
          (10, 2, 'N', 'C2'), (12, 2, 'N', 'G2'), (14, 2, 'N', 'Gb2')]
STOP = [(0, 8, 'P', 'C2')]                                    # akkoord hangt 2 tellen, dan stilte

VERSE = [RIFF_A1, RIFF_A2, RIFF_A1, RIFF_A3] * 2
CHORUS = [RIFF_B1, RIFF_B2, RIFF_B1, RIFF_B4] * 2
CHORUS_END = CHORUS[:7] + [STOP]

# ---- lead in R3: laag, kreunend, lange noten ('b' = bend van 2 halve tonen eronder, 'v' = vibrato) -------------
MOAN = [
    [(0, 8, 'C4', 'b'), (8, 8, 'Eb4', 'v')],
    [(0, 12, 'C4', 'v')],
    [(0, 4, 'F4', ''), (4, 4, 'Gb4', ''), (8, 8, 'F4', 'v')],
    [(0, 6, 'Eb4', 'b'), (6, 2, 'C4', ''), (8, 8, 'Bb3', 'v')],
    [(0, 8, 'G4', 'bv'), (8, 8, 'F4', 'v')],
    [(0, 6, 'Eb4', ''), (6, 2, 'F4', ''), (8, 8, 'Eb4', 'v')],
    [(0, 8, 'Gb4', 'v'), (8, 8, 'F4', 'bv')],
    [(0, 12, 'C4', 'v')],
]


class Parts:
    def __init__(self):
        self.n = {k: [] for k in ('pwrL', 'pwrR', 'ntL', 'ntR', 'muteL', 'muteR', 'bass', 'lead', 'fb',
                                  'kick', 'snare', 'cym', 'tom')}
        self.fx = {k: [] for k in list(self.n) + ['drums']}   # (tick, 'vol'|'mod'|'bend', waarde); 'vol' = CC7 in %

    def add(self, part, start, length, note, vel):
        self.n[part].append([int(start), int(start + length), note, vel])

    def vol(self, parts, bar, pct):
        for k in parts:
            self.fx[k].append((bar * BAR, 'vol', pct))


def slide(P, part, s):
    """In de noot glijden: begint 2 halve tonen lager, in een 8e omhoog (pitchwheel; bereik 2 halve tonen)."""
    for k in range(0, 7):
        P.fx[part].append((s + k * E // 6, 'bend', min(8191, int(8192 * (k / 6 - 1)))))


def riff(P, bar, pattern, guitars=True, bass=True, sides=('L', 'R'), vel=116):
    """Gitaren en bas spelen exact dezelfde noten (de bas klinkt een octaaf lager: zie de samples)."""
    for st, ln, kind, nm, *fx in pattern:
        s = bar * BAR + st * S
        acc = 8 if st in (0, 8) else 0
        if guitars:
            for sd in sides:
                part = ('pwr' if kind == 'P' else 'nt') + sd
                P.add(part, s, ln * S, p(nm), vel + acc - (6 if sd == 'R' else 0))
                if fx and 's' in fx[0]:
                    slide(P, part, s)
        if bass:
            P.add('bass', s, ln * S, p(nm), 112 + acc)
            if fx and 's' in fx[0]:
                slide(P, 'bass', s)


def palm_mute(P, bar, pattern, sides=('L',), vel=100):
    """Dezelfde riff gedempt: elke riffnoot als gedempte 8e-chugs zolang de noot duurt."""
    for st, ln, kind, nm, *fx in pattern:
        for k in range(0, ln, 2):
            s = bar * BAR + (st + k) * S
            for sd in sides:
                P.add('mute' + sd, s, min(E, (ln - k) * S), p(nm),
                      vel + (10 if st + k in (0, 8) else 0) - (4 if sd == 'R' else 0))


def lead(P, bar, phrase, vel=112, part='lead'):
    for st, ln, nm, fx in phrase:
        s = bar * BAR + st * S
        P.add(part, s, ln * S, p(nm) - (2 if 'b' in fx else 0), vel)
        if 'b' in fx:                                       # bend: begint 2 halve tonen lager, in een 8e omhoog
            for k in range(1, 7):
                P.fx[part].append((s + k * E // 6, 'bend', min(8191, int(8192 * k / 6))))
        if 'v' in fx and ln >= 4:                           # vertraagd, traag vibrato
            P.fx[part].append((s + E, 'mod', 6))


def hats(P, b, vel=74):
    for q in range(4):
        P.add('cym', b + q * TPB, DRUM_LEN[HAT], HAT, vel + (6 if q % 2 == 0 else 0))


def verse_drums(P, bar, first):
    """Strofe: kick op 1, de 'en' van 2 en 3; snare (dof) op 2 en 4; hihat in kwarten; crash alleen op maat 1."""
    b = bar * BAR
    for k in (0, 6, 8):
        P.add('kick', b + k * S, DRUM_LEN[KICK], KICK, 122 if k == 0 else 110)
    for q in (4, 12):
        P.add('snare', b + q * S + LAY, DRUM_LEN[SNARE], SNARE, 114)
    if first:
        P.add('cym', b, DRUM_LEN[CRASH], CRASH, 104)
        for q in (1, 2, 3):
            P.add('cym', b + q * TPB, DRUM_LEN[HAT], HAT, 74)
    else:
        hats(P, b)


def chorus_drums(P, bar, pattern, first):
    """Refrein: kick op elk akkoord van de riff, snare op 2 en 4, hihat in kwarten, crash alleen op maat 1."""
    b = bar * BAR
    for st, ln, kind, nm, *fx in pattern:
        if kind == 'P':
            P.add('kick', b + st * S, DRUM_LEN[KICK], KICK, 127 if st in (0, 8) else 116)
    if pattern is STOP:
        P.add('cym', b, DRUM_LEN[CRASH], CRASH, 112)
        return
    for q in (4, 12):
        P.add('snare', b + q * S + LAY, DRUM_LEN[SNARE], SNARE, 122)
    if first:
        P.add('cym', b, DRUM_LEN[CRASH], CRASH, 112)
        for q in (1, 2, 3):
            P.add('cym', b + q * TPB, DRUM_LEN[HAT], HAT, 80)
    else:
        hats(P, b, 80)


def feedback(P, start, length, note, top=100, mod_at=None):
    """De versterker huilt: lange wah-noot die aanzwelt (CC7) en pas laat gaat trillen."""
    P.add('fb', start, length, p(note), 110)
    steps = 24
    for j in range(steps + 1):
        P.fx['fb'].append((start + j * length * 3 // 4 // steps, 'vol', int(top * (0.15 + 0.85 * (j / steps) ** 1.5))))
    P.fx['fb'] += [(start, 'mod', 0), (start + (mod_at if mod_at is not None else length // 2), 'mod', 8)]


def chorus(P, bar0, pats, lead_phrases=None):
    for i, pat in enumerate(pats):
        b = bar0 + i
        riff(P, b, pat)
        chorus_drums(P, b, pat, i == 0)
        if lead_phrases:
            lead(P, b, lead_phrases[i])


def verse(P, bar0, mute_from, sides_from):
    for i, pat in enumerate(VERSE):
        b = bar0 + i
        riff(P, b, pat, guitars=False)                      # de bas speelt de gitaarriff, de gitaar zwijgt/dempt
        verse_drums(P, b, i == 0)
        if i >= mute_from:
            palm_mute(P, b, pat, ('L', 'R') if i >= sides_from else ('L',))


def build():
    P = Parts()
    G = ('pwrL', 'pwrR', 'ntL', 'ntR')

    # ---- intro: zwelling, de refreinriff als statement, de stop -------------------------------------------------
    P.add('pwrL', 0, 2 * BAR - S, p('C2'), 116)
    P.add('pwrR', 0, 2 * BAR - S, p('C2'), 110)
    for k in range(33):                                     # powerchord zwelt in 2 maten aan
        for sd in ('pwrL', 'pwrR'):
            P.fx[sd].append((k * 2 * BAR // 32, 'vol', int(8 + 92 * (k / 32) ** 1.6)))
    feedback(P, BAR // 2, BAR + BAR // 2 - S, 'G4', 80, BAR // 2)
    for k in range(8):                                      # lava-rommel: floor tom in 8en die aanzwelt
        P.add('tom', BAR + k * E, E, FTOM, 64 + k * 8)
    P.vol(G + ('bass',), INTRO_RIFF, 100)
    P.vol(('fb',), INTRO_RIFF, 100)
    chorus(P, INTRO_RIFF, [RIFF_B1, RIFF_B4, STOP])
    feedback(P, STOP0 * BAR + 2 * S, BAR - 3 * S, 'G4', 90, 4 * S)

    # ---- V1: alleen bas + drums; vanaf maat 9 zacht de palm-muted riff links ----------------------------------------
    P.vol(('bass',), V1, 100)
    P.vol(('muteL', 'muteR'), V1, 86)
    P.fx['drums'].append((V1 * BAR, 'vol', 92))
    verse(P, V1, 4, 99)

    # ---- R1 ----------------------------------------------------------------------------------------------------
    P.vol(G, R1, 100)
    P.vol(('bass',), R1, 96)
    P.fx['drums'].append((R1 * BAR, 'vol', 100))
    chorus(P, R1, CHORUS)

    # ---- V2: palm-mute links en rechts -----------------------------------------------------------------------------
    P.vol(('bass',), V2, 100)
    P.vol(('muteL', 'muteR'), V2, 92)
    P.fx['drums'].append((V2 * BAR, 'vol', 92))
    verse(P, V2, 0, 0)

    # ---- R2 ----------------------------------------------------------------------------------------------------
    P.vol(('bass',), R2, 96)
    P.fx['drums'].append((R2 * BAR, 'vol', 100))
    chorus(P, R2, CHORUS)

    # ---- B: hypnotische pedaalriff, drums bouwen op ----------------------------------------------------------------
    P.vol(G, B, 88)
    P.vol(('bass',), B, 100)
    P.fx['drums'].append((B * BAR, 'vol', 100))
    for i in range(8):
        b = B + i
        bb = b * BAR
        if i == 4:
            P.vol(G, b, 100)
        riff(P, b, RIFF_C, sides=('L',) if i < 2 else ('L', 'R'))
        if i < 2:                                           # alleen floor tom in 8en
            for e in range(8):
                P.add('tom', bb + e * E, E, FTOM, 92 + (8 if e % 2 == 0 else 0))
        elif i < 4:                                         # + kick op de tellen
            for e in range(8):
                P.add('tom', bb + e * E, E, FTOM, 96 + (8 if e % 2 == 0 else 0))
            for q in range(4):
                P.add('kick', bb + q * TPB, DRUM_LEN[KICK], KICK, 116)
        else:                                               # volle groove: kick 1/3 + 'en' van 2, snare 2/4, hihat
            for k in (0, 6, 8):
                P.add('kick', bb + k * S, DRUM_LEN[KICK], KICK, 124 if k == 0 else 112)
            for q in (4, 12):
                P.add('snare', bb + q * S + LAY, DRUM_LEN[SNARE], SNARE, 118)
            if i == 4:
                P.add('cym', bb, DRUM_LEN[CRASH], CRASH, 104)
                for q in (1, 2, 3):
                    P.add('cym', bb + q * TPB, DRUM_LEN[HAT], HAT, 76)
            else:
                hats(P, bb, 76)
    lb = (R3 - 1) * BAR                                     # de enige fill: snare in 8en over tel 3-4
    P.n['snare'] = [x for x in P.n['snare'] if not (lb + 8 * S <= x[0] < lb + BAR)]
    P.n['kick'] = [x for x in P.n['kick'] if not (lb + 8 * S <= x[0] < lb + BAR)]
    P.n['cym'] = [x for x in P.n['cym'] if not (lb + 8 * S <= x[0] < lb + BAR)]
    for k in range(4):
        P.add('snare', lb + (8 + 2 * k) * S, DRUM_LEN[SNARE], SNARE, 104 + k * 6)
    feedback(P, (B + 4) * BAR, 4 * BAR - S, 'G4', 92, BAR)

    # ---- R3: refrein + kreunende wah-lead; maat 52 = de stop ----------------------------------------------------
    P.vol(G, R3, 100)
    P.vol(('bass',), R3, 96)
    P.vol(('fb',), R3, 100)
    P.fx['drums'].append((R3 * BAR, 'vol', 100))
    chorus(P, R3, CHORUS_END, MOAN)
    feedback(P, (END - 1) * BAR + 2 * S, BAR - 3 * S, 'G4', 90, 4 * S)
    # de stop aan het eind van de loop = de stop van de intro (maat 4): naadloos terug naar de strofe

    for k in P.n:
        P.n[k] = dedupe(P.n[k])
    return P


def write_voicegroup():
    """grounded_gm + 28 palm-mute, 29 riffnoot, 30 powerchord, 31 wah-lead, 34 fuzzbas (allemaal keysplit_heatran:
    één sample per toonhoogte) en 127 = de eigen drumkit."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Heatran (Kyuss-desert rock). Gegenereerd door tools/grounded/heatran_theme.py.'
    lines[1] = ('@ 28 = palm-mute, 29 = riffnoot, 30 = powerchord, 31 = cocked-wah-lead, 34 = fuzzbas (keysplit_heatran, '
                'één sample per toonhoogte), 127 = drumkit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 28': '\tvoice_keysplit voicegroup_heatran_mute_keysplit, keysplit_heatran  @ 28',
        '@ 29': '\tvoice_keysplit voicegroup_heatran_note_keysplit, keysplit_heatran  @ 29',
        '@ 30': '\tvoice_keysplit voicegroup_heatran_power_keysplit, keysplit_heatran  @ 30',
        '@ 31': '\tvoice_keysplit voicegroup_heatran_lead_keysplit, keysplit_heatran  @ 31',
        '@ 34': '\tvoice_keysplit voicegroup_heatran_bass_keysplit, keysplit_heatran  @ 34',
        '@ 127': '\tvoice_keysplit_all voicegroup_heatran_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))

    # keysplits: index 0-5 = riffnoten C2 Eb2 F2 G2 Bb2 C3, 6-8 = lead C4 F4 Bb4 (zie keysplit_heatran)
    riff_keys, lead_keys = (36, 39, 41, 43, 46, 48), (60, 65, 70)
    kinds = {'power': ('pw', POWER, 'powerchord (grondtoon+kwint+octaaf)'), 'note': ('nt', NOTE, 'riffnoot (+octaaf)'),
             'mute': ('pm', MUTE, 'palm-mute'), 'bass': ('bs', BASS, 'fuzzbas (klinkt een octaaf lager)'),
             'lead': ('ld', LEAD, 'cocked-wah-lead/feedback')}
    for kind, (pre, prog, desc) in kinds.items():
        if kind == 'lead':
            keys = [lead_keys[0]] * 6 + list(lead_keys)
        else:
            keys = list(riff_keys) + [riff_keys[-1]] * 3
        body = ''.join('\tvoice_directsound %d, 0, DirectSoundWaveData_heatran_%s_%d, 255, 0, 255, %d\n'
                       % (k, pre, k, REL[prog]) for k in keys)
        open('sound/voicegroups/keysplits/heatran_%s.inc' % kind, 'w').write(
            '@ Project Grounded: Battle! Heatran, %s; één sample per toonhoogte (heatran_samples.py),\n'
            '@ tabel keysplit_heatran (sound/keysplit_tables.inc). Gegenereerd door tools/grounded/heatran_theme.py.\n'
            'voice_group heatran_%s_keysplit\n%s' % (desc, kind, body))
    kit = [   # vanaf noot 36; alles DirectSound
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_heatran_ky_kick, 255, 0, 255, %d' % DRUM_REL[KICK],
        'voice_directsound_no_resample 60, 60, DirectSoundWaveData_heatran_ky_snare, 255, 0, 255, %d' % DRUM_REL[SNARE],
        'voice_directsound_no_resample 60, 76, DirectSoundWaveData_heatran_ky_hat, 255, 0, 255, %d' % DRUM_REL[HAT],
        'voice_directsound_no_resample 60, 44, DirectSoundWaveData_heatran_ky_crash, 255, 0, 255, %d' % DRUM_REL[CRASH],
        'voice_directsound 60, 52, DirectSoundWaveData_heatran_ky_floor_tom, 255, 0, 255, %d' % DRUM_REL[FTOM],
    ]
    open('sound/voicegroups/drumsets/heatran.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Heatran (heatran_theme.py), FluidR3 Power-kit (heatran_samples.py):\n'
        '@ 36 kick, 37 snare (dof), 38 hihat, 39 crash, 40 floor tom.\n'
        'voice_group heatran_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


def fx_events(fx, notes, base=0):
    """bend/mod terugzetten op het begin van de volgende noot (niet bij de note-off: dan zakt de uitklinktijd).
    base = vaste bend van het spoor (rechter gitaar); bends komen erbovenop."""
    starts = sorted(set(n[0] for n in notes))
    ev = [x for x in fx if x[1] == 'vol']
    pm = [x for x in fx if x[1] != 'vol']
    pm_ticks = {(t, k) for t, k, v in pm}
    for t, kind, v in pm:
        ev.append((t, kind, v + (base if kind == 'bend' else 0)))
        nxt = next((s for s in starts if s > t), None)
        if nxt is not None and (nxt, kind) not in pm_ticks:
            ev.append((nxt, kind, base if kind == 'bend' else 0))
    best = {}
    for t, kind, v in ev:
        if kind == 'vol' or (t, kind) not in best or (t, kind) in pm_ticks:
            if (t, kind) in pm_ticks and (t, kind) in best and kind != 'vol':
                if v == (base if kind == 'bend' else 0):
                    continue                                 # een reset wint niet van een eigen waarde
            best[(t, kind)] = v
    return [(t, k, v) for (t, k), v in best.items()]


def save(P, path):
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    cond.append(mido.MetaMessage('set_tempo', tempo=int(60e6 / BPM), time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=V1 * BAR))
    cond.append(mido.MetaMessage('marker', text=']', time=(END - V1) * BAR))
    out.tracks.append(cond)
    layout = [  # naam, programma, volume (100%), kanaal, pan, vaste bend
        ('pwrL', POWER, 100, 0, 30, 0),
        ('pwrR', POWER, 94, 1, 98, R_BEND),
        ('ntL', NOTE, 100, 2, 30, 0),
        ('ntR', NOTE, 94, 3, 98, R_BEND),
        ('muteL', MUTE, 84, 4, 36, 0),
        ('muteR', MUTE, 80, 5, 92, R_BEND),
        ('bass', BASS, 92, 7, 64, 0),
        ('lead', LEAD, 84, 8, 70, 0),
        ('fb', LEAD, 66, 10, 54, 0),
    ]
    for name, prog, vol, ch, pan, bend in layout:
        fx = fx_events(P.fx[name], P.n[name], bend)
        if bend:
            fx = [(0, 'bend', bend)] + [x for x in fx if not (x[0] == 0 and x[1] == 'bend')]
        add_track(out, P.n[name], prog, vol, ch, pan, fx)
    drums = ('kick', 'snare', 'cym', 'tom')
    add_track(out, sorted(sum((P.n[k] for k in drums), [])), DRUMS, 118, 9, 64, P.fx['drums'])
    written = {k for k, *_ in layout} | set(drums)
    assert not [k for k in P.n if P.n[k] and k not in written], 'partij niet weggeschreven'
    out.save(path)


def add_track(out, notes, prog, vol, ch, pan, fx):
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    t.append(mido.Message('control_change', channel=ch, control=20, value=2, time=0))   # BENDR 2 halve tonen
    ev = []
    for tk, kind, v in fx:     # volgorde op één tick: note-off, controllers, note-on
        if kind == 'vol':
            ev.append((tk, 1, mido.Message('control_change', channel=ch, control=7, value=max(0, min(127, v * vol // 100)))))
        elif kind == 'mod':
            ev.append((tk, 1, mido.Message('control_change', channel=ch, control=1, value=v)))
        elif kind == 'bend':
            ev.append((tk, 1, mido.Message('pitchwheel', channel=ch, pitch=max(-8192, min(8191, v)))))
    for s, e, n, v in notes:
        ev.append((e, 0, mido.Message('note_off', channel=ch, note=n, velocity=0)))
        ev.append((s, 2, mido.Message('note_on', channel=ch, note=n, velocity=max(1, min(127, int(v))))))
    last = 0
    for tk, _, m in sorted(ev, key=lambda x: (x[0], x[1])):
        t.append(m.copy(time=tk - last))
        last = tk
    out.tracks.append(t)


def one_string(P, sd):
    """Riffnoten en powerchords van één gitaar zijn één partij: elke noot stopt waar de volgende begint."""
    both = sorted([x + ['pwr'] for x in P.n['pwr' + sd]] + [x + ['nt'] for x in P.n['nt' + sd]])
    for i, x in enumerate(both[:-1]):
        nxt = both[i + 1][0]
        if nxt > x[0]:
            x[1] = min(x[1], nxt)
    P.n['pwr' + sd] = [x[:4] for x in both if x[4] == 'pwr']
    P.n['nt' + sd] = [x[:4] for x in both if x[4] == 'nt']


def main():
    P = build()
    write_voicegroup()
    rel = releases(VG)
    progs = {'pwrL': POWER, 'pwrR': POWER, 'ntL': NOTE, 'ntR': NOTE, 'muteL': MUTE, 'muteR': MUTE, 'bass': BASS,
             'lead': LEAD, 'fb': LEAD}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    tail['kick'] = tail['snare'] = tail['tom'] = 0
    tail['cym'] = 0                                          # crash: de noot zelf duurt 2 tellen (zoals de lint telt)
    for sd in ('L', 'R'):
        one_string(P, sd)
    for k in progs:
        P.n[k] = detach(P.n[k], tail[k])
    for sd in ('L', 'R'):                                    # ook tussen powerchord en riffnoot: release eerder los
        both = sorted(P.n['pwr' + sd] + P.n['nt' + sd])
        starts = sorted(set(x[0] for x in both))
        for x in both:
            nxt = next((t for t in starts if t > x[0]), None)
            if nxt is not None:
                x[1] = min(x[1], max(x[0] + 6, nxt - tail['pwr' + sd]))
    # zelfde toonhoogte mag in één spoor niet overlappen (de note-off van de eerste zou de tweede afkappen)
    for k in P.n:
        ns = sorted(P.n[k])
        for i, x in enumerate(ns):
            nxt = next((y[0] for y in ns[i + 1:] if y[2] == x[2] and y[0] >= x[0]), None)
            if nxt is not None and nxt < x[1]:
                x[1] = max(x[0] + 6, nxt - 1)
        P.n[k] = ns
    order = ['bass', 'pwrL', 'ntL', 'kick', 'snare', 'lead', 'pwrR', 'ntR', 'muteL', 'cym', 'fb', 'tom', 'muteR']
    kept = allocate({k: P.n[k] for k in order}, order, tail, max_voices=11)
    print('tail (ticks):', tail)
    for k in order:
        n = len(P.n[k])
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        P.n[k] = kept[k]
    save(P, OUT)
    spb = 4 * 60 / BPM
    print(OUT, '%.1f s intro, %.1f s loop' % (V1 * spb, (END - V1) * spb))
    for nm, a, b in (('intro', 0, V1), ('V1', V1, R1), ('R1', R1, V2), ('V2', V2, R2), ('R2', R2, B), ('B', B, R3),
                     ('R3', R3, END)):
        print('  %-5s maat %2d-%2d  %6.1f - %6.1f s' % (nm, a, b - 1, a * spb, b * spb))


if __name__ == '__main__':
    main()
