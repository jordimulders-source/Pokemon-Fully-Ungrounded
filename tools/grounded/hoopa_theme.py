#!/usr/bin/env python3
"""Project Grounded: "Battle! Hoopa" (song 662, MUS_GROUNDED_VS_HOOPA), eigen compositie, v1.

Concept (goedgekeurd door Jordi): Arabisch-mystiek, de djinn uit de ring. Hijaz-toonladder op D (D Eb F# G A Bb C:
frygisch-dominant, de overmatige secunde Eb-F#), darbuka + lijsttrom + vingerbekkens, oud als getokkelde lead, een
slangenbezweerder-riet (mizmar/zurna, middenregister, níet schel), strijkers in unisono-loopjes. Het nummer kantelt van
speels-ondeugend (Hoopa Confined: de trickster; pizzicato, lichte percussie, oud) naar massief en dreigend (Hoopa
Unbound: laag koper, pauken, koor, zware 3-3-2-slagen). Het Unbound-thema = het Confined-thema in dubbele notenwaarden
op het koper (zelfde motief, andere gedaante).

160 bpm, maat = 1,5 s. Vorm:
  intro i1-i4 (6,0 s)  i1 vingerbekken + lijsttrom, oud-flourish omhoog door de hijaz, portaal-'zoef' (PSG-ruis);
                       i2 STIL (cry ±2,3-3 s): alleen een zachte strijkersdrone D-A en één bekkentje;
                       i3 darbuka begint (maqsum, zacht), pizzicato-ostinato, mizmar-roep; i4 darbuka-roffel,
                       strijkers-unisono-run omhoog, paukenroffel -> loop
  [loop]
  A   1-8    Confined: thema op de oud (D D Cm D | D Gm Eb D), pizzicato 8en (grondtoon-kwint-octaaf), darbuka
             maqsum met de tek als backbeat, vingerbekkens op 2 en 4
  A'  9-16   mizmar neemt het thema over, de oud speelt heterofoon een octaaf lager mee (versierd), bas + lijsttrom erbij,
             tamboerijn in 8en
  B  17-24   de ring groeit: Gm Gm Cm Cm Eb Eb D D; mizmar-roep <-> strijkers-antwoord in 16en, ayyub-galop op de
             darbuka, koor zwelt aan, maat 23 unisono-run (strijkers + oud) door twee octaven, maat 24 Eb-D-jammerklacht
             op de mizmar + paukenroffel + portaal-'zoef' -> stilte van een tel
  C  25-32   Unbound: thema x2 op hoorns (laag, D3-Bb3) + tuba (grondtonen), koor, pauken en taiko in 3-3-2, darbuka
             8en, bas 3-3-2, strijkers-ostinato laag (slangachtig D-Eb-D-C), PSG-golf als sub
  C' 33-40   tweede helft van het thema x2: trompet erbij (unisono met de hoorns een octaaf hoger), koor drie stemmen,
             crashes; maat 39-40 alles in 16en omhoog
  K  41-42   de djinn lacht: darbuka-solo + oud-giecheltje (snelle omspeling), terug naar Confined (A)
  ]
Instrumenten: eigen samples (tools/grounded/hoopa_samples.py, voorvoegsel hoopa_*, ±86 KB): 105 oud (keysplit
hoopa_oud), 111 mizmar (hoopa_mizmar), drumkit drumsets/hoopa.inc (dum, tek, ka, lijsttrom, vingerbekken + stock
crash/taiko/tamboerijn/orkestsnare); stock: 45 pizzicato, 48 strijkers (eigen keysplit hoopa_str met korte release),
33 fingered bass, 56 trompet, 58 tuba, 60 hoorn, 52 koor, 47 pauken, 84 PSG-golf (sub), 121 PSG-ruis (portaal).
Gebruik: python3 tools/grounded/hoopa_theme.py [--render <map>] [-v]"""
import math, os, subprocess, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_hoopa.mid'
VG = 'grounded_hoopa'
TPB = 96
S = TPB // 4                 # een 16e
BAR = TPB * 4
BPM = 160
MAX_V = 11                   # legendary-budget

OUD, MIZ, PIZZ, STR, BASS, TPT, TUBA, HORN, CHOIR, TIMP, WAVE, NOISE, DRUMS = \
    105, 111, 45, 48, 33, 56, 58, 60, 52, 47, 84, 121, 127
(DUM, TEK, KA, BENDIR, ZILL, CRASH, TAIKO, TAMB, SNARE_R, DUM_LO) = range(36, 46)

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


HIJAZ = (2, 3, 6, 7, 9, 10, 0)
CH = {'D': (2, (2, 6, 9)), 'Eb': (3, (3, 7, 10)), 'Cm': (0, (0, 3, 7)), 'Gm': (7, (7, 10, 2))}


def scale(lo, hi):
    return [m for m in range(lo, hi + 1) if m % 12 in HIJAZ]


def tones(ch, lo, hi):
    return [m for m in range(lo, hi + 1) if m % 12 in CH[ch][1]]


def near(pc, lo):
    return lo + ((pc - lo) % 12)


def pat(s):
    """'stap:lengte:noot ...' -> [(stap, lengte, noot)]"""
    out = []
    for w in s.split():
        a, b, c = w.split(':')
        out.append((int(a), int(b), p(c)))
    return out


# ---- materiaal ---------------------------------------------------------------------------------------------------
THEME = [pat(x) for x in (   # 8 maten, Confined (oud / mizmar)
    '0:1:A4 1:1:Bb4 2:2:A4 4:2:F#4 6:1:G4 7:1:F#4 8:2:Eb4 10:2:F#4 12:3:D4',
    '2:1:D5 3:1:C5 4:2:Bb4 6:2:A4 8:1:G4 9:1:A4 10:2:Bb4 12:4:A4',
    '0:1:D5 1:1:Eb5 2:2:D5 4:2:C5 6:1:Bb4 7:1:C5 8:2:G4 10:2:Bb4 12:4:G4',
    '0:2:F#4 2:2:G4 4:2:A4 6:2:Bb4 8:1:A4 9:1:Bb4 10:1:A4 11:1:G4 12:4:F#4',
    '0:1:A4 1:1:Bb4 2:2:A4 4:2:F#4 6:1:G4 7:1:F#4 8:2:Eb4 10:2:F#4 12:3:D4',
    '0:2:D5 2:1:Eb5 3:1:D5 4:2:C5 6:2:Bb4 8:2:G4 10:2:Bb4 12:2:D5 14:2:C5',
    '0:3:Bb4 3:1:G4 4:2:Eb4 6:2:F#4 8:2:G4 10:2:Bb4 12:1:A4 13:1:G4 14:2:F#4',
    '0:2:Eb4 2:8:D4 12:1:D4 13:1:Eb4 14:1:F#4 15:1:G4',
)]
PROG = {'A': ['D', 'D', 'Cm', 'D', 'D', 'Gm', 'Eb', 'D'],
        'B': ['Gm', 'Gm', 'Cm', 'Cm', 'Eb', 'Eb', 'D', 'D'],
        'C': ['D', 'D', 'D', 'D', 'Cm', 'Cm', 'D', 'D'],         # = thema maat 1-4 in dubbele waarden
        'C2': ['D', 'D', 'Gm', 'Gm', 'Eb', 'Eb', 'D', 'D'],      # = thema maat 5-8 in dubbele waarden
        'K': ['D', 'D'], 'I': ['D', 'D', 'D', 'D']}
CALL = [pat(x) for x in (    # B: mizmar-roep in de eerste helft van elke maat, de strijkers antwoorden
    '0:2:D5 2:1:Eb5 3:1:D5 4:4:Bb4',
    '0:2:G4 2:2:A4 4:4:Bb4',
    '0:2:C5 2:1:D5 3:1:C5 4:4:G4',
    '0:2:Eb4 2:2:F#4 4:4:G4',
    '0:2:Bb4 2:1:C5 3:1:Bb4 4:4:G4',
    '0:2:Eb5 2:2:D5 4:4:Bb4',
    '0:16:A4',
    '0:8:Eb5 8:4:D5',
)]
GIGGLE = pat('0:1:A4 1:1:Bb4 2:1:A4 3:1:G4 4:1:F#4 5:1:G4 6:1:F#4 7:1:Eb4 8:2:D4 12:1:D5 13:1:C5 14:1:Bb4 15:1:A4')
GIGGLE2 = pat('0:1:G4 1:1:F#4 2:1:Eb4 3:1:F#4 4:2:D4 8:1:A3 9:1:Bb3 10:1:C4 11:1:D4 12:1:D4 13:1:Eb4 14:1:F#4 15:1:G4')


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def timeline():
    tl = []
    for sec, n, var in (('I', 4, ''), ('A', 8, 'a1'), ('A', 8, 'a2'), ('B', 8, ''), ('C', 8, 'c1'), ('C2', 8, 'c2'),
                        ('K', 2, '')):
        for i in range(n):
            tl.append((len(tl), sec, i, var))
    return tl


TL = timeline()
INTRO = 4
END = len(TL)


def put(P, key, t0, ph, vel, shift=0, scale_t=1):
    for st, ln, n in ph:
        P[key].append([t0 + st * S * scale_t, t0 + (st + ln) * S * scale_t, n + shift, vel])


def gust(P, CC, EX, name, t0, length, key, vmax, rise=12):
    """portaal-'zoef' op PSG-ruis: één noot, CC7 zwelt aan, pitch bend stijgt (BENDR 12)."""
    P[name].append([t0, t0 + length, key, 110])
    steps = max(2, length // S)
    for k in range(steps + 1):
        x = k / steps
        CC[name].append((t0 + k * S, 7, int(6 + vmax * x ** 1.6)))
        EX[name].append((t0 + k * S, mido.Message('pitchwheel', pitch=max(-8192, min(8191, int((-6 + rise * x) / 12 * 8191))))))
    CC[name].append((t0 + length, 7, 0))
    EX[name].append((t0 + length, mido.Message('pitchwheel', pitch=0)))


def compose():
    P, CC, EX = Parts(), Parts(), Parts()
    FX = {'miz': {}}            # (start, noot) -> 'scoop' / 'vib' voor de mizmar
    for b, sec, i, var in TL:
        t0 = b * BAR
        ch = PROG[sec][i]
        r = CH[ch][0]
        # ------------------------------------------------------------------ intro
        if sec == 'I':
            if i == 0:
                P['perc'] += [[t0, t0 + 6 * S, ZILL, 92], [t0, t0 + 8 * S, BENDIR, 110]]
                run = scale(p('D3'), p('D5'))
                P['oud'] += [[t0 + (2 + k) * S // 1, t0 + (3 + k) * S, run[k], 84 + 3 * k] for k in range(13)]
                P['oud'].append([t0 + 15 * S, t0 + 16 * S, p('A4'), 112])
                gust(P, CC, EX, 'noise', t0, BAR - 2 * S, 64, 90)
                P['timp'].append([t0, t0 + 4 * S, p('D3'), 104])
            elif i == 1:   # stil: de cry
                P['str'] += [[t0, t0 + BAR - 12, n, 46] for n in (p('D3'), p('A3'))]
                P['perc'].append([t0 + 8 * S, t0 + 12 * S, ZILL, 58])
            elif i == 2:
                P['str'] += [[t0, t0 + BAR - 12, n, 56] for n in (p('D3'), p('A3'))]
                for k, (st, v) in enumerate(((0, 70), (2, 54), (4, 64), (6, 54), (8, 72), (10, 50), (12, 66), (14, 56))):
                    P['drk'].append([t0 + st * S, t0 + st * S + S, DUM if st in (0, 8) else (TEK if st in (4, 12) else KA), v])
                put(P, 'miz', t0, pat('0:6:A4 6:2:Bb4 8:4:A4 12:2:G4 14:2:F#4'), 100)
                FX['miz'][(t0, p('A4'))] = 'scoop vib'
                P['pizz'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, (p('D3'), p('A3'), p('D4'), p('A3'))[k % 4], 82] for k in range(8)]
            else:
                P['drk'] += [[t0 + k * S, t0 + k * S + S, TEK if k % 2 == 0 else KA, 62 + 3 * k] for k in range(15)]
                P['drk'].append([t0 + 15 * S, t0 + 16 * S, DUM, 118])
                run = scale(p('D4'), p('D6'))
                P['str'] += [[t0 + k * S, t0 + (k + 1) * S, run[k], 70 + 3 * k] for k in range(15)]
                P['timp'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, p('D3'), 64 + 7 * k] for k in range(8)]
                P['pizz'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, (p('D3'), p('A3'), p('D4'), p('A3'))[k % 4], 90] for k in range(4)]
            continue
        # ------------------------------------------------------------------ A / A': Confined
        if sec == 'A':
            if var == 'a1':
                put(P, 'oud', t0, THEME[i], 112)
            else:
                put(P, 'miz', t0, THEME[i], 108)
                for st, ln, n in THEME[i]:
                    if ln >= 3:
                        FX['miz'][(t0 + st * S, n)] = 'scoop vib'
                # heterofonie: de oud een octaaf lager, lange noten als tremolo (16en), korte met een voorslag
                for st, ln, n in THEME[i]:
                    if ln >= 4:
                        P['oud'] += [[t0 + (st + k) * S, t0 + (st + k + 1) * S, n - 12, 92 if k == 0 else 70] for k in range(ln)]
                    else:
                        P['oud'].append([t0 + st * S, t0 + (st + ln) * S, n - 12, 96])
            # pizzicato in 8en: grondtoon-kwint-octaaf-kwint (de 'trickster'-tred), staccato
            ivs = (0, 7, 12, 7, 3 if ch in ('Cm', 'Gm') else 4, 7, 12, 7)
            base = near(r, p('C3'))
            P['pizz'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, base + ivs[k], 96 if k % 2 == 0 else 80] for k in range(8)]
            if var == 'a2':
                P['bass'] += [[t0, t0 + 6 * S, near(r, p('C2')), 100], [t0 + 8 * S, t0 + 14 * S, near(r, p('C2')), 92]]
                P['perc'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, TAMB, 64 if k % 2 == 0 else 50] for k in range(8)]
                P['frm'] += [[t0, t0 + 4 * S, BENDIR, 104], [t0 + 10 * S, t0 + 14 * S, BENDIR, 86]]
            # darbuka: maqsum met de tek als backbeat (2 en 4), ka's vullen de 8en
            hits = ((0, DUM, 112), (2, KA, 62), (4, TEK, 108), (6, KA, 72), (8, DUM, 106), (10, KA, 66), (12, TEK, 110),
                    (14, KA, 70))
            P['drk'] += [[t0 + st * S, t0 + st * S + S, n, v] for st, n, v in hits]
            if var == 'a2' and i % 2 == 1:
                P['drk'].append([t0 + 15 * S, t0 + 16 * S, KA, 64])
            if i == 7:     # fill naar de volgende sectie
                P['drk'] = [d for d in P['drk'] if not (t0 + 12 * S <= d[0] < t0 + BAR)]
                P['drk'] += [[t0 + (12 + k) * S, t0 + (13 + k) * S, (TEK, KA, TEK, DUM)[k], 84 + 8 * k] for k in range(4)]
            if var == 'a1':
                P['perc'] += [[t0 + st * S, t0 + st * S + 2 * S, ZILL, 70] for st in (4, 12)]
            else:
                P['perc'] += [[t0 + st * S, t0 + st * S + 2 * S, ZILL, 66] for st in (4,)]
            if i == 0:
                P['perc'].append([t0, t0 + 4 * S, CRASH, 96 if var == 'a1' else 104])
                P['timp'].append([t0, t0 + 3 * S, p('D3'), 100])
            # strijkers: alleen in A' een zachte lange onderstem (grondtoon + kwint per halve maat)
            if var == 'a2':
                for h in (0, 8):
                    P['str'].append([t0 + h * S, t0 + (h + 8) * S - 12, near(r, p('D4')) - 12, 60])
            continue
        # ------------------------------------------------------------------ B: de ring groeit
        if sec == 'B':
            if i < 6:
                put(P, 'miz', t0, CALL[i], 110)
                for st, ln, n in CALL[i]:
                    if ln >= 3:
                        FX['miz'][(t0 + st * S, n)] = 'scoop vib'
                # strijkers-antwoord: 16en door de hijaz, omhoog of omlaag vanaf een akkoordtoon
                lo = tones(ch, p('G4'), p('D5'))[0]
                sc = scale(p('D4'), p('G5'))
                k0 = sc.index(lo) if lo in sc else 0
                seq = sc[k0:k0 + 8] if i % 2 == 0 else sc[max(0, k0 + 3 - 7):k0 + 4][::-1]
                P['str'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, seq[k % len(seq)], 92 if k == 0 else 80] for k in range(8)]
            elif i == 6:   # unisono-run door twee octaven (strijkers + oud), de mizmar houdt A4 vast
                put(P, 'miz', t0, CALL[6], 106)
                FX['miz'][(t0, p('A4'))] = 'scoop vib'
                run = scale(p('D4'), p('D6')) + [p('Eb6')]
                P['str'] += [[t0 + k * S, t0 + (k + 1) * S, run[k], 76 + 2 * k] for k in range(16)]
                P['oud'] += [[t0 + k * S, t0 + (k + 1) * S, run[k] - 12, 80 + 2 * k] for k in range(16)]
            else:          # Eb-D jammerklacht, alles valt stil op tel 4
                put(P, 'miz', t0, CALL[7], 114)
                FX['miz'][(t0, p('Eb5'))] = 'scoop vib'
                FX['miz'][(t0 + 8 * S, p('D5'))] = 'vib'
                P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('D3'), 60 + 4 * k] for k in range(12)]
                gust(P, CC, EX, 'noise', t0, 12 * S, 60, 110, rise=18)
                P['str'] += [[t0, t0 + 12 * S - 12, n, 96] for n in (p('D4'), p('Eb4'))]
            # choir zwelt aan vanaf maat 21
            if 4 <= i < 7:
                for n in tones(ch, p('G4'), p('Eb5'))[:2]:
                    for h in (0, 8):
                        P['choir'].append([t0 + h * S, t0 + (h + 8) * S - 12, n, 70 + 6 * (i - 4)])
            # bas in 8en op de grondtoon, octaafsprong op de 'en' van 2 en 4
            if i < 7:
                base = near(r, p('C2'))
                P['bass'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S + 6, base + (12 if k in (3, 7) else 0), 104 if k % 4 == 0 else 92]
                              for k in range(8)]
            else:
                P['bass'] += [[t0, t0 + 12 * S, p('D2'), 104]]
            # darbuka: ayyub-galop (dum . ka dum tek . ka . per halve maat)
            if i < 7:
                hits = ((0, DUM, 112), (3, KA, 70), (4, DUM, 100), (6, TEK, 108))
                for h in (0, 8):
                    P['drk'] += [[t0 + (h + st) * S, t0 + (h + st + 1) * S, n, v + 2 * i] for st, n, v in hits]
                if i in (3, 5):
                    P['drk'] = [d for d in P['drk'] if not (t0 + 12 * S <= d[0] < t0 + BAR)]
                    P['drk'] += [[t0 + (12 + k) * S, t0 + (13 + k) * S, TEK if k % 2 == 0 else KA, 90 + 6 * k] for k in range(4)]
                if i == 6:
                    P['drk'] = [d for d in P['drk'] if not (t0 + 8 * S <= d[0] < t0 + BAR)]
                    P['drk'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, TEK if k % 2 == 0 else KA, 76 + 6 * k] for k in range(8)]
                P['frm'] += [[t0, t0 + 4 * S, BENDIR, 110], [t0 + 8 * S, t0 + 12 * S, BENDIR, 100]]
                P['perc'] += [[t0 + st * S, t0 + st * S + 2 * S, ZILL, 74] for st in (4, 12)]
            else:
                P['drk'] += [[t0 + (k * 2) * S, t0 + (k * 2 + 1) * S, SNARE_R, 70 + 8 * k] for k in range(6)]
            if i in (0, 4):
                P['perc'].append([t0, t0 + 4 * S, CRASH, 104])
                P['timp'].append([t0, t0 + 3 * S, near(r, p('C3')), 104])
            continue
        # ------------------------------------------------------------------ C / C': Unbound
        if sec in ('C', 'C2'):
            src = THEME[(i // 2) + (0 if sec == 'C' else 4)]
            half = i % 2
            ph = [(st * 2 - half * 16, ln * 2, n) for st, ln, n in src if half * 8 <= st < half * 8 + 8]
            put(P, 'horn', t0, ph, 116, shift=-12)
            if sec == 'C2':
                put(P, 'tpt', t0, ph, 112)
            # tuba: grondtoon in halve noten (>= C3: geen 'puuup')
            P['tuba'] += [[t0 + h * S, t0 + (h + 8) * S - 12, near(r, p('C3')), 110] for h in (0, 8)]
            # koor: c1 twee stemmen, c2 drie
            nv = 2 if sec == 'C' else 1          # C': de trompet neemt de tweede stem over
            for n in tones(ch, p('A3'), p('A4'))[-nv:]:
                for h in (0, 8):                 # in halve maten (een kanaalroof kost dan geen hele maat)
                    P['choir'].append([t0 + h * S, t0 + (h + 8) * S - 12, n, 84 if sec == 'C' else 96])
            # 3-3-2: bas, pauken, taiko, lijsttrom op 16e 0, 6, 12
            base = near(r, p('C2'))
            last = i == 7
            P['bass'] += [[t0 + st * S, t0 + (st + ln) * S - 6, base, 116 if st == 0 else 104] for st, ln in ((0, 6), (6, 6), (12, 4))]
            P['timp'] += [[t0 + st * S, t0 + (st + 3) * S, near(r, p('C3')), 118 if st == 0 else 104] for st in (0, 6, 12)]
            P['frm'] += [[t0 + st * S, t0 + (st + 4) * S, TAIKO if st == 0 else BENDIR, 120 if st == 0 else 108] for st in (0, 6, 12)]
            P['wave'].append([t0, t0 + BAR - 12, base, 80])
            # darbuka: 8en, dum op de 3-3-2, tek ertussen
            hits = ((0, DUM_LO, 112), (2, TEK, 96), (4, KA, 84), (6, DUM_LO, 106), (8, TEK, 100), (10, KA, 86),
                    (12, DUM_LO, 108), (14, TEK, 98))
            P['drk'] += [[t0 + st * S, t0 + st * S + S, n, v] for st, n, v in hits]
            # strijkers: laag slangachtig ostinato in 16en (D Eb D C | D Eb F# Eb), vanaf C' een octaaf hoger
            cell = (0, 1, 0, -2, 0, 1, 4, 1)
            sb = near(r, p('C3')) + (12 if sec == 'C2' else 0)
            if not (sec == 'C2' and i >= 6):
                P['str'] += [[t0 + k * S, t0 + (k + 1) * S, sb + cell[k % 8], 92 if k % 4 == 0 else 78] for k in range(16)]
            else:      # maat 39-40: alles in 16en omhoog (39) en een dalende hijaz-run terug naar Confined (40)
                run = scale(p('D4'), p('D6')) + [p('Eb6')]
                seq = run if i == 6 else run[::-1]
                P['str'] += [[t0 + k * S, t0 + (k + 1) * S, seq[k], 84 + 2 * k if i == 6 else 112 - 2 * k] for k in range(16)]
            if i % 2 == 0:
                P['perc'].append([t0, t0 + 4 * S, CRASH, 108 if sec == 'C' else 116])
            if last and sec == 'C2':
                P['drk'] = [d for d in P['drk'] if not (t0 + 8 * S <= d[0] < t0 + BAR)]
                P['drk'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, (TEK, KA, TEK, KA, TEK, DUM, TEK, DUM)[k], 86 + 4 * k] for k in range(8)]
            continue
        # ------------------------------------------------------------------ K: de djinn lacht, terug naar Confined
        if sec == 'K':
            put(P, 'oud', t0, GIGGLE if i == 0 else GIGGLE2, 114)
            hits = ((0, DUM, 116), (2, TEK, 90), (3, KA, 74), (4, TEK, 104), (6, DUM, 108), (7, KA, 70), (8, TEK, 100),
                    (10, DUM, 110), (11, KA, 76), (12, TEK, 102), (13, KA, 80), (14, TEK, 106), (15, KA, 84))
            if i == 1:
                hits = ((0, DUM, 116), (2, KA, 80), (4, TEK, 104), (6, KA, 82), (8, DUM, 110)) + \
                       tuple((12 + k, TEK if k % 2 == 0 else KA, 90 + 6 * k) for k in range(4))
            P['drk'] += [[t0 + st * S, t0 + st * S + S, n, v] for st, n, v in hits]
            P['perc'] += [[t0 + st * S, t0 + st * S + 2 * S, ZILL, 76] for st in (4, 12)]
            P['pizz'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, (p('D3'), p('A3'), p('D4'), p('A3'))[k % 4], 88] for k in range(8)]
            if i == 0:
                P['frm'].append([t0, t0 + 4 * S, BENDIR, 104])
    return P, CC, EX, FX


# ---- voicegroup, keysplits, drumkit -------------------------------------------------------------------------------
KIT = [   # vanaf noot 36: (regel, lengte van de sample in s; None = geloopt)
    ('voice_directsound 60, 64, DirectSoundWaveData_hoopa_dum, 255, 0, 255, 160', 0.42),
    ('voice_directsound 60, 64, DirectSoundWaveData_hoopa_tek, 255, 0, 255, 100', 0.16),
    ('voice_directsound 56, 64, DirectSoundWaveData_hoopa_tek, 255, 0, 255, 100', 0.20),
    ('voice_directsound 60, 64, DirectSoundWaveData_hoopa_bendir, 255, 0, 255, 180', 0.75),
    ('voice_directsound 60, 64, DirectSoundWaveData_hoopa_zill, 255, 0, 255, 180', 0.55),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 170', None),
    ('voice_directsound 57, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180', 0.50),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 120', 0.17),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 150', 0.16),
    ('voice_directsound 54, 64, DirectSoundWaveData_hoopa_dum, 255, 0, 255, 170', 0.59),
]
KEYSPLITS = {   # naam: [(sample, release)]; tabellen in sound/keysplit_tables.inc
    'hoopa_oud': [('hoopa_oud_%d' % k, 255, 110) for k in (50, 57, 64, 71)],
    'hoopa_mizmar': [('hoopa_mizmar_%d' % k, 200, 120) for k in (57, 64, 71)],
    'hoopa_str': [('sc88pro_string_ensemble_%d' % k, 255, 110) for k in (60, 72, 84)],
}
VOICES = {
    OUD: 'voice_keysplit voicegroup_hoopa_oud_keysplit, keysplit_hoopa_oud',
    MIZ: 'voice_keysplit voicegroup_hoopa_mizmar_keysplit, keysplit_hoopa_mizmar',
    STR: 'voice_keysplit voicegroup_hoopa_str_keysplit, keysplit_strings',
    PIZZ: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_pizzicato_strings, 255, 0, 255, 120',
    TIMP: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 150',
    WAVE: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
    NOISE: 'voice_noise_alt 60, 0, 0, 0, 0, 15, 2',
    DRUMS: 'voice_keysplit_all voicegroup_hoopa_drumset',
}


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Hoopa. Gegenereerd door tools/grounded/hoopa_theme.py.'
    lines[1] = ('@ eigen samples (hoopa_samples.py): 105 oud, 111 mizmar (keysplits hoopa_*), 127 = drumkit hoopa; '
                'stock: 45 pizzicato, 48 strijkers, 33 bas, 56 trompet, 58 tuba, 60 hoorn, 52 koor, 47 pauken.')
    lines[2] = 'voice_group %s' % VG
    out = []
    for l in lines:
        if l.startswith('\t') and '@' in l:
            prog = int(l.rsplit('@', 1)[1])
            if prog in VOICES:
                l = '\t%s  @ %d' % (VOICES[prog], prog)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/drumsets/hoopa.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Hoopa (hoopa_theme.py): 36 darbuka dum, 37 tek, 38 ka, 39 lijsttrom\n'
        '@ (bendir), 40 vingerbekken, 41 crash, 42 taiko, 43 tamboerijn, 44 orkestsnare (roffels), 45 lage dum.\n'
        '@ hoopa_* = eigen samples (hoopa_samples.py).\n'
        'voice_group hoopa_drumset, 36\n' + ''.join('\t%s\n' % k for k, _ in KIT) + '\n')
    for name, samples in KEYSPLITS.items():
        open('sound/voicegroups/keysplits/%s.inc' % name, 'w').write(
            '@ Project Grounded: Battle! Hoopa, %s. Gegenereerd door tools/grounded/hoopa_theme.py.\n'
            'voice_group %s_keysplit\n' % (name, name) +
            ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_%s, %d, 0, 255, %d\n' % (s, a, r) for s, a, r in samples))


# ---- bouwen ---------------------------------------------------------------------------------------------------------
TRACKS = [   # (naam, programma, volume, pan)
    ('oud', OUD, 120, 56), ('miz', MIZ, 112, 70), ('str', STR, 92, 76), ('pizz', PIZZ, 100, 52),
    ('bass', BASS, 96, 64), ('horn', HORN, 110, 58), ('tuba', TUBA, 96, 64), ('tpt', TPT, 82, 72),
    ('choir', CHOIR, 76, 64), ('timp', TIMP, 100, 64), ('drk', DRUMS, 112, 60), ('frm', DRUMS, 108, 64),
    ('perc', DRUMS, 76, 74), ('wave', WAVE, 44, 64), ('noise', NOISE, 60, 64),
]
PSG = {'wave', 'noise'}
ORDER = ['oud', 'miz', 'horn', 'tpt', 'drk', 'str', 'bass', 'frm', 'perc', 'tuba', 'choir', 'timp', 'pizz']
DRUMPARTS = ('drk', 'frm', 'perc')
# hoe lang een slag mag doorklinken (16en); de volgende slag in dezelfde partij kapt eerder
RING = {DUM: 4, TEK: 2, KA: 2, BENDIR: 6, ZILL: 4, CRASH: 4, TAIKO: 6, TAMB: 1, SNARE_R: 1, DUM_LO: 5}
FREE = (CRASH, ZILL)          # bekkens klinken los van de rest van hun partij uit


def tight(ev, tail):
    """tokkels (oud, pizzicato): noot + uitklinktijd past tot de volgende aanslag (min. 3 ticks)."""
    ev = sorted(ev)
    starts = sorted(set(e[0] for e in ev))
    out = []
    for e in ev:
        nxt = next((t for t in starts if t > e[0]), None)
        end = e[1] if nxt is None else min(e[1], max(e[0] + 3, nxt - tail))
        out.append([e[0], end, e[2], e[3]])
    return out


def kit_rel(n):
    return int(KIT[n - 36][0].rsplit(',', 1)[1])


def ring_gates(notes):
    notes = sorted(notes)
    starts = sorted({n[0] for n in notes if n[2] not in FREE})
    out = []
    for n in notes:
        ln = RING.get(n[2], 2) * S
        if n[2] not in FREE:
            nxt = next((x for x in starts if x > n[0]), None)
            if nxt is not None:
                r = release_ticks(kit_rel(n[2]), TPB, BPM) + 1
                ln = min(ln, max(3, nxt - n[0] - r))
        out.append([n[0], n[0] + ln, n[2], n[3]])
    return out


def no_overlap(ev):
    ev = sorted(ev)
    for i, e in enumerate(ev):
        nxt = next((x[0] for x in ev[i + 1:] if x[2] == e[2] and x[0] >= e[0] and x is not e), None)
        if nxt is not None and nxt < e[1]:
            e[1] = max(e[0] + 1, nxt)
    return ev


def miz_fx(notes, fx):
    """mizmar: scoop (pitch bend van -1 halve toon naar 0 in ±3 frames) en vibrato (CC1 na een 16e, LFO ±5,5 Hz)
    op lange noten; terugzetten op de volgende noot. BENDR 2 (8192 = 2 halve tonen)."""
    ev = [(0, mido.Message('control_change', control=20, value=2)), (0, mido.Message('pitchwheel', pitch=0)),
          (0, mido.Message('control_change', control=1, value=0))]
    notes = sorted(notes)
    for i, (s, e, n, v) in enumerate(notes):
        f = fx.get((s, n), '')
        nxt = notes[i + 1][0] if i + 1 < len(notes) else e + TPB
        if 'scoop' in f:
            ev.append((s, mido.Message('pitchwheel', pitch=-4096)))
            for k in range(1, 4):
                ev.append((s + 4 * k, mido.Message('pitchwheel', pitch=-4096 + 4096 * k // 3)))
        if 'vib' in f and e - s > 2 * S:
            ev.append((s + S + S // 2, mido.Message('control_change', control=1, value=5)))
            ev.append((nxt, mido.Message('control_change', control=1, value=0)))
    return ev


def build(render_dir=None):
    write_voicegroup()
    rel = releases(VG)
    P, CC, EX, FX = compose()
    parts = {k: dedupe(v) for k, v in P.items()}
    progs = {k: pr for k, pr, _, _ in TRACKS}
    tail = {}
    for k, pr in progs.items():
        tail[k] = 0 if (k in PSG or pr == DRUMS) else release_ticks(rel.get(pr, 200), TPB, BPM) + 2
    for k in ('miz', 'str', 'bass', 'horn', 'tuba', 'tpt', 'choir', 'timp'):
        if k in parts:
            parts[k] = detach(parts[k], tail[k])
    for k in ('oud', 'pizz'):
        parts[k] = tight(parts[k], tail[k])
    for k in DRUMPARTS:
        parts[k] = ring_gates(parts[k])
    for k in parts:
        parts[k] = no_overlap(parts[k])
    for k, pr in progs.items():
        if k in PSG or pr == DRUMS:
            continue
        assert all(n >= 28 for _, _, n, _ in parts.get(k, [])), '%s: noten onder E1' % k
        if pr in (TPT, HORN, TUBA):
            assert all(n >= 48 for _, _, n, _ in parts.get(k, [])), '%s: koper onder C3' % k
    proxy = {}
    for k in DRUMPARTS:
        proxy[k] = []
        for i, (s0, e0, n, v) in enumerate(parts[k]):
            line, slen = KIT[n - 36]
            occ = e0 - s0 + release_ticks(kit_rel(n), TPB, BPM) + 2
            if slen is not None:
                key = int(line.split()[1].rstrip(','))
                sec = slen * (2 ** ((60 - key) / 12) if 'no_resample' not in line else 1)
                occ = min(occ, int(sec * BPM / 60 * TPB) + 1)
            proxy[k].append([s0, s0 + occ, n, v, i])
    alloc_in = {k: (proxy[k] if k in proxy else parts.get(k, [])) for k in ORDER}
    kept = allocate(alloc_in, ORDER, tail, max_voices=MAX_V)
    for k in proxy:
        idx = {e[4] for e in kept[k]}
        kept[k] = [e for i, e in enumerate(parts[k]) if i in idx]
    for k in ORDER:
        n = len(parts.get(k, []))
        weg = [e for e in parts.get(k, []) if e not in kept[k]]
        gone = sorted({e[0] // BAR - INTRO + 1 for e in weg})
        if "-v" in sys.argv and weg:
            print("     ", [(e[0] // BAR - INTRO + 1, (e[0] % BAR) // S, e[2]) for e in weg])
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, len(weg), 100 * len(weg) / max(n, 1),
                                                             ' (maten %s)' % gone[:16] if gone else ''))
        parts[k] = kept[k]
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.tempo(INTRO * BAR, BPM / 120)
    song.loop = (INTRO * BAR, END * BAR)
    for ch, (k, prog, vol, pan) in enumerate(TRACKS):
        notes = sorted(parts.get(k, []))
        extra = list(EX.get(k, []))
        ccs = list(CC.get(k, []))
        if k == 'miz':
            extra = miz_fx(notes, FX['miz'])
        if k == 'noise':
            extra = [(0, mido.Message('control_change', control=20, value=12))] + extra
        song.add(notes, prog, vol, ch, pan, extra=extra, ccs=ccs)
    song.save(OUT, END * BAR)
    print(OUT, 'intro %.2f s, loop %.1f s' % (INTRO * 4 * 60 / BPM, (END - INTRO) * 4 * 60 / BPM))
    if render_dir:
        render_gm(render_dir)


# ---- offline-render (FluidR3 GM; andere klanken dan de GBA, wel noten/vorm/tempo) ------------------------------------
GM_PROG = {'oud': 24, 'miz': 111, 'str': 48, 'pizz': 45, 'bass': 33, 'horn': 60, 'tuba': 58, 'tpt': 56, 'choir': 52,
           'timp': 47, 'wave': 38, 'noise': 0}
GM_DRUM = {DUM: 35, TEK: 37, KA: 39, BENDIR: 41, ZILL: 81, CRASH: 49, TAIKO: 36, TAMB: 54, SNARE_R: 38, DUM_LO: 35}


def render_gm(outdir):
    os.makedirs(outdir, exist_ok=True)
    m = mido.MidiFile(OUT)
    gm = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    gm.tracks.append(m.tracks[0])
    free = [c for c in range(16) if c != 9]
    for i, (k, prog, vol, pan) in enumerate(TRACKS):
        drum = prog == DRUMS
        if k == 'noise':
            continue
        ch = 9 if drum else free.pop(0)
        t = mido.MidiTrack()
        for x in m.tracks[i + 1]:
            if x.type == 'program_change':
                x = x.copy(channel=ch, program=0 if drum else GM_PROG[k])
            elif x.type in ('note_on', 'note_off') and drum:
                x = x.copy(channel=ch, note=GM_DRUM.get(x.note, 47))
            elif hasattr(x, 'channel'):
                x = x.copy(channel=ch)
            t.append(x)
        gm.tracks.append(t)
    mid = os.path.join(outdir, 'hoopa_gm.mid')
    gm.save(mid)
    wav = os.path.join(outdir, 'hoopa_fluidr3.wav')
    subprocess.run(['fluidsynth', '-ni', '-g', '0.5', '-r', '44100', '-F', wav, '/usr/share/sounds/sf2/FluidR3_GM.sf2',
                    mid], check=True, capture_output=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-t', '72', '-af',
                    'loudnorm=I=-16:TP=-1.5,afade=t=out:st=70:d=2', '-b:a', '160k', wav[:-4] + '.mp3'], check=True)
    os.remove(wav)
    print('render:', wav[:-4] + '.mp3')


if __name__ == '__main__':
    build(sys.argv[sys.argv.index('--render') + 1] if '--render' in sys.argv else None)
