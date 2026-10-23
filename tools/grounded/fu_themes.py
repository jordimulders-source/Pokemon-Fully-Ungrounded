#!/usr/bin/env python3
"""Fully Ungrounded: de eerste originele schetsen op de gedeelde instrumentenset (fu_samples.py, voicegroup `fu`).

Jordi (22 okt): geen nummers namaken, alles origineel in Zuid-/Latijns-Amerikaanse stijlen, één gedeelde set
instrumenten. Dit script maakt zes MIDI's (elk loopbaar, met loopmarkers):
  611 MUS_FU_DEMO       instrumentendemo: elk instrument los (zie docs/concept/muziek/previews/README.md)
  612 MUS_FU_ALTIPLANO  route op de altiplano: huayno (zampoña in kwarten, quena, charango-rasgueo, bombo), wind
  613 MUS_FU_VS_WILD    wild gevecht in de Andes: snel, hook op quena, fanfare-B (diablada), zampoña-hoquetus
  614 MUS_FU_LA_PAZ     La Paz: caporales/saya-fanfare (trompet, trombones, tuba, bombo, caixa) + teleférico-B
  615 MUS_FU_BENDE      reggaeton-bende: dembow, 808 met slides, supersaw-stabs, zampoña-hook, nylon-ostinato
  616 MUS_FU_SAMBA      samba/batucada: surdo, caixa, tamborim, agogô, cuíca, apito, cavaquinho, flauta + trompet
Gebruik: python3 tools/grounded/fu_themes.py [naam ...]   (namen: demo altiplano wild lapaz bende samba)"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

VG = 'fu'
TPB = 48
S = TPB // 4                   # een 16e
BAR = TPB * 4
MID = 'sound/songs/midi/'

NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def p(name):
    """'A4', 'C#5', 'Bb3' -> midi-noot (C4 = 60)."""
    n = NOTE[name[0]]
    rest = name[1:]
    while rest and rest[0] in '#b':
        n += 1 if rest[0] == '#' else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + n


# drumkit (sound/voicegroups/drumsets/fu.inc)
KICK, SNARE, CLAP, BOMBO, ARO, CAJ_B, CAJ_S, BONGO_H, BONGO_L, CONGA_S, CONGA_O, TUMBA, GUIRO_L, GUIRO_S, SHAKER, \
    CLAVES, COWBELL, CRASH, CAIXA, HH_C, HH_O, SURDO_L, SURDO_H, TAMBORIM, AGOGO_H, AGOGO_L, APITO = range(36, 63)

CHORD = {   # naam -> (grondtoon-pc, akkoordtonen-pc)
    'Am': (9, (9, 0, 4)), 'C': (0, (0, 4, 7)), 'G': (7, (7, 11, 2)), 'Em': (4, (4, 7, 11)), 'E': (4, (4, 8, 11)),
    'F': (5, (5, 9, 0)), 'D': (2, (2, 6, 9)), 'B7': (11, (11, 3, 6, 9)), 'Dm': (2, (2, 5, 9)), 'Bb': (10, (10, 2, 5)),
    'Gm': (7, (7, 10, 2)), 'A': (9, (9, 1, 4)), 'E7': (4, (4, 8, 11, 2)), 'D7': (2, (2, 6, 9, 0)), 'A7': (9, (9, 1, 4, 7)),
}


def place(pc, lo):
    """Toonhoogteklasse pc op de eerste noot >= lo."""
    n = lo + (pc - lo) % 12
    return n


class Arr:
    """Een arrangement: partijen met noten [start, eind, noot, vel] in ticks, plus extra MIDI-events en CC's."""

    def __init__(self, name, bpm, tracks):
        self.name, self.bpm, self.tracks = name, bpm, tracks       # tracks: [(naam, programma, vol, pan, soort)]
        self.parts = {t[0]: [] for t in tracks}
        self.extra = {t[0]: [] for t in tracks}
        self.ccs = {t[0]: [] for t in tracks}
        self.kind = {t[0]: t[4] for t in tracks}
        self.prog = {t[0]: t[1] for t in tracks}

    @staticmethod
    def t(bar, pos):
        return int(round(bar * BAR + pos * S))

    def n(self, part, bar, pos, ln, note, vel):
        s, e = self.t(bar, pos), self.t(bar, pos + ln)
        ev = [s, max(s + 2, e), note, max(1, min(127, int(vel)))]
        self.parts[part].append(ev)
        return ev

    def line(self, part, bar, text, vel=100, shift=0, legato=0.88, accent=8):
        """'E5:2 D5:1 r:2 ...' (lengtes in 16en) vanaf maat `bar`; loopt door over maatgrenzen. Korte noten
        staccato, lange legato; accent op de tel."""
        pos, out = 0.0, []
        for tok in text.split():
            nm, d = tok.split(':')
            d = float(d)
            if nm != 'r':
                ln = d * legato if d >= 2 else min(d, 0.75)
                v = vel + (accent if pos % 4 == 0 else 0)
                out.append(self.n(part, bar, pos, ln, p(nm) + shift, v))
            pos += d
        return out

    def copy_to(self, part, notes, shift=0, vel=0):
        out = []
        for s, e, n, v in notes:
            ev = [s, e, n + shift, max(1, min(127, v + vel))]
            self.parts[part].append(ev)
            out.append(ev)
        return out

    def cc(self, part, tick, ctrl, val):
        self.ccs[part].append((tick, ctrl, val))

    def vibrato(self, part, depth=30, speed=44, min_len=5, delay=3):
        """Vibrato (CC1, MOD) op lange noten van een partij, na een korte aanzet; terug op 0 bij de volgende noot."""
        ev = [(0, mido.Message('control_change', control=21, value=speed)),
              (0, mido.Message('control_change', control=1, value=0))]
        notes = sorted(self.parts[part])
        for i, (s, e, n, v) in enumerate(notes):
            if e - s >= min_len * S:
                nxt = notes[i + 1][0] if i + 1 < len(notes) else e + TPB
                ev.append((s + delay * S, mido.Message('control_change', control=1, value=depth)))
                ev.append((nxt, mido.Message('control_change', control=1, value=0)))
        self.extra[part] += ev

    def bends(self, part, items, rng=12):
        """Pitch bends: items = [(start_tick, eind_tick, halve tonen, stappen)], terug naar 0 op `reset`."""
        ev = [(0, mido.Message('control_change', control=20, value=rng)), (0, mido.Message('pitchwheel', pitch=0))]
        for s, e, semis, steps, reset in items:
            for k in range(1, steps + 1):
                val = int(round(8191 * semis / rng * k / steps)) if semis > 0 else int(round(8192 * semis / rng * k / steps))
                ev.append((s + (e - s) * k // steps, mido.Message('pitchwheel', pitch=max(-8192, min(8191, val)))))
            ev.append((reset, mido.Message('pitchwheel', pitch=0)))
        self.extra[part] += ev

    def build(self, loop, end, order, mixvol=None):
        rel = releases(VG)
        tail = {}
        for name, prog, vol, pan, kind in self.tracks:
            if kind == 'ds':
                r = rel.get(prog)
                tail[name] = release_ticks(r if r is not None else 200, TPB, self.bpm)
            elif kind == 'drum':
                tail[name] = 3
        for k in self.parts:
            self.parts[k] = dedupe(self.parts[k])
        for name, prog, vol, pan, kind in self.tracks:
            if kind == 'ds':
                self.parts[name] = detach(self.parts[name], tail[name])
        ds = {k: self.parts[k] for k in order}
        missing = [t[0] for t in self.tracks if t[4] in ('ds', 'drum') and t[0] not in order and self.parts[t[0]]]
        assert not missing, 'niet in de stemverdeler: %s' % missing
        kept = allocate(ds, order, tail)
        print('%s: %d sporen, %.1f s intro, %.1f s loop' % (self.name, len(self.tracks), loop * 240 / self.bpm,
                                                              (end - loop) * 240 / self.bpm))
        for k in order:
            n = len(ds[k])
            gone = sorted({e[0] // BAR for e in ds[k] if e not in kept[k]})
            if n:
                print('  %-8s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / n,
                                                                     ' maten %s' % gone[:12] if gone else ''))
            self.parts[k] = kept[k]
        song = Song(TPB, 500000)
        song.tempo(0, self.bpm / 120)
        song.loop = (loop * BAR, end * BAR)
        assert len(self.tracks) <= 16
        for ch, (name, prog, vol, pan, kind) in enumerate(self.tracks):
            ccs = sorted(self.ccs[name], key=lambda c: (c[0], str(c[1])))
            song.add(self.parts[name], prog, vol, ch, pan, extra=self.extra[name], ccs=ccs)
        path = MID + 'mus_fu_%s.mid' % self.name
        song.save(path, end * BAR)
        print('  ->', path)


def drums(a, part, bar, pattern, note, vel=100, ln=0.75):
    """pattern = posities (16en) of [(pos, vel)]."""
    for x in pattern:
        pos, v = (x, vel) if not isinstance(x, tuple) else x
        a.n(part, bar, pos, ln, note, v)


def strum(a, part, bar, chord, pattern, lo=57, shift=0):
    """Rasgueo met de kwintakkoord-sample: één noot per slag, grondtoon tussen lo en lo+11."""
    root = place(CHORD[chord][0], lo) + shift
    for pos, ln, v in pattern:
        a.n(part, bar, pos, ln, root, v)


# ======================================================================================================================
# 611: instrumentendemo
# ======================================================================================================================
def demo():
    """Elk instrument los, in een vaste volgorde; de tijdstempels staan in de README (print)."""
    bpm = 150
    a = Arr('demo', bpm, [('mel', 73, 127, 64, 'ds'), ('chd', 26, 120, 64, 'ds'), ('dr', 127, 127, 64, 'drum'),
                          ('psg', 121, 70, 64, 'psg')])
    segs, bar = [], 0

    def seg(title, bars):
        nonlocal bar
        segs.append((bar, title))
        b = bar
        bar += bars
        return b

    def prog(part, b, pr):
        a.cc(part, a.t(b, 0), 'prog', pr)

    b = seg('quena (73)', 2); prog('mel', b, 73)
    a.line('mel', b, 'E5:4 G5:2 A5:2 C6:6 A5:2 G5:4 E5:2 D5:2 E5:8')
    b = seg('zampoña (75), daarna in kwarten', 2); prog('mel', b, 75); prog('chd', b, 75)
    m = a.line('mel', b, 'A4:2 C5:1 D5:1 E5:2 G5:1 E5:1 D5:2 C5:1 A4:1 G4:4 A4:4 C5:2 D5:2 E5:8')
    a.copy_to('chd', [e for e in m if e[0] >= a.t(b + 1, 0)], -5, -14)
    b = seg('charango, tokkel (25)', 2); prog('mel', b, 25)
    for k, nm in enumerate('E5 A5 C6 E6 D6 C6 A5 E5 G5 B5 D6 G6 E6 D6 B5 G5'.split()):
        a.n('mel', b, k * 2, 1.6, p(nm), 104)
    b = seg('charango, rasgueo (26, huayno)', 2); prog('chd', b, 26)
    for bb, ch in ((b, 'Am'), (b + 1, 'G')):
        strum(a, 'chd', bb, ch, [(q * 4 + o, l, v) for q in range(4) for o, l, v in ((0, 2, 112), (2, 1, 80), (3, 1, 92))])
    b = seg('nylongitaar (24)', 2); prog('mel', b, 24)
    for k, nm in enumerate('A2 E3 A3 C4 E4 C4 A3 E3 G2 D3 G3 B3 D4 B3 G3 D3'.split()):
        a.n('mel', b, k * 2, 3, p(nm), 104)
    b = seg('accordeon (21, cumbia)', 2); prog('mel', b, 21)
    a.line('mel', b, 'E5:1 r:1 E5:1 r:1 F5:2 E5:2 D5:2 C5:2 D5:4 B4:1 r:1 B4:1 r:1 C5:2 D5:2 E5:4 A4:4', vel=100)
    b = seg('trompet (56, vanilla)', 2); prog('mel', b, 56)
    a.line('mel', b, 'D5:3 D5:1 G5:4 B5:3 A5:1 G5:4 A5:3 B5:1 A5:2 F#5:2 D6:8')
    b = seg('trombone (57)', 2); prog('mel', b, 57)
    a.line('mel', b, 'G3:3 G3:1 B3:4 D4:3 C4:1 B3:4 C4:2 D4:2 E4:2 F#4:2 G4:8', vel=110)
    b = seg('tuba (58, vanilla)', 2); prog('mel', b, 58)
    a.line('mel', b, 'G2:4 D2:4 G2:4 D2:4 C2:4 G2:4 D2:4 D3:4', vel=112)
    b = seg('808-bas (38), met slide', 2); prog('mel', b, 38)
    a.line('mel', b, 'D2:5 r:1 D2:2 D2:3 F2:3 D2:2 Bb1:5 r:1 Bb1:2 Bb1:3 C2:3 A1:2', vel=118)
    a.bends('mel', [(a.t(b + 1, 14), a.t(b + 1, 15.5), 5, 6, a.t(b + 2, 0))], rng=12)
    b = seg('supersaw (81): stabs en lead', 2); prog('chd', b, 81)
    for pos in (3, 6, 11, 14):
        for nm in ('D4', 'F4', 'A4'):
            a.n('chd', b, pos, 1, p(nm), 96)
    a.line('chd', b + 1, 'A4:4 F4:2 E4:2 D4:6 r:2', vel=96)
    b = seg('cuíca (78)', 2); prog('mel', b, 78)
    cu = []
    for k, (pos, nm) in enumerate(((0, 'C5'), (3, 'C5'), (6, 'D5'), (8, 'C5'), (12, 'E5'), (16, 'C5'), (19, 'C5'),
                                   (22, 'G5'), (24, 'E5'))):
        e = a.n('mel', b, pos, 2, p(nm), 110)
        cu.append((e[0], e[0] + 2 * S, 3 if k % 2 == 0 else -2, 4, e[0] + 2 * S + 2))
    a.bends('mel', cu, rng=4)
    for title, hits in (
            ('bombo + aro (39/40)', [(0, BOMBO, 118), (2, ARO, 80), (3, BOMBO, 90), (4, BOMBO, 110), (6, ARO, 80),
                                      (8, BOMBO, 118), (10, ARO, 80), (11, BOMBO, 90), (12, BOMBO, 110), (14, ARO, 80)]),
            ('cajón (41/42)', [(0, CAJ_B, 118), (3, CAJ_S, 100), (6, CAJ_B, 100), (8, CAJ_S, 116), (10, CAJ_B, 90),
                               (12, CAJ_S, 70), (13, CAJ_S, 110), (15, CAJ_B, 80)]),
            ('bongó (43/44)', [(k, BONGO_H if k % 4 != 3 else BONGO_L, 110 if k % 2 == 0 else 70) for k in range(16)]),
            ('conga slap / open / tumba (45-47)', [(0, CONGA_S, 80), (2, CONGA_S, 112), (4, CONGA_S, 80),
                                                    (6, CONGA_O, 108), (7, CONGA_O, 104), (8, CONGA_S, 80),
                                                    (10, CONGA_S, 112), (12, CONGA_S, 80), (14, TUMBA, 110),
                                                    (15, TUMBA, 104)]),
            ('güiro (48/49) + shaker (50)', [(q * 4, GUIRO_L, 104) for q in range(2)] + [(q * 4 + 2, GUIRO_S, 90) for q in range(2)]
             + [(q * 4 + 3, GUIRO_S, 80) for q in range(2)] + [(8 + k, SHAKER, 110 if k % 2 == 0 else 72) for k in range(8)]),
            ('claves (51) + cowbell (52)', [(0, CLAVES, 110), (3, CLAVES, 110), (6, CLAVES, 110), (10, CLAVES, 110),
                                             (12, CLAVES, 110)] + [(k * 2 + 1, COWBELL, 96) for k in range(8)]),
            ('dembow: kick, snare, clap, hihat (36/37/38/55)',
             [(k, KICK, 120) for k in (0, 4, 8, 12)] + [(k, SNARE, 108) for k in (3, 6, 11, 14)]
             + [(k, CLAP, 100) for k in (6, 14)] + [(k, HH_C, 80) for k in (2, 10)]),
            ('surdo laag/hoog (57/58)', [(0, SURDO_H, 104), (4, SURDO_L, 124), (8, SURDO_H, 104), (11, SURDO_H, 80),
                                         (12, SURDO_L, 124)]),
            ('tamborim (59) + caixa (54)', [(k, TAMBORIM, 112) for k in (0, 2, 3, 5, 7)]
             + [(8 + k, CAIXA, (112, 50, 80, 96)[k % 4]) for k in range(8)]),
            ('agogô (60/61) + apito (62) + crash (53)', [(0, AGOGO_H, 110), (2, AGOGO_H, 100), (3, AGOGO_L, 100),
                                                          (5, AGOGO_H, 100), (6, AGOGO_L, 100), (8, APITO, 110),
                                                          (11, APITO, 100), (12, CRASH, 112)])):
        b = seg(title, 1)
        for pos, nt, v in hits:
            a.n('dr', b, pos, 2 if nt not in (SURDO_L, SURDO_H, BOMBO, CRASH) else 6, nt, v)
    end = bar + 1                                                   # een maat stilte, dan opnieuw
    a.build(0, end, ['mel', 'chd', 'dr'])
    print('  tijdstempels (s):')
    for b, title in segs:
        print('   %5.1f  %s' % (b * 240 / bpm, title))


# ======================================================================================================================
# 612: route op de altiplano (huayno)
# ======================================================================================================================
ALT_A = ['E5:2 D5:1 C5:1 A4:2 C5:1 D5:1 E5:3 G5:1 E5:2 D5:2',
         'C5:2 D5:1 C5:1 A4:2 G4:1 A4:1 C5:4 A4:4',
         'G5:2 E5:1 G5:1 A5:2 G5:1 E5:1 D5:2 E5:1 D5:1 C5:4',
         'D5:2 C5:1 D5:1 E5:2 D5:1 B4:1 G4:6 r:2',
         'E5:2 D5:1 C5:1 A4:2 C5:1 D5:1 E5:2 A5:2 G5:2 E5:2',
         'D5:2 E5:1 D5:1 B4:2 G4:1 B4:1 D5:2 B4:2 E5:4',
         'C5:2 B4:1 A4:1 G4:2 A4:1 B4:1 C5:2 B4:1 G4:1 E4:4',
         'G4:2 E4:1 G4:1 A4:8 r:4']
ALT_A_CH = ['Am', 'Am', 'C', 'G', 'Am', 'Em', 'Am', 'Am']
ALT_B = ['C6:6 A5:2 G5:4 A5:4', 'G5:8 E5:4 G5:4', 'D6:6 C6:2 B5:4 G5:4', 'A5:12 r:4',
         'C6:6 A5:2 G5:4 A5:2 C6:2', 'E6:8 D6:4 C6:4', 'B5:6 D6:2 B5:4 G#5:4', 'A5:12 r:4']
ALT_B_CH = ['F', 'C', 'G', 'Am', 'F', 'C', 'E', 'Am']
# zampoña-antwoorden in B (in de rusten van de quena, huayno-ritme)
ALT_B_ECHO = {3: 'r:12 E5:2 G5:1 A5:1', 7: 'r:12 C5:2 D5:1 E5:1'}


def altiplano():
    bpm = 112
    a = Arr('altiplano', bpm, [
        ('quena', 73, 100, 70, 'ds'), ('zamp', 75, 104, 52, 'ds'), ('zamp2', 75, 84, 76, 'ds'),
        ('strum', 26, 82, 84, 'ds'), ('pluck', 25, 76, 40, 'ds'), ('bass', 33, 100, 64, 'ds'),
        ('gtr', 24, 84, 48, 'ds'), ('bombo', 127, 104, 64, 'drum'), ('perc', 127, 72, 80, 'drum'),
        ('wind', 123, 44, 64, 'psg'), ('shk', 122, 46, 70, 'psg')])
    I, A1, A2, B, A3, END = 0, 4, 12, 20, 28, 36

    # intro: wind, bas-drone, quena solo (rubato-achtig: lange noten met vibrato), charango-opmaat
    a.line('quena', I, 'r:4 E5:12 D5:4 E5:4 G5:8 A5:12 G5:2 E5:2 D5:6 C5:2 A4:8', vel=96, legato=0.95)
    for k in range(4):
        a.n('bass', I + k, 0, 15, p('A1'), 84)
    strum(a, 'strum', I + 3, 'Am', [(12, 2, 96), (14, 1, 76), (15, 1, 88)])
    a.n('bombo', I + 3, 12, 4, BOMBO, 100)

    huayno = [(q * 4 + o, l, v) for q in range(4) for o, l, v in ((0, 2, 108), (2, 1, 70), (3, 1, 86))]

    def groove(b, ch, full=True, light=False):
        strum(a, 'strum', b, ch, [(x, l, v - (16 if light else 0)) for x, l, v in huayno])
        root = CHORD[ch][0]
        r, f = place(root, 33), place((root + 7) % 12, 33)
        for half in (0, 8):
            a.n('bass', b, half, 3, r, 108)
            a.n('bass', b, half + 4, 3, f if half == 0 else r + 12 if r + 12 <= 52 else r, 98)
        for half in (0, 8):                                         # bombo: |X . a X|X . a a|
            for pos, nt, v in ((0, BOMBO, 118), (2, ARO, 66), (3, BOMBO, 88), (4, BOMBO, 108), (6, ARO, 70),
                               (7, ARO, 56)):
                if light and nt == BOMBO and pos in (3,):
                    continue
                a.n('bombo', b, half + pos, 2.5 if nt == BOMBO else 0.75, nt, v - (12 if light else 0))
        if full:
            for k in range(8):                                     # chajchas (shaker) in 8en, PSG
                a.n('shk', b, k * 2, 0.5, 86, 70 if k % 2 == 0 else 48)

    def bass_run(b, notes):
        """gitaar-bordoneo naar de volgende frase (laatste tel)."""
        for k, nm in enumerate(notes):
            a.n('gtr', b, 12 + k, 1, p(nm), 100)

    # A: zampoña solo (eenstemmig), A2: quena + zampoña in kwarten eronder, A3: zampoña tutti (kwarten) + quena octaaf
    for i in range(8):
        a.line('zamp', A1 + i, ALT_A[i], vel=108)
        groove(A1 + i, ALT_A_CH[i], full=i >= 4)
        groove(A2 + i, ALT_A_CH[i])
        q = a.line('quena', A2 + i, ALT_A[i], vel=104, shift=12)
        a.copy_to('zamp', q, -12, -2)
        a.copy_to('zamp2', q, -17, -16)
        m = a.line('zamp', A3 + i, ALT_A[i], vel=110)
        a.copy_to('zamp2', m, -5, -12)
        a.copy_to('quena', m, 12, -10)
        groove(A3 + i, ALT_A_CH[i])
    for b in (A1 + 3, A2 + 3, A3 + 3):
        bass_run(b, ['G2', 'A2', 'B2', 'C3'])
    for b in (A1 + 7, A2 + 7):
        bass_run(b, ['E2', 'G2', 'A2', 'B2'])
    bass_run(A3 + 7, ['E2', 'G2', 'G#2', 'A2'])
    # B: weids, relatief majeur; quena lang met vibrato, charango-tremolo, lichte groove; zampoña antwoordt
    for i in range(8):
        a.line('quena', B + i, ALT_B[i], vel=104, legato=0.94)
        groove(B + i, ALT_B_CH[i], full=False, light=True)
        root, tones = CHORD[ALT_B_CH[i]]
        arp = [place(t, 64) for t in tones[:3]]
        arp = sorted(arp) + [sorted(arp)[0] + 12]
        for k in range(16):                                        # tremolo-arpeggio (16en)
            a.n('pluck', B + i, k, 0.8, arp[[0, 1, 2, 3, 2, 1, 2, 1][k % 8]], 92 if k % 4 == 0 else 70)
        if i in ALT_B_ECHO:
            e = a.line('zamp', B + i, ALT_B_ECHO[i], vel=100)
            a.copy_to('zamp2', e, -5, -14)
    bass_run(B + 7, ['E2', 'G2', 'G#2', 'B2'])
    # wind: lange ruisnoten met zwellend volume (intro, en zacht onder B)
    for b0, n in ((I, 4), (B, 8)):
        for k in range(0, n, 2):
            a.n('wind', b0 + k, 0, 31, 52 if k % 4 == 0 else 50, 90)
    a.vibrato('quena', depth=26, speed=40, min_len=5)
    a.vibrato('zamp', depth=14, speed=36, min_len=6)
    # dynamiek
    for part, vol in (('zamp', 104), ('zamp2', 84), ('strum', 82), ('bass', 100), ('bombo', 104), ('perc', 72)):
        a.cc(part, a.t(A1, 0), 7, vol)
    for part, g in (('strum', .8), ('bombo', .82), ('bass', .9)):
        vol = dict((t[0], t[2]) for t in a.tracks)[part]
        a.cc(part, a.t(B, 0), 7, round(vol * g))
        a.cc(part, a.t(A3, 0), 7, vol)
    a.build(A1, END, ['quena', 'zamp', 'bass', 'bombo', 'strum', 'zamp2', 'gtr', 'pluck', 'perc'])


# ======================================================================================================================
# 613: wild gevecht in de Andes
# ======================================================================================================================
W_HOOK = ['E5:2 G5:2 B5:3 A5:1 G5:2 E5:2 D5:2 E5:2', 'G5:3 A5:1 G5:2 E5:2 C6:4 B5:4',
          'A5:2 B5:2 A5:2 F#5:2 D5:3 E5:1 F#5:2 A5:2', 'B5:4 A5:2 F#5:2 D#5:4 B4:4',
          'E5:2 G5:2 B5:3 A5:1 G5:2 E5:2 D5:2 E5:2', 'G5:3 A5:1 B5:2 C6:2 E6:4 D6:2 C6:2',
          'A5:2 C6:2 B5:2 A5:2 G5:2 F#5:2 E5:2 D#5:2', 'E5:8 r:4 B4:1 D5:1 E5:1 F#5:1']
W_HOOK_CH = ['Em', 'C', 'D', 'B7', 'Em', 'C', ('Am', 'B7'), 'Em']
W_FAN = ['D5:3 D5:1 G5:4 B5:3 A5:1 G5:4', 'A5:3 A5:1 F#5:4 D5:4 r:4', 'G5:3 G5:1 B5:4 E6:3 D6:1 B5:4',
         'C6:3 B5:1 A5:2 G5:2 E5:8', 'D5:3 D5:1 G5:4 B5:3 A5:1 G5:4', 'A5:3 B5:1 A5:2 F#5:2 D6:8',
         'E6:4 D6:2 C6:2 B5:4 A5:4', 'B5:2 A5:2 G5:2 F#5:2 D#5:2 F#5:2 A5:2 B5:2']
W_FAN_CH = ['G', 'D', 'Em', 'C', 'G', 'D', 'C', 'B7']
W_HOCKET = ['E5 G5 A5 B5 A5 G5 E5 D5 E5 G5 A5 B5 D6 B5 A5 G5', 'D5 F#5 A5 B5 A5 F#5 D5 C5 D5 F#5 A5 B5 D6 B5 A5 F#5',
            'E5 G5 A5 B5 A5 G5 E5 D5 E5 G5 A5 B5 E6 D6 B5 A5', 'C5 E5 G5 A5 G5 E5 C5 B4 D5 F#5 A5 B5 A5 F#5 D#5 B4']
W_HOCKET_CH = ['Em', 'D', 'Em', ('C', 'B7')]


def wild():
    bpm = 160
    a = Arr('vs_wild', bpm, [
        ('quena', 73, 104, 70, 'ds'), ('tpt', 56, 100, 80, 'ds'), ('tpt2', 56, 84, 92, 'ds'), ('trb', 57, 104, 44, 'ds'),
        ('zamp', 75, 100, 34, 'ds'), ('zamp2', 75, 100, 94, 'ds'), ('strum', 26, 84, 60, 'ds'), ('bass', 33, 112, 64, 'ds'),
        ('bombo', 127, 108, 64, 'drum'), ('caixa', 127, 92, 70, 'drum'), ('arp', 82, 52, 64, 'psg'),
        ('shk', 122, 44, 64, 'psg')])
    I, A1, A2, B1, B2, C, END = 0, 2, 10, 18, 26, 34, 42

    def chords_of(spec):
        return [(spec, 0, 16)] if isinstance(spec, str) else [(spec[0], 0, 8), (spec[1], 8, 8)]

    def battle_groove(b, spec, mode='A', arp=True):
        for ch, s0, ln in chords_of(spec):
            root = CHORD[ch][0]
            r = place(root, 33)
            for k in range(ln // 2):                               # pompende octaafbas in 8en
                a.n('bass', b, s0 + k * 2, 1.6, r + (12 if k % 2 else 0), 116 if k % 2 == 0 else 100)
            strum(a, 'strum', b, ch, [(s0 + x, l, v) for x, l, v in ((0, 1.5, 110), (2, 1, 82), (3, 1, 92), (4, 1.5, 104),
                                                                      (6, 1, 80), (7, 1, 90)) if x < ln])
            if arp:
                tones = [place(t, 72) for t in CHORD[ch][1][:3]]
                tones = sorted(tones) + [sorted(tones)[0] + 12]
                for k in range(ln):
                    a.n('arp', b, s0 + k, 0.7, tones[[0, 1, 2, 3, 2, 1][k % 6]], 72 if k % 4 == 0 else 54)
        if mode == 'A':                                            # strak: bombo + backbeat op de caixa
            drums(a, 'bombo', b, [(0, 120), (6, 100), (8, 116), (10, 90)], BOMBO, ln=2.5)
            drums(a, 'caixa', b, [(4, 112), (12, 112), (14, 56), (15, 70)], CAIXA)
        else:                                                      # B: diablada-mars, bombo op elke tel, caixa-roffels
            drums(a, 'bombo', b, [(0, 122), (4, 110), (8, 118), (12, 110)], BOMBO, ln=2.5)
            drums(a, 'caixa', b, [(2, 96), (3, 70), (6, 100), (7, 76), (10, 96), (11, 70), (13, 64), (14, 104), (15, 84)],
                  CAIXA)
        for k in range(8):
            a.n('shk', b, k * 2 + 1, 0.5, 88, 64)

    # intro: koperstoten + charango, dan een chromatische quena/trompet-loop naar beneden en een opmaat
    for pos in (0, 1.5, 3, 6, 7.5, 9):
        a.n('tpt', I, pos, 1, p('E5'), 118)
        a.n('trb', I, pos, 1, p('B3'), 116)
        a.n('strum', I, pos, 1, p('E4'), 112)
        a.n('bombo', I, pos, 2, BOMBO, 118)
    a.n('bass', I, 0, 1.5, p('E2'), 118)
    for k in range(4):
        a.n('caixa', I, 12 + k, 1, CAIXA, 70 + k * 12)
    run = ['E6', 'D#6', 'D6', 'C#6', 'C6', 'B5', 'A#5', 'A5', 'G#5', 'G5', 'F#5', 'F5', 'B4', 'D5', 'E5', 'F#5']
    for k, nm in enumerate(run):
        a.n('quena', I + 1, k, 0.8, p(nm), 108)
        if k < 12:
            a.n('tpt', I + 1, k, 0.8, p(nm) - 12, 100)
    for k in range(8):
        a.n('bass', I + 1, k * 2, 1.6, p('E2') - (k // 2), 110)
    drums(a, 'bombo', I + 1, [0, 4, 8], BOMBO, 114, ln=3)
    drums(a, 'caixa', I + 1, [(12, 80), (13, 92), (14, 104), (15, 116)], CAIXA)

    for i in range(8):
        a.line('quena', A1 + i, W_HOOK[i], vel=110)
        battle_groove(A1 + i, W_HOOK_CH[i])
        q = a.line('quena', A2 + i, W_HOOK[i], vel=112)
        a.copy_to('tpt', q, -12, -10)                              # A2: trompet een octaaf lager mee
        battle_groove(A2 + i, W_HOOK_CH[i])
        f = a.line('tpt', B1 + i, W_FAN[i], vel=114)               # B: fanfare (diablada)
        for s, e, n, v in f:
            a.parts['trb'].append([s, e, n - 12 - (3 if (n % 12) in (2, 7, 11) else 4), v - 4])   # terts eronder
        battle_groove(B1 + i, W_FAN_CH[i], mode='B', arp=False)
        f2 = a.line('quena', B2 + i, W_FAN[i], vel=110)            # B2: quena voorop, trompetten in tertsen
        a.copy_to('tpt', f2, -12, -8)
        for s, e, n, v in f2:
            a.parts['tpt2'].append([s, e, n - 12 - (3 if (n % 12) in (2, 7, 11) else 4), v - 14])
        battle_groove(B2 + i, W_FAN_CH[i], mode='B', arp=i >= 4)
    for k, nm in enumerate(('D#5', 'E5', 'F#5', 'G5', 'A5', 'B5', 'C6', 'D#6')):   # B2 eind: koper naar boven
        a.n('trb', B2 + 7, 8 + k, 0.8, p(nm) - 12, 110)
    # C: hoquetus (ira/arca): twee zampoña's, links/rechts om en om; daarna opbouw
    for i in range(4):
        notes = W_HOCKET[i].split()
        for k, nm in enumerate(notes):
            a.n('zamp' if k % 2 == 0 else 'zamp2', C + i, k, 0.9, p(nm), 108 if k % 4 == 0 else 96)
        battle_groove(C + i, W_HOCKET_CH[i], arp=False)
    for i in range(4):
        notes = W_HOCKET[i].split()
        for k, nm in enumerate(notes):
            a.n('zamp' if k % 2 == 0 else 'zamp2', C + 4 + i, k, 0.9, p(nm) + (0 if i < 2 else 0), 100)
        battle_groove(C + 4 + i, W_HOCKET_CH[i], arp=True)
        a.n('tpt', C + 4 + i, 0, 15, p(('B4', 'D5', 'E5', 'F#5')[i]), 96 + i * 6)
        a.n('trb', C + 4 + i, 0, 15, p(('G4', 'A4', 'B4', 'B4')[i]) - 12, 92 + i * 6)
    for k in range(16):
        a.n('caixa', C + 7, k, 1, CAIXA, 60 + k * 4)
    a.n('caixa', A1, 0, 6, CRASH, 112)
    a.n('caixa', B1, 0, 6, CRASH, 112)
    a.n('caixa', C, 0, 6, CRASH, 100)
    a.vibrato('quena', depth=20, speed=60, min_len=4, delay=2)
    a.vibrato('tpt', depth=12, speed=60, min_len=6, delay=3)
    a.build(A1, END, ['quena', 'tpt', 'bass', 'bombo', 'caixa', 'trb', 'zamp', 'zamp2', 'strum', 'tpt2'])


# ======================================================================================================================
# 614: La Paz (caporales/saya-fanfare + teleférico)
# ======================================================================================================================
LP_A = ['D5:2 G5:2 G5:3 F#5:1 G5:2 A5:2 B5:4', 'B5:3 A5:1 G5:2 F#5:2 E5:2 F#5:2 G5:4',
        'E5:2 G5:2 C6:3 B5:1 A5:2 G5:2 E5:4', 'F#5:3 G5:1 A5:2 F#5:2 D5:8',
        'D5:2 G5:2 G5:3 F#5:1 G5:2 B5:2 D6:4', 'E6:3 D6:1 B5:2 G5:2 E5:2 G5:2 B5:4',
        'A5:3 B5:1 A5:2 G5:2 F#5:2 E5:2 F#5:2 A5:2', 'G5:8 r:2 D5:2 F#5:2 A5:2']
LP_A_CH = ['G', 'G', 'C', 'D', 'G', 'Em', ('A7', 'D'), 'G']
LP_B = ['B5:6 A5:2 G5:4 E5:4', 'E5:6 G5:2 C6:8', 'B5:6 A5:2 G5:4 D5:4', 'F#5:4 A5:4 D6:8',
        'E6:6 D6:2 B5:4 G5:4', 'C6:6 B5:2 A5:4 G5:4', 'A5:4 C6:4 E6:4 D6:4', 'D6:6 C6:2 B5:2 A5:2 F#5:4']
LP_B_CH = ['Em', 'C', 'G', 'D', 'Em', 'C', 'Am', 'D']


def lapaz():
    bpm = 116
    a = Arr('la_paz', bpm, [
        ('tpt', 56, 104, 72, 'ds'), ('tpt2', 56, 86, 88, 'ds'), ('trb', 57, 100, 44, 'ds'), ('trb2', 57, 88, 34, 'ds'),
        ('tuba', 58, 108, 60, 'ds'), ('quena', 73, 100, 76, 'ds'), ('pluck', 25, 84, 48, 'ds'), ('strum', 26, 80, 84, 'ds'),
        ('bombo', 127, 104, 64, 'drum'), ('caixa', 127, 84, 70, 'drum'), ('plat', 127, 60, 84, 'drum'),
        ('shk', 122, 40, 64, 'psg')])
    I, A1, B, A2, END = 0, 4, 12, 20, 28

    def saya(b, ch_spec, soft=False):
        specs = [(ch_spec, 0, 16)] if isinstance(ch_spec, str) else [(ch_spec[0], 0, 8), (ch_spec[1], 8, 8)]
        for ch, s0, ln in specs:
            root = CHORD[ch][0]
            r, f = place(root, 31), place((root + 7) % 12, 31)
            for k in range(0, ln, 4):                              # tuba: grondtoon/kwint op de tellen
                a.n('tuba', b, s0 + k, 2.5, r if (k // 4) % 2 == 0 else f, 112 - (14 if soft else 0))
        sd = 16 if soft else 0
        drums(a, 'bombo', b, [(0, 120 - sd), (6, 92 - sd), (8, 116 - sd), (14, 92 - sd)], BOMBO, ln=2.5)
        drums(a, 'caixa', b, [(2, 104 - sd), (3, 54), (6, 100 - sd), (7, 54), (10, 104 - sd), (11, 54), (12, 70),
                              (13, 70), (14, 100 - sd)], CAIXA)
        if not soft:
            drums(a, 'plat', b, [(2, 84), (6, 76), (10, 84), (14, 76)], HH_O, ln=2)
        for k in range(8):
            a.n('shk', b, k * 2 + 1, 0.5, 86, 56)

    def third_below(notes, part, vel=-14):
        for s, e, n, v in notes:
            a.parts[part].append([s, e, n - (3 if (n % 12) in (11, 4, 9) else 4), v + vel])

    # intro: teleférico (charango-arpeggio omhoog, quena lang), bombo-opbouw
    up = ['G4', 'B4', 'D5', 'F#5', 'G5', 'B5', 'D6', 'B5']
    for b in range(4):
        for k in range(16):
            a.n('pluck', I + b, k, 0.8, p(up[k % 8]) + (0, 0, -2, 2)[b] * 0 + ((-7) if b == 2 else 0), 92 if k % 4 == 0 else 72)
    a.line('quena', I, 'D6:16 C6:8 B5:8 A5:16 F#5:12 r:4', vel=92, legato=0.95)
    for b in range(4):
        a.n('tuba', I + b, 0, 12, p(('G2', 'G2', 'C2', 'D2')[b]), 96)
    for k, (pos, v) in enumerate(((0, 80), (4, 84), (8, 88), (12, 92), (14, 100), (15, 110))):
        a.n('bombo', I + 3, pos, 2, BOMBO, v)
    for k in range(8):
        a.n('caixa', I + 3, 8 + k, 1, CAIXA, 60 + k * 8)

    for i in range(8):
        t = a.line('tpt', A1 + i, LP_A[i], vel=110)
        tr = a.copy_to('trb', t, -12, -6)
        third_below(tr, 'trb2')
        saya(A1 + i, LP_A_CH[i])
        # B: teleférico boven de stad: quena + charango-tremolo, lichte saya
        a.line('quena', B + i, LP_B[i], vel=104, legato=0.94)
        tones = sorted(place(x, 62) for x in CHORD[LP_B_CH[i]][1][:3])
        arp = tones + [tones[0] + 12]
        for k in range(16):
            a.n('pluck', B + i, k, 0.8, arp[[0, 1, 2, 3, 2, 1, 2, 1][k % 8]] + 12, 90 if k % 4 == 0 else 68)
        saya(B + i, LP_B_CH[i], soft=True)
        if i % 2 == 1:                                             # koper antwoordt zacht aan het eind van de frase
            a.line('trb', B + i, 'r:12 D4:1 E4:1 F#4:1 G4:1' if i % 4 == 1 else 'r:12 B3:1 C4:1 D4:1 E4:1', vel=94)
        # A2: tutti, trompetten in tertsen, charango-rasgueo erbij
        t2 = a.line('tpt', A2 + i, LP_A[i], vel=114)
        third_below(t2, 'tpt2', -12)
        tr2 = a.copy_to('trb', t2, -12, -4)
        third_below(tr2, 'trb2')
        saya(A2 + i, LP_A_CH[i])
        for ch, s0, ln in ([(LP_A_CH[i], 0, 16)] if isinstance(LP_A_CH[i], str) else
                           [(LP_A_CH[i][0], 0, 8), (LP_A_CH[i][1], 8, 8)]):
            strum(a, 'strum', A2 + i, ch, [(s0 + x, 1.5, v) for x, v in ((0, 104), (2, 84), (4, 96), (6, 84))
                                           if x < ln])
    for b in (A1, B, A2):
        a.n('plat', b, 0, 6, CRASH, 108)
    a.vibrato('quena', depth=24, speed=44, min_len=5)
    a.vibrato('tpt', depth=10, speed=50, min_len=6, delay=4)
    a.build(A1, END, ['tpt', 'quena', 'tuba', 'bombo', 'trb', 'caixa', 'pluck', 'trb2', 'strum', 'tpt2', 'plat'])


# ======================================================================================================================
# 615: reggaeton-bende
# ======================================================================================================================
BD_HOOK = ['r:2 A5:2 F5:1 E5:1 D5:2 r:2 D5:1 E5:1 F5:2 A5:2', 'r:2 Bb5:2 A5:1 G5:1 F5:2 r:2 F5:1 G5:1 A5:2 D5:2',
           'r:2 G5:2 F5:1 E5:1 D5:2 r:2 Bb4:1 C5:1 D5:2 G5:2', 'A5:3 G5:1 F5:2 E5:2 C#5:4 E5:4']
BD_HOOK_END = 'A5:3 G5:1 F5:2 E5:2 E5:2 F5:2 G5:2 A5:2'
BD_CH = ['Dm', 'Bb', 'Gm', 'A']
BD_VERSE = ['r:4 D5:2 F5:2 E5:2 D5:2 A4:4', 'r:4 D5:2 F5:2 G5:2 F5:1 E5:1 D5:4', 'r:4 F5:2 D5:2 Bb4:2 C5:2 D5:4',
            'E5:4 C#5:4 A4:4 r:4']
BD_VERSE_END = 'E5:2 F5:2 G5:2 A5:2 Bb5:4 A5:4'
BD_VERSE_CH = ['Dm', 'Dm', 'Bb', 'A']
STAB = {'Dm': ('D4', 'F4', 'A4'), 'Bb': ('D4', 'F4', 'Bb4'), 'Gm': ('D4', 'G4', 'Bb4'), 'A': ('C#4', 'E4', 'A4')}


def bende():
    bpm = 96
    a = Arr('bende', bpm, [
        ('kick', 127, 106, 64, 'drum'), ('snare', 127, 104, 64, 'drum'), ('b808', 38, 88, 64, 'ds'),
        ('zamp', 75, 112, 70, 'ds'), ('stab', 81, 88, 56, 'ds'), ('gtr', 24, 92, 80, 'ds'),
        ('lead', 80, 62, 50, 'psg'), ('hat', 121, 48, 72, 'psg'), ('riser', 123, 40, 64, 'psg')])
    I, A1, V, A2, END = 0, 2, 10, 18, 26
    slides = []

    def dembow(b, half=False, rolls=False):
        drums(a, 'kick', b, [(0, 124), (8, 120)] if half else [(0, 124), (4, 116), (8, 122), (12, 116)], KICK, ln=3)
        drums(a, 'snare', b, [(3, 108), (6, 112), (11, 108), (14, 112)], SNARE, ln=2)
        drums(a, 'snare', b, [(6, 84), (14, 84)], CLAP, ln=2)
        for k in range(8):
            a.n('hat', b, k * 2 + 1 if not half else k * 2, 0.5, 96, 70)
        if rolls:
            for k in range(6):
                a.n('hat', b, 12 + k * 2 / 3, 0.4, 98, 60 + k * 4)

    def bass(b, ch, nxt=None, sparse=False):
        r = place(CHORD[ch][0], 33)
        pat = ((0, 5), (8, 3), (14, 2)) if sparse else ((0, 5), (6, 2), (8, 3), (11, 3), (14, 2))
        for pos, ln in pat:
            e = a.n('b808', b, pos, ln, r, 118 if pos in (0, 8) else 104)
        if nxt:                                                    # slide naar de grondtoon van de volgende maat
            tgt = place(CHORD[nxt][0], 33)
            d = tgt - r
            if d > 6:
                d -= 12
            if d:
                slides.append((e[0] + S // 2, e[1], d, 6, a.t(b + 1, 0)))

    def stabs(b, ch, pat=(3, 6, 11, 14)):
        for pos in pat:
            for nm in STAB[ch]:
                a.n('stab', b, pos, 0.9, p(nm), 92)

    # intro: twee maten stabs + riser, 808-val
    stabs(I, 'Dm', (0, 3, 6))
    stabs(I + 1, 'A', (0, 3, 6, 10, 12, 14))
    a.n('b808', I, 0, 8, p('D2'), 112)
    slides.append((a.t(I, 2), a.t(I, 8), -7, 8, a.t(I, 9)))
    a.n('riser', I, 0, 31, 50, 80)
    drums(a, 'snare', I + 1, [(12, 80), (13, 88), (14, 100), (15, 112)], SNARE)

    for i in range(8):
        ch, nxt = BD_CH[i % 4], BD_CH[(i + 1) % 4]
        # A: hook op de zampoña (pan flute in de productie), stabs, volle dembow
        a.line('zamp', A1 + i, BD_HOOK[i % 4] if i != 7 else BD_HOOK_END, vel=110)
        stabs(A1 + i, ch)
        dembow(A1 + i, rolls=i % 4 == 3)
        bass(A1 + i, ch, nxt if i % 4 == 3 else None)
        # V: couplet, nylon-ostinato (tresillo), PSG-lead, halve kick, spaarzame 808
        vch, vnxt = BD_VERSE_CH[i % 4], BD_VERSE_CH[(i + 1) % 4]
        root, tones = CHORD[vch]
        arp = sorted(place(t, 57) for t in tones[:3])
        for pos, k in ((0, 0), (3, 2), (6, 1), (8, 0), (11, 2), (14, 1)):
            a.n('gtr', V + i, pos, 2.5, arp[k] + (12 if pos >= 8 else 0), 100 if pos in (0, 8) else 84)
        a.line('lead', V + i, BD_VERSE[i % 4] if i != 7 else BD_VERSE_END, vel=100)
        dembow(V + i, half=i < 4, rolls=i == 7)
        bass(V + i, vch, sparse=True)
        # A2: hook + PSG-lead een octaaf lager, stabs op elke 16e-syncope
        a.line('zamp', A2 + i, BD_HOOK[i % 4] if i != 7 else BD_HOOK_END, vel=112)
        a.line('lead', A2 + i, BD_HOOK[i % 4] if i != 7 else BD_HOOK_END, vel=88, shift=-12)
        stabs(A2 + i, ch, (0, 3, 6, 10, 11, 14) if i % 2 else (3, 6, 11, 14))
        dembow(A2 + i, rolls=i % 4 == 3)
        bass(A2 + i, ch, nxt if i % 4 == 3 else None)
    a.n('riser', V + 7, 0, 15, 54, 80)
    a.n('riser', A1 + 7, 8, 7, 56, 70)
    a.bends('b808', slides, rng=12)
    a.vibrato('zamp', depth=16, speed=40, min_len=4)
    a.build(A1, END, ['kick', 'snare', 'b808', 'zamp', 'stab', 'gtr'])


# ======================================================================================================================
# 616: samba (batucada)
# ======================================================================================================================
SB_A = ['D5:2 E5:1 G5:2 G5:1 E5:2 D5:2 B4:2 D5:4', 'r:1 B5:2 B5:1 G#5:2 E5:2 D5:2 E5:1 G#5:2 B5:3',
        'C6:3 B5:1 A5:2 E5:2 G5:1 A5:2 C6:1 A5:4', 'r:2 F#5:2 A5:1 C6:2 B5:1 A5:2 F#5:2 D5:4',
        'D5:2 E5:1 G5:2 G5:1 E5:2 G5:2 B5:2 D6:4', 'r:1 E6:2 D6:1 B5:2 G#5:2 B5:2 D6:1 E6:2 D6:3',
        'C6:2 A5:1 E5:2 A5:1 C6:2 D6:2 C6:1 A5:2 F#5:3', 'G5:8 r:4 B4:1 D5:1 E5:1 F#5:1']
SB_CH = ['G', 'E7', 'Am', 'D7', 'G', 'E7', ('Am', 'D7'), 'G']
TELECOTECO = [0, 2, 3, 5, 7, 9, 10, 12, 14]


def samba():
    bpm = 120
    a = Arr('samba', bpm, [
        ('flute', 73, 100, 70, 'ds'), ('tpt', 56, 92, 86, 'ds'), ('cav', 26, 78, 84, 'ds'), ('bass', 24, 100, 56, 'ds'),
        ('surdo', 127, 112, 64, 'drum'), ('caixa', 127, 80, 76, 'drum'), ('tamb', 127, 84, 90, 'drum'),
        ('agogo', 127, 76, 40, 'drum'), ('cuica', 78, 90, 30, 'ds'), ('apito', 127, 84, 64, 'drum'),
        ('ganza', 122, 48, 64, 'psg')])
    I, A1, P, A2, C, END = 0, 2, 10, 14, 22, 30
    cu = []

    def bateria(b, surdo=True, caixa=True, tamb=True, agogo=True, cuica=False, ganza=True):
        if surdo:   # segunda (hoog) op 1 en 3, primeira (laag, open) op 2 en 4; terceira-syncope
            drums(a, 'surdo', b, [(0, 100), (8, 100)], SURDO_H, ln=2)
            drums(a, 'surdo', b, [(4, 124), (12, 124)], SURDO_L, ln=3)
            drums(a, 'surdo', b, [(7, 70), (15, 74)], SURDO_H, ln=1)
        if caixa:
            drums(a, 'caixa', b, [(k, (104, 46, 72, 88)[k % 4]) for k in range(16)], CAIXA)
        if tamb:
            drums(a, 'tamb', b, [(k, 110 if k in (0, 9) else 96) for k in TELECOTECO], TAMBORIM)
        if agogo:
            drums(a, 'agogo', b, [(0, 104), (2, 92), (5, 96), (8, 100), (10, 92), (13, 96)], AGOGO_H, ln=1)
            drums(a, 'agogo', b, [(3, 92), (6, 92), (11, 92), (14, 92)], AGOGO_L, ln=1)
        if cuica:
            for pos, nt, up in ((2, 74, 3), (6, 72, -2), (10, 74, 3), (13, 77, -3)):
                e = a.n('cuica', b, pos, 1.5, nt, 104)
                cu.append((e[0], e[1], up, 4, e[1] + 2))
        if ganza:
            for k in range(16):
                a.n('ganza', b, k, 0.4, 90, 72 if k % 4 == 0 else 46 if k % 2 else 58)

    def harmony(b, spec, cav=True, bass=True):
        specs = [(spec, 0, 16)] if isinstance(spec, str) else [(spec[0], 0, 8), (spec[1], 8, 8)]
        for ch, s0, ln in specs:
            root = CHORD[ch][0]
            if cav:   # cavaquinho = charango-rasgueo een octaaf hoger, samba-patroon
                strum(a, 'cav', b, ch, [(s0 + x, 0.7, v) for x, v in ((0, 100), (2, 82), (3, 92), (5, 90), (7, 84),
                                                                      (8, 100), (10, 82), (11, 92), (13, 90), (15, 84))
                                        if x < ln], lo=64)
            if bass:  # 7-snarige gitaar: grondtoon op 2 en 4 (met de primeira), kwint ertussen
                r = place(root, 40)
                for pos, nt in ((0, r + 7 if r + 7 < 52 else r - 5), (4, r), (8, r + 7 if r + 7 < 52 else r - 5),
                                (12, r)):
                    if pos < s0 or pos >= s0 + ln:
                        continue
                    a.n('bass', b, pos, 3, nt, 100 if pos % 8 == 4 else 88)

    # intro: apito-signaal (lang, kort, kort), tamborim-chamada, dan een virada naar de volle bateria
    for pos, ln in ((0, 3), (4, 1), (6, 1)):
        a.n('apito', I, pos, ln, APITO, 110)
    drums(a, 'tamb', I, [8, 10, 11, 13, 14], TAMBORIM, 112)
    bateria(I + 1, surdo=False, agogo=False, ganza=False, tamb=False)
    drums(a, 'surdo', I + 1, [(12, 110), (13, 110), (14, 120), (15, 120)], SURDO_L, ln=1)
    drums(a, 'tamb', I + 1, [12, 13, 14, 15], TAMBORIM, 110)

    for i in range(8):
        a.line('flute', A1 + i, SB_A[i], vel=108)
        bateria(A1 + i, cuica=i % 4 == 3)
        harmony(A1 + i, SB_CH[i])
        f = a.line('flute', A2 + i, SB_A[i], vel=110)
        for s, e, n, v in f:                                       # A2: trompet een terts onder de fluit
            a.parts['tpt'].append([s, e, n - 12 - (3 if (n % 12) in (11, 4, 9, 2) else 4) + 12, v - 10])
        bateria(A2 + i, cuica=i % 2 == 1)
        harmony(A2 + i, SB_CH[i])
    # P: paradinha (4 maten): surdos stil, tamborim + caixa in unisono, cuíca praat, dan de virada
    for i in range(4):
        b = P + i
        if i < 3:
            hits = [0, 3, 6, 8, 10, 12] if i % 2 == 0 else [0, 2, 4, 7, 10, 13]
            drums(a, 'tamb', b, hits, TAMBORIM, 112)
            drums(a, 'caixa', b, [(x, 100) for x in hits], CAIXA)
            bateria(b, surdo=False, caixa=False, tamb=False, agogo=i == 2, cuica=True, ganza=True)
            harmony(b, ('Am', 'D7', 'G')[i], cav=i == 2, bass=False)
            a.n('apito', b, 15, 1, APITO, 96)
        else:
            drums(a, 'caixa', b, [(k, 60 + k * 4) for k in range(16)], CAIXA)
            drums(a, 'surdo', b, [(0, 110), (4, 116), (8, 120), (10, 120), (12, 124), (14, 124)], SURDO_L, ln=2)
            a.line('tpt', b, 'D5:2 D5:2 E5:2 F#5:2 G5:2 A5:2 B5:2 D6:2', vel=108)
    # C: bateria met trompet-riff (gafieira) en cuíca, cavaquinho, fluit in de rust
    C_RIFF = ['G5:1 r:1 G5:1 B5:2 G5:1 E5:2 D5:2 E5:2 G5:4', 'r:8 G#5:1 B5:2 D6:2 B5:1 G#5:2',
              'A5:1 r:1 A5:1 C6:2 A5:1 E5:2 A5:2 C6:2 E6:4', 'D6:2 C6:2 A5:2 F#5:2 D5:8']
    for i in range(8):
        bateria(C + i, cuica=True, agogo=True)
        harmony(C + i, SB_CH[i])
        a.line('tpt', C + i, C_RIFF[i % 4], vel=110)
        if i >= 4:
            a.line('flute', C + i, C_RIFF[i % 4], vel=96, shift=12)
    a.n('apito', C + 7, 12, 1, APITO, 104)
    a.n('apito', C + 7, 14, 1, APITO, 104)
    a.bends('cuica', cu, rng=4)
    a.vibrato('flute', depth=16, speed=50, min_len=4)
    a.build(A1, END, ['flute', 'tpt', 'surdo', 'caixa', 'tamb', 'bass', 'cav', 'agogo', 'cuica', 'apito'])


SONGS = {'demo': demo, 'altiplano': altiplano, 'wild': wild, 'lapaz': lapaz, 'bende': bende, 'samba': samba}

if __name__ == '__main__':
    for name in (sys.argv[1:] or SONGS):
        SONGS[name]()
