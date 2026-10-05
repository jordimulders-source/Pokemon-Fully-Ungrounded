#!/usr/bin/env python3
"""Project Grounded: Battle! Genesect v1, een eigen compositie: industrial / big beat à la The Prodigy (Firestarter,
Breathe, Voodoo People, Smack My Bitch Up) met hard-techno-delen.

Jordi: 'Genesect mag idd industrial/big beat, beetje Prodigy achtig, met wat hard techno inspiratie.'
Genesect = 300 miljoen jaar oude insect-cyborg met een kanon: mechanisch, koud, agressief.

144 bpm (Firestarter 141, hard techno 145-150), E-frygisch (E F G A Bb-kleur: de b2 en de tritonus = metaal).
1 tel = 24,9 frames, 1 maat = 1,67 s.
Het motief: de baslijn-riff (distorted bas) E . . E G . E . Bb . A . E E D . | E . . E G . E . F . F G E - - -, die in elk
deel terugkomt (intro solo, big beat, kanon-stinger), en de hook erboven (gescheurde 'hoover'-lead):
E E G F E D | E - B D E G | A G F G F E | F E D E---  (b2 -> 1: frygisch).

Intro (4 maten, 6,7 s), op de transitie (scanlijnen, vizier, LOCKED ON, Techno Blast, wit; de muziek start ±25 frames
vóór het beeld):
  0     scan: metalen tikken in 16den die aanzwellen, PSG-datapiepjes, ruisriser, reverse crash naar maat 1
  1     wit = KANON (Techno Blast) + crash + stoot, dan de riff solo (donkere bas + sub), aambeeld op 2 en 4
  2     riff (B) + machinepers; hier klinkt de cry (±2,3-3 s na het gevecht): geen drop
  3     riff + four-on-the-floor + snareroffel + reverse crash (= maat 39: naadloze loop)
Loop (maat 4-39, 36 maten, 60 s):
  4-11  BIG BEAT: breakbeat met harde snare, riff, noisestoten op de 'en' van 4; hook vanaf 8
  12-19 hook x2 met een acid-tegenlijn (303), orchestra hits, crashes; 19 = fill
  20-23 INDUSTRIAL BREAK: geen kick/bas; aambeeld, pers, buis, clap, acid solo (filter gaat open), sub-drone, piepjes
  24-25 build-up: kick 4en -> 8sten, roffel, PSG-sirene, riser, bas die een octaaf opstijgt, de laatste 8ste stil
  26-33 HARD TECHNO: four-on-the-floor + rumble (k-r-r), clap, open hats op de 'en', acid in 16den, stoten; hook vanaf 30
  34    KANON: Techno Blast, dan de tweede helft van de riff solo + roffel
  35-38 big beat + hook (climax), 38 = fill
  39    = maat 3, terug naar 4
Max. 11 DirectSound-noten (legendary): lead > kick > snare > bas > acid > crash > fx > stoot > hit > hats > metaal > ...
PSG (kost niets): sub (golf), hook-verdubbeling/sirene (vierkant 1), datapiepjes (vierkant 2), riser/shaker (ruis).
Voicegroup grounded_genesect = grounded_gm + eigen samples (genesect_samples.py) + eigen drumkit (drumsets/genesect.inc).
v3 (Jordi over v2/Prodigy: 'saai, terug naar de eerste versie, de cyber-funk/slap-bass-track; de swingende groove en
de catchy synth-riffs houden, alleen de arrangement-overgangen en percussie net wat strakker'): v1 noot voor noot als
basis (riff, hook, acid, bas, hats met hun accenten 118/70/96/74 = de swing), en alleen:
  - ghosts opgeruimd: nooit twee ghosts naast elkaar, max. 2 per maat buiten roffels (big beat 'a': g op 6 en 14,
    de g op 15 weg; industrial break: alleen de g op 14);
  - fills strak: snare in 8sten -> 16den op de laatste tel (geen ghosts ertussen); roffels in 16den, geen 32sten;
  - stops: de laatste 16de vóór elke nieuwe sectie is stil (alleen de fill-snare/het bekken loopt door), vóór de
    hard-techno-drop de laatste 8ste;
  - een crash op elk sectiebegin (ook de build-up, maat 24).
groove_checks() controleert dit (en dat de swing er nog in zit: hat-accentspreiding, kick/bas op oneven 16den).
Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/genesect_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_genesect.mid'
VG = 'grounded_genesect'
TPB, BPM = 96, 144
S = TPB // 4                 # zestiende
E = TPB // 2                 # achtste
BAR = TPB * 4
MAX_VOICES = 11              # legendary

# programma's (voicegroup grounded_genesect)
BASS, BASS_DARK, LEAD, ACID, ACID_ACC, STAB, OHIT = 32, 33, 34, 35, 36, 37, 38
SIREN, BLIP, LEADSQ, SUB, RISER, SHAKER, DRUMS = 80, 81, 82, 84, 120, 121, 127
REL = {BASS: 140, BASS_DARK: 150, LEAD: 165, ACID: 120, ACID_ACC: 120, STAB: 170, OHIT: 180}
# drumkit (drumsets/genesect.inc, vanaf 36): naam, sample, release, lengte (ticks)
KIT = [
    ('KICK', 'genesect_kick', 175, E),
    ('RUMBLE', 'genesect_rumble', 140, 16),
    ('SNARE', 'genesect_snare', 185, E + S),
    ('GHOST', 'genesect_ghost', 140, 20),
    ('CLAP', 'sc88pro_tr909_hand_clap', 180, E),
    ('HAT', 'genesect_hat', 110, 14),
    ('OHAT', 'genesect_ohat', 150, E),
    ('ANVIL', 'genesect_anvil', 190, TPB),
    ('PIPE', 'genesect_pipe', 200, TPB * 2),
    ('PRESS', 'genesect_press', 170, E + S),
    ('CRASH', 'trinity_cymbal_crash', None, TPB + E),
    ('REVCYM', 'genesect_revcym', 120, 0),
    ('CANNON', 'genesect_cannon', 200, TPB * 3),
    ('ROLL', 'genesect_ghost', 110, 12),
]
for i, (nm, *_) in enumerate(KIT):
    globals()[nm] = 36 + i
KITLEN = {36 + i: k[3] for i, k in enumerate(KIT)}
REVLEN = int(1.4 * BPM / 60 * TPB)          # reverse crash: 1,4 s -> eindigt precies op de volgende maat

INTRO = 4
LOOP_START, LOOP_END = INTRO * BAR, 40 * BAR
NOTE = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def n(name):
    return NOTE[name[:-1]] + 12 * (int(name[-1]) + 1)


def t(bar, pos=0):
    return bar * BAR + int(pos * S)


# ---------------- het motief ----------------
RIFF_A = [(0, 2, 'E2'), (3, 1, 'E2'), (4, 2, 'G2'), (6, 1, 'E2'), (8, 2, 'Bb2'), (10, 2, 'A2'), (12, 1, 'E2'),
          (13, 1, 'E2'), (14, 2, 'D3')]
RIFF_B = [(0, 2, 'E2'), (3, 1, 'E2'), (4, 2, 'G2'), (6, 1, 'E2'), (8, 2, 'F2'), (10, 1, 'F2'), (11, 1, 'G2'),
          (12, 4, 'E2')]
HOOK = [
    [(0, 3, 'E4'), (3, 3, 'E4'), (6, 2, 'G4'), (8, 3, 'F4'), (11, 3, 'E4'), (14, 2, 'D4')],
    [(0, 6, 'E4'), (6, 2, 'B3'), (8, 2, 'D4'), (10, 2, 'E4'), (12, 4, 'G4')],
    [(0, 3, 'A4'), (3, 3, 'G4'), (6, 2, 'F4'), (8, 3, 'G4'), (11, 3, 'F4'), (14, 2, 'E4')],
    [(0, 4, 'F4'), (4, 2, 'E4'), (6, 2, 'D4'), (8, 8, 'E4')],
]
HOOK4B = [(0, 4, 'F4'), (4, 2, 'G4'), (6, 2, 'A4'), (8, 4, 'B4'), (12, 4, 'Bb4')]     # spanning terug naar het begin
HOOK_ROOTS = [0, 0, -4, -2]                  # E E C D: de riff schuift mee onder de hook
# acid (303): intervallen t.o.v. E3 per 16de en accenten
ACID_PAT = [0, 0, 12, 0, 3, 0, 6, 0, 5, 0, 12, 10, 0, 3, 1, 0]
ACID_ACC_POS = {0, 6, 10, 11, 14}
# datapiepjes (PSG): vaste 'willekeurige' reeks hoge noten
BLIPS = [84, 91, 79, 88, 96, 83, 90, 86, 81, 95, 87, 92, 80, 89, 94, 85]


def build():
    P = {k: [] for k in ('kick', 'rumble', 'snare', 'ghost', 'clap', 'hat', 'metal', 'crash', 'fx', 'bass', 'lead',
                         'acid', 'stab', 'ohit', 'sq1', 'sq2', 'sub', 'noise')}
    bass_prog, acid_prog = [], []
    noise_prog, sq1_prog = [(0, RISER)], [(0, LEADSQ)]
    extra = {'bass': [], 'sq1': []}

    def drum(part, nt, b, p, v=127):
        st = t(b) + int(p * S)
        P[part].append([st, st + KITLEN[nt], nt, v])

    # ---------------- drums ----------------
    def bigbeat(b, kind):
        K = lambda p, v=127: drum('kick', KICK, b, p, v)
        SN = lambda p, v=124: drum('snare', SNARE, b, p, v)
        G = lambda p, v: drum('ghost', GHOST, b, p, v)
        if kind == 'a':          # K . . . S . g K . . K . S . g g
            K(0); SN(4); G(6, 64); K(7, 108); K(10); SN(12); G(14, 72)           # v3: g op 15 weg
        elif kind == 'b':        # K . K . S . . . . g K K S . . g
            K(0); K(2, 112); SN(4); G(9, 62); K(10); K(11, 104); SN(12); G(15, 74)
        elif kind == 'fill':     # tweede helft: snareroffel in 16den
            K(0); SN(4); K(7, 110); SN(8, 104); SN(10, 110)                     # v3: strak, geen ghosts
            SN(12, 114); SN(13, 118); SN(14, 122); SN(15, 126)

    def hats(b, dens=16, vel=1.0, open_pos=()):
        acc = [118, 70, 96, 74]
        for p in range(16):
            if dens == 8 and p % 2:
                continue
            if p in open_pos:
                drum('hat', OHAT, b, p, int(104 * vel))
                continue
            drum('hat', HAT, b, p, int(acc[p % 4] * vel))

    def techno(b, fill=False):
        for q in (0, 4, 8, 12):
            drum('kick', KICK, b, q, 127)
            if not (fill and q == 12):
                drum('rumble', RUMBLE, b, q + 1, 112)
                drum('rumble', RUMBLE, b, q + 2, 92)
                drum('rumble', RUMBLE, b, q + 3, 70)
        drum('clap', CLAP, b, 4, 120); drum('clap', CLAP, b, 12, 120)
        for p in range(16):
            if p % 4 == 2:
                drum('hat', OHAT, b, p, 100)
            elif p % 2:
                drum('hat', HAT, b, p, 76)
        if fill:
            for p, v in ((13, 90), (14, 104), (15, 120)):
                drum('snare', SNARE, b, p, v)

    def crash(b, v=112, p=0):
        drum('crash', CRASH, b, p, v)

    def revcym(b, v=104):
        """reverse crash die op maat b eindigt."""
        P['fx'].append([t(b) - REVLEN, t(b) - 2, REVCYM, v])

    def roll(b, start=8, v0=80):
        """roffel tot het einde van de maat: 8sten -> 16den -> 32sten (de laatste tel)."""
        pts = [(p, v0 + 3 * i) for i, p in enumerate(range(start, 12, 2))]
        pts += [(12 + q, v0 + 16 + 8 * q) for q in range(4)]             # v3: 16den i.p.v. 32sten (strakker)
        for p, v in pts:
            st = t(b) + int(p * S)
            P['ghost'].append([st, st + KITLEN[ROLL], ROLL, min(127, v)])

    # ---------------- bas en sub ----------------
    def sub_note(st, en, nt, v=112):
        while nt > n('Eb2'):
            nt -= 12
        while nt < n('E1'):
            nt += 12
        P['sub'].append([st, en, nt, v])

    def riff(b, pat, shift=0, prog=BASS, vel=118, sub=True, frm=0):
        for p, ln, nm in pat:
            if p < frm:
                continue
            nt = n(nm) + shift
            st, en = t(b, p), t(b, p + ln)
            P['bass'].append([st, en, nt, vel if ln > 1 else vel - 8])
            bass_prog.append((st, prog))
            if sub:
                sub_note(st, en, nt, 108)

    # ---------------- melodisch ----------------
    def hook(b, mel, vel=124, oct=0, sq=True):
        for p, ln, nm in mel:
            nt = n(nm) + oct
            P['lead'].append([t(b, p), t(b, p + ln), nt, vel])
            if sq:
                P['sq1'].append([t(b, p), t(b, p + ln), nt + 12, 96])

    def acid(b, shift=0, vel=104, acc_extra=(), only=None):
        for p, iv in enumerate(ACID_PAT):
            if only is not None and p not in only:
                continue
            accent = p in ACID_ACC_POS or p in acc_extra
            nt = n('E3') + iv + shift
            st = t(b, p)
            P['acid'].append([st, st + S - 4, nt, vel + (18 if accent else 0)])
            acid_prog.append((st, ACID_ACC if accent else ACID))

    def stabs(b, pos, shift=0, vel=110):
        for p in pos:
            P['stab'].append([t(b, p), t(b, p) + S + 4, n('E3') + shift, vel])

    def ohit(b, p=0, shift=0, vel=118):
        P['ohit'].append([t(b, p), t(b, p) + E + S, n('E4') + shift, vel])

    def metal(b, nt, p, v=112):
        drum('metal', nt, b, p, v)

    def blips(b, vel=60, start=0, every=1):
        for i, p in enumerate(range(start, 16, every)):
            P['sq2'].append([t(b, p), t(b, p) + 8, BLIPS[(b * 5 + i) % 16], vel])

    # ---------------- secties ----------------
    def lockon_bar(b):
        """maat 3 / 39: riff + four-on-the-floor + snareroffel + reverse crash naar de drop."""
        riff(b, RIFF_A, prog=BASS)
        for q in (0, 4, 8, 12):
            drum('kick', KICK, b, q, 120)
        drum('snare', SNARE, b, 4, 116)
        hats(b, 16, 0.85)
        roll(b, 8, 78)
        revcym(b + 1, 100)

    def bigbeat_bar(b, k, riff_pat, shift=0, mel=None, kind=None, stab_pos=(14,)):
        kind = kind or ('b' if k % 2 else 'a')
        bigbeat(b, kind)
        hats(b, 16, 1.0, open_pos=(14,) if k % 2 and kind != 'fill' else ())
        riff(b, riff_pat, shift)
        if mel is not None:
            hook(b, mel)
        if kind != 'fill':
            stabs(b, stab_pos, shift)
        if kind == 'fill':
            metal(b, ANVIL, 0, 100)

    # ================= INTRO =================
    # maat 0: scan
    metal(0, PIPE, 0, 96)
    for p in range(16):
        drum('hat', HAT, 0, p, 36 + 4 * p)
    blips(0, 54)
    P['noise'] += [[t(0) + i * E, t(0) + i * E + E, 46 + i, 28 + 6 * i] for i in range(7)]
    revcym(1, 96)
    # maat 1: KANON op het witte scherm, riff solo
    drum('fx', CANNON, 1, 0, 124)
    crash(1, 116)
    drum('kick', KICK, 1, 0, 127)
    ohit(1, 0)
    riff(1, RIFF_A, prog=BASS_DARK, vel=112)
    metal(1, ANVIL, 4, 100); metal(1, ANVIL, 12, 104)
    noise_prog.append((t(1), SHAKER))
    # maat 2: riff B + pers (de cry)
    riff(2, RIFF_B, prog=BASS_DARK, vel=114)
    metal(2, PRESS, 4, 104); metal(2, PRESS, 12, 108); metal(2, ANVIL, 14, 90)
    drum('kick', KICK, 2, 0, 116); drum('kick', KICK, 2, 8, 112)
    hats(2, 8, 0.7)
    # maat 3: lock-on
    lockon_bar(3)

    # ================= LOOP =================
    # BIG BEAT (4-11): riff spotlight, hook vanaf 8
    crash(4, 118)
    ohit(4, 0)
    for k in range(8):
        b = 4 + k
        if k < 4:
            bigbeat_bar(b, k, RIFF_A if k % 2 == 0 else RIFF_B, stab_pos=(14,) if k % 2 else (6, 14))
        else:
            j = k - 4
            bigbeat_bar(b, k, RIFF_A if j % 2 == 0 else RIFF_B, HOOK_ROOTS[j], HOOK[j],
                        kind='fill' if k == 7 else None)
    crash(8, 108)
    # HOOK x2 + ACID (12-19)
    for k in range(8):
        b = 12 + k
        j = k % 4
        mel = HOOK4B if k == 7 else HOOK[j]
        bigbeat_bar(b, k, RIFF_A if j % 2 == 0 else RIFF_B, HOOK_ROOTS[j], mel,
                    kind='fill' if k == 7 else None, stab_pos=(3, 14) if k % 2 else (14,))
        acid(b, HOOK_ROOTS[j], 84)
        if j == 0:
            crash(b, 114)
            ohit(b, 0, HOOK_ROOTS[j])
    # INDUSTRIAL BREAK (20-23)
    crash(20, 104)
    metal(20, PIPE, 0, 116)
    for i in range(4):
        b = 20 + i
        metal(b, ANVIL, 0, 118); metal(b, ANVIL, 6, 96); metal(b, ANVIL, 11, 104)
        metal(b, PRESS, 4, 112); metal(b, PRESS, 12, 116)
        if i % 2:
            metal(b, PIPE, 8, 100)
        drum('clap', CLAP, b, 12, 96)
        drum('ghost', GHOST, b, 14, 76)                                    # v3: één ghost (was 14 + 15)
        hats(b, 8, 0.6)
        acid(b, 0, 88 + 4 * i, acc_extra=set(range(0, 16, 4 - i)) if i else ())
        P['noise'] += [[t(b, p), t(b, p) + 8, 90 if p % 2 else 94, 46 if p % 2 else 64] for p in range(16)]
        sub_note(t(b), t(b + 1) - 6, n('E1'), 100)
        blips(b, 48, start=1, every=4)
    noise_prog.append((t(20), SHAKER))
    # BUILD-UP (24-25)
    drum('kick', KICK, 24, 0, 124)
    for p in (4, 8, 12):
        drum('kick', KICK, 24, p, 112)
    for p in (0, 2, 4, 6, 8, 10):
        drum('kick', KICK, 25, p, 116)
    rl = [(p, 64 + 2 * p) for p in range(0, 16, 2)] + [(16 + p, 84 + 2 * p) for p in range(8)]
    rl += [(24 + q, 102 + 4 * q) for q in range(6)]                      # v3: 16den tot tel 4, dan stil (was 32sten)
    crash(24, 104)                                                       # v3: crash op het sectiebegin
    for p, v in rl:
        st = t(24) + int(p * S)
        P['ghost'].append([st, st + KITLEN[ROLL], ROLL, min(127, v)])
    for p in range(28):
        drum('hat', HAT, 24, p, 44 + 2 * p)
    noise_prog.extend([(t(24), RISER), (t(26), SHAKER)])
    P['noise'] += [[t(24) + i * E, t(24) + i * E + E, 46 + i, 28 + 6 * i] for i in range(14)]
    sq1_prog.extend([(t(24), SIREN), (t(26), LEADSQ)])
    P['sq1'].append([t(24), t(25, 14), n('E4'), 100])
    extra['sq1'] += [(t(24) + i * 24, mido.Message('pitchwheel', pitch=min(8191, int(8192 * (i / 30) ** 1.4))))
                     for i in range(1, 31)]
    extra['sq1'].append((t(25, 14), 'reset'))
    P['bass'].append([t(24), t(25) - 8, n('E2'), 108]); bass_prog.append((t(24), BASS_DARK))
    P['bass'].append([t(25), t(25, 14), n('E2'), 112]); bass_prog.append((t(25), BASS))
    extra['bass'] += [(t(25) + (t(25, 14) - t(25)) * i // 16,
                       mido.Message('pitchwheel', pitch=min(8191, int(8192 * (i / 16) ** 1.5)))) for i in range(1, 17)]
    extra['bass'].append((t(25, 14), 'reset'))
    sub_note(t(24), t(25, 12), n('E1'), 104)
    acid(24, 0, 84, only=range(0, 16, 2))
    acid(25, 0, 92)
    revcym(26, 108)
    # HARD TECHNO (26-33)
    for k in range(8):
        b = 26 + k
        j = k % 4
        techno(b, fill=k == 7)
        acid(b, HOOK_ROOTS[j] if k >= 4 else 0, 96)
        sub_note(t(b), t(b, 4) - 6, n('E1') + (HOOK_ROOTS[j] if k >= 4 else 0), 104)
        if k % 2 == 1:
            stabs(b, (3, 6, 11), HOOK_ROOTS[j] if k >= 4 else 0, 104)
        if k >= 4:
            hook(b, HOOK[j] if k < 7 else HOOK4B, 120)
        if k in (0, 4):
            crash(b, 116)
    ohit(26, 0)
    ohit(30, 0)
    revcym(34, 104)
    # KANON (34)
    drum('fx', CANNON, 34, 0, 127)
    crash(34, 118)
    drum('kick', KICK, 34, 0, 127)
    ohit(34, 0)
    stabs(34, (0,), 0, 118)
    riff(34, RIFF_A, frm=8)
    blips(34, 56, start=2, every=2)
    roll(34, 10, 84)
    # RETURN (35-38): big beat + hook
    crash(35, 120)
    ohit(35, 0)
    for k in range(4):
        b = 35 + k
        bigbeat_bar(b, k, RIFF_A if k % 2 == 0 else RIFF_B, HOOK_ROOTS[k], HOOK[k] if k < 3 else HOOK4B,
                    kind='fill' if k == 3 else None, stab_pos=(3, 14))
        acid(b, HOOK_ROOTS[k], 80, only=range(0, 16, 2))
    crash(37, 112)
    ohit(37, 0, HOOK_ROOTS[2])
    # 39 = 3
    lockon_bar(39)

    # v3: stops. De laatste 16de (vóór de hard-techno-drop de laatste 8ste) vóór een nieuwe sectie is stil: alles
    # wat dan zou klinken wordt afgekapt, alleen de fill (snare/roffel) en de reverse crash lopen door.
    def stop(b, frm, keep=('snare', 'ghost', 'fx', 'crash')):
        st, en = t(b, frm), t(b + 1)
        for k in P:
            if k in keep:
                continue
            P[k] = [[a, min(e, st) if a < st else e, nt, v] for a, e, nt, v in P[k] if not st <= a < en]
            P[k] = [x for x in P[k] if x[1] > x[0]]
    for b in (3, 7, 11, 19, 33, 38, 39):
        stop(b, 15)
    stop(25, 14)
    return P, dict(bass=bass_prog, acid=acid_prog, noise=noise_prog, sq1=sq1_prog), extra


SECTIONS = (4, 8, 12, 16, 20, 24, 26, 30, 34, 35)


def groove_checks(P):
    """v3 (omgekeerde funk_meter van v2): de swing moet blijven, de percussie strak."""
    ghosts = {}
    roll_bars = {3, 24, 25, 34, 39}
    for a, e, nt, v in P['ghost']:
        if nt == GHOST:
            ghosts.setdefault(a // BAR, []).append(a % BAR // S)
    bad = []
    for b, ps in ghosts.items():
        ps = sorted(ps)
        if b in roll_bars:
            continue
        if len(ps) > 2 or any(q - p == 1 for p, q in zip(ps, ps[1:])):
            bad.append((b, ps))
    assert not bad, 'ghost-ophopingen: %s' % bad
    for b in SECTIONS:
        assert any(a == t(b) for a, *_ in P['crash']) or any(a == t(b) and nt == CANNON for a, e, nt, v in P['fx']), \
            'geen crash op maat %d' % b
    for b in (3, 7, 11, 19, 33, 38, 39):
        st = t(b, 15)
        for k in ('bass', 'lead', 'acid', 'stab', 'hat', 'rumble', 'kick'):
            assert not [x for x in P[k] if x[0] < t(b + 1) and x[1] > st], 'stop maat %d niet stil: %s' % (b, k)
    loop = lambda lst: [x for x in lst if LOOP_START <= x[0] < LOOP_END]
    hats = [v for a, e, nt, v in loop(P['hat']) if nt == HAT]
    spread = (max(hats) - min(hats)) / 127.0
    odd_k = sum(1 for a, *_ in loop(P['kick']) if (a // S) % 2) / max(1, len(loop(P['kick'])))
    odd_b = sum(1 for a, *_ in loop(P['bass']) if (a // S) % 2) / max(1, len(loop(P['bass'])))
    gpb = sum(1 for a, e, nt, v in loop(P['ghost']) if nt == GHOST) / ((LOOP_END - LOOP_START) / BAR)
    print('  groove: hat-accentspreiding %.2f, kick op oneven 16den %.0f%%, bas op oneven 16den %.0f%%, '
          'ghosts %.2f per maat' % (spread, 100 * odd_k, 100 * odd_b, gpb))
    assert spread >= 0.3 and odd_k >= 0.1 and odd_b >= 0.15, 'de swing is weg'


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
    groove_checks(P)
    # golfkanaal: een golf van één periode klinkt een octaaf lager dan genoteerd (zie MUZIEK.md)
    P['sub'] = [[a, b, nt + 12, v] for a, b, nt, v in P['sub']]
    write_voicegroup()
    rel = {'bass': REL[BASS], 'lead': REL[LEAD], 'acid': REL[ACID], 'stab': REL[STAB], 'ohit': REL[OHIT]}
    tail = {k: release_ticks(r, TPB, BPM) for k, r in rel.items()}
    kitrel = {36 + i: k[2] for i, k in enumerate(KIT)}
    for k in ('kick', 'rumble', 'snare', 'ghost', 'clap', 'hat', 'metal', 'fx'):
        tail[k] = max(release_ticks(kitrel[nt], TPB, BPM) if kitrel[nt] else 0 for _, _, nt, _ in P[k]) if P[k] else 0
    tail['crash'] = 0
    for k in ('bass', 'lead'):
        P[k] = detach(P[k], tail[k])
    P['kick'] = [[a, b, nt, int(v * 0.88)] for a, b, nt, v in P['kick']]     # minder < 150 Hz (gemeten: 47-65%)
    order = ['lead', 'kick', 'snare', 'clap', 'bass', 'crash', 'fx', 'acid', 'stab', 'ohit', 'metal', 'hat', 'ghost',
             'rumble']
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
        lst = sorted(set(lst))
        out = [(tk, 'prog', p) for tk, p in lst if tk < LOOP_END]
        cur = [p for tk, p in lst if tk <= LOOP_START]
        if cur and not any(tk == LOOP_START for tk, _ in lst):
            out.append((LOOP_START, 'prog', cur[-1]))
        return out

    def bends(track):
        """pitchwheel; 'reset' pas bij de volgende noot (anders springt de uitklinkende staart). BENDR 12."""
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
        ('rumble', P['rumble'], DRUMS, 84, 11, 64, (), ()),
        ('hats', P['hat'], DRUMS, 120, 8, 76, (), ()),
        ('cym', P['crash'], DRUMS, 96, 10, 56, (), ()),
        ('metal', P['metal'], DRUMS, 116, 7, 48, (), ()),
        ('fx', P['fx'], DRUMS, 104, 12, 64, (), ()),
        ('bass', P['bass'], BASS, 92, 0, 64, progs(progs_['bass']), bends('bass')),
        ('lead', P['lead'], LEAD, 100, 1, 62, (), ()),
        ('acid', P['acid'], ACID, 80, 2, 72, progs(progs_['acid']), ()),
        ('stab', P['stab'], STAB, 84, 3, 56, (), ()),
        ('ohit', P['ohit'], OHIT, 88, 4, 64, (), ()),
        ('sq1', P['sq1'], LEADSQ, 44, 5, 52, progs(progs_['sq1']), bends('sq1')),
        ('sq2', P['sq2'], BLIP, 40, 6, 88, (), ()),
        ('sub', P['sub'], SUB, 38, 13, 64, (), ()),
        ('noise', P['noise'], RISER, 64, 14, 70, progs(progs_['noise']), ()),
    ]
    for name, notes, prog, vol, ch, pan, ccs, extr in layout:
        song.add(notes, prog, vol, ch, pan, extra=extr, ccs=ccs)
    written = {'kick', 'snare', 'ghost', 'clap', 'hat', 'crash'} | {nm for nm, *_ in layout}
    assert not [k for k in P if P[k] and k not in written], 'partij niet weggeschreven'
    assert len(layout) <= 16
    song.save(OUT, LOOP_END)
    sec = lambda tk: tk / TPB * 60 / BPM
    print(OUT, '%d sporen, intro %.1f s, loop %.1f s, totaal %.1f s' % (len(layout), sec(LOOP_START),
                                                                      sec(LOOP_END - LOOP_START), sec(LOOP_END)))
    for nm, b in (('scan', 0), ('kanon', 1), ('lock-on', 3), ('big beat', 4), ('hook+acid', 12), ('industrial', 20),
                  ('build-up', 24), ('hard techno', 26), ('kanon', 34), ('return', 35), ('lock-on', 39)):
        print('  %-11s maat %2d  %5.1f s' % (nm, b, sec(t(b))))


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + industrial/big-beat-samples (genesect_samples.py) en een eigen drumkit voor Battle! Genesect.'
    lines[1] = '@ Gegenereerd door tools/grounded/genesect_theme.py.'
    lines[2] = 'voice_group %s' % VG
    ds = lambda smp, rel, key=60, att=255, dec=0, sus=255: \
        '\tvoice_directsound %d, 0, DirectSoundWaveData_%s, %d, %d, %d, %d' % (key, smp, att, dec, sus, rel)
    rep = {
        BASS: ds('genesect_bass', REL[BASS]), BASS_DARK: ds('genesect_bass_dark', REL[BASS_DARK]),
        LEAD: ds('genesect_lead', REL[LEAD]),
        ACID: ds('genesect_acid', REL[ACID]), ACID_ACC: ds('genesect_acid_acc', REL[ACID_ACC]),
        STAB: ds('genesect_stab', REL[STAB]), OHIT: ds('genesect_ohit', REL[OHIT]),
        SIREN: '\tvoice_square_1 60, 0, 0, 2, 0, 0, 15, 2',
        BLIP: '\tvoice_square_2 60, 0, 3, 0, 1, 0, 1',
        LEADSQ: '\tvoice_square_1 60, 0, 0, 2, 0, 2, 10, 1',
        SUB: '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_8, 0, 7, 15, 1',
        RISER: '\tvoice_noise_alt 60, 0, 0, 3, 0, 15, 2',
        SHAKER: '\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0',
        DRUMS: '\tvoice_keysplit_all voicegroup_genesect_drumset',
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
    open('sound/voicegroups/drumsets/genesect.inc', 'w').write(
        '@ Project Grounded: industrial/big-beat-kit voor Battle! Genesect (genesect_theme.py), alles DirectSound:\n'
        '@ ' + ', '.join('%d %s' % (36 + i, k[0].lower()) for i, k in enumerate(KIT)) + '.\n'
        'voice_group genesect_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    main()
