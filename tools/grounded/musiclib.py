"""Project Grounded: gedeelde bouwstenen voor muziekscripts (zie tools/grounded/MUZIEK.md).

Hierin zit wat we eerder fout deden, zodat elk nieuw nummer het automatisch goed doet:
  notes_of()   -> noten uit een MIDI-spoor, ontdubbeld (dubbele noten = klik + kanaalroof)
  thin()       -> akkoorden uitdunnen tot n noten (bovenstem of onderstem)
  allocate()   -> stemverdeler: max. MAX_VOICES DirectSound-noten tegelijk, op prioriteit, over de hele nootduur
  Song         -> sporen + tempokaart + loopmarkers wegschrijven als MIDI voor mid2agb
Noten zijn lijsten [start, eind, noot, velocity] in ticks."""
import math, os, re
import mido

MAX_VOICES = 10         # src/m4a.c: 12 DirectSound-kanalen, 2 vrij voor geluidseffecten
PSG_DRUMS = {37, 44, 49, 51, 52, 56, 58, 61, 63}   # rs_drumset: piepjes
DRUM_FIX = {37: 38, 44: 42, 52: 57, 49: 57, 51: 57}


def notes_of(track):
    tick, on, ev = 0, {}, []
    for msg in track:
        tick += msg.time
        if msg.type == 'note_on' and msg.velocity:
            on.setdefault(msg.note, []).append((tick, msg.velocity))
        elif msg.type in ('note_on', 'note_off') and on.get(msg.note):
            s, vel = on[msg.note].pop(0)
            ev.append([s, tick, msg.note, vel])
    return dedupe(ev)


def dedupe(ev):
    seen, out = set(), []
    for e in sorted(ev):
        if (e[0], e[2]) not in seen:
            seen.add((e[0], e[2]))
            out.append(list(e))
    return out


def thin(ev, maxn, keep='top'):
    """Akkoorden uitdunnen tot maxn noten (hoogste of laagste houden); oude noten worden legato afgekapt."""
    out, by_start = [], {}
    for e in ev:
        by_start.setdefault(e[0], []).append(list(e))
    for s in sorted(by_start):
        grp = sorted(by_start[s], key=lambda e: -e[2] if keep == 'top' else e[2])[:maxn]
        active = [o for o in out if o[0] < s < o[1]]
        while len(active) + len(grp) > maxn and active:
            active.pop(0)[1] = s
        out += grp
    return sorted(out)


def detach(ev, gap):
    """Legato-partij: elke noot eindigt `gap` ticks (= de uitklinktijd) vóór de volgende noot in dezelfde partij,
    zodat de release van de vorige noot geen tweede kanaal bezet op het moment dat de nieuwe begint."""
    ev = sorted(ev)
    starts = sorted(set(e[0] for e in ev))
    out = []
    for e in ev:
        nxt = next((t for t in starts if t > e[0]), None)
        end = e[1] if nxt is None else min(e[1], max(e[0] + 6, nxt - gap))
        out.append([e[0], end, e[2], e[3]])
    return out


def allocate(parts, order, tail, drum_len=None, drum_parts=(), max_voices=MAX_VOICES, preset=()):
    """parts: {naam: noten}; order: namen van hoog naar laag. PSG-sporen hier niet in stoppen (tellen niet mee).
    tail = uitklinktijd in ticks (getal, of {naam: ticks} per spoor); drum_len = hoe lang een drumnoot een kanaal
    bezet houdt."""
    busy, res = list(preset), {}   # preset: (start, eind) van noten die al vastliggen (bv. het origineel)
    for name in order:
        kept = []
        t = tail.get(name, 0) if isinstance(tail, dict) else tail    # tail mag per partij (dict)
        for e in parts.get(name, []):
            s = e[0]
            en = (s + drum_len) if (name in drum_parts and drum_len) else e[1] + t
            pts = [s] + [b[0] for b in busy if s < b[0] < en]
            if all(sum(1 for b in busy if b[0] <= p < b[1]) < max_voices for p in pts):
                kept.append(e)
                busy.append((s, en))
        res[name] = kept
    for name in parts:
        res.setdefault(name, parts[name])
    return res


class Song:
    def __init__(self, tpb, base_tempo):
        self.tpb, self.base = tpb, base_tempo
        self.tempo_map = []          # (tick, factor)
        self.loop = None
        self.tracks = []

    def tempo(self, tick, factor):
        self.tempo_map.append((int(tick), factor))

    def add(self, notes, program, volume, channel, pan=None, extra=(), ccs=()):
        """extra: [(tick, mido.Message)] zoals pitchwheel/control_change (BENDR = CC20, MOD = CC1, LFOS = CC21);
        op dezelfde tick komen ze na de note-offs en vóór de note-ons.
        ccs: extra controllers [(tick, controller, waarde)], bv. CC7-automatisering per sectie (dynamiek) of een
        programmawissel (controller 'prog'). mid2agb kent alleen CC7 (VOL), CC10 (PAN) en CC1 (MOD); CC11 doet niets."""
        self.tracks.append((notes, program, volume, channel, pan, list(extra), list(ccs)))

    def save(self, path, end):
        out = mido.MidiFile(type=1, ticks_per_beat=self.tpb)
        cond = mido.MidiTrack()
        ev = [(t, 0, mido.MetaMessage('set_tempo', tempo=int(self.base / f))) for t, f in self.tempo_map]
        if self.loop:
            ev += [(self.loop[0], 1, mido.MetaMessage('marker', text='[')),
                   (self.loop[1], 2, mido.MetaMessage('marker', text=']'))]
        ev.append((end, 3, mido.MetaMessage('end_of_track')))
        last = 0
        for t, _, m in sorted(ev, key=lambda x: (x[0], x[1])):
            if m.type == 'end_of_track':
                break
            cond.append(m.copy(time=t - last))
            last = t
        out.tracks.append(cond)
        for notes, prog, vol, ch, pan, extra, ccs in self.tracks:
            t = mido.MidiTrack()
            t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
            t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
            if pan is not None:
                t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
            # volgorde per tick: note-offs, dan controllers/programma's, dan note-ons
            msgs = ([(s, 2, n, v, None) for s, e, n, v in notes] + [(e, 0, n, 0, None) for s, e, n, v in notes]
                    + [(tk, 1, i, 0, m) for i, (tk, m) in enumerate(extra)] + [(tk, 1, c, v, None) for tk, c, v in ccs])
            # (twee sorteringen zodat bestaande nummers byte-gelijk blijven: Keccles v2 sorteerde met ccs op str(noot))
            msgs.sort(key=(lambda x: (x[0], x[1], str(x[2]))) if ccs else (lambda x: x[:4]))
            last = 0
            for tk, kind, n, v, m in msgs:
                if kind == 1:
                    if m is not None:
                        t.append(m.copy(channel=ch, time=tk - last))
                    elif n == 'prog':
                        t.append(mido.Message('program_change', channel=ch, program=v, time=tk - last))
                    else:
                        t.append(mido.Message('control_change', channel=ch, control=n, value=max(0, min(127, int(v))),
                                              time=tk - last))
                else:
                    t.append(mido.Message('note_on' if kind else 'note_off', channel=ch, note=n,
                                          velocity=max(1, min(127, int(v))) if kind else 0, time=tk - last))
                last = tk
            out.tracks.append(t)
        out.save(path)


def releases(vg):
    """programma -> release-byte uit sound/voicegroups/<vg>.inc (keysplit: 200, PSG: None)."""
    out, prog = {}, 0
    for line in open(os.path.join('sound/voicegroups', vg + '.inc')):
        line = line.strip()
        if not line.startswith('voice_') or line.startswith('voice_group'):
            continue
        m = re.search(r'@\s*(\d+)', line)
        if m:
            prog = int(m.group(1))
        kind = line.split()[0]
        if kind.startswith(('voice_square', 'voice_noise', 'voice_programmable')):
            out[prog] = None
        elif kind.startswith('voice_keysplit_all'):
            out[prog] = None               # drumkit: lengte via drum_len
        elif kind.startswith('voice_keysplit'):
            name = line.split('voicegroup_')[1].split('_keysplit')[0]
            path = os.path.join('sound/voicegroups/keysplits', name + '.inc')
            rel = [int(l.split('@')[0].split(',')[-1]) for l in open(path) if l.strip().startswith('voice_directsound')] \
                if os.path.exists(path) else []
            out[prog] = max(rel) if rel else 200
        else:
            out[prog] = int(line.split('@')[0].split(',')[-1])
        prog += 1
    return out


def release_ticks(rel, tpb, bpm):
    """Ticks tot het volume na de note-off onder 1/16 is (m4a: envelope x rel/256 per frame)."""
    if rel is None:
        return 0
    if rel >= 255:
        return tpb * 4
    frames = math.log(1 / 16) / math.log(max(rel, 1) / 256) if rel > 0 else 1
    return int(frames * tpb * bpm / 3600) + 1


def ds_occupancy(track, rel, tpb, bpm, drum_len=None):
    """(start, eind) per DirectSound-noot van een bestaand spoor, met het instrument dat op dát moment actief is
    (sporen wisselen soms van programma). PSG-noten tellen niet mee; drums (programma 0/127 drumkit) kort."""
    tick, prog, on, out = 0, 0, {}, []
    for x in track:
        tick += x.time
        if x.type == 'program_change':
            prog = x.program
        if x.type == 'note_on' and x.velocity:
            on.setdefault(x.note, []).append((tick, prog))
        elif x.type in ('note_on', 'note_off') and on.get(x.note):
            s, p = on[x.note].pop(0)
            r = rel.get(p, 200)
            if r is None:
                if drum_len:
                    out.append((s, min(tick, s + drum_len)))
                continue
            out.append((s, tick + release_ticks(r, tpb, bpm)))
    return out
