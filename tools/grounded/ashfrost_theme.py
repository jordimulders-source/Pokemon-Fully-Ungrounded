#!/usr/bin/env python3
"""Project Grounded: Ashfrost Village = een wintervariant van het Fallarbor-thema (MUS_FALLARBOR), als eigen nummer
MUS_GROUNDED_ASHFROST. Jordi: 'de juiste nummerkeuze, maar de sound mag meer winter-achtig'.

Zelfde melodie, harmonie en structuur: de negen sporen van mus_fallarbor.mid worden 1-op-1 gekopieerd (noten,
CC7-swells, modulatie), alleen instrumenten wisselen en er komen lagen bij:
  - tempo 148 -> 138 bpm (±7% trager, meer ruimte);
  - leadspoor: nylongitaar -> blokfluit (ashfrost_recorder; de fluit- en strijkersdelen van het origineel blijven);
  - intro-arpeggio (pizzicato, maat 0-2) -> celesta een octaaf hoger: sneeuwvlokjes;
  - de aangehouden PSG-akkoorden (maat 3-15) -> warme pad (ashfrost_warm_pad, FluidR3 'Warm Pad');
  - de PSG-arpeggio's vanaf maat 16: één blijft PSG (zachter), de andere wordt celesta;
  - nylon-arpeggio's (maat 24-31) -> speeldoos (jirachi_music_box);
  - de hoornbas (spoor 4) wordt vanaf maat 16 een getokkelde contrabas (shaymin_upright): warme bas, en koper
    onder C3 klinkt als 'puuup' (MUZIEK.md); in het rustige A-deel blijft de hoorn;
  - nieuw: sleebellen op de tellen in het vrolijke deel (maat 16-31) en zacht windgeruis op het PSG-ruiskanaal
    (lange zwellingen, geen constante toon).
voicegroup_grounded_ashfrost = voicegroup_fallarbor (harp/glockenspiel met een kortere uitklinktijd, zodat de
stemverdeling binnen 10 DirectSound-noten blijft) + de extra instrumenten op 84-90. Zie tools/grounded/MUZIEK.md.
Samples: tools/grounded/ashfrost_samples.py. Gebruik: python3 tools/grounded/ashfrost_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import allocate, releases, release_ticks, ds_occupancy, MAX_VOICES

SRC = 'sound/songs/midi/mus_fallarbor.mid'
OUT = 'sound/songs/midi/mus_grounded_ashfrost.mid'
VG = 'grounded_ashfrost'
TPB = 24
BAR = 96
SRC_BPM = 60e6 / 405405          # 148
BPM = 138
CELESTA, MUSICBOX, RECORDER, PAD, UPRIGHT, SLEIGH, WIND = 84, 85, 86, 87, 88, 89, 90
EXTRA = {
    CELESTA:  'voice_directsound 60, 0, DirectSoundWaveData_jirachi_celesta, 255, 248, 0, 180',
    MUSICBOX: 'voice_directsound 60, 0, DirectSoundWaveData_jirachi_music_box, 255, 248, 0, 190',
    RECORDER: 'voice_directsound 60, 0, DirectSoundWaveData_ashfrost_recorder, 255, 0, 255, 110',   # kort: de CC7-swells van het origineel doen de frasering
    PAD:      'voice_directsound 60, 0, DirectSoundWaveData_ashfrost_warm_pad, 255, 0, 255, 200',
    UPRIGHT:  'voice_directsound 60, 0, DirectSoundWaveData_shaymin_upright, 255, 0, 255, 150',
    SLEIGH:   'voice_directsound 60, 0, DirectSoundWaveData_ashfrost_sleigh, 255, 0, 255, 150',
    WIND:     'voice_noise 60, 0, 0, 7, 0, 15, 7',     # 15-bit ruis, trage aanzet en uitklinktijd: zwellende windvlaag
}
CELESTA_LEN = 4
RELEASE_FIX = {9: 200, 46: 175, 73: 135}   # glockenspiel 249 / harp 242 klonken 1-2 s na: tot 19 noten tegelijk in het origineel

# programma's die per spoor vervangen worden: {spoor: [(vanaf tick, oud programma, nieuw programma)]}
PROG_MAP = {
    1: {24: RECORDER},
    2: {45: CELESTA},
    5: {24: MUSICBOX},
}
VOL = {   # CC7 per spoor waar het nieuwe instrument een ander niveau nodig heeft: {spoor: {tick: waarde}}
    2: {0: 82},                       # celesta (was pizzicato op 127)
    6: {0: 48, 384: 42, 1536: 30},    # pad (maat 3-15), dan PSG-arpeggio zachter dan het origineel (50)
    7: {0: 48, 384: 40, 1536: 58},    # pad, dan celesta
}


def voicegroup():
    src = [l for l in open('sound/voicegroups/fallarbor.inc').read().split('\n') if l.strip().startswith('voice_')
           and not l.strip().startswith('voice_group')]
    assert len(src) == CELESTA, 'fallarbor heeft %d stemmen' % len(src)
    for p, rel in RELEASE_FIX.items():
        parts = src[p].rsplit(',', 1)
        src[p] = '%s, %d' % (parts[0], rel)
    out = ['@ Project Grounded: voicegroup_fallarbor + winterinstrumenten voor Ashfrost Village (MUS_GROUNDED_ASHFROST).',
           '@ Gegenereerd door tools/grounded/ashfrost_theme.py. Glockenspiel (9) en harp (46) klinken korter na.',
           '@ 84 celesta, 85 speeldoos, 86 blokfluit, 87 warme pad, 88 contrabas, 89 sleebellen, 90 wind (PSG-ruis).',
           'voice_group %s' % VG] + src
    out += ['\t%s  @ %d' % (EXTRA[p], p) for p in sorted(EXTRA)]
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out) + '\n')
    inc = open('sound/voice_groups.inc').read()
    line = '.include "sound/voicegroups/%s.inc"' % VG
    if line not in inc:
        open('sound/voice_groups.inc', 'w').write(inc.rstrip('\n') + '\n' + line + '\n')


def absolute(track):
    tick, out = 0, []
    for x in track:
        tick += x.time
        out.append((tick, x))
    return out


def relative(events):
    t, last = mido.MidiTrack(), 0
    for tick, x in events:
        t.append(x.copy(time=tick - last))
        last = tick
    return t


def transform(i, track):
    """Spoor i van het origineel kopiëren met de winterinstrumenten (noten en swells blijven gelijk)."""
    ev = absolute(track)
    ch = next(x.channel for _, x in ev if hasattr(x, 'channel'))
    out, prog = [], None
    for tick, x in ev:
        if x.type == 'program_change':
            prog = PROG_MAP.get(i, {}).get(x.program, x.program)
            x = x.copy(program=prog)
        if i in (6, 7) and x.type == 'program_change' and tick == 0:
            x = x.copy(program=PAD)
        if i == 4 and x.type == 'program_change' and tick == 1536:
            x = x.copy(program=UPRIGHT)
        if i == 7 and x.type == 'program_change' and tick == 1536:
            x = x.copy(program=CELESTA)
        if x.type == 'control_change' and x.control == 7 and i in VOL and tick in VOL[i]:
            x = x.copy(value=VOL[i][tick])
        if i == 2 and prog == CELESTA and x.type in ('note_on', 'note_off'):
            x = x.copy(note=x.note + 12)           # sneeuwvlokjes: een octaaf hoger
        out.append((tick, x))
    if i == 7:   # celesta vanaf maat 16 (het origineel heeft hier een programmawissel nodig)
        if not any(t == 1536 and x.type == 'program_change' for t, x in out):
            k = next(n for n, (t, x) in enumerate(out) if t >= 1536)
            out.insert(k, (1536, mido.Message('program_change', channel=ch, program=CELESTA)))
    if i == 6:   # PSG-vierkant terug vanaf maat 16
        k = next(n for n, (t, x) in enumerate(out) if t >= 1536)
        out.insert(k, (1536, mido.Message('program_change', channel=ch, program=80)))
    for tick, val in VOL.get(i, {}).items():
        if not any(t == tick and x.type == 'control_change' and x.control == 7 for t, x in out):
            k = next(n for n, (t, x) in enumerate(out) if t >= tick)
            out.insert(k, (tick, mido.Message('control_change', channel=ch, control=7, value=val)))
    if i == 1:
        # blokfluit (houdt aan, i.p.v. de uitklinkende nylongitaar): de CC7-dips aan het eind van lange noten in
        # stappen van 3-10 dB per frame; bij een aanhoudend instrument per tick lineair interpoleren (vloeiend)
        cc = [(t, x) for t, x in out if x.type == 'control_change' and x.control == 7]
        smooth = []
        for (t0, a), (t1, b) in zip(cc, cc[1:]):
            if b.value < a.value and t1 - t0 > 1 and (t0 < 1488 or t0 >= 3072):
                smooth += [(t, a.copy(value=round(a.value + (b.value - a.value) * (t - t0) / (t1 - t0))))
                           for t in range(t0 + 1, t1)]
        out += smooth
        out.sort(key=lambda e: e[0])
        # blokfluit houdt aan waar de nylon uitklonk: solo ±3 dB luider gemeten -> CC7 x 0,75 in die delen
        out = [(t, x.copy(value=max(1, round(x.value * 0.75))) if x.type == 'control_change' and x.control == 7
                and (t < 1488 or t >= 3072) else x) for t, x in out]
    notes, other = split(out)
    if i in (6, 7):
        # pad (maat 0-15): korte doorgangsnoten (< 1 tel) vallen weg in een pad met trage aanzet; de vorige noot
        # houdt aan. Dan elk akkoord één uitklinktijd vóór het volgende loslaten (detach): 1 kanaal per stem.
        pad = [e for e in notes if e[0] < 1536]
        keep = []
        for e in pad:
            if e[1] - e[0] < TPB and keep and keep[-1][1] == e[0]:
                keep[-1][1] = e[1]
            else:
                keep.append(list(e))
        gap = release_ticks(int(EXTRA[PAD].rsplit(',', 1)[1]), TPB, BPM)
        for k, e in enumerate(keep):
            nxt = keep[k + 1][0] if k + 1 < len(keep) else 1536
            if e[1] >= nxt - gap:
                e[1] = max(e[0] + 6, nxt - gap)
        notes = keep + [e for e in notes if e[0] >= 1536]
    if i == 4:   # hoorn (A-deel) en contrabas (vanaf maat 16): één uitklinktijd vóór de volgende noot loslaten
        rel = releases(VG)
        starts = sorted(set(e[0] for e in notes))
        for e in notes:
            gap = release_ticks(rel[UPRIGHT if e[0] >= 1536 else 60], TPB, BPM)
            nxt = next((t for t in starts if t > e[0]), None)
            if e[0] >= 288 and nxt is not None and e[1] > nxt - gap:
                e[1] = max(e[0] + 6, nxt - gap)
    if i == 9:   # de fluit-tegenmelodie speelt de draaiers van de lead parallel mee (maat 26 en 30): daar één noot
        for bar in (26, 30):
            grp = [e for e in notes if bar * BAR + 48 <= e[0] < bar * BAR + 64]
            if len(grp) > 1:
                grp[0][1] = max(e[1] for e in grp)
                notes = [e for e in notes if e not in grp[1:]]
    if i == 7:   # celesta-achtsten kort (nootlengte + uitklinktijd <= een achtste): 1 kanaal i.p.v. 2
        for e in notes:
            if e[0] >= 1536:
                e[1] = min(e[1], e[0] + CELESTA_LEN)
    return merge(notes, other, ch)


def split(events):
    """(tick, bericht)-lijst -> noten [start, eind, noot, velocity] + de overige berichten."""
    on, notes, other = {}, [], []
    for t, x in events:
        if x.type == 'note_on' and x.velocity:
            on.setdefault(x.note, []).append((t, x.velocity))
        elif x.type in ('note_on', 'note_off'):
            if on.get(x.note):
                st, v = on[x.note].pop(0)
                notes.append([st, t, x.note, v])
        else:
            other.append((t, x))
    return sorted(notes), other


def merge(notes, other, ch):
    ev = [(t, 1, k, x) for k, (t, x) in enumerate(other)]
    ev += [(s, 2, n, mido.Message('note_on', channel=ch, note=n, velocity=v)) for s, e, n, v in notes]
    ev += [(e, 0, n, mido.Message('note_off', channel=ch, note=n, velocity=0)) for s, e, n, v in notes]
    ev.sort(key=lambda m: m[:3])
    return relative([(t, x) for t, _, _, x in ev])


def note_track(notes, prog, vol, ch, pan=64, ccs=()):
    msgs = [(s, 2, mido.Message('note_on', channel=ch, note=n, velocity=v)) for s, e, n, v in notes]
    msgs += [(e, 0, mido.Message('note_off', channel=ch, note=n, velocity=0)) for s, e, n, v in notes]
    msgs += [(t, 1, mido.Message('control_change', channel=ch, control=c, value=v)) for t, c, v in ccs]
    msgs.sort(key=lambda m: (m[0], m[1]))
    head = [(0, mido.Message('program_change', channel=ch, program=prog)),
            (0, mido.Message('control_change', channel=ch, control=7, value=vol)),
            (0, mido.Message('control_change', channel=ch, control=10, value=pan))]
    return relative(head + [(t, m) for t, _, m in msgs])


def sleigh_bells():
    """Sleebellen op de tellen in het vrolijke deel (maat 16-31), zachte achtsten erbij vanaf maat 24, en een
    korte schudroffel in de laatste maat naar het loopbegin."""
    out = []
    for bar in range(16, 32):
        for beat in range(4):
            t = bar * BAR + beat * TPB
            out.append([t, t + 7, 60, 100 if beat in (0, 2) else 76])
            if bar >= 24:
                out.append([t + TPB // 2, t + TPB // 2 + 6, 60, 46])
    for k, v in ((48, 60), (60, 70), (72, 80), (84, 70)):
        out.append([32 * BAR + k, 32 * BAR + k + 6, 60, v])
    return out


def wind():
    """Windvlagen op het PSG-ruiskanaal: lange noten (trage aanzet/uitklinktijd in de stem) met een langzame CC7-
    zwelling erbovenop; tussen de vlagen stilte. (maat, lengte in maten, toets = kleur van de ruis, sterkte)"""
    gusts = [(1, 3, 50, 20), (7, 2, 53, 16), (11, 3, 49, 20), (19, 2, 52, 14), (27, 3, 50, 18)]
    notes, ccs = [], []
    for bar, length, key, peak in gusts:
        s, e = bar * BAR, (bar + length) * BAR
        notes.append([s, e - TPB, key, 100])
        steps = 12
        for k in range(steps + 1):          # op en neer: sin-vormige zwelling
            import math
            v = int(peak * math.sin(math.pi * k / steps) ** 1.5)
            ccs.append((s + (e - s) * k // steps, 7, max(v, 1)))
    return notes, ccs


def main():
    voicegroup()
    src = mido.MidiFile(SRC)
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = []
    for tick, x in absolute(src.tracks[0]):
        if x.type == 'set_tempo':
            x = x.copy(tempo=int(round(60e6 / BPM)))
        cond.append((tick, x))
    out.tracks.append(relative(cond))
    for i in range(1, len(src.tracks)):
        out.tracks.append(transform(i, src.tracks[i]))
    # stemverdeling: het (omgezette) origineel ligt vast, de nieuwe lagen vullen aan tot MAX_VOICES
    rel = releases(VG)
    preset = []
    for t in out.tracks[1:]:
        preset += ds_occupancy(t, rel, TPB, BPM)
    peak = max(sum(1 for a, b in preset if a <= s < b) for s, _ in preset)
    print('origineel (omgezet): max. %d DirectSound-noten tegelijk' % peak)
    parts = {'sleigh': sleigh_bells()}
    tail = {'sleigh': release_ticks(rel[SLEIGH], TPB, BPM)}
    kept = allocate(parts, ['sleigh'], tail, preset=preset)
    for k in parts:
        lost = len(parts[k]) - len(kept[k])
        print('  %-7s %3d noten, %d vallen weg (%.0f%%)' % (k, len(parts[k]), lost, 100.0 * lost / max(1, len(parts[k]))))
    wn, wcc = wind()
    out.tracks.append(note_track(kept['sleigh'], SLEIGH, 62, 9, 76))
    out.tracks.append(note_track(wn, WIND, 1, 10, 64, wcc))
    for k in ('sleigh',):
        assert kept[k], k
    out.save(OUT)
    print(OUT)


if __name__ == '__main__':
    main()
