#!/usr/bin/env python3
"""Project Grounded: vier remixes van het Emerald-gymleiderthema (mus_vs_gym_leader.mid), één per gymleider.

Jordi: 'Gymleiders allemaal een remix van het originele gym leader theme, die moet echt duidelijk nog te herkennen
blijven, zelfde melodie, andere instrumenten.' Dus: melodie (spoor 1 en 2), harmonie (bas, spoor 3), vorm en loop
(maat 10-62) van het origineel noot voor noot; alleen de instrumenten, de ritmesectie en (licht) het tempo wisselen.

  647 MUS_GROUNDED_VS_ROXANNE   hard rock power ballad, 188 bpm met half-time drums (voelt als 94), zingende
                                overdrive-leadgitaar, strijkers/piano eronder, powerchords, cleane arpeggio's
  648 MUS_GROUNDED_VS_BRAWLY    nu-metal (Slipknot/Drowning Pool/Stemm), 196 bpm: lage C-powerchords in gesyncopeerde
                                chugs (kick op elke chug), breakdown in het B-deel, galop + dubbele bassdrum in de opbouw
  649 MUS_GROUNDED_VS_WATTSON   gabber/happy hardcore, 176 bpm: vervormde gabberkick op elke tel, supersaw-lead,
                                happy-hardcore-piano, hoover, supersaw-stoten op de achtste 'en', breakdown + roffel
  650 MUS_GROUNDED_VS_FLANNERY  flamenco (rumba flamenca), 196 bpm: nylongitaar met trémolo op lange noten, viool,
                                rasgueado (C-Db-C = de Frygische wending zit al in het origineel), palmas, cajón,
                                castagnetten, fretloze bas

Ronde 2 (Jordi, GBA-instructies per leider; Wattson goedgekeurd en byte-identiek gebleven):
  Roxanne   80s hard rock: Emerald-kit (drum_and_percussion_kick, sd90_solo_snare gegate + PSG-ruistik op 2 en 4),
            Emerald-slapbas, dual lead in tertsen (soms sexten) op twee sporen met de Emerald-distortiongitaar,
            vibrato met pitch bend op lange noten
  Brawly    drop-gestemde chugs (Emerald-distortiongitaar een octaaf omlaag als powerchord-sample, 2 ticks + release
            70) op de off-beats, Emerald-kick + double-kick in zestienden op de PSG-ruis, PSG-ruis-scratches
            (pitch-bend-sweeps) op elke overgang
  Flannery  GBA-nylongitaar (melodie + rasgueado als snelle opvolgende arpeggio's), palmas = Emerald-snare hoog
            gestemd als rimshot/side stick in zestienden, castagnetten op de PSG-ruis

Het origineel wordt één keer ontleed (Src): noten per spoor met het programma op dat moment, de grondtonen per halve
maat (uit de bas; in maat 2-9 uit de riff), het ritme van de pauken (spoor 8) en de snare (spoor 7). Per leider
bepaalt een functie welk instrument elke noot krijgt en welke begeleiding erbij komt. De PSG-sporen (3x, geen
DirectSound-kanalen) blijven zoals ze zijn, behalve waar een DirectSound-instrument hun partij overneemt.
Stemverdeler: max. 10 DirectSound-noten tegelijk incl. uitklinktijd, melodie eerst (zie MUZIEK.md).
Per leider een eigen voicegroup (vs_gym_leader + extra instrumenten vanaf 91) en een eigen drumkit.
Samples: tools/grounded/gym_samples.py (gym_*).  Gebruik: python3 tools/grounded/gym_remixes.py"""
import math, os, re, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import Song, releases, release_ticks, MAX_VOICES

SRC = 'sound/songs/midi/mus_vs_gym_leader.mid'
SRC_VG = 'vs_gym_leader'
TPB, BAR = 24, 96
S16, S8, BEAT = 6, 12, 24
NBARS = 62
LOOP = (10 * BAR, NBARS * BAR)
SEC = {'intro': (0, 2), 'riff': (2, 10), 'A1': (10, 18), 'C1': (18, 22), 'A2': (22, 30), 'C2': (30, 34),
       'bridge': (34, 37), 'B': (37, 48), 'pedal': (48, 54), 'build': (54, 62)}
FIRST = 91                       # vs_gym_leader heeft stemmen 0-90; eigen instrumenten vanaf hier
NOISE_HAT = 84                   # toets op het PSG-ruiskanaal (hihat)
PIANO, STRINGS, FBASS = 1, 48, 33   # programma's in vs_gym_leader (alleen om het origineel te lezen)


def sec(t):
    b = t // BAR
    return next(k for k, (a, z) in SEC.items() if a <= b < z)


def in_bars(t, a, z):
    return a * BAR <= t < z * BAR


def place(pc, lo):
    """Toonhoogte met toonklasse pc in [lo, lo + 11]."""
    return lo + (pc - lo) % 12


# ---- het origineel ---------------------------------------------------------------------------------------------------
class Src:
    def __init__(self):
        m = mido.MidiFile(SRC)
        assert m.ticks_per_beat == TPB
        self.notes, self.other = {}, {}
        for i in range(1, 9):
            tick, prog, on, ev, other, seen = 0, 0, {}, [], [], set()
            for x in m.tracks[i]:
                tick += x.time
                if x.type == 'program_change':
                    prog = x.program
                if x.type == 'note_on' and x.velocity:
                    on.setdefault(x.note, []).append((tick, x.velocity, prog))
                elif x.type in ('note_on', 'note_off'):
                    if on.get(x.note):
                        s, v, p = on[x.note].pop(0)
                        if (s, x.note) not in seen:          # ontdubbelen
                            seen.add((s, x.note))
                            ev.append([s, tick, x.note, v, p])
                elif not x.is_meta:
                    other.append((tick, x))
            self.notes[i] = sorted(ev)
            self.other[i] = other
        # de riff in maat 2-9: spoor 2 + de stem eronder (spoor 1 in maat 2-5, PSG-spoor 4 in maat 6-9). Een kwart of
        # kwint = powerchord (C5 - Db5 - C5); een terts/tritonus (maat 3, 5, 7: E-G, F-Ab, Bb-Db) blijft losse noten.
        low1 = {s: n for s, e, n, v, p in self.notes[1]}
        low4 = {s: n for s, e, n, v, p in self.notes[4]}
        self.riff, self.riff_notes = [], set()
        for s, e, n, v, p in self.notes[2]:
            if in_bars(s, 2, 10):
                lo = low1.get(s) if s < 6 * BAR else low4.get(s)
                iv = (n - lo) % 12
                if iv in (5, 7):
                    self.riff.append((s, e, n % 12 if iv == 5 else lo % 12))
                else:
                    self.riff_notes.add(s)
        # grondtonen: maat 2-9 uit de powerchords van de riff (anders C), daarna per halve maat de laagste basnoot
        ch = [(0, 0), (BAR, 8)] + [(2 * BAR, 0)] + [(s, pc) for s, e, pc in self.riff]
        for h in range(20, NBARS * 2):
            bn = [n for s, e, n, v, p in self.notes[3] if h * 48 <= s < h * 48 + 48]
            ch.append((h * 48, min(bn) % 12))
        self.changes = sorted(ch)

    def root(self, t):
        return [pc for tk, pc in self.changes if tk <= t][-1]

    def bar_hits(self, track, bar):
        """Aanslagen (ticks binnen de maat) van spoor 7 (snare) of 8 (pauken) in deze maat."""
        return sorted(s - bar * BAR for s, e, n, v, p in self.notes[track] if bar * BAR <= s < bar * BAR + BAR)


# ---- instrumenten en voicegroup ----------------------------------------------------------------------------------------
class Kit:
    def __init__(self, name, voices):
        """voices: [(naam, regel)] vanaf toets 36."""
        self.name, self.voices = name, voices
        self.key = {nm: 36 + i for i, (nm, _) in enumerate(voices)}
        self.rel = {36 + i: int(line.rsplit(',', 1)[1]) for i, (nm, line) in enumerate(voices)}

    def write(self, leader):
        out = ['@ Project Grounded: drumkit voor de gymleider-remix van %s (tools/grounded/gym_remixes.py).' % leader,
               '@ ' + ', '.join('%d %s' % (self.key[nm], nm) for nm, _ in self.voices) + '. Alles DirectSound.',
               'voice_group %s_drumset, 36' % self.name]
        out += ['\t' + line for _, line in self.voices]
        open('sound/voicegroups/drumsets/%s.inc' % self.name, 'w').write('\n'.join(out) + '\n')


class Voicegroup:
    def __init__(self, name, kit, insts):
        """insts: {naam: [(label-toets, regel)]}; een instrument met meer samples krijgt een programma per sample."""
        self.name, self.kit = name, kit
        self.lines = ['voice_keysplit_all voicegroup_%s_drumset' % kit.name]
        self.progs = {}
        self.rel = dict(releases(SRC_VG))
        p = FIRST + 1
        for nm, samples in insts.items():
            self.progs[nm] = []
            for key, line in samples:
                self.progs[nm].append((key, p))
                self.lines.append(line)
                self.rel[p] = int(line.rsplit(',', 1)[1]) if line.startswith('voice_directsound') else None
                p += 1
        assert p <= 128, p
        self.kitprog = FIRST

    def prog(self, inst, n=60):
        return min(self.progs[inst], key=lambda kp: (abs(kp[0] - n), -kp[0]))[1]

    def write(self, leader, desc):
        src = [l for l in open('sound/voicegroups/%s.inc' % SRC_VG).read().split('\n')
               if l.strip().startswith('voice_') and not l.strip().startswith('voice_group')]
        assert len(src) == FIRST, len(src)
        out = ['@ Project Grounded: voicegroup_vs_gym_leader + instrumenten voor de remix van %s.' % leader,
               '@ Gegenereerd door tools/grounded/gym_remixes.py. %s' % desc,
               'voice_group %s' % self.name] + src
        out += ['\t%s  @ %d' % (l, FIRST + i) for i, l in enumerate(self.lines)]
        open('sound/voicegroups/%s.inc' % self.name, 'w').write('\n'.join(out) + '\n')


def ds(sample, rel, sustain=255, decay=0, attack=255):
    return 'voice_directsound 60, 0, DirectSoundWaveData_%s, %d, %d, %d, %d' % (sample, attack, decay, sustain, rel)


def dk(sample, rel, pan=64):
    return 'voice_directsound_no_resample 60, %d, DirectSoundWaveData_%s, 255, 0, 255, %d' % (pan, sample, rel)


def gen3(piano_rel=150, strings_rel=180, bass_rel=120):
    """De Gen 3-piano, -strijkers en -bas van het origineel als losse samples (zelfde samples als de keysplits van
    vs_gym_leader), maar met een kortere uitklinktijd: de vanilla-piano (release 221-239) klinkt ±50 ticks na en
    bezette in de intro-loop tien kanalen."""
    return {'piano': [(k, ds('sc88pro_piano1_%d' % k, piano_rel, 0, 250)) for k in (48, 60, 72, 84)],
            'strings': [(k, ds('sc88pro_string_ensemble_%d' % k, strings_rel)) for k in (60, 72, 84)],
            'fbass': [(60, ds('sc88pro_fingered_bass', bass_rel))]}


# ---- partijen -------------------------------------------------------------------------------------------------------
class Part:
    def __init__(self, name, track, ds=True):
        self.name, self.track, self.ds = name, track, ds
        self.notes = []            # [start, eind, noot, velocity, programma]
        self.ccs = []              # (tick, controller, waarde)
        self.bends = []            # (tick, mido-pitchwheel)

    def add(self, s, e, n, v, p):
        self.notes.append([int(s), int(e), int(n), max(1, min(127, int(v))), p])


def legato(notes, gap, keep=0.6):
    """Legato-partij: elke noot laat `gap` ticks (uitklinktijd) vóór de volgende aanslag los, maar houdt minstens
    `keep` van zijn lengte (korte noten worden dus niet staccato)."""
    notes = sorted(notes)
    starts = sorted(set(n[0] for n in notes))
    for x in notes:
        nxt = next((t for t in starts if t > x[0]), None)
        if nxt is not None and x[1] > nxt - gap:
            x[1] = max(x[0] + max(3, int((x[1] - x[0]) * keep)), nxt - gap)
            x[1] = min(x[1], max(x[0] + 3, nxt))
    return notes


def tremolo(notes, step=S16, min_len=36, pattern=(1.0, 0.78, 0.88, 0.82), length=2):
    """Flamenco-trémolo: lange noten worden herhaald in zestienden (p-a-m-i)."""
    out = []
    for s, e, n, v, p in notes:
        if e - s < min_len:
            out.append([s, e, n, v, p])
            continue
        k = 0
        for t in range(s, e - step // 2, step):
            out.append([t, min(t + length, e), n, v * pattern[k % len(pattern)], p])
            k += 1
    return out


def vibrato(part, depth, delay=18, min_len=36, speed=20):
    """Vertraagde vibrato (MOD, CC1) op lange noten; LFO-snelheid via CC21."""
    part.ccs.append((0, 21, speed))
    part.ccs.append((0, 1, 0))
    notes = sorted(part.notes)
    for i, (s, e, n, v, p) in enumerate(notes):
        nxt = notes[i + 1][0] if i + 1 < len(notes) else None
        if e - s >= min_len:
            part.ccs.append((s + delay, 1, depth))
            off = e if nxt is None or nxt > e else nxt
            part.ccs.append((off, 1, 0))


def allocate(parts, vg, max_voices=MAX_VOICES, bpm=196):
    """Gretig per partij (in volgorde van belang): een noot blijft als er over zijn hele duur (incl. uitklinktijd)
    minder dan max_voices DirectSound-noten klinken. Drumnoten: de eigen lengte + de release van de kitstem."""
    busy, report = [], []
    for part in parts:
        if not part.ds:
            continue
        kept = []
        for x in sorted(part.notes):
            s, e, n, v, p = x
            if p == vg.kitprog:
                tail = release_ticks(vg.kit.rel[n], TPB, bpm) + 1
                en = s + min(e - s, 2 * TPB) + tail
            else:
                en = e + release_ticks(vg.rel.get(p, 200), TPB, bpm) + 1
            pts = [s] + [b[0] for b in busy if s < b[0] < en]
            if all(sum(1 for b in busy if b[0] <= q < b[1]) < max_voices for q in pts):
                kept.append(x)
                busy.append((s, en))
        lost = len(part.notes) - len(kept)
        report.append((part.name, len(part.notes), lost))
        part.notes = kept
    return report


def fit(part, vg, bpm, minlen=3):
    """Eén kanaal per partij: elke noot eindigt zo dat noot + uitklinktijd vóór de volgende aanslag klaar is."""
    notes = sorted(part.notes)
    starts = sorted(set(x[0] for x in notes))
    for x in notes:
        nxt = next((t for t in starts if t > x[0]), None)
        if nxt is None:
            continue
        rel = vg.kit.rel[x[2]] if x[4] == vg.kitprog else vg.rel.get(x[4], 200)
        tail = release_ticks(rel, TPB, bpm) + 1
        x[1] = max(x[0] + minlen, min(x[1], nxt - tail))
    part.notes = notes


def no_overlap(notes):
    """Dezelfde toonhoogte mag in één spoor niet overlappen (anders kapt de engine/lint)."""
    notes = sorted(notes)
    last = {}
    for x in notes:
        if x[2] in last and last[x[2]][1] > x[0]:
            last[x[2]][1] = x[0]
        last[x[2]] = x
    return [x for x in notes if x[1] > x[0]]


# ---- ronde 2: pitch bend, PSG-ruis, Emerald-drums ---------------------------------------------------------------------
def dkp(sample, key, rel, pan=64, decay=0, sustain=255):
    """Drumkitregel die de sample op toets `key` speelt (60 = eigen hoogte), met eigen envelope."""
    return 'voice_directsound %d, %d, DirectSoundWaveData_%s, 255, %d, %d, %d' % (key, pan, sample, decay, sustain, rel)


def pw(c):
    """Pitch bend in stappen van 1/64 x BENDR (m4a: -64..63)."""
    return mido.Message('pitchwheel', pitch=max(-8192, min(8191, int(c) * 128)))


def bend_vibrato(part, bpm, cents=26, hz=5.6, delay=10, ramp=14, min_len=30, tail=12, bendr=1):
    """Vibrato met pitch bend (Jordi: 'Pitch Bend voor vibrato op lange noten'): vertraagd, ingefaded, door tot in de
    uitklinktijd; de bend staat weer op 0 vóór de volgende aanslag (zelfde tick, vóór de note-on)."""
    part.ccs.append((0, 20, bendr))
    tps = bpm * TPB / 60.0
    notes = sorted(part.notes)
    for i, (s, e, n, v, p) in enumerate(notes):
        nxt = notes[i + 1][0] if i + 1 < len(notes) else None
        if e - s < min_len:
            continue
        stop = e + tail if nxt is None else min(nxt, e + tail)
        last = 0
        for t in range(s + delay, stop):
            amp = min(1.0, (t - s - delay) / float(ramp)) * cents / 100.0 * 64 / bendr
            c = int(round(amp * math.sin(2 * math.pi * hz * (t - s - delay) / tps)))
            if c != last:
                part.bends.append((t, pw(c)))
                last = c
        if last != 0:
            part.bends.append((stop, pw(0)))


def noise_sweep(part, prog, t, length, keys, vel, key=56, bendr=24):
    """PSG-ruis-sweep (scratch/whoosh): één ruisnoot met een pitch-bend-curve door `keys` (halve tonen t.o.v. `key`,
    lineair tussen de punten). Daarna staat de bend weer op 0. BENDR moet op het spoor `bendr` zijn."""
    part.add(t, t + length, key, vel, prog)
    pts = len(keys) - 1
    last = None
    for k in range(length):
        x = k / float(length) * pts
        i = min(int(x), pts - 1)
        semis = keys[i] + (keys[i + 1] - keys[i]) * (x - i)
        c = int(round(semis * 64.0 / bendr))
        if c != last:
            part.bends.append((t + k, pw(c)))
            last = c
    part.bends.append((t + length, pw(0)))


# ---- gedeelde begeleiding ------------------------------------------------------------------------------------------------
def psg_copy(src, i, vol, drop=None, name=None):
    """PSG-spoor van het origineel 1-op-1 (noten, programmawissels, XCMD's, pan, MOD), zonder de noten waar
    drop(noot) waar is (die partij speelt dan een DirectSound-instrument)."""
    part = Part(name or 'psg%d' % i, name or 'psg%d' % i, ds=False)
    part.notes = [list(x) for x in src.notes[i] if not (drop and drop(x))]
    part.extra = [(t, m) for t, m in src.other[i] if not (m.type == 'control_change' and m.control == 7)]
    part.first_prog = next(m.program for t, m in src.other[i] if m.type == 'program_change')
    part.vol = vol
    return part


def write_song(path, bpm, parts, vols, pans):
    song = Song(TPB, int(round(60e6 / bpm)))
    song.tempo(0, 1.0)
    song.loop = LOOP
    tracks = []
    for p in parts:
        if p.track not in tracks:
            tracks.append(p.track)
    assert len(tracks) <= 16, tracks
    for ch, tr in enumerate(tracks):
        ps = [p for p in parts if p.track == tr]
        if hasattr(ps[0], 'extra'):                       # PSG-kopie
            p = ps[0]
            song.add([x[:4] for x in sorted(p.notes)], p.first_prog, p.vol, ch, None, p.extra)
            continue
        notes = sorted(x for p in ps for x in p.notes)
        notes = no_overlap(notes)
        ccs, cur = [], None
        for s, e, n, v, prog in notes:
            if prog != cur:
                ccs.append((s, 'prog', prog))
                cur = prog
        for p in ps:
            ccs += p.ccs
        first = notes[0][4] if notes else 0
        ccs = [c for c in ccs if not (c[0] == notes[0][0] and c[1] == 'prog')] if notes else ccs
        bends = sorted((b for p in ps for b in p.bends), key=lambda b: b[0])
        song.add([x[:4] for x in notes], first, vols.get(tr, 100), ch, pans.get(tr, 64), bends, ccs)
    song.save(path, NBARS * BAR)


# ---- per leider ---------------------------------------------------------------------------------------------------------
def melody_parts(src, vg, route1, route2):
    """Spoor 1 en 2 noot voor noot; route(noot) -> (partijnaam, instrument) of None (wegvalt: andere partij speelt
    hetzelfde, bv. de riff als powerchord)."""
    parts = {}
    for i, route in ((1, route1), (2, route2)):
        for s, e, n, v, p in src.notes[i]:
            r = route(s, n, p)
            if r is None:
                continue
            pname, inst = r
            prog = inst if isinstance(inst, int) else vg.prog(inst, n)
            parts.setdefault(pname, Part(pname, pname)).add(s, e, n, v, prog)
    return parts


def riff_onsets(src):
    """Maat 2-9: de powerchord-aanslagen van de riff (C5 - Db5 - C5 op 0, 36 en 72): (start, eind, grondtoon)."""
    return src.riff


def riff_route(src, s, track):
    """Maat 2-9: noten van de riff die geen powerchord zijn (tertsen/tritonus) blijven losse noten; spoor 1 telt
    alleen in maat 2-5 mee (in 6-9 speelt het lange noten)."""
    if s in src.riff_notes and (track == 2 or s < 6 * BAR):
        return True
    return False


SC_MAJ = {0, 2, 4, 5, 7, 9, 10}      # A- en C-delen: C-mixolydisch (= F-groot)
SC_PHR = {0, 1, 3, 5, 7, 8, 10}      # B-deel: C-frygisch


def diatonic(n, scale, steps):
    """`steps` toonladdertrappen omlaag (negatief) of omhoog vanaf n (n moet in de toonladder liggen)."""
    if n % 12 not in scale:
        return None
    k, cnt = n, 0
    while cnt < abs(steps):
        k += -1 if steps < 0 else 1
        if k % 12 in scale:
            cnt += 1
    return k


def twin_harmony(src, s, e, n, scale, tracks=(1, 3, 4, 5, 6)):
    """Tweede leadgitaar: diatonische terts onder de melodie (80s dual lead). Vormt die een kleine secunde/none of
    grote septiem met wat de rest van het origineel op dat moment speelt, dan de sext eronder (omkering van de terts,
    in twin leads gebruikelijk)."""
    third, sixth = diatonic(n, scale, -2), diatonic(n, scale, -5)
    if third is None:
        return None
    other = [m for i in tracks for a, b, m, v, p in src.notes[i] if a < e and b > s]
    clash = lambda h: sum(1 for m in other if (h - m) % 12 in (1, 11))
    return third if clash(third) <= clash(sixth) else sixth


def roxanne(src):
    """Ronde 2 (Jordi: '80s Hard Rock'): Emerald-drums (drum_and_percussion_kick, sd90_solo_snare = de rock-snare,
    gegate) + PSG-ruistik op 2 en 4 (gated snare), Emerald-slapbas, dual lead in tertsen op twee DirectSound-sporen
    met de Emerald-distortiongitaar (sd90_classical_distortion_guitar_high) en pitch-bend-vibrato op lange noten."""
    kit = Kit('gym_roxanne', [('kick', dk('drum_and_percussion_kick', 170)),
                              ('snare', dk('sd90_solo_snare', 90)),
                              ('hat', 'voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_close_hihat, '
                                      '255, 127, 0, 120'),
                              ('crash', 'voice_directsound_no_resample 60, 54, DirectSoundWaveData_trinity_cymbal_crash, '
                                        '255, 235, 0, 165'),
                              ('tom_lo', dkp('sd90_ambient_tom', 64, 180, 44)),
                              ('tom_mid', dkp('sd90_ambient_tom', 68, 180, 64)),
                              ('tom_hi', dkp('sd90_ambient_tom', 72, 180, 84))])
    vg = Voicegroup('grounded_gym_roxanne', kit, dict(gen3(), **{
        'lead': [(60, ds('sd90_classical_distortion_guitar_high', 165))],
        'power': [(45, ds('gym_rox_power', 180))],
        'clean': [(k, ds('gym_rox_clean_%d' % k, 160)) for k in (60, 72)],
        'slap': [(60, 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_slap_bass, 255, 235, 128, 99')],
        'gate': [(60, 'voice_noise 60, 0, 0, 0, 0, 15, 0')],
    }))
    K = kit.key

    def r2(s, n, p):
        b = s // BAR
        if 2 <= b < 10:                                  # riff -> powerchords (tertsen: losse gitaarnoten)
            return ('lead2', 'lead') if riff_route(src, s, 2) else None
        if p == PIANO and b >= 2:
            return ('piano', 'piano')                    # brug: de piano blijft
        if b >= 54:
            return ('strings', 'strings')
        return ('lead', 'lead')

    def r1(s, n, p):
        b = s // BAR
        if b < 2:
            return ('lead2', 'lead')                     # intro: tweede gitaar speelt de chromatische loop
        if 2 <= b < 6:
            return ('lead2', 'lead') if riff_route(src, s, 1) else None
        if p == PIANO:
            return ('piano', 'piano')
        return ('strings', 'strings')

    mp = melody_parts(src, vg, r1, r2)
    lead, lead2, strings, piano = mp['lead'], mp['lead2'], mp['strings'], mp['piano']
    lead.notes = legato(lead.notes, 9)
    strings.notes = legato(strings.notes, 13)
    vibrato(strings, 3)

    # dual lead: gitaar 2 een terts (soms sext) onder de melodie, zelfde ritme, eigen spoor
    twin = Part('twin', 'twin')
    for s, e, n, v, p in lead.notes:
        sc = sec(s)
        scale = SC_MAJ if sc in ('A1', 'C1', 'A2', 'C2') else SC_PHR if sc == 'B' else None
        h = twin_harmony(src, s, e, n, scale) if scale else None
        if h is not None:
            twin.add(s, e, h, v * 0.92, vg.prog('lead'))
    bend_vibrato(lead, 188, cents=28, hz=5.6)
    bend_vibrato(twin, 188, cents=24, hz=5.1, delay=13)

    power = Part('power', 'power')
    pw_ = lambda pc: place(pc, 41)                        # F2..E3 rond de A2-sample
    for s, e, pc in riff_onsets(src):
        power.add(s, s + 20, pw_(pc), 112, vg.prog('power'))
    for b in range(10, NBARS):
        sc = sec(b * BAR)
        if sc == 'bridge':
            continue
        if sc == 'build':                                  # opbouw: powerchord-achtsten, crescendo
            for k in range(8):
                t = b * BAR + k * S8
                power.add(t, t + 8, pw_(src.root(t)), 84 + (b - 54) * 4 + (12 if k % 2 == 0 else 0), vg.prog('power'))
            continue
        halves = (0, 48) if sc in ('C1', 'C2') else (0,) if sc != 'pedal' else ((0,) if b % 2 == 0 else ())
        span = 2 * BAR if sc == 'pedal' else BAR
        for h in halves:
            t = b * BAR + h
            if h == 0 and sc != 'pedal' and 48 not in halves and src.root(b * BAR + 48) != src.root(t):
                halves = halves + (48,)                   # grondtoon wisselt halverwege de maat: opnieuw aanslaan
            nxt = [c for c, _ in src.changes if t < c < b * BAR + span and src.root(c) != src.root(t)]
            end = nxt[0] if nxt else b * BAR + span
            power.add(t, end - 2, pw_(src.root(t)), 104 if sc in ('C1', 'C2', 'B', 'pedal') else 86, vg.prog('power'))
            if h == 0 and 48 in halves and sc not in ('C1', 'C2'):
                t2 = b * BAR + 48
                power.add(t2, b * BAR + BAR - 2, pw_(src.root(t2)), 98, vg.prog('power'))
    power.notes = legato(power.notes, 10)

    clean = Part('clean', 'clean')
    arps = lambda x: sec(x[0]) in ('C1', 'C2', 'build')
    for s, e, n, v, p in src.notes[4]:
        if arps([s]):
            clean.add(s, s + 11, n, 92, vg.prog('clean', n))
    psg4 = psg_copy(src, 4, 70, drop=arps)
    psg5 = psg_copy(src, 5, 64)
    psg6 = psg_copy(src, 6, 72)

    bass = Part('bass', 'bass')                            # Emerald-slapbas (ronkt), noten van spoor 3
    for s, e, n, v, p in src.notes[3]:
        bass.add(s, e - 1, n, 116 if s % BEAT == 0 else 104, vg.prog('slap'))

    kick, snare, hats, cym, toms = (Part(n, 'drums') for n in ('kick', 'snare', 'hats', 'cym', 'toms'))
    hats.track = cym.track = 'cym'
    gate = Part('gate', 'gate', ds=False)                 # PSG-ruis: de 'gated reverb'-tik op 2 en 4
    kp, gp = vg.kitprog, vg.prog('gate')

    def d(part, t, key, v, ln=12):
        part.add(t, t + ln, K[key], v, kp)

    def snare_hit(t, v):
        d(snare, t, 'snare', v, 9)                         # sd90_solo_snare na ±120 ms afgekapt = gated
        gate.add(t, t + 8, 69, min(127, v), gp)
    fills = {9: 48, 17: 48, 21: 72, 29: 48, 33: 48, 36: 48, 47: 48, 53: 0, 61: 48}
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        timp, sn = src.bar_hits(8, b), src.bar_hits(7, b)
        fill = fills.get(b)
        cut = lambda t: fill is None or t < fill
        if sc == 'intro':
            for t in timp:
                d(toms, t0 + t, 'tom_lo', 120, 16)
            if b == 0:
                d(cym, t0, 'crash', 110, 48)
            for t in sn:
                snare_hit(t0 + t, 120)
            continue
        if sc == 'bridge':                                 # brug: half-time, snare op 3
            for t in timp:
                if t != 48:
                    d(kick, t0 + t, 'kick', 120 if t == 0 else 104)
            if cut(48):
                snare_hit(t0 + 48, 104)
            for k in range(4):
                if cut(k * BEAT):
                    d(hats, t0 + k * BEAT, 'hat', 84 if k % 2 == 0 else 56, 3)
        else:                                              # 80s hard rock: kick 1 en 3 (+ pauken), snare 2 en 4
            sn2 = sorted(set(sn) | {24, 72}) if sc in ('riff', 'build') else (24, 72)
            for t in sorted(set(timp) | {0, 48}):
                if cut(t) and t not in sn2:
                    d(kick, t0 + t, 'kick', 122 if t in (0, 48) else 106)
            for t in sn2:
                if cut(t):
                    snare_hit(t0 + t, 122 if sc != 'pedal' else 100 + (b - 48) * 4)
            for k in range(8):
                if cut(k * S8):
                    d(hats, t0 + k * S8, 'hat', 96 if k % 2 == 0 else 66, 3)
        if b in (2, 6, 10, 18, 22, 30, 37, 41, 48, 50, 52, 54, 58):
            d(cym, t0, 'crash', 112, 48)
        if fill is not None:                               # tomroffel naar de volgende sectie
            seq = ['tom_hi', 'tom_hi', 'tom_mid', 'tom_mid', 'tom_lo', 'tom_lo', 'snare', 'snare'] * 2
            n = (BAR - fill) // S16
            for k in range(n):
                key = seq[len(seq) - n + k] if n <= len(seq) else seq[k % len(seq)]
                d(toms if key.startswith('tom') else snare, t0 + fill + k * S16, key, 96 + k * 3, S16)
    for prt in (power, bass, kick, snare, toms, hats, clean):
        fit(prt, vg, 188)
    order = [lead, power, kick, snare, bass, twin, lead2, strings, piano, cym, clean, toms, hats]
    tracks = dict(vols={'lead': 118, 'twin': 100, 'lead2': 96, 'power': 84, 'strings': 70, 'piano': 92, 'bass': 100,
                        'drums': 112, 'cym': 82, 'clean': 74, 'gate': 50},
                  pans={'lead': 58, 'twin': 72, 'lead2': 52, 'power': 64, 'strings': 76, 'piano': 58, 'bass': 64,
                        'drums': 64, 'cym': 70, 'clean': 44, 'gate': 64})
    return dict(leader='Roxanne', key='roxanne', bpm=188, vg=vg, kit=kit, order=order, psg=[psg4, psg5, psg6, gate],
                desc='91 kit (drumsets/gym_roxanne.inc: Emerald-kick/-snare/-hihat/-crash/-toms), daarna Emerald-'
                     'distortiongitaar (dual lead), powerchord (A2), cleane gitaar, Emerald-slapbas, PSG-ruis (gated snare).',
                **tracks)


def brawly(src):
    """Ronde 2 (Jordi: 'Nu-Metal / Bro-Metal'): de Emerald-distortiongitaar een octaaf omlaag (drop-tuning,
    gym_bra_epower) in extreem korte chugs op de off-beats, de Emerald-kick (drum_and_percussion_kick) met een
    double-kick in zestienden op het PSG-ruiskanaal, en scratches (PSG-ruis-sweeps + de scratch-sample) op de
    overgangen."""
    kit = Kit('gym_brawly', [('kick', dk('drum_and_percussion_kick', 150)), ('snare', dk('gym_bra_snare', 170)),
                             ('hat', dk('gym_bra_hat', 120)), ('china', dk('gym_bra_china', 200)),
                             ('crash', dk('gym_bra_crash', 205)), ('tom_lo', dk('gym_bra_tom_41', 170, 54)),
                             ('tom_mid', dk('gym_bra_tom_45', 170, 64)), ('tom_hi', dk('gym_bra_tom_48', 170, 74)),
                             ('scratch', dk('gym_bra_scratch', 140))])
    vg = Voicegroup('grounded_gym_brawly', kit, dict(gen3(), **{
        'lead': [(k, ds('gym_bra_lead_%d' % k, 170)) for k in (60, 72, 84)],
        'lead2': [(k, ds('gym_bra_lead2_%d' % k, 170)) for k in (60, 72, 84)],
        'chug': [(36, ds('gym_bra_epower', 70))],         # staccato: korte noot + bijna geen uitklinktijd
        'power': [(36, ds('gym_bra_epower', 160))],
        'bass': [(36, ds('gym_bra_bass', 120))],
        'nkick': [(60, 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0')],     # PSG-ruis: double-kick-tik
        'nsweep': [(60, 'voice_noise 60, 0, 0, 0, 0, 15, 0')],       # PSG-ruis: scratch/sweep (aangehouden)
    }))
    K = kit.key

    def r2(s, n, p):
        b = s // BAR
        if 2 <= b < 10:
            return ('lead2', 'lead2') if riff_route(src, s, 2) else None
        if p == PIANO and b >= 2:
            return ('piano', 'piano')                    # griezelpiano in de brug (nu-metal-intro)
        return ('lead', 'lead')

    def r1(s, n, p):
        b = s // BAR
        if 2 <= b < 6:
            return ('lead2', 'lead2') if riff_route(src, s, 1) else None
        if p == PIANO and b >= 34:
            return ('piano', 'piano')
        return ('lead2', 'lead2')

    mp = melody_parts(src, vg, r1, r2)
    lead, lead2, piano = mp['lead'], mp['lead2'], mp['piano']
    lead.notes = legato(lead.notes, 9)
    lead2.notes = legato(lead2.notes, 9)
    vibrato(lead, 5)

    gtr = Part('gtr', 'gtr')
    chug_p, pow_p = vg.prog('chug'), vg.prog('power')
    low = lambda pc: place(pc, 34)                       # A#1..A2: drop-gestemd
    CH = 2                                               # chug = 2 ticks (±25 ms) + release 70: extreem staccato
    riff = riff_onsets(src)
    riff_t = {s for s, e, pc in riff}
    for s, e, n, v, p in src.notes[3]:                   # maat 2-9: de chromatische basriff als chugs, unisono
        if in_bars(s, 2, 10) and s not in riff_t:
            gtr.add(s, s + CH, n, 104, chug_p)
    for s, e, pc in riff:
        gtr.add(s, s + 10, low(pc), 118, pow_p)
    # A: de tel 1 als anker, verder alleen off-beats: elke achtste 'en' + de laatste zestiende ervoor/erna
    PAT_A = (0, 12, 18, 36, 42, 60, 66, 84, 90)
    PAT_B = (0, 6, 12, 30, 36, 54, 60, 78, 84)          # breakdown: half-time, gesyncopeerd
    GALLOP = (0, 12, 18, 24, 36, 42, 48, 60, 66, 72, 84, 90)
    kick_t = []
    for b in range(10, NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        if sc in ('A1', 'A2'):
            for k in PAT_A:
                t = t0 + k
                gtr.add(t, t + CH, low(src.root(t)), 118 if k == 0 else 112 if k % 24 == 12 else 96, chug_p)
                if k % 24 != 18:
                    kick_t.append(t)
        elif sc in ('C1', 'C2'):
            for h in (0, 48):
                t = t0 + h
                gtr.add(t, t + 40, low(src.root(t)), 116, pow_p)
        elif sc == 'bridge':
            hits = (0, 36) if b < 36 else (0,)
            for k in hits:
                t = t0 + k
                gtr.add(t, t + 22, low(src.root(t)), 118, pow_p)
                kick_t.append(t)
        elif sc == 'B':
            for k in PAT_B:
                t = t0 + k
                gtr.add(t, t + CH, low(src.root(t)), 120 if k in (0, 36, 60) else 100, chug_p)
                kick_t.append(t)
        elif sc == 'pedal':
            for k in range(16):                           # tremolo-chugs in zestienden, crescendo
                t = t0 + k * S16
                gtr.add(t, t + CH, low(src.root(t)), 70 + (b - 48) * 8 + (10 if k % 4 == 0 else 0), chug_p)
        elif sc == 'build':
            pat = GALLOP if b < 61 else (0, 12, 24)
            for k in pat:
                t = t0 + k
                gtr.add(t, t + CH, low(src.root(t)), 118 if k % 24 == 0 else 104, chug_p)

    bass = Part('bass', 'bass')
    for s, e, n, v, p in src.notes[3]:
        bass.add(s, e - 1, n, 112, vg.prog('bass'))

    psg4 = psg_copy(src, 4, 56)
    psg5 = psg_copy(src, 5, 56)
    psg6 = psg_copy(src, 6, 64)
    noise = Part('noise', 'noise', ds=False)
    noise.ccs.append((0, 20, 24))                         # BENDR 24 voor de sweeps
    nk, ns = vg.prog('nkick'), vg.prog('nsweep')

    kick, snare, hats, cym, toms, fx = (Part(n, 'drums') for n in ('kick', 'snare', 'hats', 'cym', 'toms', 'fx'))
    hats.track = cym.track = fx.track = 'cym'
    kp = vg.kitprog

    def d(part, t, key, v, ln=10):
        part.add(t, t + ln, K[key], v, kp)

    def dkick(t, v, upto=BAR):
        """Double-kick: PSG-ruistik op elke zestiende (DS-kick speelt alleen de achtsten)."""
        for k in range(0, upto, S16):
            noise.add(t + k, t + k + 2, 44, v if k % S8 == 0 else v - 14, nk)
    fills = {9: 72, 17: 72, 21: 72, 29: 72, 33: 48, 47: 48, 53: 48, 61: 72}
    # scratches op de overgangen: (maat, begin in de maat, lengte, curve in halve tonen)
    WIKKA = (0, 16, -8, 14, -10, 18, 0)
    SCR = {9: (72, 24, WIKKA), 17: (78, 18, (0, 14, -6, 16, 0)), 21: (72, 24, WIKKA), 29: (78, 18, (0, 14, -6, 16, 0)),
           33: (48, 48, (-20, 20, -12, 16, -6, 22)), 36: (72, 24, WIKKA), 47: (60, 36, (-18, 20, -10, 18, -4, 22)),
           53: (48, 48, (-22, 22)), 61: (72, 24, WIKKA)}
    for t in kick_t:
        d(kick, t, 'kick', 118, 6)
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        timp, sn = src.bar_hits(8, b), src.bar_hits(7, b)
        fill = fills.get(b)
        cut = lambda t: fill is None or t < fill
        if sc == 'intro':
            for t in timp:
                d(toms, t0 + t, 'tom_lo', 120, 12)
            for t in sn:
                d(snare, t0 + t, 'snare', 124)
            if b == 0:
                d(cym, t0, 'china', 110, 48)
            continue
        if sc == 'riff':
            for t in timp:
                d(kick, t0 + t, 'kick', 120, 6)
            for t in sn:
                if cut(t):
                    d(snare, t0 + t, 'snare', 120)
            for k in range(8):
                if cut(k * S8):
                    d(hats, t0 + k * S8, 'hat', 90 if k % 2 == 0 else 62, 3)
        elif sc in ('A1', 'A2'):
            for t in (24, 72):
                if cut(t):
                    d(snare, t0 + t, 'snare', 124)
            for k in range(8):
                if cut(k * S8):
                    d(hats, t0 + k * S8, 'hat', 88 if k % 2 == 0 else 60, 3)
        elif sc in ('C1', 'C2'):
            for k in range(8):
                if cut(k * S8):
                    d(kick, t0 + k * S8, 'kick', 116, 6)
            dkick(t0, 52, fill or BAR)
            for t in (24, 72):
                if cut(t):
                    d(snare, t0 + t, 'snare', 124)
            d(cym, t0, 'crash', 108, 40)
            if cut(48):
                d(cym, t0 + 48, 'china', 96, 30)
        elif sc == 'bridge':
            for k in ((0, 36) if b < 36 else (0,)):
                d(cym, t0 + k, 'china' if k else 'crash', 110, 30)
            if b == 36:
                d(fx, t0 + 30, 'scratch', 112, 26)
        elif sc == 'B':
            d(snare, t0 + 48, 'snare', 126, 14)
            for k in range(4):
                if cut(k * BEAT):
                    d(cym if b >= 40 else hats, t0 + k * BEAT, 'china' if b >= 40 else 'hat', 92 if b >= 40 else 84,
                      20 if b >= 40 else 3)
        elif sc == 'pedal':
            for k in range(8):
                if cut(k * S8):
                    d(kick, t0 + k * S8, 'kick', 96 + (b - 48) * 4, 6)
            if b >= 52:
                dkick(t0, 40 + (b - 52) * 8, fill or BAR)
            if b >= 50:
                for t in (24, 72):
                    if cut(t):
                        d(snare, t0 + t, 'snare', 116)
            if b in (48, 50, 52):
                d(cym, t0, 'crash', 110, 48)
        elif sc == 'build':
            for k in range(8):                            # DS-kick op de achtsten, PSG vult de zestienden
                if cut(k * S8) and (b < 61 or k * S8 < 30):
                    d(kick, t0 + k * S8, 'kick', 116 if k % 2 == 0 else 104, 4)
            dkick(t0, 56, (fill or BAR) if b < 61 else 30)
            for t in (24, 72):
                if cut(t):
                    d(snare, t0 + t, 'snare', 124)
            for k in range(4):
                if cut(k * BEAT):
                    d(cym, t0 + k * BEAT, 'china' if k % 2 else 'crash', 88 if k else 110, 20)
            if b == 61:
                d(fx, t0 + 36, 'scratch', 116, 26)
        if b in (2, 6, 10, 22, 37, 54, 58):
            d(cym, t0, 'crash', 116, 48)
        if b == 47:
            d(fx, t0 + 12, 'scratch', 108, 24)
        if b in SCR:
            st, ln, curve = SCR[b]
            noise.notes = [x for x in noise.notes if not (t0 + st <= x[0] < t0 + st + ln)]
            noise_sweep(noise, ns, t0 + st, ln, curve, 92)
        if fill is not None:
            seq = ['snare', 'snare', 'tom_hi', 'tom_hi', 'tom_mid', 'tom_mid', 'tom_lo', 'tom_lo']
            n = (BAR - fill) // S16
            for k in range(n):
                key = seq[len(seq) - n + k] if n <= len(seq) else seq[k % len(seq)]
                d(toms if key.startswith('tom') else snare, t0 + fill + k * S16, key, 100 + k * 3, S16)
    for prt in (gtr, bass, kick, snare, toms, hats):
        fit(prt, vg, 196)
    order = [lead, gtr, kick, snare, bass, lead2, piano, cym, toms, fx, hats]
    return dict(leader='Brawly', key='brawly', bpm=196, vg=vg, kit=kit, order=order, psg=[psg4, psg5, psg6, noise],
                vols={'lead': 118, 'lead2': 90, 'gtr': 104, 'piano': 96, 'bass': 106, 'drums': 116, 'cym': 80,
                      'noise': 64},
                pans={'lead': 64, 'lead2': 54, 'gtr': 64, 'piano': 70, 'bass': 64, 'drums': 64, 'cym': 72, 'noise': 64},
                desc='91 kit (drumsets/gym_brawly.inc, kick = Emerald drum_and_percussion_kick), daarna distortion-lead, '
                     'overdrive-lead2, chug + powerchord (Emerald-distortiongitaar een octaaf omlaag, C2), bas, PSG-ruis '
                     '(double-kick, scratch-sweeps).')


def wattson(src):
    kit = Kit('gym_wattson', [('kick', dk('gym_wat_kick', 150)),
                              ('clap', dk('sc88pro_tr909_hand_clap', 160)),
                              ('hat', dk('unknown_close_hihat', 120)),
                              ('ohat', dk('unknown_open_hihat', 150)),
                              ('crash', dk('trinity_cymbal_crash', 205)),
                              ('snare', dk('gym_wat_snare', 140))])
    vg = Voicegroup('grounded_gym_wattson', kit, dict(gen3(), **{
        'saw': [(k, ds('gym_wat_saw_%d' % k, 170)) for k in (60, 72, 84)],
        'stab': [(55, ds('gym_wat_stab', 140))],
        'hoover': [(48, ds('gym_wat_hoover', 175))],
        'bass': [(36, ds('gym_wat_bass', 130))],
        'noise': [(60, 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0')],
    }))
    K = kit.key

    def r2(s, n, p):
        b = s // BAR
        if 2 <= b < 10:
            return ('hoover', 'hoover')                  # de riff op de hoover (zelfde toonklasse, laag)
        if p == PIANO and b >= 2:
            return ('piano', 'piano')
        return ('lead', 'saw')

    def r1(s, n, p):
        b = s // BAR
        if 48 <= b < 54:
            return ('pad', 'saw')                        # breakdown: lange supersaw-akkoorden
        return ('piano', 'piano')                          # happy-hardcore-piano

    mp = melody_parts(src, vg, r1, r2)
    lead, piano, hov, pad = mp['lead'], mp['piano'], mp['hoover'], mp['pad']
    for x in hov.notes:                                  # hoover: C3-sample, de riff in G2..F#3
        x[2] = place(x[2] % 12, 43)
        x[4] = vg.prog('hoover')
    for x in pad.notes:
        x[4] = vg.prog('saw', x[2])
    lead.notes = legato(lead.notes, 9)
    hov.notes = legato(hov.notes, 9)
    vibrato(lead, 4, delay=24)
    # B-deel: de PSG-orgelpunten (spoor 4: C - Db - Eb) worden een hoover-drone
    pedal = lambda x: sec(x[0]) == 'B'
    for s, e, n, v, p in src.notes[4]:
        if pedal([s]):
            hov.add(s, e - 4, place(n % 12, 43), 104, vg.prog('hoover'))
    hov.track = 'hoover'
    hov.notes = no_overlap(hov.notes)

    stab = Part('stab', 'stab')
    for b in range(2, NBARS):
        sc = sec(b * BAR)
        if sc in ('bridge', 'pedal', 'riff'):
            continue
        for k in (12, 36, 60, 84):
            t = b * BAR + k
            stab.add(t, t + 6, place(src.root(t), 50), 100 if sc != 'B' else 84, vg.prog('stab'))

    bass = Part('bass', 'bass')
    for s, e, n, v, p in src.notes[3]:
        on_beat = (s % BEAT) == 0
        bass.add(s, s + (5 if on_beat else 9), n, 78 if on_beat else 116, vg.prog('bass'))

    psg4 = psg_copy(src, 4, 66, drop=pedal)
    psg5 = psg_copy(src, 5, 66)
    psg6 = psg_copy(src, 6, 74)
    nhat = Part('nhat', 'nhat', ds=False)

    kick, clap, hats, cym, roll = (Part(n, 'drums') for n in ('kick', 'clap', 'hats', 'cym', 'roll'))
    hats.track = cym.track = 'cym'
    kp = vg.kitprog

    def d(part, t, key, v, ln=10):
        part.add(t, t + ln, K[key], v, kp)

    def snare_roll(b, start, step, v0, v1):
        n = (BAR - start) // step
        for k in range(n):
            d(roll, b * BAR + start + k * step, 'snare', v0 + (v1 - v0) * k // max(1, n - 1), min(step, 6))
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        sn = src.bar_hits(7, b)
        if sc == 'intro':
            if b == 0:
                d(cym, t0, 'crash', 110, 48)
                for t in src.bar_hits(8, b):
                    d(kick, t0 + t, 'kick', 116, 12)
            else:
                snare_roll(b, 0, S16, 60, 118)
            continue
        four = sc not in ('bridge', 'pedal') or (sc == 'bridge' and b == 34)
        if four:
            for k in range(4):
                d(kick, t0 + k * BEAT, 'kick', 124, 16)
            if sc == 'B':                                 # hardcore: extra kick op de laatste zestiende
                d(kick, t0 + 90, 'kick', 104, 6)
            for t in sn:
                d(clap, t0 + t, 'clap', 112)
            for k in (12, 36, 60, 84):
                d(hats, t0 + k, 'ohat', 86, 8)
            if sc not in ('riff',):
                for k in range(16):
                    nhat.add(t0 + k * S16, t0 + k * S16 + 2, NOISE_HAT, 64 if k % 4 == 0 else 40, vg.prog('noise'))
        if b in (2, 6, 10, 14, 18, 22, 26, 30, 37, 41, 45, 54, 58):
            d(cym, t0, 'crash', 108, 48)
        if b == 35:
            snare_roll(b, 48, S8, 70, 96)
        if b == 36:
            snare_roll(b, 0, S16, 80, 122)
        if b in (52, 53):
            snare_roll(b, 0, S8 if b == 52 else S16, 60 if b == 52 else 86, 86 if b == 52 else 120)
        if b == 60:
            snare_roll(b, 48, S16, 84, 104)
        if b == 61:
            snare_roll(b, 0, S16, 100, 124)
        if b == 9:
            snare_roll(b, 48, S16, 80, 116)
    for prt in (kick, clap, bass, stab, roll, hats):
        fit(prt, vg, 176)
    order = [kick, lead, hov, clap, bass, piano, pad, stab, cym, roll, hats]
    return dict(leader='Wattson', key='wattson', bpm=176, vg=vg, kit=kit, order=order,
                psg=[psg4, psg5, psg6, nhat],
                vols={'lead': 112, 'hoover': 92, 'piano': 96, 'pad': 80, 'stab': 70, 'bass': 92, 'drums': 118,
                      'cym': 74, 'nhat': 40},
                pans={'lead': 64, 'hoover': 64, 'piano': 56, 'pad': 72, 'stab': 76, 'bass': 64, 'drums': 64,
                      'cym': 68, 'nhat': 64},
                desc='91 kit (drumsets/gym_wattson.inc), daarna supersaw (C4/C5/C6), supersaw-stoot, hoover, bas, PSG-ruis.')


def flannery(src):
    """Ronde 2 (Jordi: 'Flamenco'): melodie en begeleiding op de GBA-nylongitaar (sc88pro_nylon_str_guitar, byte-kopie
    met label 48 = klinkt op de geschreven hoogte); rasgueado als snelle, opvolgende arpeggio's (elke slag = de
    akkoordtonen één tick na elkaar, de rasgueado = vier slagen in tweeëndertigsten); palmas als Emerald-snare
    (sd90_solo_snare) hoog gestemd als rimshot (accent) en side stick (zestienden); castagnetten op het PSG-ruiskanaal
    (de Emerald-bank heeft geen castagnetten)."""
    kit = Kit('gym_flannery', [('cajon', dk('gym_fla_cajon_bass', 150)), ('slap', dk('gym_fla_cajon_slap', 150)),
                               ('rim', dkp('sd90_solo_snare', 70, 80, 72, decay=200, sustain=0)),
                               ('stick', dkp('sd90_solo_snare', 77, 50, 56, decay=170, sustain=0))])
    vg = Voicegroup('grounded_gym_flannery', kit, {
        'nylon': [(48, ds('gym_fla_gba_nylon', 90, 25, 249))],
        'rnylon': [(48, ds('gym_fla_gba_nylon', 50, 25, 245))],
        'violin': [(k, ds('gym_fla_violin_%d' % k, 175)) for k in (60, 72)],
        'fretless': [(60, ds('sc88pro_fretless_bass', 120))],
        'cast': [(60, 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0')],
    })
    K = kit.key

    def r2(s, n, p):
        b = s // BAR
        if 2 <= b < 10:                                  # riff = rasgueado (tertsen: losse nylonnoten)
            return ('lead', 'nylon') if riff_route(src, s, 2) else None
        return ('lead', 'nylon')

    def r1(s, n, p):
        b = s // BAR
        if 2 <= b < 6:
            return ('lead', 'nylon') if riff_route(src, s, 1) else None
        return ('violin', 'violin')

    mp = melody_parts(src, vg, r1, r2)
    lead, violin = mp['lead'], mp['violin']
    lead.notes = tremolo(lead.notes)
    violin.notes = legato(violin.notes, 11)
    vibrato(violin, 5, delay=12)

    gtr = Part('rasg', 'rasg')
    group = {}                                           # (start, noot) -> begin van de slag
    RP = vg.prog('rnylon')
    gp = lambda pc: place(pc, 41)                        # grondtoon F2..E3

    def voicing(t):
        r = gp(src.root(t))
        return (r, r + 7, r + 12, r + 19)                # grondtoon, kwint, octaaf, kwint (geen terts: Frygisch veilig)

    def strum(t, v, up=False, ln=None, n=3):
        """Eén slag: de snaren één tick na elkaar (omlaag = laag -> hoog)."""
        keys = voicing(t)[:n]
        keys = keys[::-1] if up else keys
        for i, k in enumerate(keys):
            gtr.add(t + i, t + i + (ln or 9), k, v - 4 * i, RP)
            group[(t + i, k)] = t

    def stroke(t, kind, v, ln=None):
        if kind == 'R':                                  # rasgueado: 4 slagen in 32sten (e-a-m-i), dan de klap erop
            for j, dt in enumerate((-12, -9, -6, -3)):
                strum(t + dt, v - 30 + 5 * j, up=(j % 2 == 1), ln=1, n=2)
            strum(t, v, ln=ln or 14, n=4)
        elif kind == 'G':                                # golpe/apagado: korte gedempte slag
            strum(t, v, up=True, ln=3, n=3)
        else:
            strum(t, v, up=(kind == 'U'), ln=ln)
    for s, e, pc in riff_onsets(src):                  # de Frygische riff C - Db - C
        stroke(s, 'R' if (s % BAR) == 0 and s > 0 else 'S', 118, 22)
    stroke(0, 'S', 120, 40)
    t5 = {s for s, e, n, v, p in src.notes[5]}
    for b in range(10, NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        if sc in ('A1', 'A2'):
            for k, kind, v in ((0, 'S', 110), (12, 'U', 84), (24, 'G', 96), (36, 'S', 104), (48, 'S', 76),
                               (60, 'U', 80), (72, 'G', 96), (84, 'S', 100)):
                stroke(t0 + k, kind, v)
        elif sc in ('C1', 'C2'):
            for k, kind, v in ((0, 'R', 118), (24, 'G', 100), (36, 'S', 108), (48, 'R', 112), (72, 'G', 100),
                               (84, 'S', 104)):
                stroke(t0 + k, kind, v)
        elif sc == 'bridge':
            stroke(t0, 'R', 112, 40)
        elif sc == 'B':
            for k, kind, v in ((0, 'R', 116), (24, 'G', 92), (36, 'S', 108), (60, 'U', 84), (72, 'G', 92),
                               (84, 'S', 104)):
                stroke(t0 + k, kind, v)
        elif sc in ('pedal', 'build'):
            if b < 50:
                if b == 48:
                    stroke(t0, 'R', 118, 40)
                continue
            for k in sorted(t for t in t5 if t0 <= t < t0 + BAR):   # het ritme van spoor 5 (da-da-daa .. da-da-da)
                stroke(k, 'R' if (k - t0) in (0, 48) else 'G' if (k - t0) % 24 else 'S',
                       112 if (k - t0) in (0, 24) else 98)
    gtr.notes = [x for x in gtr.notes if x[0] >= 0]
    gtr.notes = no_overlap(gtr.notes)

    psg4 = psg_copy(src, 4, 60)
    psg5 = psg_copy(src, 5, 56)
    psg6 = psg_copy(src, 6, 70)

    bass = Part('bass', 'bass')
    for s, e, n, v, p in src.notes[3]:
        bass.add(s, e - 1, n, 112, vg.prog('fretless'))

    caj, slap, palm, ghost = (Part(n, 'perc') for n in ('cajon', 'slap', 'palmas', 'ghost'))
    palm.track = ghost.track = 'palmas'
    cast = Part('cast', 'cast', ds=False)                 # castagnetten: PSG-ruis, hoog en kort
    kp, cp = vg.kitprog, vg.prog('cast')

    def d(part, t, key, v, ln=8):
        part.add(t, t + ln, K[key], v, kp)

    def c(t, v, ln=2):
        cast.add(t, t + ln, 80, v, cp)
    # palmas in zestienden: rimshot (palma clara) op de accenten, side stick (sorda) op de rest
    CLARA = {0: 104, 24: 116, 36: 96, 72: 116, 84: 96}
    fills = {9: 48, 17: 48, 21: 48, 29: 48, 33: 48, 36: 48, 47: 48, 53: 48, 61: 48}
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        timp, sn = src.bar_hits(8, b), src.bar_hits(7, b)
        for t in timp:
            d(caj, t0 + t, 'cajon', 120 if t == 0 else 108)
        for t in sn:
            d(slap, t0 + t, 'slap', 118)
        if sc == 'intro':
            continue
        fill = fills.get(b, BAR)
        if sc == 'bridge':
            for t in sn:
                d(palm, t0 + t, 'rim', 108, 4)
        else:
            dense = sc in ('C1', 'C2', 'build', 'B')
            for k in range(0, fill, S16):
                if k in CLARA:
                    d(palm, t0 + k, 'rim', CLARA[k] - (0 if dense else 10), 4)
                elif k % S8 == 0 or dense:
                    d(ghost, t0 + k, 'stick', (78 if k % S8 == 0 else 56) + (6 if dense else 0), 3)
        # (de cajón-ghosts van v1 in het B-deel zijn nu de side-stick-palmas in zestienden)
        # castagnetten: 'ta-ki-TA' naar tel 2 en 4, in de refreinen ook naar 1 en 3
        if sc not in ('bridge',):
            targets = (24, 72) if sc not in ('C1', 'C2', 'build') else (0, 24, 48, 72)
            for tg in targets:
                if tg - 12 >= 0 and tg < fill:
                    c(t0 + tg - 12, 58)
                    c(t0 + tg - 6, 66)
                    c(t0 + tg, 92, 3)
        if b in FILLS_CAST:                                # castagnettenroffel (carretilla) naar de volgende sectie
            for k in range(fills[b], BAR, 3):
                c(t0 + k, 60 + (k - fills[b]) * 40 // (BAR - fills[b]))
    cast.notes = no_overlap(cast.notes)
    # slagen laten doorklinken tot de volgende slag (fit() per noot zou elke arpeggionoot na 3 ticks afkappen)
    gs = sorted(set(group.values()))
    tail = release_ticks(vg.rel[RP], TPB, 196) + 1
    for x in gtr.notes:
        g = group[(x[0], x[2])]
        nxt = next((t for t in gs if t > g), None)
        if nxt is not None:
            x[1] = max(x[0] + 2, min(x[1], nxt - tail))
    for prt in (bass, caj, slap, palm, ghost):
        fit(prt, vg, 196)
    order = [lead, bass, violin, caj, slap, palm, gtr, ghost]
    return dict(leader='Flannery', key='flannery', bpm=196, vg=vg, kit=kit, order=order,
                psg=[psg4, psg5, psg6, cast],
                vols={'lead': 124, 'violin': 88, 'rasg': 100, 'bass': 100, 'perc': 112, 'palmas': 92, 'cast': 52},
                pans={'lead': 64, 'violin': 76, 'rasg': 52, 'bass': 64, 'perc': 64, 'palmas': 72, 'cast': 80},
                desc='91 kit (drumsets/gym_flannery.inc: cajón, Emerald-snare als rimshot/side stick), daarna '
                     'GBA-nylongitaar (melodie, rasgueado), viool, fretloze bas, PSG-ruis (castagnetten).')


FILLS_CAST = (9, 17, 21, 29, 33, 36, 47, 53, 61)


LEADERS = [(647, 'MUS_GROUNDED_VS_ROXANNE', roxanne, 78), (648, 'MUS_GROUNDED_VS_BRAWLY', brawly, 76),
           (649, 'MUS_GROUNDED_VS_WATTSON', wattson, 74), (650, 'MUS_GROUNDED_VS_FLANNERY', flannery, 84)]
COMMENT = {'roxanne': 'hard rock power ballad', 'brawly': 'nu-metal', 'wattson': 'gabber/happy hardcore',
           'flannery': 'flamenco'}


def hook(path, line, after_pat=None):
    txt = open(path).read()
    if line in txt:
        return
    if after_pat:
        lines = txt.split('\n')
        idx = max(i for i, l in enumerate(lines) if re.search(after_pat, l))
        lines.insert(idx + 1, line)
        txt = '\n'.join(lines)
    else:
        txt = txt.rstrip('\n') + '\n' + line + '\n'
    open(path, 'w').write(txt)


def register(num, const, key, V):
    mid = 'mus_grounded_vs_%s' % key
    hook('sound/voice_groups.inc', '.include "sound/voicegroups/drumsets/gym_%s.inc"' % key, r'voicegroups/drumsets/')
    hook('sound/voice_groups.inc', '.include "sound/voicegroups/grounded_gym_%s.inc"' % key)
    cfg = open('sound/songs/midi/midi.cfg').read()
    line = '%s.mid: -E -R50 -G_grounded_gym_%s -V%03d' % (mid, key, V)
    cfg = re.sub(r'(?m)^%s\.mid:.*$' % mid, line, cfg) if (mid + '.mid:') in cfg else cfg.rstrip('\n') + '\n' + line + '\n'
    open('sound/songs/midi/midi.cfg', 'w').write(cfg)
    hook('include/constants/songs.h', '#define %-27s %d // Project Grounded: gymleider-remix (%s) van het Emerald-gymleiderthema '
         '(tools/grounded/gym_remixes.py)' % (const, num, COMMENT[key]), r'^#define MUS_GROUNDED_\w+\s+6\d\d')
    tbl = open('sound/song_table.inc').read()
    entries = re.findall(r'(?m)^\tsong (\w+), MUSIC_PLAYER_\w+, \d+$', tbl)
    want = '\tsong %s, MUSIC_PLAYER_BGM, 0' % mid
    if mid not in entries:
        assert len(entries) == num, 'song_table heeft %d nummers, verwacht %d vóór %s' % (len(entries), num, mid)
        last = re.findall(r'(?m)^\tsong \w+, MUSIC_PLAYER_\w+, \d+$', tbl)[-1]
        tbl = tbl.replace(last + '\n', last + '\n' + want + '\n', 1) if tbl.count(last + '\n') == 1 else None
        assert tbl, 'laatste song_table-regel niet uniek'
        open('sound/song_table.inc', 'w').write(tbl)


def main():
    src = Src()
    for num, const, fn, V in LEADERS:
        r = fn(src)
        vg, kit = r['vg'], r['kit']
        kit.write(r['leader'])
        vg.write(r['leader'], r['desc'])
        rep = allocate(r['order'], vg, bpm=r['bpm'])
        print('%s (%d bpm, %s):' % (r['leader'], r['bpm'], const))
        for name, n, lost in rep:
            print('  %-8s %4d noten, %3d vallen weg (%.1f%%)' % (name, n, lost, 100.0 * lost / max(1, n)))
        path = 'sound/songs/midi/mus_grounded_vs_%s.mid' % r['key']
        write_song(path, r['bpm'], r['order'] + r['psg'], r['vols'], r['pans'])
        register(num, const, r['key'], V)
        print('  ->', path)


if __name__ == '__main__':
    main()
