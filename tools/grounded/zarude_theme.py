#!/usr/bin/env python3
"""Project Grounded: "Battle! Zarude" – eigen gevechtsmuziek (legendary-stijl, jungle, groovy).

Opbouw (niet herhaald, ±11 s, loopt synchroon met de gevechtstransitie):
  maat 1-2  taiko + strijkers-tremolo + dreun (transitie)
  maat 3-6  koperfanfare, congas en bas komen erbij, marimba-ostinato
  maat 7-8  tomroffel en strijkersloop omhoog, crash
Loop (16 maten, ±23 s): A = fluitmelodie op een funky slapbas en bongo-groove,
B = strijkers nemen het over, trompetstoten, call-and-response, terug naar A.

Instrumenten = programma's van voicegroup_grounded_gm (drums: kanaal 10, rs_drumset:
36 kick, 39 klap, 41-50 toms, 54 tamboerijn, 57 crash, 62 hoge conga, 64 lage conga).
Gebruik: python3 tools/grounded/zarude_theme.py  (schrijft sound/songs/midi/mus_grounded_vs_zarude.mid)
"""
import mido

TPB = 48            # ticks per kwartnoot
S16 = TPB // 4      # een zestiende
BAR = 16 * S16
BPM = 168
OUT = 'sound/songs/midi/mus_grounded_vs_zarude.mid'

D, E, F, G, A, Bb, C = 2, 4, 5, 7, 9, 10, 0
def n(pc, octv):     # nootnummer, C4 = 60
    return 12 * (octv + 1) + pc

# akkoorden (grondtoon, mineur?)
LOOP_A = [(D, 1), (D, 1), (Bb, 0), (C, 0), (D, 1), (D, 1), (G, 1), (A, 0)]
LOOP_B = [(Bb, 0), (C, 0), (D, 1), (D, 1), (Bb, 0), (C, 0), (A, 0), (A, 0)]
INTRO_BARS = 8


class Track:
    def __init__(self, name, ch, prog, vol, pan=64):
        self.name, self.ch, self.ev = name, ch, []
        self.prog, self.vol, self.pan = prog, vol, pan

    def note(self, bar, pos16, dur16, note, vel=100, raw=False):
        if bar >= 2 and not raw:
            bar += 1        # extra spanningsmaat: de blazers wachten tot de transitie voorbij is (Jordi)
        t = bar * BAR + pos16 * S16
        self.ev.append((t, 1, note, vel))
        self.ev.append((t + max(1, int(dur16 * S16) - 1), 0, note, 0))

    def midi(self):
        tr = mido.MidiTrack()
        tr.append(mido.MetaMessage('track_name', name=self.name, time=0))
        tr.append(mido.Message('program_change', channel=self.ch, program=self.prog, time=0))
        tr.append(mido.Message('control_change', channel=self.ch, control=7, value=self.vol, time=0))
        tr.append(mido.Message('control_change', channel=self.ch, control=10, value=self.pan, time=0))
        now = 0
        for t, on, note, vel in sorted(self.ev, key=lambda e: (e[0], e[1])):
            tr.append(mido.Message('note_on' if on else 'note_off', channel=self.ch, note=note,
                                   velocity=vel if on else 0, time=t - now))
            now = t
        return tr


drums = Track('drums', 9, 127, 110)
taiko = Track('taiko', 0, 116, 115)
bass = Track('bass', 1, 36, 112)
marimba = Track('marimba', 2, 12, 92, 44)
lead = Track('flute', 3, 73, 108, 70)
brass = Track('trumpet', 4, 56, 96, 84)
strings = Track('strings', 5, 48, 92, 54)
sq1 = Track('square1', 6, 80, 58, 30)     # PSG: harmonie onder de melodie
sq2 = Track('square2', 7, 81, 52, 98)     # PSG: arpeggio-glitter
noise = Track('shaker', 8, 120, 40)       # PSG-ruis: shaker
TRACKS = [drums, taiko, bass, marimba, lead, brass, strings]   # PSG (sq1/sq2/ruis) eruit: losse piepjes (Jordi)


def third(minor):
    return 3 if minor else 4


# ----------------------------------------------------------------- groove-bouwstenen
def groove(bar, full=True, soft=False):
    v = 70 if soft else 104
    # bongo/conga: hoog (62) en laag (64), funky zestienden
    pat = {0: 64, 2: 62, 3: 62, 5: 64, 6: 62, 8: 64, 10: 62, 11: 64, 13: 62, 14: 62, 15: 62}
    for p, nt in pat.items():
        drums.note(bar, p, 1, nt, v - (18 if p in (3, 13, 15) else 0))
    if not full:
        return
    for p in (0, 6, 10):
        drums.note(bar, p, 1, 36, 120)               # kick
    for p in range(16):
        noise.note(bar, p, 0.5, 60, 50 if p % 2 else 80)


def bassline(bar, root, minor, octv=2):
    r = n(root, octv)
    seq = [(0, 1, 0, 120), (3, 1, 0, 96), (4, 1, 12, 110), (6, 1, 0, 100), (8, 1, 0, 116),
           (10, 1, 10 if minor else 12, 100), (11, 1, 12, 108), (14, 1, 7, 104), (15, 1, 5 if minor else 7, 90)]
    for p, d, iv, v in seq:
        bass.note(bar, p, d, r + iv, v)


def ostinato(bar, root, minor, octv=4, vel=86):
    r = n(root, octv)
    t3 = third(minor)
    iv = [0, 7, 12, 7, t3 + 12, 12, 7, 12, 0, 7, 12, 7, t3 + 12, 12, 19, t3 + 12]
    for p, x in enumerate(iv):
        marimba.note(bar, p, 1, r + x, vel - (14 if p % 2 else 0))


def arp(bar, root, minor, octv=5):
    r = n(root, octv)
    t3 = third(minor)
    for p, x in enumerate([0, t3, 7, 12] * 4):
        sq2.note(bar, p, 0.75, r + x, 70)


# ----------------------------------------------------------------- intro (8 maten)
# maat 1-2: transitie. Taiko, strijkerstremolo op lage D, PSG-dreun die aanzwelt.
for b in (0, 1):
    for p, v in ((0, 127), (6, 100), (8, 120), (12, 96), (14, 104)):
        taiko.note(b, p, 2, n(D, 2), v)
    for p in range(16):
        strings.note(b, p, 1, n(D, 3) + (12 if b == 1 and p >= 8 else 0), 50 + b * 30 + p * 2)
    sq1.note(b, 0, 16, n(D, 3), 60 + 30 * b)
taiko.note(1, 15, 1, n(D, 2), 127)
# maat 2: taiko in achtsten die aanzwellen (geen conga-roffel meer: te druk)
for p in range(0, 16, 2):
    taiko.note(1, p, 2, n(D, 2), 70 + p * 3)

# extra maat 3 (raw): spanning houden, taiko in achtsten, strijkers tremolo een octaaf hoger
for p in range(0, 16, 2):
    taiko.note(2, p, 2, n(D, 2), 96 + p * 2, raw=True)
for p in range(16):
    strings.note(2, p, 1, n(D, 4), 90 + p, raw=True)
for p in (0, 8):
    bass.note(2, p, 4, n(D, 1), 100, raw=True)

# maat 4-7: koperfanfare
fanfare = [(2, 0, 6, n(D, 4)), (2, 6, 2, n(F, 4)), (2, 8, 4, n(G, 4)), (2, 12, 4, n(A, 4)),
           (3, 0, 12, n(A, 4)), (3, 12, 2, n(G, 4)), (3, 14, 2, n(A, 4)),
           (4, 0, 6, n(Bb, 4)), (4, 6, 2, n(A, 4)), (4, 8, 4, n(G, 4)), (4, 12, 4, n(F, 4)),
           (5, 0, 12, n(E, 4)), (5, 12, 4, n(A, 3))]
for b, p, d, nt in fanfare:
    brass.note(b, p, d, nt, 116)
    sq1.note(b, p, d, nt - 12, 90)
for b in (2, 3, 4, 5):
    taiko.note(b, 0, 2, n(D, 2), 124)
    if b == 2:      # alleen lage conga's op de tellen
        for p in (0, 4, 8, 12):
            drums.note(b, p, 1, 64, 70)
    elif b == 3:    # achtsten, hoog/laag
        for p in range(0, 16, 2):
            drums.note(b, p, 1, 64 if p % 4 == 0 else 62, 76)
    elif b == 4:    # achtsten met een paar zestienden
        for p in (0, 2, 4, 6, 7, 8, 10, 12, 14, 15):
            drums.note(b, p, 1, 64 if p % 4 == 0 else 62, 84)
    else:           # maat 6: de groove, nog zonder kick
        groove(b, full=False, soft=True)
    root, minor = [(D, 1), (D, 1), (Bb, 0), (A, 0)][b - 2]
    bass.note(b, 0, 2, n(root, 2), 118)
    bass.note(b, 8, 2, n(root, 2), 110)
    if b >= 4:
        ostinato(b, root, minor, vel=76)
        bassline(b, root, minor)

# maat 7-8: tomroffel, strijkersloop omhoog (A harmonisch mineur), crash
toms = [50, 50, 48, 48, 47, 47, 45, 45, 43, 43, 41, 41, 50, 48, 45, 41]
for p, t in enumerate(toms):
    drums.note(6, p, 1, t, 80 + p * 3)
run = [n(A, 3), n(Bb, 3), n(C + 1, 4), n(D, 4), n(E, 4), n(F, 4), n(G + 1, 4), n(A, 4),
       n(Bb, 4), n(C + 1, 5), n(D, 5), n(E, 5), n(F, 5), n(G + 1, 5), n(A, 5), n(Bb, 5)]
for p, nt in enumerate(run):
    strings.note(6, p, 1, nt, 70 + p * 3)
    marimba.note(6, p, 1, nt, 60 + p * 2)
bass.note(6, 0, 8, n(A, 1), 120)
bass.note(6, 8, 8, n(A, 2), 120)
for p in (0, 4, 8, 10, 12, 14):
    taiko.note(7, p, 2, n(D, 2), 127)
for p in (0, 4, 8):
    brass.note(7, p, 3, n(A, 4) if p != 8 else n(C + 1, 5), 124)
    sq1.note(7, p, 3, n(E, 4), 100)
drums.note(7, 0, 4, 57, 120)
strings.note(7, 0, 12, n(A, 5), 110)
bass.note(7, 0, 4, n(A, 1), 124)
bass.note(7, 4, 4, n(A, 1), 124)
bass.note(7, 8, 4, n(A, 1), 124)
for p in range(12, 16):
    drums.note(7, p, 1, 41 + (p - 12) * 3, 110)

# ----------------------------------------------------------------- loop A (8 maten)
MEL_A = [
    [(0, 3, n(D, 5)), (3, 3, n(F, 5)), (6, 2, n(A, 5)), (8, 2, n(G, 5)), (10, 2, n(F, 5)), (12, 4, n(E, 5))],
    [(0, 2, n(F, 5)), (2, 2, n(E, 5)), (4, 4, n(D, 5)), (8, 6, n(A, 4)), (14, 2, n(C, 5))],
    [(0, 3, n(D, 5)), (3, 3, n(F, 5)), (6, 2, n(Bb, 5)), (8, 4, n(A, 5)), (12, 2, n(G, 5)), (14, 2, n(F, 5))],
    [(0, 6, n(G, 5)), (6, 2, n(E, 5)), (8, 6, n(C, 5)), (14, 2, n(E, 5))],
    [(0, 3, n(A, 5)), (3, 3, n(C, 6)), (6, 2, n(D, 6)), (8, 2, n(C, 6)), (10, 2, n(A, 5)), (12, 4, n(G, 5))],
    [(0, 2, n(A, 5)), (2, 2, n(G, 5)), (4, 4, n(F, 5)), (8, 4, n(E, 5)), (12, 4, n(D, 5))],
    [(0, 4, n(G, 5)), (4, 4, n(Bb, 5)), (8, 4, n(D, 6)), (12, 4, n(C, 6))],
    [(0, 6, n(C + 1, 6)), (6, 2, n(A, 5)), (8, 8, n(E, 5))],
]
L0 = INTRO_BARS
for i, (root, minor) in enumerate(LOOP_A):
    b = L0 + i
    groove(b)
    bassline(b, root, minor)
    ostinato(b, root, minor)
    for p, d, nt in MEL_A[i]:
        lead.note(b, p, d, nt, 112)
        sq1.note(b, p, d, nt - (3 if minor else 4) - 12, 80)   # PSG-tertsen onder de fluit
    if i in (3, 7):
        for p, t in zip(range(12, 16), (50, 47, 45, 41)):
            drums.note(b, p, 1, t, 108)
    if i == 0:
        drums.note(b, 0, 4, 57, 118)
        taiko.note(b, 0, 2, n(D, 2), 127)

# ----------------------------------------------------------------- loop B (8 maten)
STR_B = [n(F, 5), n(G, 5), n(A, 5), n(D, 6), n(D, 6), n(E, 6), n(E, 6), n(A, 5)]
CALL = [(0, 2, 0), (2, 2, 3), (4, 4, 7)]   # marimba-vraag; fluit antwoordt
B0 = L0 + 8
for i, (root, minor) in enumerate(LOOP_B):
    b = B0 + i
    groove(b)
    bassline(b, root, minor)
    strings.note(b, 0, 16, STR_B[i], 104)
    for p in (2, 6, 10, 14):                       # trompetstoten op de offbeat
        brass.note(b, p, 1, n(root, 4) + third(minor), 100)
    arp(b, root, minor)
    if i % 2 == 0:                                  # call...
        for p, d, iv in CALL:
            marimba.note(b, p, d, n(root, 5) + iv, 100)
        for p, d, iv in CALL:                       # ...en response
            lead.note(b, 8 + p, d, n(root, 5) + 12 + iv - (0 if p < 4 else 2), 104)
    else:
        ostinato(b, root, minor, vel=80)
    if i == 3:
        taiko.note(b, 0, 2, n(D, 2), 120)
    if i == 7:   # roffel terug naar A
        for p in range(16):
            drums.note(b, p, 1, [50, 48, 47, 45][p // 4], 84 + p * 2)
        taiko.note(b, 8, 2, n(D, 2), 124)
        taiko.note(b, 12, 2, n(D, 2), 127)

END = (B0 + 9) * BAR


def build():
    m = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    cond.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM), time=0))
    cond.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=(L0 + 1) * BAR))
    cond.append(mido.MetaMessage('marker', text=']', time=END - (L0 + 1) * BAR))
    m.tracks.append(cond)
    for t in TRACKS:
        m.tracks.append(t.midi())
    m.save(OUT)
    print(OUT, '%.1f s intro, %.1f s loop' % ((L0 + 1) * 4 * 60 / BPM, 16 * 4 * 60 / BPM))


if __name__ == '__main__':
    build()
