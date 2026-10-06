#!/usr/bin/env python3
"""Project Grounded: Battle! Forces of Nature (Tornadus, Thundurus, Landorus), drie eigen composities op één thema.

Jordi: "voor Landorus, Tornadus en Thundurus ook wat bedenken ... die drie een vergelijkbaar theme geven met ander
tempo en instrumentatie". Eén gedeeld 'Forces'-motief (zelfde melodie en akkoordskelet), drie arrangementen.

Het motief (geschreven in D-klein, 8 maten): kop = gestippelde kwart D, dan E-F-A omhoog (een windstoot die opstijgt);
antwoord zakt stapsgewijs terug. Akkoorden A: Dm-Bb-C-A | Dm-Bb-Gm/A-Dm (i-bVI-bVII-V).
Brug B: dezelfde kop als sequens omhoog op Bb, C en D (de storm klimt), daarna Gm-A-Bb-A (dominant).
C (alleen Landorus): het motief in D-GROOT (D-Bb-C-D | G-A-Bb/C-D), triomfantelijk: Landorus bedaart de andere twee
en brengt de oogst (Abundant Shrine): trompetten, koor en buisklokken.

v2 (Jordi over v1: 'klinkt heel erg als Megaman, alsof dit voor een SNES is'): geen PSG-leads/-arpeggio's meer (alleen
PSG-golf als sub en PSG-ruis voor wind/bliksem/aardrommel), volle GBA-orkestratie, stereo uitgespreid.
  Tornadus  (wind)      176 bpm, E-klein (+2). Lead = trompet + strijkers unisono (was het 'hoge fluitje'), hoorns als
                        tweede stem, spiccato-strijkerswerveling in 16en, koor (a1), pauken, drumstel + conga's;
                        windstoten = PSG-ruis met volume-zwelling en wervelende pitch bend (blijven, Jordi: 'tof').
                        Intro 4 maten, loop A-A2-B-S(werveling, 4 maten)-A3.
  Thundurus (bliksem)   152 bpm, C-klein (-2). Compositie als v1: distortion-gitaarlead + strijkers unisono,
                        gesyncopeerd motief, trompetstoten off-beat, riff 3+3+2, synth-bas + tuba op de zware tellen +
                        PSG-sub, snare = rnd-snare + orkestsnare (geen PSG-crack), tamboerijn, koor/orgel-pads;
                        bliksem = crash + ruis die omlaag buigt + korte zap. Intro 4 maten, loop A-A2-B-K(stormbreak).
  Landorus  (aarde)     132 bpm (was 112), D-klein. Battle-groove: drumstel + taiko, strijkersostinato in 16en, bas in
                        springende achtsten, pauken; hoorns (a1), trompet + hoorns + strijkers-tegenmelodie (a2),
                        B = vraag-antwoord hoorns/trompetten met dubbeltempo-drums, C = climax in D-groot: trompetten,
                        hoorn-tegenstem, koor, tuba, buisklokken, crashes. Intro 4 maten, loop A-A2-B-C.

Alleen Emerald-samples (geen eigen samples). Voicegroup voicegroup_grounded_forces (grounded_gm + overrides) en keysplit
keysplits/forces_spicc.inc (spiccato-strijkers, korte release). Stemverdeler max. 11 DirectSound-noten (legendary).
Schrijft ook FluidR3-referentie-MIDI's (met de octaafcorrecties van de GBA-samples) naar een map naar keuze:
  python3 tools/grounded/forces_theme.py [--ref <map>]
Zie tools/grounded/MUZIEK.md."""
import math, os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

VG = 'grounded_forces'
MAXV = 11                     # v2: legendary-budget (lint: MAX_PER_SONG)
TPB = 96
S = TPB // 4                  # een 16e
BAR = TPB * 4

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- het gedeelde materiaal (geschreven in D-klein) ----------------------------------------------------------------
CH = {'Dm': (2, (2, 5, 9)), 'Bb': (10, (10, 2, 5)), 'C': (0, (0, 4, 7)), 'A': (9, (9, 1, 4)), 'Gm': (7, (7, 10, 2)),
      'D': (2, (2, 6, 9)), 'G': (7, (7, 11, 2))}
PROG = {
    'A': [[(0, 'Dm')], [(0, 'Bb')], [(0, 'C')], [(0, 'A')], [(0, 'Dm')], [(0, 'Bb')], [(0, 'Gm'), (8, 'A')], [(0, 'Dm')]],
    'B': [[(0, 'Bb')], [(0, 'C')], [(0, 'Dm')], [(0, 'Dm')], [(0, 'Gm')], [(0, 'A')], [(0, 'Bb')], [(0, 'A')]],
    'C': [[(0, 'D')], [(0, 'Bb')], [(0, 'C')], [(0, 'D')], [(0, 'G')], [(0, 'A')], [(0, 'Bb'), (8, 'C')], [(0, 'D')]],
    'I': [[(0, 'Dm')], [(0, 'Dm')], [(0, 'Dm')], [(0, 'A')]],
}
PROG['S'] = PROG['K'] = PROG['A'][:4]
MEL = {   # (16e-stap, lengte in 16en, noot)
    'A': [[(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'A5')],
          [(0, 8, 'G5'), (8, 2, 'F5'), (10, 2, 'E5'), (12, 4, 'D5')],
          [(0, 6, 'E5'), (6, 2, 'F5'), (8, 4, 'G5'), (12, 4, 'C6')],
          [(0, 8, 'A5'), (8, 4, 'E5'), (12, 4, 'C#5')],
          [(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'A5')],
          [(0, 8, 'D6'), (8, 2, 'C6'), (10, 2, 'Bb5'), (12, 4, 'A5')],
          [(0, 4, 'G5'), (4, 4, 'Bb5'), (8, 4, 'A5'), (12, 2, 'G5'), (14, 2, 'E5')],
          [(0, 12, 'D5')]],
    'B': [[(0, 6, 'Bb4'), (6, 2, 'C5'), (8, 4, 'D5'), (12, 4, 'F5')],
          [(0, 6, 'C5'), (6, 2, 'D5'), (8, 4, 'E5'), (12, 4, 'G5')],
          [(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'A5')],
          [(0, 12, 'D6'), (12, 2, 'C6'), (14, 2, 'A5')],
          [(0, 8, 'Bb5'), (8, 4, 'A5'), (12, 4, 'G5')],
          [(0, 8, 'E5'), (8, 4, 'C#5'), (12, 4, 'A4')],
          [(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'G5')],
          [(0, 16, 'A5')]],
    'C': [[(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F#5'), (12, 4, 'A5')],
          [(0, 8, 'Bb5'), (8, 2, 'A5'), (10, 2, 'G5'), (12, 4, 'F5')],
          [(0, 6, 'E5'), (6, 2, 'F5'), (8, 4, 'G5'), (12, 4, 'C6')],
          [(0, 16, 'D6')],
          [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'G5'), (12, 4, 'D6')],
          [(0, 8, 'C#6'), (8, 4, 'B5'), (12, 4, 'A5')],
          [(0, 4, 'F5'), (4, 4, 'Bb5'), (8, 4, 'G5'), (12, 4, 'C6')],
          [(0, 16, 'D6')]],
}
SCALE = (2, 4, 5, 7, 9, 10, 0)      # D-eolisch
KICK, SNARE, OSNARE, TOM_L, HH, TOM_M, TOM_H, TOM_X, TAMB, CRASH, CONGA_H, CONGA_L = \
    36, 38, 40, 41, 42, 45, 47, 48, 54, 57, 62, 64

# programma's in voicegroup_grounded_forces
BELL, ORGAN, FBASS, SBASS, DIST_LO, DIST_HI, STR, TIMP, SPICC, CHOIR, TPT, TUBA, HORN, FLUTE, TAIKO, KIT = \
    14, 19, 33, 38, 29, 30, 48, 47, 49, 52, 56, 58, 60, 73, 116, 127
SQ_ARP, SQ_LEAD, SQ_ECHO, WAVE, GUST, CRACK = 80, 81, 82, 84, 121, 122
TROLL = 45           # v2: pauk met korte release (roffels en accenten; 16en op 47 bezetten 3 kanalen)
TAIKO_KEY = 57      # sc88pro_taiko klinkt 88 Hz op toets 60 (gemeten); 57 = 74 Hz = D2, de grondtoon (C3 gaf 44 Hz-dreun)
OCT_DOWN = {DIST_LO: 12, ORGAN: 12}   # GBA-sample klinkt een octaaf lager dan geschreven (gemeten): geschreven +12


def near(pc, lo):
    return lo + ((pc - lo) % 12)


def segs(sec, i):
    s = PROG[sec][i]
    return [(st, s[k + 1][0] if k + 1 < len(s) else 16, name) for k, (st, name) in enumerate(s)]


def chord_at(sec, i, step):
    return [n for st, n in PROG[sec][i] if st <= step][-1]


def tones(name, lo, hi):
    return [m for m in range(lo, hi + 1) if m % 12 in CH[name][1]]


def scale(lo, hi, harmonic=False):
    pcs = set(SCALE) - ({0} if harmonic else set()) | ({1} if harmonic else set())
    return [m for m in range(lo, hi + 1) if m % 12 in pcs]


def mel(sec, i, t0, vel, shift=0, pat=None):
    return [[t0 + st * S, t0 + (st + ln) * S, p(n) + shift, vel] for st, ln, n in (pat or MEL[sec][i])]


def push(pat):
    """Thundurus: de aanslag op tel 3 een 16e naar voren (gesyncopeerd), de vorige noot korter."""
    out = [list(x) for x in pat]
    for k in range(1, len(out)):
        if out[k][0] == 8 and out[k - 1][0] < 7:
            out[k][0], out[k][1] = 7, out[k][1] + 1
            out[k - 1][1] = 7 - out[k - 1][0]
    return out


def harmony_below(notes, sec_of):
    """Tweede stem: de hoogste akkoordtoon minstens een kleine terts onder elke melodienoot."""
    out = []
    for s, e, n, v in notes:
        sec, i, t0 = sec_of(s)
        ch = chord_at(sec, i, (s - t0) // S)
        cand = [m for m in tones(ch, n - 9, n - 3)]
        if cand:
            out.append([s, e, max(cand), v])
    return out


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def gust(P, CC, EX, name, t0, length, key, vmax, wobble=5, seed=0, down=False):
    """Windstoot/donder op een PSG-ruisspoor: één noot, CC7 zwelt aan en af, pitch bend wervelt (BENDR 12)."""
    P[name].append([t0, t0 + length, key, 110])
    steps = max(2, length // S)
    for k in range(steps + 1):
        x = k / steps
        CC[name].append((t0 + k * S, 7, int(8 + vmax * math.sin(math.pi * min(1.0, x)) ** 1.5)))
        semis = (-12 * x) if down else wobble * math.sin(2 * math.pi * (x * 1.5 + seed * 0.37))
        EX[name].append((t0 + k * S, mido.Message('pitchwheel', pitch=max(-8192, min(8191, int(semis / 12 * 8191))))))


def timeline(plan):
    tl = []
    for sec, n, var in plan:
        for i in range(n):
            tl.append((len(tl), sec, i, var))
    return tl


# ---- v2: gedeelde hulpjes ---------------------------------------------------------------------------------------
def counter_line(tl, secs, lo, hi, vel, unit=8):
    """Tegenmelodie: per halve maat (unit 16en) een akkoordtoon in lo..hi, zo dicht mogelijk bij de vorige,
    maar niet drie keer dezelfde (dan de dichtstbijzijnde andere): een langzame, zingende lijn."""
    out, prev, same = [], None, 0
    for b, sec, i, var in tl:
        if (sec, var) not in secs and sec not in secs:
            continue
        t0 = b * BAR
        for h in range(0, 16, unit):
            ch = chord_at(sec, i, h)
            cand = tones(ch, lo, hi)
            if prev is None:
                n = cand[len(cand) // 2]
            else:
                cand.sort(key=lambda m: (abs(m - prev), m))
                n = cand[0]
                if n == prev:
                    same += 1
                    if same >= 2 and len(cand) > 1:
                        n, same = cand[1], 0
                else:
                    same = 0
            out.append([t0 + h * S, t0 + (h + unit) * S - 8, n, vel])
            prev = n
    return out


def ostinato16(P, key, t0, st, en, r, lo, vel, pat=(0, 0, 7, 0, 12, 0, 7, 0)):
    """strijkersostinato in 16en vanaf grondtoon r (pc) boven lo, accent op elke tel."""
    base = near(r, lo)
    for k in range(st, en):
        P[key].append([t0 + k * S, t0 + k * S + S, base + pat[k % len(pat)], vel + (14 if k % 4 == 0 else 0)])


# ---- Tornadus v2: wind ------------------------------------------------------------------------------------------
# Jordi (v1): 'Tornadus wordt bijna helemaal gedragen door dat hoge fluitje, wat het erg wimpy maakt, de tornado's wel
# tof'; alles 'klinkt als Megaman/SNES'. v2: de melodie op trompet + strijkers unisono (hoorn eronder als tweede stem),
# de werveling in spiccato-strijkersloopjes (geen PSG-arpeggio's of -echo meer), koor + hoorns als harmonie, pauken,
# volledig drumstel; de windstoten (PSG-ruis met wervelende pitch bend) blijven.
def tornadus():
    P, CC, EX = Parts(), Parts(), Parts()
    tl = timeline([('I', 4, ''), ('A', 8, 'a1'), ('A', 8, 'a2'), ('B', 8, ''), ('S', 4, ''), ('A', 8, 'a3')])
    for b, sec, i, var in tl:
        t0 = b * BAR
        sg = segs(sec, i)
        root = CH[chord_at(sec, i, 0)][0]
        if sec == 'I':
            if b == 0:     # windstoot, de strijkers wervelen zacht op Dm (op en neer)
                gust(P, CC, EX, 'gust', t0, 2 * BAR - S, 64, 100, seed=1)
                P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('D2') + 12, 40 + 3 * k] for k in range(16)]
            if b in (0, 1):
                ts = tones('Dm', p('D4'), p('D5'))
                cyc = ts + ts[-2:0:-1]
                P['runs'] += [[t0 + k * S, t0 + k * S + S, cyc[k % len(cyc)], 56 + 3 * b + (10 if k % 4 == 0 else 0)] for k in range(16)]
                P['wave'].append([t0, t0 + BAR - 8, near(root, 38), 60])
            if b == 1:     # hoorns zwellen aan
                P['horn'] += [[t0, t0 + 8 * S - 8, p('A3'), 80], [t0 + 8 * S, t0 + 16 * S - 8, p('D4'), 90]]
                P['pad'] += [[t0, t0 + BAR - 8, n, 60] for n in (p('F4'), p('A4'))]
                P['drums'] += [[t0 + k * TPB, t0 + k * TPB + 2 * S, KICK, 70 + 6 * k] for k in range(4)]
            if b == 2:     # strijkersloop omhoog over twee octaven, trompet roept de kop van het motief
                run = scale(p('D4'), p('E6'))
                P['runs'] += [[t0 + k * S, t0 + k * S + S, run[k], 66 + k * 3] for k in range(16)]
                P['lead'] += mel('A', 0, t0, 104, shift=-12)
                P['horn'] += [[t0, t0 + 16 * S - 8, p('D4'), 96]]
                P['pad'] += [[t0, t0 + BAR - 8, n, 70] for n in (p('F4'), p('A4'))]
                P['drums'] += [[t0 + k * TPB, t0 + k * TPB + 2 * S, KICK, 90] for k in range(4)]
                P['drums'] += [[t0 + 12 * S + k * S, t0 + 13 * S + k * S, (TOM_H, TOM_M, TOM_L, TOM_L)[k], 90 + 4 * k] for k in range(4)]
                P['bass'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, near(2, 38), 92] for k in range(8)]
                P['wave'].append([t0, t0 + BAR - 8, near(root, 38), 70])
            if b == 3:     # dominant: trompet + strijkers dalen, arpeggio, snare-opbouw, windstoot
                P['lead'] += [[t0, t0 + 6 * S, p('A5'), 104], [t0 + 6 * S, t0 + 8 * S, p('G5'), 106],
                              [t0 + 8 * S, t0 + 12 * S, p('F5'), 110], [t0 + 12 * S, t0 + 16 * S, p('E5'), 114]]
                arp = tones('A', 57, 81)
                P['runs'] += [[t0 + k * S, t0 + k * S + S, arp[k % len(arp)], 80] for k in range(16)]
                P['horn'] += [[t0, t0 + 8 * S - 8, p('C#4'), 100], [t0 + 8 * S, t0 + 16 * S - 8, p('E4'), 104]]
                P['pad'] += [[t0, t0 + BAR - 8, n, 74] for n in (p('E4'), p('A4'))]
                P['drums'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, SNARE, 60 + 5 * k] for k in range(4)]
                P['drums'] += [[t0 + 8 * S + k * S, t0 + 9 * S + k * S, SNARE, 76 + 6 * k] for k in range(8)]
                P['drums'] += [[t0 + k * TPB, t0 + k * TPB + 2 * S, KICK, 104] for k in range(4)]
                P['timp'] += [[t0 + 8 * S + k * S, t0 + 9 * S + k * S, p('A2'), 70 + 6 * k] for k in range(8)]
                P['bass'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, near(9, 38), 96] for k in range(8)]
                P['wave'].append([t0, t0 + BAR - 8, near(9, 38), 70])
                gust(P, CC, EX, 'gust', t0 + 8 * S, 8 * S, 70, 110, seed=2)
            continue
        # ---- loop: melodie op trompet (+ strijkers unisono) --------------------------------------------------------
        if sec == 'A':
            vel = {'a1': 108, 'a2': 112, 'a3': 118}[var]
            P['lead'] += mel('A', i, t0, vel)
        elif sec == 'B':
            P['lead'] += mel('B', i, t0, 112)
        elif sec == 'S' and i in (0, 2):     # de werveling: de trompet antwoordt met de kop van het motief
            P['lead'] += mel('A', 0, t0, 108, pat=[(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'A5')]) if i == 2 else \
                mel('A', 0, t0, 108, pat=[(0, 3, 'A5'), (3, 1, 'G5'), (4, 2, 'F5'), (6, 2, 'E5'), (8, 8, 'D5')])
        # strijkerswerveling: altijd 16en, op en neer over de akkoordtonen; loopjes in de lange melodienoten
        if sec == 'S':
            lo = {0: p('D4'), 1: p('D6'), 2: p('C4'), 3: p('A3')}[i]
            if i == 3:
                arp = tones('A', 57, 81)
                seq = arp + arp[::-1]
            else:
                sc = scale(min(lo, p('D4') - 2), p('D6') + 2)
                seq = [m for m in sc if m >= lo][:16] if i != 1 else [m for m in sc if m <= lo][::-1][:16]
            P['runs'] += [[t0 + k * S, t0 + (k + 1) * S, seq[k % len(seq)], 80 + (k % 4 == 0) * 12] for k in range(16)]
        elif (sec == 'A' and i in (3, 7)) or (sec == 'B' and i % 2 == 1):
            ch = chord_at(sec, i, 0)
            for st, en, c in sg:
                if st < 8:
                    ts = tones(c, 62, 76)[:4]
                    cyc = ts + ts[-2:0:-1]
                    P['runs'] += [[t0 + k * S, t0 + k * S + S, cyc[k % len(cyc)], 96 if k % 4 == 0 else 80] for k in range(st, min(en, 8))]
            if sec == 'B' and i == 7:
                run = scale(p('A3'), p('Bb5'), harmonic=True)
                P['runs'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, run[k * 2], 70 + k * 5] for k in range(8)]
            else:
                lo = p('A4') if (sec == 'A' and i == 3) else near(CH[chord_at(sec, i, 8)][0], 62)
                run = scale(lo, p('E6'), harmonic=chord_at(sec, i, 8) == 'A')
                P['runs'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, run[k], 72 + k * 4] for k in range(8)]
        else:
            for st, en, ch in sg:
                ts = tones(ch, 62, 76)[:4]
                cyc = ts + ts[-2:0:-1]
                P['runs'] += [[t0 + k * S, t0 + k * S + S, cyc[k % len(cyc)], 96 if k % 4 == 0 else 80] for k in range(st, en)]
        # bas (fingered) in een springend ritme + PSG-golf als sub eronder
        for st, en, ch in sg:
            r = near(CH[ch][0], 38)
            if sec == 'B':
                P['bass'] += [[t0 + (st + k) * S, t0 + (st + k + 2) * S - 6, r + o, 100 if k == 0 else 88]
                              for k, o in ((0, 0), (3, 0), (6, 12), (10, 0), (12, 7), (14, 12)) if st + k < en]
            else:
                for k in (0, 3, 6, 8, 11, 14):
                    if st <= k < en:
                        P['bass'].append([t0 + k * S, t0 + k * S + 2 * S - 6, r + (12 if k in (6, 14) else 0), 104 if k in (0, 8) else 92])
            P['wave'] += [[t0 + st * S, t0 + en * S - 8, near(CH[ch][0], 38), 64]]
        # hoorns: tweede stem onder de melodie in a2/a3/B, lange akkoordtonen in a1 en de werveling
        if sec != 'S' and var != 'a1':
            pass       # (harmony_below na de lus)
        else:
            for st, en, ch in sg:
                n = tones(ch, p('F3'), p('E4'))[-1]
                for h in range(st, en, 8):
                    P['horn'].append([t0 + h * S, t0 + min(en, h + 8) * S - 8, n, 88])
        # koor: luchtige pad (in de werveling hoger en voller); in a2/a3/B speelt de hoorn de tweede stem
        for st, en, ch in (sg if var == 'a1' else []):
            for n in tones(ch, 57, 69)[1:3 if sec == 'B' else 2] if sec != 'S' else tones(ch, 62, 74)[:1]:
                for h in range(st, en, 8):
                    P['pad'].append([t0 + h * S, t0 + min(en, h + 8) * S - 8, n, 60 if sec == 'A' else 70])
        # pauken op de grondtoon (frase-begin) + roffel naar de volgende frase
        if i % 2 == 0:
            P['timp'].append([t0, t0 + 2 * S, near(root, 38) + (12 if near(root, 38) < p('F2') else 0), 108])
        if i in (3, 7) and sec != 'S' or (sec == 'S' and i == 3):
            P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('A2'), 64 + 5 * (k - 8)] for k in range(8, 16)]
        # drums: kick 1 + 3 (+ 'en' van 3), snare 2 + 4, hihat in achtsten, conga's in B/S/A3
        P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, KICK, 110] for k in ((0, 8) if sec != 'S' else (0, 4, 8, 12))]
        if var in ('a2', 'a3') or sec == 'B':
            P['drums'].append([t0 + 10 * S, t0 + 12 * S, KICK, 96])
        P['drums'] += [[t0 + k * S, t0 + k * S + 3 * S, SNARE, 96 if sec != 'B' else 90] for k in (4, 12)]
        P['hats'] += [[t0 + k * S, t0 + k * S + S, HH, 70 if k % 4 == 0 else 54] for k in range(0, 16, 2)]
        if sec in ('B', 'S') or var == 'a3':
            P['hats'] += [[t0 + k * S, t0 + k * S + 2 * S, CONGA_H if k in (3, 11) else CONGA_L, 70] for k in (3, 7, 11, 14)]
        if i % 4 == 0:
            P['drums'].append([t0, t0 + 2 * TPB, CRASH, 108])
        if (sec == 'A' and i == 7) or (sec == 'B' and i == 7) or (sec == 'S' and i == 3):
            P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, (SNARE, SNARE, TOM_X, TOM_H, TOM_M, TOM_M, TOM_L, TOM_L)[k - 8], 80 + 4 * (k - 8)]
                           for k in range(8, 16)]
        elif sec == 'A' and i == 3:
            P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, SNARE, 70 + 6 * (k - 12)] for k in range(12, 16)]
        # windstoten (Jordi: 'de tornado's wel tof')
        if i == 7 or (sec == 'B' and i % 2 == 1) or sec == 'S':
            ln = 8 * S if sec != 'S' else BAR - S
            gust(P, CC, EX, 'gust', t0 + (BAR - ln - S if sec != 'S' else 0), ln, 60 + 4 * (i % 3), 96, seed=b)
    sec_of = lambda t: next(((sec, i, b * BAR) for b, sec, i, var in tl if b * BAR <= t < (b + 1) * BAR))
    loopmel = [x for x in P['lead'] if x[0] >= 12 * BAR and not (32 * BAR <= x[0] < 36 * BAR)]
    P['horn'] += harmony_below([[s, e, n - 12, int(v * 0.82)] for s, e, n, v in loopmel], sec_of)
    P['lead_s'] = [[s, e, n, int(v * 0.86)] for s, e, n, v in P['lead']]
    P['runs'] = [[s, e, n, min(127, int(v * 1.3))] for s, e, n, v in P['runs']]   # werveling hoorbaar (solo: -13 dB t.o.v. lead)
    return dict(parts=P, cc=CC, ex=EX, end=len(tl) * BAR, loop=4, bpm=176, shift=2,
                order=['lead', 'lead_s', 'drums', 'hats', 'bass', 'runs', 'horn', 'timp', 'pad'],
                detach=('lead', 'lead_s', 'horn', 'pad'),
                layout=[('lead', TPT, 102, 0, 64), ('lead_s', STR, 88, 1, 52), ('runs', SPICC, 127, 2, 34),
                        ('horn', HORN, 76, 3, 92), ('pad', CHOIR, 64, 4, 80), ('bass', FBASS, 106, 5, 64),
                        ('timp', TROLL, 96, 6, 60), ('wave', WAVE, 46, 7, 64), ('gust', GUST, 60, 8, 64)],
                drums=("drums", "hats"), drumvol=127)


# ---- Thundurus v2: bliksem --------------------------------------------------------------------------------------
# Jordi (v1): 'klinkt goed, maar ook als Shovel Knight of Megaman, kan je het een iets voller GBA-sound geven?'
# v2: compositie ongewijzigd; de gitaarlead krijgt strijkers unisono (i.p.v. een PSG-blokgolf), de PSG-arpeggio's en
# -snarecracks zijn weg (alleen de bliksemflitsen in intro/stormbreak blijven als effect), snare = rnd-snare +
# orkestsnare, bekkens, tuba onder de riff op de zware tellen, koor- en strijkerspads, steviger sub.
RIFF = [(0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)]          # 3+3+2 | 3+3+2


def thundurus():
    P, CC, EX = Parts(), Parts(), Parts()
    tl = timeline([('I', 4, ''), ('A', 8, 'a1'), ('A', 8, 'a2'), ('B', 8, ''), ('K', 4, '')])
    for b, sec, i, var in tl:
        t0 = b * BAR
        sg = segs(sec, i)
        if sec == 'I':
            if b == 0:      # donder: tomroffel + lage ruis + pauk
                P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, (TOM_L, TOM_L, TOM_M, TOM_L)[k % 4], 54 + 4 * k] for k in range(16)]
                gust(P, CC, EX, 'crack', t0, BAR, 40, 90, wobble=3)
                P['wave'] += [[t0, t0 + BAR - 8, p('D2'), 80]]
                P['bass'] += [[t0 + 8 * S, t0 + 16 * S - 8, p('D2'), 90]]
                P['pad'] += [[t0 + 8 * S, t0 + BAR - 8, n, 64] for n in (p('D4'), p('A4'))]
            if b == 1:      # BLIKSEM op tel 1, daarna stil (cry)
                P['drums'] += [[t0, t0 + 2 * TPB, CRASH, 124], [t0, t0 + 2 * S, KICK, 124], [t0, t0 + 2 * S, OSNARE, 120]]
                P['stabs'] += [[t0, t0 + 2 * S, n, 120] for n in (p('F4'), p('A4'))]
                P['tuba'] += [[t0, t0 + 6 * S, p('D3'), 116]]
                gust(P, CC, EX, 'crack', t0, TPB, 76, 120, down=True)
                P['zap'] += [[t0 + k * 12, t0 + k * 12 + 12, n, 80] for k, n in enumerate(tones('Dm', 62, 98)[::-1][:12])]
                P['bass'] += [[t0, t0 + 6 * S, p('D2'), 110]]
                P['wave'] += [[t0, t0 + BAR - 8, p('D2'), 80]]
                P['riff'] += [[t0 + k * S, t0 + k * S + S, p('D2') + 12, 60 + 3 * k] for k in (8, 10, 12, 14)]
            if b >= 2:      # riff valt in, opbouw
                ch = chord_at('I', b, 0)
                r = near(CH[ch][0], 38)
                P['riff'] += [[t0 + st * S, t0 + (st + ln) * S - 10, r + 12, 104] for st, ln in RIFF]
                P['bass'] += [[t0 + st * S, t0 + (st + ln) * S - 10, r, 108] for st, ln in RIFF]
                P['wave'] += [[t0, t0 + BAR - 8, r, 80]]
                P['drums'] += [[t0 + st * S, t0 + st * S + 2 * S, KICK, 110] for st, _ in RIFF]
                P['pad'] += [[t0, t0 + BAR - 8, n, 70] for n in tones(ch, 57, 69)[:2]]
                if b == 2:
                    P['hats'] += [[t0 + k * S, t0 + k * S + S, HH, 70] for k in range(0, 16, 2)]
                    P['stabs'] += [[t0 + k * S, t0 + k * S + S, n, 110] for k in (3, 6, 11, 14) for n in (p('F4'), p('A4'))]
                else:
                    P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, SNARE if k % 2 == 0 else OSNARE, 70 + 3 * k] for k in range(16)]
                    P['stabs'] += [[t0 + k * S, t0 + k * S + S, n, 116] for k in (0, 3, 6) for n in (p('E4'), p('A4'))]
                    P['zap'] += [[t0 + 8 * S + k * 12, t0 + 8 * S + k * 12 + 12, n, 70] for k, n in enumerate(tones('A', 57, 93)[:16])]
                    P['tuba'] += [[t0, t0 + 6 * S, p('A2') + 12, 108]]
            continue
        if sec == 'A':
            P['lead'] += mel('A', i, t0, 112, pat=push(MEL['A'][i]))
        elif sec == 'B':
            P['lead'] += mel('B', i, t0, 112, pat=push(MEL['B'][i]))
        # riff + bas + sub
        for st, en, ch in sg:
            r = near(CH[ch][0], 38)
            if sec == 'B' and i < 6:     # half-time
                pat = [(0, 6), (8, 6)]
            else:
                pat = RIFF
            for k, ln in pat:
                if st <= k < en:
                    P['riff'].append([t0 + k * S, t0 + (k + ln) * S - 10, r + 12, 108 if k in (0, 8) else 96])
                    P['bass'].append([t0 + k * S, t0 + (k + ln) * S - 10, r, 112 if k in (0, 8) else 100])
            P['wave'].append([t0 + st * S, t0 + en * S - 8, r, 84])
            # tuba (koper, >= C3) op de zware tellen: geeft de riff gewicht
            if var == 'a2' or sec in ('B', 'K'):
                for k in (0, 8):
                    if st <= k < en:
                        P['tuba'].append([t0 + k * S, t0 + (k + 3) * S - 10, near(CH[ch][0], 50), 104])
        # koperstoten (off-beat, gesyncopeerd)
        if var == 'a2' or sec in ('B', 'K'):
            hits = (2, 5, 10, 13) if sec != 'K' else (0, 3, 6, 8, 11, 14)
            if sec == 'B' and i % 2 == 0:
                hits = (6, 14)
            for k in hits:
                ch = chord_at(sec, i, k)
                for n in tones(ch, 62, 72)[:2]:
                    P['stabs'].append([t0 + k * S, t0 + k * S + S, n, 118 if sec == 'K' else 108])
        # pads: strijkers in a1 (zacht), koor in a2/K, orgel in de brug
        for st, en, ch in sg:
            if sec == 'B':
                for n in tones(ch, 50, 62)[1:2]:
                    for h in range(st, en, 8):
                        P['organ'].append([t0 + h * S, t0 + min(en, h + 8) * S - 8, n + 12, 70])
            for n in (tones(ch, 57, 69)[:2] if var == 'a1' else tones(ch, 57, 69)[1:2]) if sec != 'B' else []:
                for h in range(st, en, 8):
                    P['pad'].append([t0 + h * S, t0 + min(en, h + 8) * S - 8, n, 66 if var == 'a1' else 78])
        # drums: snare-zwaar, echte snare (rnd + orkest)
        half = sec == 'B' and i < 6
        if half:
            kicks, snares = (0, 3, 10), (8,)
        else:
            kicks, snares = (0, 3, 6, 10), (4, 12)
        P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, KICK, 118] for k in kicks]
        P['drums'] += [[t0 + k * S, t0 + k * S + 3 * S, SNARE, 122] for k in snares]
        P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, OSNARE, 96] for k in snares]
        P['hats'] += [[t0 + k * S, t0 + k * S + S, HH, 76 if k % 4 == 0 else 58] for k in range(0, 16, 2)]
        if var == 'a2' or sec == 'K':
            P['hats'] += [[t0 + k * S, t0 + k * S + S, TAMB, 58] for k in (4, 12)]
        if i % 4 == 0:
            P['drums'].append([t0, t0 + 2 * TPB, CRASH, 112])
            gust(P, CC, EX, 'crack', t0, TPB, 76, 100, down=True)
        if (sec == 'A' and i == 7) or (sec == 'B' and i in (6, 7)) or (sec == 'K' and i == 3):
            if sec == 'K' or (sec == 'B' and i == 7):
                fill = [(k, (TOM_X, TOM_H, TOM_M, TOM_L)[(k - 8) // 2]) for k in range(8, 16)]
                P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, n, 100 + k] for k, n in fill]
            else:
                P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, SNARE, 76 + 4 * (k - 8)] for k in range(8, 16)]
        if sec == 'K':    # stormbreak: bliksem op tel 1 van maat 1 en 3
            if i in (0, 2):
                P['drums'].append([t0, t0 + 2 * TPB, CRASH, 124])
            P['zap'] += [[t0 + 12 * S + k * 12, t0 + 12 * S + k * 12 + 12, n, 74]
                         for k, n in enumerate(tones(chord_at('K', i, 12), 62, 98)[::-1][:8])]
            if i == 3:     # de lead schreeuwt omhoog naar de loop
                P['lead'] += [[t0, t0 + 8 * S, p('E5'), 112], [t0 + 8 * S, t0 + 16 * S - 8, p('A5'), 116]]
    # strijkers unisono met de gitaarlead (a2, B, K; in a1 alleen de tweede helft) = voller dan de PSG-blokgolf
    P['lead_s'] = [[s, e, n, 96] for s, e, n, v in P['lead'] if s >= 8 * BAR]
    return dict(parts=P, cc=CC, ex=EX, end=len(tl) * BAR, loop=4, bpm=152, shift=-2,
                order=['lead', 'drums', 'lead_s', 'bass', 'riff', 'stabs', 'hats', 'tuba', 'pad', 'organ'],
                detach=('lead', 'lead_s', 'pad', 'organ', 'tuba'),
                layout=[('lead', DIST_HI, 94, 0, 64), ('lead_s', STR, 80, 1, 46), ('riff', DIST_LO, 84, 2, 40),
                        ('stabs', TPT, 92, 3, 88), ('bass', SBASS, 110, 4, 64), ('tuba', TUBA, 84, 5, 72),
                        ('pad', CHOIR, 66, 6, 84), ('organ', ORGAN, 58, 7, 64), ('zap', SQ_ARP, 26, 8, 96),
                        ('wave', WAVE, 64, 10, 64), ('crack', GUST, 70, 11, 64)],
                drums=("drums", "hats"), drumvol=127)


# ---- Landorus v2: aarde -----------------------------------------------------------------------------------------
# Jordi (v1): 'te saai, gebeurt te weinig, daar mag meer epische instrumentatie in, klinkt meer als een aankondiging
# van een gevecht dan echt een battle theme'. v2: 132 bpm (was 112), echte battle-groove: drumstel (kick/snare/hihat)
# + taiko, strijkersostinato in 16en, bas in springende achtsten, tuba; hoorns met het motief, trompetten erbij,
# een tegenmelodie in de strijkers, koor, paukenroffels, bekkens, tomfills; B = momentum (vraag-antwoord hoorns <->
# trompetten, dubbel tempo in de drums, crescendo); C (D-groot) = de climax van het gevecht, niet een fanfare:
# de groove loopt door, trompetten + hoorn-tegenstem + koor + buisklokken.
def landorus():
    P, CC, EX = Parts(), Parts(), Parts()
    tl = timeline([('I', 4, ''), ('A', 8, 'a1'), ('A', 8, 'a2'), ('B', 8, ''), ('C', 8, '')])
    for b, sec, i, var in tl:
        t0 = b * BAR
        sg = segs(sec, i)
        if sec == 'I':
            if b == 0:      # aardrommel: paukenroffel, taiko, lage ruis, bas-pedaal
                P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('D2') + 12, 44 + 4 * k] for k in range(16)]
                P['taiko'] += [[t0 + k * S, t0 + k * S + TPB, TAIKO_KEY, 110 - 2 * k] for k in (0, 6, 12)]
                gust(P, CC, EX, 'rumble', t0, 2 * BAR - S, 36, 80, wobble=2)
                P['choir'] += [[t0, t0 + BAR - 8, p('D4'), 70]]
            if b in (0, 1):
                P['bass'].append([t0, t0 + BAR - 8, p('D2'), 96])
                P['wave'].append([t0, t0 + BAR - 8, p('D2'), 80])
            if b == 1:      # ostinato valt in, drums beginnen te stampen
                ostinato16(P, 'strings', t0, 0, 16, 2, 50, 64)
                P['taiko'] += [[t0 + k * S, t0 + k * S + TPB, TAIKO_KEY, 104] for k in (0, 6, 8, 14)]
                P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, KICK, 100] for k in (0, 6, 8, 14)]
                P['choir'] += [[t0, t0 + BAR - 8, n, 76] for n in (p('D4'), p('A4'))]
            if b == 2:      # de hoornroep: de kop van het motief, groove loopt
                P['horn'] += mel('A', 0, t0, 116, shift=-12)
                P['tuba'] += [[t0, t0 + 8 * S - 8, p('D3'), 100], [t0 + 8 * S, t0 + 16 * S - 8, p('A3'), 100]]
                P['timp'] += [[t0, t0 + 2 * S, p('D2') + 12, 120], [t0 + 8 * S, t0 + 10 * S, p('A2'), 110]]
                ostinato16(P, 'strings', t0, 0, 16, 2, 50, 74)
                P['bass'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, p('D2') + (12 if k in (2, 6) else 0), 104] for k in range(8)]
                P['wave'].append([t0, t0 + BAR - 8, p('D2'), 80])
                P['drums'] += [[t0, t0 + 2 * TPB, CRASH, 110]]
                P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, KICK, 108] for k in (0, 6, 8, 14)]
                P['drums'] += [[t0 + k * S, t0 + k * S + 3 * S, SNARE, 104] for k in (4, 12)]
                P['taiko'] += [[t0 + k * S, t0 + k * S + TPB, TAIKO_KEY, 110] for k in (0, 8)]
            if b == 3:      # dominant: hoorn houdt A, trompetten antwoorden, roffels, crash op de loop
                P['horn'] += [[t0, t0 + 12 * S, p('A4'), 118], [t0 + 12 * S, t0 + 14 * S, p('G4'), 110],
                              [t0 + 14 * S, t0 + 16 * S, p('E4'), 112]]
                P['tpt'] += [[t0 + 4 * S, t0 + 6 * S, p('C#5'), 104], [t0 + 6 * S, t0 + 8 * S, p('E5'), 108],
                             [t0 + 8 * S, t0 + 12 * S, p('A5'), 114]]
                P['tuba'] += [[t0, t0 + 16 * S - 8, p('A3'), 104]]
                P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('A2'), 64 + 4 * k] for k in range(16)]
                P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, OSNARE, 64 + 4 * k] for k in range(8)]
                P['drums'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, (TOM_X, TOM_X, TOM_H, TOM_H, TOM_M, TOM_M, TOM_L, TOM_L)[k], 96 + 3 * k]
                               for k in range(8)]
                P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, KICK, 110] for k in (0, 4, 8, 12)]
                ostinato16(P, 'strings', t0, 0, 16, 9, 45, 80, pat=(0, 0, 7, 0, 12, 0, 7, 0))
                P['bass'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, near(9, 38) + (12 if k % 2 else 0), 104] for k in range(8)]
                P['wave'].append([t0, t0 + BAR - 8, p('A2'), 80])
                P['choir'] += [[t0, t0 + BAR - 8, n, 84] for n in (p('C#4'), p('E4'))]
                gust(P, CC, EX, 'rumble', t0 + 8 * S, 8 * S, 40, 100, wobble=2)
            continue
        # ---- melodie --------------------------------------------------------------------------------------------
        if sec == 'A':
            if var == 'a1':
                P['horn'] += mel('A', i, t0, 116, shift=-12)
            else:
                P['tpt'] += mel('A', i, t0, 112)
                P['horn'] += mel('A', i, t0, 108, shift=-12)
        elif sec == 'B':
            # vraag-antwoord: hoorns spelen de sequens, trompetten antwoorden in de lange noten met een gestoten kop
            P['horn'] += mel('B', i, t0, 116, shift=-12)
            if i in (3, 7):
                ch = chord_at('B', i, 0)
                ts = tones(ch, p('A4'), p('A5'))
                P['tpt'] += [[t0 + k * S, t0 + k * S + S + 4, ts[(k - 8) // 2 % len(ts)], 104 + k] for k in (8, 10, 12, 14)]
            elif i % 2 == 1:
                P['tpt'] += [[t0 + 12 * S, t0 + 13 * S, p('A5'), 106], [t0 + 13 * S, t0 + 14 * S, p('A5'), 100],
                             [t0 + 14 * S, t0 + 16 * S - 4, p('D6') if i != 5 else p('C#6'), 112]]
            if i >= 4:
                P['tpt'] += mel('B', i, t0, 104)
        elif sec == 'C':
            P['tpt'] += mel('C', i, t0, 120)
        for st, en, ch in sg:
            r = CH[ch][0]
            # bas: springende achtsten (grondtoon, octaaf, kwint)
            pat = (0, 0, 12, 0, 7, 0, 12, 10) if sec != 'C' else (0, 12, 0, 12, 7, 12, 0, 12)
            for k in range(st, en, 2):
                iv = pat[(k // 2) % 8]
                if iv == 10 and CH[ch][1][1] - r not in (3, -9):
                    iv = 7
                P['bass'].append([t0 + k * S, t0 + k * S + 2 * S - 8, near(r, 38) + iv, 108 if k % 8 == 0 else 96])
            P['wave'].append([t0 + st * S, t0 + en * S - 8, near(r, 38), 80])
            # tuba: halve noten op de grondtoon (a2, B, C)
            if sec == 'B':
                P['tuba'] += [[t0 + h * S, t0 + min(en, h + 8) * S - 8, near(r, 48), 100] for h in range(st, en, 8)]
            # pauken: grondtoon op 1, kwint op 3
            P['timp'].append([t0 + st * S, t0 + st * S + 2 * S, near(r, 38) + (12 if near(r, 38) < p('F2') else 0), 118])
            if en - st > 8:
                q = near((r + 7) % 12, 38)
                P['timp'].append([t0 + (st + 8) * S, t0 + (st + 10) * S, q + (12 if q < p('F2') else 0), 104])
            # strijkersostinato in 16en, altijd (B 1-4 in de lage ligging, daarna hoger = opbouw)
            lo = 50 if (sec == "B" and i < 4) else 57
            ostinato16(P, 'strings', t0, st, en, r, lo, 88 if sec != "C" else 96)
            # koor: a1 één stem, a2/B twee, C drie (de climax)
            n_ch = {'A': 1 if var == 'a1' else 0, 'B': 1, 'C': 2}[sec]
            for n in tones(ch, 57, 72)[-n_ch:] if n_ch else []:
                for h in range(st, en, 8):
                    P['choir'].append([t0 + h * S, t0 + min(en, h + 8) * S - 8, n, 72 if sec == 'A' else 84])
            # buisklokken: de oogst, op elke maat van C
            if sec == 'C' and st == 0 and i % 2 == 1:
                P['bell'].append([t0, t0 + 6 * S, near(r, 74), 94])
        # drums: battle-groove. kick 1, 2-en, 3 (+ 4-en), snare 2 + 4, hihat in achtsten (a2/B/C), taiko op 1 + 3
        if sec == 'B' and i >= 4:          # dubbel tempo, crescendo naar C
            kicks, snares = (0, 3, 6, 8, 11, 14), ((4, 12) if i < 6 else (2, 4, 6, 10, 12, 14))
        else:
            kicks, snares = ((6,) if var == 'a1' else (6, 14)), (4, 12)
        if sec == 'B' and i >= 4:
            kicks = tuple(k for k in kicks if k not in (0, 8))     # taiko draagt 1 en 3
        P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, KICK, 116 if k in (0, 8) else 104] for k in kicks]
        P['drums'] += [[t0 + k * S, t0 + k * S + 3 * S, SNARE, 112 if k in (4, 12) else 88 + 2 * i] for k in snares]
        if var == 'a2' or sec in ('B', 'C'):
            P['hats'] += [[t0 + k * S, t0 + k * S + S, HH, 72 if k % 4 == 0 else 56] for k in range(0, 16, 2)]
        tk = (0, 8) if sec != 'C' else (0, 6, 8, 14)
        P['taiko'] += [[t0 + k * S, t0 + k * S + TPB, TAIKO_KEY, 116 if k in (0, 8) else 100] for k in tk]
        if i % 4 == 0 or (sec in ('B', 'C') and i % 2 == 0):
            P['drums'].append([t0, t0 + 2 * TPB, CRASH, 116 if sec == 'C' else 104])
        # fills en paukenroffels aan het eind van elke frase
        if i in (3, 7):
            if i == 7:
                P['drums'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, (OSNARE, OSNARE, TOM_X, TOM_H, TOM_M, TOM_M, TOM_L, TOM_L)[k], 92 + 4 * k]
                               for k in range(8)]
                P['timp'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, p('A2'), 70 + 6 * k] for k in range(8)]
            else:
                P['drums'] += [[t0 + (12 + k) * S, t0 + (13 + k) * S, (TOM_H, TOM_M, TOM_L, TOM_L)[k], 96 + 4 * k] for k in range(4)]
        if sec == 'B' and i == 7:
            gust(P, CC, EX, 'rumble', t0, BAR - S, 38, 110, wobble=2)
    # tegenmelodie in de (legato) strijkers boven de melodie: a2 en C
    P['counter'] = counter_line(tl, (('A', 'a2'),), p('A5'), p('F6'), 88)
    P['horn'] += counter_line(tl, ('C',), p('D4'), p('A4'), 112, unit=4)     # C: hoorns als tegenstem in kwarten
    return dict(parts=P, cc=CC, ex=EX, end=len(tl) * BAR, loop=4, bpm=132, shift=0,
                order=['horn', 'tpt', 'drums', 'hats', 'bass', 'strings', 'timp', 'taiko', 'counter', 'choir', 'bell', 'tuba'],
                detach=('horn', 'tpt', 'tuba', 'choir', 'counter'),
                layout=[('horn', HORN, 94, 0, 58), ("tpt", TPT, 88, 1, 72), ('tuba', TUBA, 86, 2, 52),
                        ('bass', FBASS, 108, 3, 64), ('timp', TROLL, 102, 4, 64), ('taiko', TAIKO, 112, 5, 64),
                        ('strings', SPICC, 127, 6, 36), ('counter', STR, 80, 7, 92), ('choir', CHOIR, 72, 8, 80),
                        ('bell', BELL, 64, 10, 84), ('wave', WAVE, 52, 11, 64), ('rumble', GUST, 60, 12, 64)],
                drums=("drums", "hats"), drumvol=127)


THEMES = {'tornadus': tornadus, 'thundurus': thundurus, 'landorus': landorus}
NOSHIFT = {'drums', 'hats', 'gust', 'crack', 'cracks', 'rumble', 'taiko'}


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor Battle! Tornadus/Thundurus/Landorus (Forces of Nature).'
    lines[1] = '@ Gegenereerd door tools/grounded/forces_theme.py. Alleen Emerald-samples.'
    lines[2] = 'voice_group %s' % VG
    over = {
        14: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_tubular_bell, 255, 165, 51, 200',
        29: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_low, 255, 0, 255, 120',
        30: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_high, 255, 0, 255, 165',
        47: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200',
        45: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 90',
        49: 'voice_keysplit voicegroup_forces_spicc_keysplit, keysplit_strings',
        80: 'voice_square_1 60, 0, 0, 1, 0, 2, 6, 1',
        81: 'voice_square_2 60, 0, 1, 0, 0, 15, 1',
        82: 'voice_square_2 60, 0, 0, 0, 2, 8, 1',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
        121: 'voice_noise_alt 60, 0, 0, 0, 0, 15, 2',
        122: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    }
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/keysplits/forces_spicc.inc', 'w').write(
        '@ Project Grounded: spiccato-strijkers (harde aanzet, kort) voor Battle! Forces of Nature (forces_theme.py).\n'
        'voice_group forces_spicc_keysplit\n' +
        ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 255, 0, 255, 110\n' % k
                for k in (60, 72, 84)))


def build(name, refdir=None):
    th = THEMES[name]()
    P, bpm = th['parts'], th['bpm']
    for k in list(P):
        if k not in NOSHIFT:
            P[k] = [[s, e, n + th['shift'], v] for s, e, n, v in P[k]]
        P[k] = dedupe(P[k])
    progs = {k: pr for k, pr, *_ in th['layout']}
    rel = releases(VG)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, bpm) + 2 for k, pr in progs.items()}
    for k, pr in progs.items():           # elke DS-partij: noot + uitklinktijd eindigt vóór de volgende aanslag
        if rel.get(pr) is not None:
            P[k] = detach(P[k], tail[k])
    for k, pr in progs.items():            # octaafcorrectie voor samples die lager klinken dan geschreven
        if pr in OCT_DOWN:
            P[k] = [[s, e, n + OCT_DOWN[pr], v] for s, e, n, v in P[k]]
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            low = [n for _, _, n, _ in P[k] if n < 28]
            assert not low, '%s %s: noten onder E1' % (name, k)
            if pr in (TPT, HORN, TUBA):
                assert all(n >= 48 for _, _, n, _ in P[k]), '%s %s: koper onder C3' % (name, k)
    order = th['order']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAXV)
    for k in order:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            print('  %s %s: %d van %d noten vallen weg (%.1f%%)' % (name, k, n - len(kept[k]), n, 100 * (n - len(kept[k])) / n))
            if os.environ.get('FORCES_DEBUG'):
                kk = {tuple(e) for e in kept[k]}
                print('     weg op maat:', [round(e[0] / BAR, 2) for e in ds[k] if tuple(e) not in kk])
                for e in [e for e in ds[k] if tuple(e) not in kk][:3]:
                    busy = {}
                    for q in order:
                        for x in kept[q]:
                            if x[0] <= e[0] < x[1] + tail.get(q, 0):
                                busy[q] = busy.get(q, 0) + 1
                    print('       %.2f bezet:' % (e[0] / BAR), busy)
        P[k] = kept[k]
    lp = th['loop'] * BAR
    for ref in (False, True):
        if ref and not refdir:
            continue
        song = Song(TPB, 500000)
        song.tempo(0, bpm / 120)
        song.loop = (lp, th['end'])
        for k, pr, vol, ch, pan in th['layout']:
            notes = P[k]
            if ref and pr in OCT_DOWN:
                notes = [[s, e, n - OCT_DOWN[pr], v] for s, e, n, v in notes]
            ccs = list(th['cc'].get(k, []))
            ex = list(th['ex'].get(k, []))
            if ex:
                ccs = [(0, 20, 12)] + ccs
            song.add(notes, pr if not ref else min(pr, 126), vol, ch, pan, extra=ex, ccs=ccs)
        song.add(sorted(sum((P[k] for k in th['drums']), [])), KIT, th.get("drumvol", 108), 9)
        written = {k for k, *_ in th['layout']} | set(th['drums'])
        assert not [k for k in P if P[k] and k not in written], '%s: partij niet weggeschreven %s' % (
            name, [k for k in P if P[k] and k not in written])
        out = os.path.join(refdir, 'forces_%s_ref.mid' % name) if ref else \
            'sound/songs/midi/mus_grounded_vs_%s.mid' % name
        song.save(out, th['end'])
        print(out, '| loop %.1f s' % ((th['end'] - lp) / TPB * 60 / bpm), '| totaal %.1f s' % (th['end'] / TPB * 60 / bpm))


if __name__ == '__main__':
    ref = sys.argv[sys.argv.index('--ref') + 1] if '--ref' in sys.argv else None
    voicegroup()
    for n in THEMES:
        build(n, ref)
