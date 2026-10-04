#!/usr/bin/env python3
"""Project Grounded: Battle! Regigigas = het originele Regi-thema (mus_vs_regi, ongewijzigd) + bombast erbovenop,
met Slow Start (Jordi).

- Maat 0 t/m tel 1 van maat 3 (±5 s, de gevechtstransitie): precies het originele Regi-thema.
- Vanaf ±5 s: Slow Start. Het tempo zakt in drie tellen naar 55% en versnelt vanaf maat 4 per maat terug naar 100%.
- Vanaf maat 8: bombast bovenop het origineel (tuba-grondtonen, taiko, crashes), in de loop (maat 20-39) een koor
  onder het koraal. Het koper zit al in het origineel.
- Maat 28-31 (begin van een frase): hij zakt nog één keer in ("bijkomen"), tel voor tel vertragend, zonder drums en
  arpeggio's, en komt met een paukenroffel terug; maat 32 vol gas met een crash.
De sporen van het origineel worden 1-op-1 gekopieerd (zelfde instrumenten, volumes, pitchbends); de extra
instrumenten staan in voicegroup_grounded_regigigas (= vs_regi + 84 trompet, 85 hoorn, 86 koor, 87 tuba, 88 taiko).
Zie tools/grounded/MUZIEK.md. Gebruik: python3 tools/grounded/regigigas_theme.py"""
import os, re, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, thin, detach, allocate, releases, release_ticks

SRC = 'sound/songs/midi/mus_vs_regi.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_regigigas.mid'
VG = 'grounded_regigigas'
TPB = 24
BAR = TPB * 4
BASE_TEMPO = 375000                     # 160 bpm, zoals het origineel
TRUMPET, HORN, CHOIR, TUBA, TAIKO, TIMPANI, DRUMS = 84, 85, 86, 87, 88, 47, 0
EXTRA = {84: 56, 85: 60, 86: 52, 87: 58, 88: 116}   # nieuwe programma's -> instrument uit grounded_gm
LOOP_START, LOOP_END = 20, 40
# Climax (Jordi: 'epischer, de leider van de Regi's'): na maat 39 nog 8 maten = het hoofdthema (maat 20-27) een hele
# toon hoger, met een vol koperkoor dat de melodie overneemt, taiko, crashes en pauken; daarna terug naar maat 20.
CLIMAX_START, CLIMAX_END, SHIFT, CLIMAX_TEMPO2 = 40, 48, 2, 1.08
CLIMAX_FROM = 20                         # bronmaat van de climax
SLOW_START = {4: 0.55, 5: 0.60, 6: 0.66, 7: 0.73, 8: 0.80, 9: 0.87, 10: 0.94, 11: 1.0}
SLOW_IN = [(3, 1, 0.82), (3, 2, 0.68), (3, 3, 0.6)]   # (maat, tel, factor): vanaf ±5 s afremmen (Jordi)
# 'bijkomen': de melodie rust in maat 28-29 (na de steek op 28). Al aan het eind van maat 27 afremmen, zodat de steek
# vertraagd valt; traagst in de rust; in 30-31 weer opbouwen; vanaf 32 de climax iets bóven het normale tempo.
DIP = {27: [0.95, 0.9, 0.85, 0.8], 28: [0.72, 0.66, 0.62, 0.6], 29: [0.6, 0.6, 0.62, 0.65],
       30: [0.7, 0.76, 0.82, 0.88], 31: [0.92, 0.96, 1.0, 1.03]}
CLIMAX = 32                             # maat 32-39: Regigigas op volle kracht (tempo 1,06, fanfare, koor, pauken)
CLIMAX_TEMPO = 1.06
QUIET = (28, 29)                        # hier vallen drums en arpeggio's weg en is alles zachter
MUTE_TRACKS = (4, 5, 7)                 # arpeggio's en drums van het origineel


def voicegroup():
    src = open('sound/voicegroups/vs_regi.inc').read().rstrip('\n').split('\n')
    gm = {}
    for l in open('sound/voicegroups/grounded_gm.inc'):
        m = re.search(r'@\s*(\d+)', l)
        if l.strip().startswith('voice_') and m:
            gm[int(m.group(1))] = l.split('@')[0].rstrip()
    out = ['@ Project Grounded: vs_regi + extra instrumenten voor Battle! Regigigas. Gegenereerd door tools/grounded/regigigas_theme.py.',
           'voice_group grounded_regigigas']
    out += [l for l in src if l.strip().startswith('voice_') and not l.strip().startswith('voice_group')]
    for prog in sorted(EXTRA):
        out.append('%s  @ %d' % (gm[EXTRA[prog]], prog))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out) + '\n')


def bar_of(t):
    return t // BAR


def copy_track(track, mute):
    """Origineel spoor 1-op-1, behalve in de QUIET-maten: zachter, of (mute) zonder noten."""
    out, tick, last, skip = mido.MidiTrack(), 0, 0, set()
    for msg in track:
        tick += msg.time
        if msg.type in ('note_on', 'note_off'):
            b = bar_of(tick)
            if msg.type == 'note_on' and msg.velocity:
                if mute and b in QUIET:
                    skip.add(msg.note)
                    continue
                skip.discard(msg.note)
                if b in QUIET:
                    msg = msg.copy(velocity=max(1, int(msg.velocity * 0.6)))
            elif msg.note in skip:
                skip.discard(msg.note)
                continue
        if msg.type == 'end_of_track':
            break
        out.append(msg.copy(time=tick - last))
        last = tick
    out.append(mido.MetaMessage('end_of_track', time=0))
    return out


def append_notes(track, notes, srctrack):
    """Noten achter een gekopieerd spoor plakken (climax), met het programma dat het spoor in de bronmaten had."""
    ch = next(x.channel for x in srctrack if x.type == 'note_on')
    tick, prog = 0, 0
    for x in srctrack:
        tick += x.time
        if x.type == 'program_change' and tick <= CLIMAX_FROM * BAR:
            prog = x.program
    msgs = list(track)[:-1]                       # zonder end_of_track
    last = sum(m.time for m in msgs)
    out = mido.MidiTrack(msgs)
    ev = [(CLIMAX_START * BAR, 0, mido.Message('program_change', channel=ch, program=prog))]
    for s, e, n, v in notes:
        ev.append((s, 2, mido.Message('note_on', channel=ch, note=n, velocity=v)))
        ev.append((e, 1, mido.Message('note_off', channel=ch, note=n, velocity=0)))
    for t, _, m in sorted(ev, key=lambda x: (x[0], x[1])):
        out.append(m.copy(time=max(0, t - last)))
        last = max(last, t)
    out.append(mido.MetaMessage('end_of_track', time=0))
    return out


def note_track(notes, prog, vol, ch, pan):
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    msgs = sorted([(s, 1, n, v) for s, e, n, v in notes] + [(e, 0, n, 0) for s, e, n, v in notes])
    last = 0
    for tk, kind, n, v in msgs:
        t.append(mido.Message('note_on' if kind else 'note_off', channel=ch, note=n,
                              velocity=max(1, min(127, int(v))) if kind else 0, time=tk - last))
        last = tk
    return t


def build():
    voicegroup()
    src = mido.MidiFile(SRC)
    assert src.ticks_per_beat == TPB
    T = {i: notes_of(src.tracks[i]) for i in range(1, 9)}
    end = CLIMAX_END * BAR

    # bombast
    add = {}
    # (geen trompet/hoorn: het origineel heeft het koper al; verdubbelen kost alleen kanalen)
    add['trumpet'], add['horn'] = [], []
    add['choir'] = [[s, e, n - 12, v] for s, e, n, v in thin(T[1], 1, 'top') if bar_of(s) >= LOOP_START]
    roots = {}
    for s, e, n, v in sorted(T[3]):
        roots.setdefault(bar_of(s), n)
    add['tuba'] = [[b * BAR, (b + 1) * BAR - 6, roots[b] + (12 if roots[b] < 31 else 0), 100]
                   for b in sorted(roots) if 8 <= b < LOOP_END]
    add['taiko'] = [[b * BAR + o, b * BAR + o + 24, 48, 112] for b in range(8, LOOP_END) for o in (0, 48)
                    if b not in QUIET]
    add['crash'] = [[b * BAR, b * BAR + 48, 57, 120] for b in (8, LOOP_START, 32, 34, 36, 38)]
    # climax: trompetfanfare op de grondtoon (grondtoon+2 oct., kwint, grondtoon) en een tweede koorstem
    add['fanfare'] = []
    # de climax-sectie: bronmaat 20-27 naar maat 40-47, +SHIFT halve tonen
    off = (CLIMAX_START - CLIMAX_FROM) * BAR
    src_rng = lambda ev: [e for e in ev if CLIMAX_FROM <= bar_of(e[0]) < CLIMAX_FROM + 8]
    mv = lambda ev, tr=SHIFT: [[s + off, e + off, n + tr, v] for s, e, n, v in src_rng(ev)]
    add['trumpet'] = [[s, e, n, 120] for s, e, n, v in mv(thin(T[1], 1, 'top'))]
    add['horn'] = [[s, e, n, 112] for s, e, n, v in mv(thin(T[2], 1, 'top'))]
    add['choir'] += [[s, e, n - 12, 118] for s, e, n, v in mv(thin(T[1], 1, 'top'))]
    # tweestemmig: een diatonische terts erboven (E-mineur, de toonsoort van de climax)
    scale = [4, 6, 7, 9, 11, 0, 2]
    def third(n):
        pcs = sorted(range(n + 1, n + 6), key=lambda x: x)
        up = [x for x in pcs if x % 12 in scale]
        return up[1] if len(up) > 1 else n + 3
    add['trumpet2'] = [[s, e, third(n), 108] for s, e, n, v in add['trumpet']]
    add['choir2'] = [[s, e, third(n), 108] for s, e, n, v in add['choir'] if bar_of(s) >= CLIMAX_START]
    for b in range(CLIMAX_START, CLIMAX_END):
        r = roots[b - CLIMAX_START + CLIMAX_FROM] + SHIFT
        add['tuba'].append([b * BAR, (b + 1) * BAR - 6, r + (12 if r < 31 else 0), 118])
        add['taiko'] += [[b * BAR + o, b * BAR + o + 12, 48, 120] for o in (0, 24, 48, 72)]
        add['crash'].append([b * BAR, b * BAR + 48, 57, 124])
        add['hits'] = add.get('hits', []) + [[b * BAR + o, b * BAR + o + 12, r % 12 + 48, 110] for o in (0, 48)]
    # originele begeleiding (bas, arpeggio's, drums, pauken) gaat mee de climax in, getransponeerd
    climax_orig = {3: mv(T[3]), 4: mv(T[4]), 5: mv(T[5])}   # originele drums en pauken: in de climax vervangen door taiko/crash/eigen pauken
    add['hits'] = add.get('hits', []) + [[b * BAR + o, b * BAR + o + 12, 48, 80 + (b - 34) * 6] for b in range(34, LOOP_END) for o in (0, 48)]
    add['roll'] = [[31 * BAR + i * 6, 31 * BAR + i * 6 + 6, 48, 40 + i * 5] for i in range(16)]   # paukenroffel naar de climax
    for k in add:
        for e in add[k]:
            if bar_of(e[0]) in QUIET:
                e[3] = int(e[3] * 0.6)

    # stemmen: het origineel ligt vast (DirectSound-noten daarvan als preset), de toevoegingen vullen aan
    rel_src = releases('vs_regi')
    preset = []
    for i in range(1, 9):
        prog = next((x.program for x in src.tracks[i] if x.type == 'program_change'), 0)
        r = rel_src.get(prog, 200)
        if r is None and prog != 0:
            continue                                          # PSG telt niet mee
        for s, e, n, v in T[i]:
            if i in MUTE_TRACKS and bar_of(s) in QUIET:
                continue
            preset.append((s, min(e, s + TPB) if prog == 0 else e + release_ticks(r, TPB, 160)))
        for s, e, n, v in climax_orig.get(i, []):
            if r is None and prog != 0:
                continue
            preset.append((s, min(e, s + TPB) if prog == 0 else e + release_ticks(r, TPB, 160)))
    rel = releases(VG)
    progs = {'trumpet2': TRUMPET, 'crash': DRUMS, 'trumpet': TRUMPET, 'horn': HORN, 'choir': CHOIR, 'choir2': CHOIR, 'tuba': TUBA, 'taiko': TAIKO,
             'roll': TIMPANI, 'hits': TIMPANI, 'fanfare': TRUMPET}
    tail = {k: release_ticks(rel.get(p, 200), TPB, 160) for k, p in progs.items()}
    for k in ('choir', 'choir2', 'tuba', 'trumpet', 'trumpet2', 'horn'):
        add[k] = detach(add[k], tail[k])
    order = ['roll', 'crash', 'trumpet', 'horn', 'choir', 'trumpet2', 'tuba', 'choir2', 'hits', 'taiko']
    kept = allocate(add, order, tail=tail, drum_parts=(), drum_len=None, max_voices=11, preset=preset)   # legendary: 11, 1 vrij voor effecten
    for k in order:
        if len(kept[k]) < len(add[k]) * 0.97:
            print('  %s: %d van %d noten vallen weg (te vol)' % (k, len(add[k]) - len(kept[k]), len(add[k])))

    kept['roll'] = sorted(kept['roll'] + kept['hits'])      # pauken samen op één spoor
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    ev = [(0, mido.MetaMessage('set_tempo', tempo=BASE_TEMPO))]
    for b, t, f in SLOW_IN:
        ev.append((b * BAR + t * TPB, mido.MetaMessage('set_tempo', tempo=int(BASE_TEMPO / f))))
    for b, f in SLOW_START.items():
        ev.append((b * BAR, mido.MetaMessage('set_tempo', tempo=int(BASE_TEMPO / f))))
    ev.append((LOOP_START * BAR, mido.MetaMessage('set_tempo', tempo=BASE_TEMPO)))
    for b, fs in DIP.items():
        for i, f in enumerate(fs):
            ev.append((b * BAR + i * TPB, mido.MetaMessage('set_tempo', tempo=int(BASE_TEMPO / f))))
    ev.append((CLIMAX * BAR, mido.MetaMessage('set_tempo', tempo=int(BASE_TEMPO / CLIMAX_TEMPO))))
    ev.append((CLIMAX_START * BAR, mido.MetaMessage('set_tempo', tempo=int(BASE_TEMPO / CLIMAX_TEMPO2))))
    ev.append((LOOP_START * BAR, mido.MetaMessage('marker', text='[')))
    ev.append((end, mido.MetaMessage('marker', text=']')))
    last = 0
    for t, m in sorted(ev, key=lambda x: (x[0], x[1].type != 'set_tempo')):
        cond.append(m.copy(time=t - last))
        last = t
    out.tracks.append(cond)
    for i in range(1, 9):
        t = copy_track(src.tracks[i], i in MUTE_TRACKS)
        if i in climax_orig:
            t = append_notes(t, climax_orig[i], src.tracks[i])
        out.tracks.append(t)
    written = set()
    kept['trumpet'] = sorted(kept['trumpet'] + kept['trumpet2'])   # tweestemmig koper op één spoor
    kept['choir'] = sorted(kept['choir'] + kept['choir2'])
    for k, prog, vol, ch, pan in (('trumpet', TRUMPET, 110, 8, 72), ('horn', HORN, 104, 11, 52), ('choir', CHOIR, 84, 10, 60),
                                  ('tuba', TUBA, 84, 12, 60), ('taiko', TAIKO, 88, 13, 64), ('roll', TIMPANI, 100, 14, 64),
                                  ('crash', DRUMS, 100, 15, 64)):
        out.tracks.append(note_track(kept[k], prog, vol, ch, pan))
        written.add(k)
    missing = [k for k in kept if kept[k] and k not in written and k not in ('trumpet2', 'choir2', 'hits')]
    assert not missing, 'partijen berekend maar niet weggeschreven: %s' % missing     # (v4: koper ontbrak zo)
    out.save(OUT)
    print(OUT)


if __name__ == '__main__':
    build()
