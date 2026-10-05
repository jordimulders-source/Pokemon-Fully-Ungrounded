#!/usr/bin/env python3
"""Project Grounded: vier remixes van het Emerald-gymleiderthema (mus_vs_gym_leader.mid), één per gymleider.

Jordi: 'Gymleiders allemaal een remix van het originele gym leader theme, die moet echt duidelijk nog te herkennen
blijven, zelfde melodie, andere instrumenten.' Dus: melodie (spoor 1 en 2), harmonie (bas, spoor 3), vorm en loop
(maat 10-62) van het origineel noot voor noot; alleen de instrumenten, de ritmesectie en (licht) het tempo wisselen.

  647 MUS_GROUNDED_VS_ROXANNE   80s female hard rock / power ballad (ronde 3)
  648 MUS_GROUNDED_VS_BRAWLY    nu-metal (ronde 3)
  649 MUS_GROUNDED_VS_WATTSON   gabber/happy hardcore, 176 bpm: vervormde gabberkick op elke tel, supersaw-lead,
                                happy-hardcore-piano, hoover, supersaw-stoten op de achtste 'en', breakdown + roffel
                                (goedgekeurd; ronde 1)
  650 MUS_GROUNDED_VS_FLANNERY  flamenco, rumba flamenca (ronde 3)

Ronde 3 (Jordi: Roxanne, Brawly en Flannery klonken alle drie als 'kermis/ska'; Wattson goedgekeurd en byte-identiek):
  van het origineel blijven alleen de melodie (melody_src, noot voor noot, gecontroleerd) en de grondtonen/akkoord-
  kwaliteit per halve maat; alle begeleiding is nieuw en in half-time (gevoelde tel = halve maat, 100-108 bpm).
  kermis_meter() meet waarom het kermis was en weigert te schrijven als het terugkomt (blazers/fluit/klokjes/orgel/
  piano/strijkers/PSG-tonen, off-beat-stoten zonder tel 1, hoempa-bas, geen kick op 1, tegenlijnen boven de melodie).
  Roxanne   80s hard rock: kick 1+3, diepe rock-snare met naklink op 2+4, achtsten op hihat/ride, distortion-lead met
            pre-bends en vibrato, lange powerchords, pompende pick-bas in achtsten (200 bpm)
  Brawly    nu-metal (Stemm 'Face the Pain'): drop-C-chugs op de gevoelde zestienden met de tel erin, kick op elke chug,
            double-kick, pick-bas mee, turntable-scratches van v1 vóór en na de zinnen (216 bpm)
  Flannery  rumba flamenca: palmas (contratiempo + zestiende-syncopen), cajón, doorlopende rasgueado (één sample per
            slag), funky fretloze bas met slides, nylonmelodie met picado-loopjes aan zinseinden (208 bpm)

Het origineel wordt één keer ontleed (Src): noten per spoor met het programma op dat moment, de grondtonen per halve
maat (uit de bas; in maat 2-9 uit de riff), het ritme van de pauken (spoor 8) en de snare (spoor 7). Per leider
bepaalt een functie welk instrument elke noot krijgt en welke begeleiding erbij komt (Wattson: de PSG-sporen van het
origineel blijven; Roxanne/Brawly/Flannery: geen PSG meer).
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


# ---- ronde 3: anti-kermis ---------------------------------------------------------------------------------------------
# Jordi (ronde 3): Roxanne, Brawly en Flannery klonken alle drie als 'kermis/ska'. Gemeten oorzaken (kermis_meter() op
# de v2-MIDI's, zie MUZIEK.md): (1) de drie PSG-sporen van het origineel (vierkant-arpeggio's in achtsten, tegenlijnen
# boven de melodie, hoge stootjes) speelden 1-op-1 mee; (2) spoor 1 (de hoorn-/trompettweede stem in tertsen en sexten
# onder de melodie = een koperblazerssectie) bleef als tweede gitaar/strijkers/viool; (3) de bas van het origineel is
# een hoempa-bas (grondtoon op de tel, kwint een octaaf hoger op elke achtste 'en') op 188-196 bpm met de snare op 2 en 4
# van diezelfde 196 bpm = polka/ska-tempo; (4) Brawly's chugs stonden op de 'en' (tel 1 en verder alleen off-beats
# = skank), Flannery's percussie volgde het pauken-ritme (0-36-84, gestippeld) en de castagnetten waren PSG-tikjes van
# 2 ticks, de nylon-melodie was trémolo (mandoline). Nu: van het origineel alleen de melodie (melody_src) en de
# grondtonen/akkoordkwaliteit per halve maat als skelet; alle begeleiding is nieuw, in half-time (de gevoelde tel = een
# halve maat van het origineel: 100-108 bpm), en het script weigert te schrijven als kermis_meter() iets vindt.
HB = 48                                         # gevoelde tel (half-time)
PHR_DOM = {0, 1, 4, 5, 7, 8, 10}                # C-Frygisch dominant (flamenco)


def melody_src(src):
    """De melodie van het origineel, sectie voor sectie uit het spoor dat hem draagt: [start, eind, noot, velocity].
    Intro: de triller (spoor 2); riff en A/C/brug/opbouw: spoor 2; B-deel: het motief C-Db-Eb (maat 37-39 uit PSG-spoor
    4, een octaaf hoger; 40-44 spoor 1; 45-48 spoor 2); orgelpunt 50-53: de lijn van PSG-spoor 5 (Bb-F-Eb-D in
    herhaalde achtsten) als één lange noot per maat."""
    mel = []
    for s, e, n, v, p in src.notes[2]:
        b = s // BAR
        if not (37 <= b < 45):
            mel.append([s, e, n, v])
    for s, e, n, v, p in src.notes[1]:
        if 40 * BAR <= s < 45 * BAR:
            mel.append([s, e, n, v])
    for s, e, n, v, p in src.notes[4]:
        if 37 * BAR <= s < 40 * BAR:
            mel.append([s, e, n + 12, v])
    for b in range(50, 54):
        bn = [n for s, e, n, v, p in src.notes[5] if b * BAR <= s < b * BAR + BAR]
        if bn:
            mel.append([b * BAR, b * BAR + BAR - 6, bn[0], 100])
    return sorted(mel)


def guitar_octave(s, n):
    """Register voor een gitaar-/nylonmelodie: intro-triller en riff 6-9 een octaaf omlaag, brug en opbouw omhoog."""
    b = s // BAR
    if b < 2 or 6 <= b < 10:
        return n - 12
    if 34 <= b < 37 or b >= 54:
        return n + 12
    return n


def intro_run(src):
    """De chromatische dalende loop van het intro (spoor 1, maat 0-1)."""
    return [[s, e, n, v] for s, e, n, v, p in src.notes[1] if s < 2 * BAR]


def quality(src, t):
    """Akkoordkwaliteit op tijd t (halve maat): 'maj' als het origineel daar alleen de grote terts boven de grondtoon
    speelt, anders 'five' (open kwint: veilig bij mineur/Frygisch/onduidelijk)."""
    h0 = t // HB * HB
    r = src.root(t)
    pcs = {n % 12 for i in range(1, 7) for s, e, n, v, p in src.notes[i] if s < h0 + HB and e > h0}
    return 'maj' if (r + 4) % 12 in pcs and (r + 3) % 12 not in pcs else 'five'


def root_spans(src, a, z):
    """(start, eind, grondtoon) van tick a tot z, opgeknipt waar de grondtoon wisselt."""
    pts = sorted({a} | {c for c, _ in src.changes if a < c < z})
    out = []
    for i, t in enumerate(pts):
        e = pts[i + 1] if i + 1 < len(pts) else z
        if out and out[-1][2] == src.root(t):
            out[-1][1] = e
        else:
            out.append([t, e, src.root(t)])
    return out


def melody_gaps(mel, minimum):
    """(einde vorige noot, begin volgende) waar de melodie minstens `minimum` ticks rust."""
    out = []
    for a, b in zip(mel, mel[1:]):
        if b[0] - a[1] >= minimum:
            out.append((a[1], b[0]))
    return out


def lead_bends(part, bpm, bendr=2, scoop=True, cents=30, hz=5.5, delay=12, min_len=30):
    """80s-gitaar: lange noten die van onderaf komen worden een hele toon ingebend (pre-bend, 5 ticks), daarna een
    vertraagde, ingefade vibrato tot in de uitklinktijd. BENDR = bendr (CC20); bend weer op 0 vóór de volgende aanslag."""
    part.ccs.append((0, 20, bendr))
    tps = bpm * TPB / 60.0
    notes = sorted(part.notes)
    step = 64.0 / bendr                                  # bend-eenheden per halve toon
    for i, (s, e, n, v, p) in enumerate(notes):
        nxt = notes[i + 1][0] if i + 1 < len(notes) else None
        if e - s < min_len:
            continue
        prev = notes[i - 1][2] if i else n
        bend_in = scoop and 1 <= n - prev <= 7 and i % 2 == 0
        stop = e + 8 if nxt is None else min(nxt, e + 8)
        last = 0
        for t in range(s, stop):
            c = 0.0
            if bend_in and t - s < 5:
                c -= 2 * step * (1 - (t - s) / 5.0)
            if t - s >= delay:
                amp = min(1.0, (t - s - delay) / 14.0) * cents / 100.0 * step
                c += amp * math.sin(2 * math.pi * hz * (t - s - delay) / tps)
            c = int(round(c))
            if c != last or t == s:
                if not (t == s and c == 0 and last == 0):
                    part.bends.append((t, pw(c)))
                last = c
        if last != 0:
            part.bends.append((stop, pw(0)))


def dk2(sample, rel, pan=64):
    """Drumkitregel met de sample op eigen hoogte (no_resample), volledige sustain: de naklink zit in de sample."""
    return 'voice_directsound_no_resample 60, %d, DirectSoundWaveData_%s, 255, 0, 255, %d' % (pan, sample, rel)


BANNED = re.compile(r'trumpet|horn|trombone|tuba|brass|sax|flute|piccolo|whistle|ocarina|recorder|glock|bell|celest|'
                    r'music_box|xylo|marimba|vibra|accordion|harmonica|organ|calliope|kazoo|honky|pizz|banjo|'
                    r'string_ensemble|strings|violin|piano|choir|_stab')


def _voice_lines(text):
    return [l.strip() for l in text.split('\n') if l.strip().startswith('voice_') and not l.strip().startswith('voice_group')]


KERMIS_TIMBRE = {'accordeon', 'tango-accordeon', 'mondharmonica', 'fluit', 'fluitje', 'ocarina', 'piano',
                 'kerkorgel', 'drawbar-orgel', 'nylon (akoestisch)', 'staalsnaar (akoestisch)', 'banjo', 'pizzicato',
                 'glockenspiel', 'trompet', 'koperblazers'}


def _sample_tone(name):
    """(spectral flatness, grondtoon in Hz) van een sample (actieve frames): < 0,03 = zuivere toon."""
    import wave, warnings
    import numpy as np, librosa
    warnings.filterwarnings('ignore')
    path = 'sound/direct_sound_samples/grounded/%s.wav' % name
    if not os.path.exists(path):
        path = 'sound/direct_sound_samples/%s.wav' % name
    w = wave.open(path)
    sr = w.getframerate()
    a = (np.frombuffer(w.readframes(w.getnframes()), np.uint8).astype(float) - 128) / 127
    S = np.abs(librosa.stft(a, n_fft=512, hop_length=128))
    e = (S ** 2).sum(0)
    act = e > 0.05 * e.max()
    fl = float(np.median(librosa.feature.spectral_flatness(S=S)[0][act]))
    f = librosa.fft_frequencies(sr=sr, n_fft=512)
    f0 = float(np.median(f[S[:, act].argmax(0)]))
    return fl, f0


def kermis_meter(mid_path, vg_text, kit_text, src, beat=HB, verbose=True, metal=False):
    """Anti-kermis-controle op een MIDI + voicegroup (+ drumkit) als tekst, zodat ook oude versies meetbaar zijn.
    Fouten (lijst van teksten):
      instrument  blazers/fluit/klokjes/accordeon/orgel/piano/strijkers/pizzicato of een PSG-toon (vierkant/golf) op
                  een melodisch spoor
      ska         een begeleidingsspoor heeft meer aanslagen op de 'en' (beat/2) dan op de tel, of mist in > 25% van
                  zijn maten de eerste tel (geen aanslag en niets aangehouden)
      hoempa      bas (mediaan < 52): > 25% van de 'en'-noten springt >= 5 halve tonen omhoog t.o.v. de noot ervoor
      kick        > 15% van de maten met drums heeft geen kick/cajón op tel 1
      tegenlijn   > 10% van de melodietijd klinkt een ander melodisch spoor bóven de melodie, of een druk melodisch
                  spoor (>= 1 aanslag per tel) speelt in het register van de melodie (mediaan >= melodie - 5)
    beat = de gevoelde tel in ticks (48 = half-time)."""
    lines = _voice_lines(vg_text)
    kit = _voice_lines(kit_text)
    kick_keys = {36 + i for i, l in enumerate(kit) if re.search(r'kick|cajon_bass', l)}
    m = mido.MidiFile(mid_path)
    lo_t, hi_t = LOOP
    tracks = []
    for ti, t in enumerate(m.tracks):
        tick, prog, on, notes = 0, 0, {}, []
        for x in t:
            tick += x.time
            if x.type == 'program_change':
                prog = x.program
            if x.type == 'note_on' and x.velocity:
                on.setdefault(x.note, []).append((tick, prog))
            elif x.type in ('note_on', 'note_off') and on.get(x.note):
                s, p = on[x.note].pop(0)
                notes.append((s, tick, x.note, p))
        if notes:
            tracks.append((ti, sorted(notes)))
    fails, info = [], []

    def kind(p):
        l = lines[p] if p < len(lines) else ''
        if l.startswith('voice_keysplit_all') or l.startswith('voice_noise'):
            return 'drum'
        if l.startswith(('voice_square', 'voice_programmable')):
            return 'psg'
        return 'ds'

    def name(p):
        l = lines[p] if p < len(lines) else ''
        mm = re.search(r'DirectSoundWaveData_(\w+)|voicegroup_(\w+)', l)
        return (mm.group(1) or mm.group(2)) if mm else l.split(' ')[0]
    pitched = []
    for ti, notes in tracks:
        mel = [x for x in notes if kind(x[3]) != 'drum']
        if not mel:
            continue
        bad = set()
        for p in sorted({x[3] for x in mel}):
            if kind(p) == 'psg':
                bad.add('PSG-toon ' + lines[p].split(' ')[0])
            elif BANNED.search(name(p)):
                bad.add(re.sub(r'_\d+$', '', name(p)))
        if bad:
            fails.append('instrument: spoor %d %s' % (ti, ', '.join(sorted(bad))))
        pitched.append((ti, mel))
    # melodiespoor: de meeste aanslagen van spoor 2 van het origineel (maat 10-34) op dezelfde tick + toonklasse
    ref = {(s, n % 12) for s, e, n, v, p in src.notes[2] if 10 * BAR <= s < 34 * BAR}
    mel_ti, mel = max(pitched, key=lambda tn: len(ref & {(x[0], x[2] % 12) for x in tn[1]}))
    mel_med = sorted(x[2] for x in mel)[len(mel) // 2]
    step = 6

    def sounding(notes, t):
        c = [x[2] for x in notes if x[0] <= t < x[1]]
        return max(c) if c else None
    mel_ticks = [t for t in range(lo_t, hi_t, step) if sounding(mel, t) is not None]
    for ti, notes in pitched:
        if ti == mel_ti:
            continue
        loop = [x for x in notes if lo_t <= x[0] < hi_t]
        if len(loop) < 16:
            continue
        med = sorted(x[2] for x in loop)[len(loop) // 2]
        on_b = sum(1 for x in loop if x[0] % beat == 0 or beat - x[0] % beat <= 9)   # rasgueado-roffel vóór de tel
        on_e = sum(1 for x in loop if x[0] % beat == beat // 2)
        bars = sorted({x[0] // BAR for x in loop})
        miss = sum(1 for b in bars if not any(x[0] <= b * BAR < x[1] or x[0] == b * BAR for x in notes))
        ratio = on_e / float(max(1, on_b))
        info.append('spoor %2d mediaan %3d: tel %3d, en %3d (%.2f), maten zonder tel 1 %d/%d' %
                    (ti, med, on_b, on_e, ratio, miss, len(bars)))
        if ratio > 1.0:
            fails.append('ska: spoor %d heeft %d aanslagen op de en tegen %d op de tel' % (ti, on_e, on_b))
        if miss > 0.25 * len(bars):
            fails.append('ska: spoor %d mist tel 1 in %d van %d maten' % (ti, miss, len(bars)))
        if med < 52:
            ups = 0
            ens = [i for i, x in enumerate(loop) if x[0] % beat == beat // 2 and i > 0]
            for i in ens:
                if loop[i][2] - loop[i - 1][2] >= 5:
                    ups += 1
            frac = ups / float(max(1, len(ens)))
            info.append('         hoempa: %d van %d en-noten springen omhoog (%.0f%%)' % (ups, len(ens), 100 * frac))
            if frac > 0.25:
                fails.append('hoempa: spoor %d springt op %.0f%% van de en-noten omhoog' % (ti, 100 * frac))
            continue
        above = sum(1 for t in mel_ticks if (sounding(notes, t) or 0) > sounding(mel, t))
        rate = len(loop) / float((hi_t - lo_t) / beat)
        info.append('         boven de melodie %.0f%%, %.2f aanslagen per tel' % (100.0 * above / max(1, len(mel_ticks)), rate))
        if above > 0.10 * len(mel_ticks):
            fails.append('tegenlijn: spoor %d klinkt %.0f%% van de melodietijd boven de melodie' %
                         (ti, 100.0 * above / len(mel_ticks)))
        if rate >= 1.0 and med >= mel_med - 5:
            fails.append('tegenlijn: spoor %d is een drukke lijn (%.1f per tel) in het melodieregister' % (ti, rate))
    kicks = [x for ti, notes in tracks for x in notes if kind(x[3]) == 'drum' and lines[x[3]].startswith('voice_keysplit_all')]
    dbars = sorted({x[0] // BAR for x in kicks if lo_t <= x[0] < hi_t})
    nok = [b for b in dbars if not any(x[0] == b * BAR and x[2] in kick_keys for x in kicks)]
    info.append('kick op tel 1: %d van %d maten' % (len(dbars) - len(nok), len(dbars)))
    if len(nok) > 0.15 * len(dbars):
        fails.append('kick: %d van %d maten zonder kick op tel 1' % (len(nok), len(dbars)))
    # ronde 4 (Brawly v3: 'speelgoedaccordeon/fluitje, akoestische tokkels'; gemeten oorzaak: een scratch die een
    # zuivere glijtoon was, chugs van ±40 ms die als mondharmonica klonken, een bas van 5 ticks als pick bass/pizzicato)
    for p in sorted({x[3] for ti, notes in tracks for x in notes if kind(x[3]) == 'drum'
                     and lines[x[3]].startswith('voice_keysplit_all')}):
        keys = sorted({x[2] for ti, notes in tracks for x in notes if x[3] == p})
        names = sorted({re.search(r'DirectSoundWaveData_(\w+)', kit[k - 36]).group(1) for k in keys
                        if 0 <= k - 36 < len(kit) and 'DirectSoundWaveData_' in kit[k - 36]})
        for sname in names:
            nm = re.search(r'(\w+)', sname)
            if not nm or re.search(r'kick|snare|tom|hat|crash|china|ride|cymbal|cajon|clap|palma|stick|castan|bongo|'
                                   r'conga|shaker|tamb', nm.group(1)):
                continue
            fl, f0 = _sample_tone(nm.group(1))
            info.append('fx-sample %s: flatness %.3f, toon %.0f Hz' % (nm.group(1), fl, f0))
            if fl < 0.03 and f0 > 400:
                fails.append('fluitje: kitstem %s is een zuivere toon (flatness %.3f, %.0f Hz) = glijfluit/'
                             'speelgoedaccordeon, geen scratch/effect' % (nm.group(1), fl, f0))
    if metal:
        import gba_sim
        tempo = next((x.tempo for t in m.tracks for x in t if x.type == 'set_tempo'), 500000)
        sec_tick = tempo / 1e6 / m.ticks_per_beat
        rel_of = lambda p: int(lines[p].split('@')[0].rsplit(',', 1)[1]) if lines[p].startswith('voice_directsound') else 0
        low_ticks = set()
        for ti, notes in pitched:
            if ti == mel_ti:
                continue
            loop = [x for x in notes if lo_t <= x[0] < hi_t and kind(x[3]) == 'ds']
            if not loop:
                continue
            durs = []
            for s, e, n, p in loop:
                r = rel_of(p)
                tail = (math.log(1 / 16.0) / math.log(r / 256.0) / 59.73) if 0 < r < 255 else 0.0
                durs.append((e - s) * sec_tick + tail)
                if n < 52:
                    low_ticks.update(range(s - s % 6, e, 6))
            med = sorted(durs)[len(durs) // 2]
            info.append('spoor %2d klinkt per noot mediaan %.0f ms' % (ti, 1000 * med))
            if med < 0.11:            # v3: chugs 71 ms ('accordeon'), bas 107 ms ('kort getokkeld gitaarnootje')
                fails.append('tokkel: spoor %d speelt korte getokkelde noten/stoten (mediaan %.0f ms incl. '
                             'uitklinktijd; metal wil palm-mutes, aangehouden akkoorden en een dragende bas)'
                             % (ti, 1000 * med))
            snames = {re.search(r'DirectSoundWaveData_(\w+)', lines[x[3]]).group(1) for x in loop}
            chord = (0, 7, 12) if any(re.search(r'power|wall|chord|strum|rasg', n) for n in snames) else (0,)
            rank = gba_sim.timbre_rank(mid_path, ti, vg_text, [kit_text], 10 * BAR * sec_tick, 30 * BAR * sec_tick,
                                       chord=chord)
            info.append('spoor %2d klinkt als: %s' % (ti, ', '.join('%s %.1f' % (nm, dd) for dd, nm in rank[:4])))
            # alleen ter info: de nabootsing (gba_sim, zonder galm/8-bit-mix) en de opname uit de game zijn het niet
            # altijd eens (v3-chugs: game 'mondharmonica', nabootsing 'overdrive gitaar'); controleer in de game met
            # timbre_rank(..., audio=solo-opname)
            bad = [nm for dd, nm in rank[:2] if nm in KERMIS_TIMBRE]
            if bad:
                info.append('         LET OP: lijkt op %s (controleer solo in de game)' % '/'.join(bad))
        steps = range(lo_t, hi_t, 6)
        frac = sum(1 for t in steps if t in low_ticks) / float(len(steps))
        info.append('lage laag (< E3) klinkt %.0f%% van de loop' % (100 * frac))
        if frac < 0.80:
            fails.append('hol: de lage laag (gitaar/bas onder E3) klinkt maar %.0f%% van de loop (muur van geluid: '
                         '>= 80%%)' % (100 * frac))
    if verbose:
        for l in info:
            print('   ', l)
    return fails


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


SC_MAJ = {0, 2, 4, 5, 7, 9, 10}      # A- en C-delen: C-mixolydisch (= F-groot)
SC_PHR = {0, 1, 3, 5, 7, 8, 10}      # B-deel: C-frygisch


def roxanne(src):
    """Ronde 3 (Jordi: 'kermis/ska met een blikkerige St. Anger-snare; moet 80s female hard rock / power ballad zijn,
    Heart/Joan Jett/Pat Benatar'): 200 bpm in half-time = een rockbeat op 100 bpm. Kick op 1 en 3, snare op 2 en 4
    (gym_rox_rsnare: diep, vol, natuurlijke naklink van ±0,8 s; de oude sd90_solo_snare ringde op 553 Hz en werd na
    120 ms gegate, met een PSG-ruistik erbij), achtsten op de hihat (refreinen/B/opbouw: ride). Melodie op de Emerald-
    distortiongitaar met sustain, pre-bends en vibrato; tweede gitaar = lange powerchords (I-V) op de grondtonen;
    pompende pick-bas in achtsten op de grondtoon (geen hoempa). Geen blazers, strijkers, piano of PSG-tegenlijnen."""
    bpm = 200
    kit = Kit('gym_roxanne', [('kick', dk('drum_and_percussion_kick', 170)),
                              ('snare', dk2('gym_rox_rsnare', 200)),
                              ('hat', 'voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_close_hihat, '
                                      '255, 127, 0, 120'),
                              ('ride', dk2('gym_rox_ride', 190, 76)),
                              ('crash', dk2('trinity_cymbal_crash', 205, 54)),
                              ('tom_lo', dkp('sd90_ambient_tom', 64, 180, 44)),
                              ('tom_mid', dkp('sd90_ambient_tom', 68, 180, 64)),
                              ('tom_hi', dkp('sd90_ambient_tom', 72, 180, 84))])
    vg = Voicegroup('grounded_gym_roxanne', kit, {
        'lead': [(60, ds('sd90_classical_distortion_guitar_high', 190))],
        'power': [(48, ds('gym_rox_open', 170))],
        'clean': [(k, ds('gym_rox_clean_%d' % k, 160)) for k in (60, 72)],
        'bass': [(36, ds('gym_rox_pbass', 120))],
    })
    K = kit.key
    mel = melody_src(src)
    lead = Part('lead', 'lead')
    for s, e, n, v in mel:
        b = s // BAR
        inst = 'clean' if 34 <= b < 37 else 'lead'      # brug: cleane gitaar, dramatisch zacht
        lead.add(s, e, guitar_octave(s, n), 112 if inst == 'lead' else 104, vg.prog(inst, n))
    lead.notes = legato(lead.notes, 4, keep=0.9)
    lead_bends(lead, bpm)
    run = Part('run', 'run')                             # intro: de chromatische loop als tweede gitaar (onder de triller)
    for s, e, n, v in intro_run(src):
        run.add(s, s + 5, n - 12, 92 + (s // 6) % 2 * 8, vg.prog('lead'))

    # tweede gitaar: lange powerchords (I-V) op elke grondtoon
    power = Part('power', 'power')
    pc_ = lambda pc: place(pc, 41)                       # F2..E3 rond de C3-sample
    pp = vg.prog('power')
    power.add(0, 2 * BAR - 4, pc_(0), 104, pp)           # intro: één lang C-akkoord onder de triller
    for s, e, pc in src.riff:                            # riff: C - Db - C aangehouden tot de volgende aanslag
        power.add(s, s + 34, pc_(pc), 116, pp)
    for b in range(10, NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        if sc == 'bridge' and b < 36:
            continue
        for s, e, pc in root_spans(src, t0, t0 + BAR):
            v = {'A1': 96, 'A2': 98, 'C1': 112, 'C2': 114, 'B': 110, 'pedal': 98 + (b - 48) * 3, 'build': 104,
                 'bridge': 100}[sc]
            power.add(s, e - 2, pc_(pc), v, pp)
    power.notes = no_overlap(power.notes)

    # pompende pick-bas: achtsten (van de gevoelde tel) op de grondtoon, accent op de kick
    bass = Part('bass', 'bass')
    bp_ = vg.prog('bass')
    for b in range(2, NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        if sc == 'bridge' and b < 36:
            bass.add(t0, t0 + BAR - 8, place(src.root(t0), 28), 108, bp_)   # brug: lange grondtoon
            continue
        for k in range(0, BAR, 24):
            t = t0 + k
            bass.add(t, t + 18, place(src.root(t), 28), 122 if k == 0 else 112 if k == 48 else 100, bp_)

    kick, snare, hats, cym, toms = (Part(n, 'drums') for n in ('kick', 'snare', 'hats', 'cym', 'toms'))
    hats.track = cym.track = 'cym'
    kp = vg.kitprog

    def d(part, t, key, v, ln=12):
        part.add(t, t + ln, K[key], v, kp)
    fills = {1: 0, 9: 48, 17: 48, 21: 48, 29: 48, 33: 48, 36: 0, 47: 48, 53: 48, 61: 48}
    crash = (0, 2, 6, 10, 14, 18, 22, 26, 30, 34, 37, 41, 45, 48, 50, 52, 54, 58)
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        fill = fills.get(b)
        cut = lambda t: fill is None or t < fill
        if b in crash:
            d(cym, t0, 'crash', 116 if b not in (34,) else 96, 60)
        if b == 0:
            d(kick, t0, 'kick', 124)
            for t in (36, 60, 72, 84):                    # pauken van het intro als toms
                d(toms, t0 + t, 'tom_lo', 110, 12)
            continue
        quiet = sc == 'bridge' and b < 36
        d(kick, t0, 'kick', 124 if not quiet else 108)      # kick op 1 en 3 (van de gevoelde maat)
        if cut(48):
            d(snare, t0 + 48, 'snare', 124 if not quiet else 104, 66)   # snare op 2 en 4, met naklink
        ride = sc in ('C1', 'C2', 'B', 'build')
        for k in range(0, BAR, 24):                       # gestage achtsten
            if cut(k) and not (b in crash and k == 0):
                d(hats, t0 + k, 'ride' if ride else 'hat', (100 if k % 48 == 0 else 80) if ride else
                  (96 if k % 48 == 0 else 72), 20 if ride else 4)
        if fill is not None:                               # tomroffel (16en van de gevoelde tel) naar de volgende sectie
            seq = ['tom_hi', 'tom_hi', 'tom_mid', 'tom_mid', 'tom_lo', 'tom_lo', 'snare', 'snare']
            n = (BAR - fill) // 12
            for k in range(n):
                key = seq[len(seq) - n + k] if n <= len(seq) else seq[k % len(seq)]
                d(toms if key.startswith('tom') else snare, t0 + fill + k * 12, key, 98 + k * 4, 12)
    for prt in (power, bass, kick, toms, hats):
        fit(prt, vg, bpm)
    order = [lead, power, kick, snare, bass, cym, hats, toms, run]
    return dict(leader='Roxanne', key='roxanne', bpm=bpm, vg=vg, kit=kit, order=order, psg=[],
                vols={'lead': 118, 'run': 90, 'power': 92, 'bass': 104, 'drums': 116, 'cym': 78},
                pans={'lead': 60, 'run': 70, 'power': 68, 'bass': 64, 'drums': 64, 'cym': 72},
                desc='91 kit (drumsets/gym_roxanne.inc: Emerald-kick, diepe rock-snare met naklink, hihat, ride, crash, '
                     'Emerald-toms), daarna Emerald-distortiongitaar (lead), powerchord, cleane gitaar (brug), pick-bas.')


def brawly(src):
    """Ronde 4 (Jordi over v3 via Gemini: 'dun gepingel op een speelgoedaccordeon/fluitje en een blije akoestische
    tokkelgitaar = kermis/ska; de bas is onhoorbaar en klinkt als een kort getokkeld gitaarnootje; dunne drums met een
    blikken kick; de scratches zijn weg'; referentie Stemm 'Face the Pain'). Gemeten in een test-ROM (solo per spoor,
    klankvergelijking met FluidR3-renders van dezelfde noten): de v3-chugs (gym_bra_epower van 2 ticks + release 70 =
    ±40 ms, 155 stoten in 30 s) klonken als een mondharmonica/tango-accordeon (kortste afstand van alle GM-
    instrumenten), de bas (pick-bas, 5 ticks) als pick bass/pizzicato, de scratch (koor-'aah' met sinusvormige
    snelheid, spectral flatness 0,005, glijtoon rond 900 Hz) als een glijfluitje. De melodie (lead) blijft noot voor
    noot en klank voor klank v3. Nieuw (samples brawly_samples.py, gym_bra4_*):
      wall   tweede Emerald-distortiongitaar (sd90_..._high): langgerekte powerchords I-V-I' (E2-D#3), aangeslagen op
             tel 1 van elke maat en bij elke akkoordwissel, aangehouden tot de volgende = de muur van geluid
      gtr    de chugs blijven (zelfde ritme) maar met een echte palm-mute-sample (gym_bra4_chug: plectrum, hand op de
             snaren, lage chunk) van 10 ticks + release 120 (±150 ms) i.p.v. stoten van 40 ms van een rietachtig
             aangehouden akkoord
      bass   overdrive-bas uit de Emerald-fingered bass, strakke achtsten mee met de kick, aangehouden; luider
      drums  zware kick (gym_bra4_kick) op de achtsten, heavy-rock-snare op 2 en 4, PSG-ruis-hihats (open) op de
             tussenliggende achtsten (. x . x), crash/china en tomfills als v3
      fx     echte scratches (gym_bra4_scratch/_chirp: vervormde 'aah' + vinylruis, breedbandig) alleen op de
             overgangen vóór elke zin (o.a. 0:07 en 0:15); de ritmische scratch-invullingen zijn weg.
    Ronde 5 (Jordi 'echt dichtbij'; Gemini noemde muur, bas en open hats als ontbrekend, terwijl v4 ze had). Gemeten
    (gba_sim per spoor, A-gewogen = zoals het oor): de lead was 74% van de waargenomen luidheid, muur 14%, bas 6%,
    drums 2%. Oorzaken: (1) gym_bra4_bass klonk twee octaven te hoog (C4 = 261 Hz met label C2; 0% energie < 100 Hz),
    (2) de muur stond op spoorvolume 62, (3) de PSG-hats waren tikjes van 90 ms op ±5/15 (decay 2 tot 0, release 0),
    (4) de kick was 6 ticks lang (de subtoon werd afgekapt). v5 (melodie, ritme, tempo, opener en snare gelijk):
    gym_bra5_bass op echt C2 met versterkte grondtoon, grom en plectrumpunch; gym_bra5_wall dikker (lage Emerald-
    distortion erbij, ronk 110-380 Hz) op volume 104; open hats 0,21 s op vol 127 (decay 1, sustain 5, release 1);
    kick 16 ticks met subtoon naar 48 Hz; lead 106 -> 80 en chugs 84 -> 60 (gym_bra5_chug: nu op de juiste octaaf,
    v4 klonk C1)."""
    bpm = 216
    kit = Kit('gym_brawly', [('kick', dk('gym_bra5_kick', 150)), ('snare', dk('gym_bra4_snare', 180)),
                             ('china', dk('gym_bra_china', 200)), ('crash', dk('gym_bra_crash', 205)),
                             ('tom_lo', dk('gym_bra_tom_41', 170, 54)), ('tom_mid', dk('gym_bra_tom_45', 170, 64)),
                             ('tom_hi', dk('gym_bra_tom_48', 170, 74)),
                             ('scratch', dk('gym_bra4_scratch', 140)), ('chirp', dk('gym_bra4_chirp', 140))])
    vg = Voicegroup('grounded_gym_brawly', kit, {
        'lead': [(k, ds('gym_bra_lead_%d' % k, 170)) for k in (60, 72, 84)],
        'chug': [(36, ds('gym_bra5_chug', 120))],         # palm-mute-sample (sterft zelf uit) + korte uitklinktijd
        'wall': [(48, ds('gym_bra5_wall', 165))],
        'bass': [(36, ds('gym_bra5_bass', 110))],
        # PSG-ruis: open hihat. v5: decay 1 tot sustain 5/15, dan release 1 (v4: decay 2 tot 0, release 0 = na de
        # noot van 8 ticks meteen stil, op ±5/15 = een tikje van 90 ms dat niemand hoorde)
        'noise': [(60, 'voice_noise_alt 60, 0, 0, 0, 1, 5, 1')],
    })
    K = kit.key
    mel = melody_src(src)
    lead = Part('lead', 'lead')
    for s, e, n, v in mel:
        lead.add(s, e, guitar_octave(s, n), 116, vg.prog('lead', guitar_octave(s, n)))
    lead.notes = legato(lead.notes, 6, keep=0.9)
    vibrato(lead, 6, delay=16)

    gtr, wall, bass = Part('gtr', 'gtr'), Part('wall', 'wall'), Part('bass', 'bass')
    chug_p, wall_p, bass_p = vg.prog('chug'), vg.prog('wall'), vg.prog('bass')
    low = lambda pc: place(pc, 34)                       # A#1..A2: drop-gestemd
    kick_t = set()

    def hit(t, pc, v, open_=False, ln=None):
        """Eén gitaaraanslag (palm-mute of open), kick erop (behalve op de snare)."""
        gtr.add(t, t + ((ln or 20) if open_ else 10), low(pc), v, chug_p)
        if (t % BAR) != 48:
            kick_t.add(t)
    VERSE = [((0, 'O', 120), (12, 'c', 100), (18, 'c', 92), (42, 'c', 104), (48, 'c', 110), (60, 'c', 100),
              (66, 'c', 92), (84, 'c', 104)),
             ((0, 'O', 118), (18, 'c', 100), (30, 'c', 96), (48, 'c', 110), (54, 'c', 96), (72, 'c', 104),
              (78, 'c', 96), (90, 'c', 100))]
    BREAK = ((0, 'O', 122), (24, 'c', 104), (30, 'c', 98), (48, 'O', 116), (72, 'c', 106), (84, 'c', 104))
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        if sc == 'intro':
            if b == 0:
                hit(t0, 0, 122, True, 88)
            else:
                for k in range(0, BAR, 12):
                    hit(t0 + k, 0, 84 + k // 4)
        elif sc == 'riff':
            ons = {s - t0: pc for s, e, pc in src.riff if t0 <= s < t0 + BAR}
            for k in (0, 12, 18, 36, 48, 54, 72, 84, 90):
                hit(t0 + k, ons.get(k, src.root(t0 + k)), 122 if k in ons else 98, k in ons, 30)
        elif sc in ('A1', 'A2'):
            for k, kind, v in VERSE[b % 2]:
                hit(t0 + k, src.root(t0 + k), v, kind == 'O', 34)
        elif sc in ('C1', 'C2'):
            for k in range(0, BAR, 12):                   # galop-chugs op de double-kick
                if k != 48:
                    hit(t0 + k, src.root(t0 + k), 112 if k % 24 == 0 else 98)
        elif sc == 'bridge':
            hit(t0, src.root(t0), 120, True, 60 if b < 36 else 40)
            if b == 36:
                for k in (48, 60, 66, 72, 78, 84, 90):
                    hit(t0 + k, src.root(t0 + k), 96 + k // 6)
        elif sc == 'B':
            for k, kind, v in BREAK:
                hit(t0 + k, src.root(t0 + k), v, kind == 'O', 22)
        elif sc == 'pedal':
            for k in range(0, BAR, 12 if b < 52 else 6):
                hit(t0 + k, src.root(t0 + k), 74 + (b - 48) * 7 + (12 if k % 48 == 0 else 0))
        elif sc == 'build':
            for k in (0, 6, 12, 24, 30, 36, 48, 54, 60, 72, 78, 84) if b < 61 else (0, 12, 24, 36):
                hit(t0 + k, src.root(t0 + k), 120 if k % 24 == 0 else 102)
        # de muur: powerchord op tel 1 en bij elke akkoordwissel (per halve maat), aangehouden
        for s, e, pc in root_spans(src, t0, t0 + BAR):
            if sc == 'bridge' and b < 36 and s > t0:
                continue
            wall.add(s, e, place(pc, 40), 120 if s == t0 else 112, wall_p)
        # bas: strakke achtsten op de grondtoon, mee met de kick
        if b == 0 or (sc == 'bridge' and b < 36):
            bass.add(t0, t0 + BAR, place(src.root(t0), 28), 127, bass_p)
        else:
            for k in range(0, BAR, 24):
                bass.add(t0 + k, t0 + k + 22, place(src.root(t0 + k), 28), 127, bass_p)
                if k != 48:
                    kick_t.add(t0 + k)
            if sc in ('C1', 'C2'):
                for k in range(0, BAR, 12):
                    if k != 48:
                        kick_t.add(t0 + k)
    gtr.notes = no_overlap(gtr.notes)
    bass.notes = no_overlap(bass.notes)
    wall.notes = no_overlap(wall.notes)

    kick, snare, cym, toms, fx = (Part(n, 'drums') for n in ('kick', 'snare', 'cym', 'toms', 'fx'))
    cym.track = 'cym'
    fx.track = 'fx'
    hats = Part('hats', 'hats', ds=False)
    kp = vg.kitprog

    def d(part, t, key, v, ln=10):
        part.add(t, t + ln, K[key], v, kp)
    fills = {9: 72, 17: 72, 21: 72, 29: 72, 33: 72, 47: 72, 53: 48, 61: 72}
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        fill = fills.get(b)
        cut = lambda t: fill is None or t < fill
        for t in sorted(x for x in kick_t if t0 <= x < t0 + BAR):
            if cut(t - t0):
                d(kick, t, 'kick', 124 if (t - t0) % 48 == 0 else 112, 16)    # v5: 16 ticks = subtoon (fit kort in)
        if t0 not in kick_t:
            d(kick, t0, 'kick', 124, 16)
        if b >= 1 and cut(48) and not (sc == 'bridge' and b < 36):
            d(snare, t0 + 48, 'snare', 127, 16)
        if b >= 1 and not (sc == 'bridge' and b < 36):     # open hihats op de tussenliggende achtsten (. x . x)
            for k in (12, 36, 60, 84):                     # v5: 18 ticks (0,21 s) open, accent op 2 en 4
                hats.add(t0 + k, t0 + k + 18, NOISE_HAT, 127 if k in (36, 84) else 112, vg.prog('noise'))
        if sc in ('C1', 'C2', 'build') and cut(48):
            d(cym, t0 + 48, 'china', 92, 20)
        if b in (0, 2, 6, 10, 14, 18, 20, 22, 26, 30, 32, 34, 37, 41, 45, 48, 50, 52, 54, 56, 58, 60):
            d(cym, t0, 'crash', 116, 48)
        if fill is not None:
            seq = ['snare', 'snare', 'tom_hi', 'tom_hi', 'tom_mid', 'tom_mid', 'tom_lo', 'tom_lo']
            n = (BAR - fill) // 6 if b == 53 else (BAR - fill) // 12
            stp = 6 if b == 53 else 12
            for k in range(n):
                key = seq[len(seq) - n + k] if n <= len(seq) else seq[(k * len(seq)) // n]
                d(toms if key.startswith('tom') else snare, t0 + fill + k * stp, key, 100 + k * 2, stp)
    # scratches alleen op de overgangen: 'wikka' + chirp in de laatste tel vóór elke zin (zinnen van 4 maten)
    starts = (6, 10, 14, 18, 22, 26, 30, 34, 37, 41, 45, 49, 54, 58)
    fx_spots = [(48, 'scratch', 24), (72, 'chirp', 20)]
    for b in starts:
        fx_spots += [(b * BAR - 24, 'scratch', 12), (b * BAR - 12, 'chirp', 12)]
    for t, key, ln in fx_spots:
        d(fx, t, key, 120, ln)
    for prt in (gtr, bass, kick, toms, wall):
        fit(prt, vg, bpm)
    order = [lead, kick, snare, bass, wall, gtr, fx, cym, toms]
    return dict(leader='Brawly', key='brawly', bpm=bpm, vg=vg, kit=kit, order=order, psg=[hats], metal=True,
                vols={'lead': 68, 'gtr': 60, 'wall': 80, 'bass': 127, 'drums': 110, 'cym': 80, 'fx': 100,
                      'hats': 127},
                pans={'lead': 64, 'gtr': 44, 'wall': 84, 'bass': 64, 'drums': 64, 'cym': 72, 'fx': 50, 'hats': 76},
                desc='91 kit (drumsets/gym_brawly.inc: zware kick, heavy-rock-snare, china, crash, toms, scratches), '
                     'daarna distortion-lead, palm-mute-chug, muur-powerchord (tweede Emerald-distortiongitaar), '
                     'overdrive-bas, PSG-ruis (open hihat).')


def flannery(src):
    """Ronde 3 (Jordi: 'stotterende, afgekapte percussie; te weinig strumming; saaie bas'): rumba flamenca, 208 bpm in
    half-time = 104 bpm. Palmas: claras (side stick + handklap, drie mensen) op de contratiempo (de 'en' van elke tel) en
    zestiende-syncopen, sordas op de tel; alles met natuurlijke naklink (lange noten, geen gegate snare, geen PSG-
    castagnetten). Cajón: bas op 1 en 3, slap op 2 en 4. Doorlopende rasgueado op de Emerald-nylongitaar: elke slag is
    één sample (down/up/golpe/rasgueado, open kwinten of majeur volgens het origineel) in gevoelde zestienden met het
    rumbapatroon. Fretloze bas met syncopen, octaafpops en slides naar de volgende grondtoon. Melodie voorop op de
    nylongitaar (geen trémolo), met af en toe een snelle Spaanse loop (picado) aan het eind van een zin."""
    bpm = 208
    kit = Kit('gym_flannery', [('cajon', dk2('gym_fla_cajon_bass', 170)), ('cslap', dk2('gym_fla_cajon_slap', 170)),
                               ('clara', dk2('gym_fla_pclara', 200, 74)), ('sorda', dk2('gym_fla_psorda', 190, 58))])
    strum_insts = {'%s_%s' % (k, q): [(45, ds('gym_fla_%s_%s' % (k, q), 150))]
                   for q in ('five', 'maj') for k in ('down', 'up', 'golpe', 'rasg')}
    vg = Voicegroup('grounded_gym_flannery', kit, dict({
        'nylon': [(48, ds('gym_fla_gba_nylon', 90, 25, 249))],
        'fretless': [(60, ds('sc88pro_fretless_bass', 100))],
    }, **strum_insts))
    K = kit.key
    RASG_LEAD = 9                                        # de accentslag zit 0,112 s (9 ticks bij 208 bpm) in de sample

    # melodie: noot voor noot (nylon klinkt natuurlijk uit), plus picado-loopjes in rusten aan het eind van een zin
    mel = melody_src(src)
    lead = Part('lead', 'lead')
    for s, e, n, v in mel:
        lead.add(s, e, guitar_octave(s, n), 118, vg.prog('nylon'))
    lead.notes = legato(lead.notes, 3, keep=0.9)
    ln = sorted(lead.notes)
    last_run = -4 * BAR
    for i in range(1, len(ln)):
        a, z = ln[i - 1], ln[i]
        free = z[0] - (a[0] + 36 if a[1] - a[0] >= 66 else a[1])   # rust, of de staart van een lange noot
        if free < 30 or z[0] - last_run < 4 * BAR or sec(z[0]) in ('intro', 'riff'):
            continue
        r = src.root(z[0] - 6)
        scale = SC_PHR if sec(z[0]) in ('B', 'pedal') else ({(r + k) % 12 for k in PHR_DOM} if r == 0 else SC_MAJ)
        k = min(6, free // 6)
        target = z[2]
        steps, cur = [], target
        while len(steps) < k:                            # van boven naar de volgende melodienoot toe (picado)
            cur += 1
            if cur % 12 in scale:
                steps.append(cur)
        t = z[0] - 6 * k
        a[1] = min(a[1], t)
        for j, nt in enumerate(reversed(steps)):
            lead.add(t + 6 * j, t + 6 * j + 5, nt, 96 + 4 * j, vg.prog('nylon'))
        last_run = z[0]
    second = Part('second', 'second')                    # intro: de chromatische loop op een tweede nylongitaar
    for s, e, n, v in intro_run(src):
        second.add(s, s + 5, n - 12, 88, vg.prog('nylon'))

    # rasgueado: doorlopend in gevoelde zestienden (12 ticks); rumbapatroon per halve maat (= 2 gevoelde tellen)
    strum = Part('strum', 'strum')
    voice = lambda pc: place(pc, 41)                     # A2-sample, grondtoon F2..E3

    def st(t, kind, v):
        q = quality(src, max(0, t))
        if kind == 'rasg':
            t -= RASG_LEAD
        strum.add(max(0, t), max(0, t) + 12, voice(src.root(max(0, t + (RASG_LEAD if kind == 'rasg' else 0)))), v,
                  vg.prog('%s_%s' % (kind, q)))
    RUMBA = ((0, 'down', 116), (12, 'up', 70), (24, 'down', 88), (36, 'up', 76),
             (48, 'golpe', 110), (60, 'up', 70), (72, 'down', 100), (84, 'up', 78))
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        if b == 0:
            st(t0, 'rasg', 120)
            continue
        if sc == 'riff':
            ons = {s - t0 for s, e, pc in src.riff if t0 <= s < t0 + BAR}
            for k, kind, v in RUMBA:
                if k in ons:
                    st(t0 + k, 'rasg', 122)
                elif not any(0 < o - k < 12 for o in ons):
                    st(t0 + k, kind, v - 10)
            continue
        if sc == 'bridge' and b < 36:
            st(t0, 'rasg', 112)
            st(t0 + 48, 'golpe', 96)
            continue
        dense = sc in ('C1', 'C2', 'build', 'B')
        for k, kind, v in RUMBA:
            if k == 0 and (b % 2 == 0 or dense):
                kind, v = 'rasg', 122                     # rasgueado-roffel naar de 1
            if k == 84 and (b % 2 == 1 or dense):
                continue                                  # die roffel begint al vóór de tel
            st(t0 + k, kind, v + (6 if dense else 0))
    strum.notes = no_overlap(strum.notes)
    starts = sorted({x[0] for x in strum.notes})
    for x in strum.notes:                                # elke slag klinkt door tot de volgende (zoals op de gitaar)
        nxt = next((s for s in starts if s > x[0]), x[0] + 2 * HB)
        x[1] = min(nxt, x[0] + 2 * HB)

    # fretloze bas: grondtoon, syncope op de 'a', octaafpop, kwint, en een chromatische nadering met slide
    bass = Part('bass', 'bass')
    bass.ccs.append((0, 20, 2))
    fp = vg.prog('fretless')
    for b in range(1, NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        r = place(src.root(t0), 28)
        r2 = place(src.root(t0 + 48), 28)
        nxt = place(src.root(t0 + BAR), 28)
        if sc == 'bridge' and b < 36:
            bass.add(t0, t0 + 40, r, 110, fp)
            continue
        pat = [(0, r, 16, 118), (36, r + 12, 6, 98), (48, r2 + 7 if r2 + 7 <= 52 else r2, 10, 106),
               (72, r2, 8, 104), (84, nxt - 1 if (b % 2) else nxt + 2, 9, 96)]
        if sc in ('C1', 'C2', 'build'):
            pat.insert(1, (18, r, 4, 84))
        for k, n, ln, v in pat:
            bass.add(t0 + k, t0 + k + ln, n, v, fp)
        if b % 2 == 0:                                    # slide in de 1: van een hele toon onder naar de grondtoon
            for j in range(6):
                bass.bends.append((t0 + j, pw(-64 + j * 64 // 6)))
            bass.bends.append((t0 + 6, pw(0)))
    bass.notes = no_overlap(bass.notes)

    caj, cslap, clara, sorda = (Part(n, 'perc') for n in ('cajon', 'cslap', 'clara', 'sorda'))
    clara.track = sorda.track = 'palmas'
    kp = vg.kitprog

    def d(part, t, key, v, ln=20):
        part.add(t, t + ln, K[key], v, kp)
    for b in range(NBARS):
        sc, t0 = sec(b * BAR), b * BAR
        dense = sc in ('C1', 'C2', 'build', 'B')
        d(caj, t0, 'cajon', 122, 22)                      # cajón: bas op 1 en 3, slap op 2 en 4
        if b == 0:
            continue
        d(cslap, t0 + 48, 'cslap', 116, 16)
        if dense:
            d(caj, t0 + 36, 'cajon', 96, 12)
            d(cslap, t0 + 84, 'cslap', 84, 10)
        if sc == 'bridge' and b < 36:
            for k in (24, 72):
                d(clara, t0 + k, 'clara', 104, 24)
            continue
        d(sorda, t0, 'sorda', 72, 18)                      # palmas sordas op de tel
        d(sorda, t0 + 48, 'sorda', 76, 18)
        for k in (24, 72):                                 # contratiempo: palma clara op de 'en'
            d(clara, t0 + k, 'clara', 116, 22)
        syn = (36, 84) if not dense else (36, 60, 84) if b % 2 else (12, 36, 60, 84)
        for k in syn:                                      # zestiende-syncopen
            d(clara, t0 + k, 'clara', 86 if k % 24 else 96, 10)
    for prt in (bass, caj, cslap, sorda):
        fit(prt, vg, bpm)
    order = [lead, bass, strum, caj, cslap, clara, sorda, second]
    return dict(leader='Flannery', key='flannery', bpm=bpm, vg=vg, kit=kit, order=order, psg=[],
                vols={'lead': 124, 'second': 96, 'strum': 104, 'bass': 108, 'perc': 112, 'palmas': 98},
                pans={'lead': 64, 'second': 74, 'strum': 50, 'bass': 64, 'perc': 64, 'palmas': 80},
                desc='91 kit (drumsets/gym_flannery.inc: cajón, palmas claras/sordas), daarna Emerald-nylongitaar '
                     '(melodie), fretloze bas, nylon-strums (down/up/golpe/rasgueado, open kwinten en majeur).')


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




LEADERS = [(647, 'MUS_GROUNDED_VS_ROXANNE', roxanne, 78), (648, 'MUS_GROUNDED_VS_BRAWLY', brawly, 76),
           (649, 'MUS_GROUNDED_VS_WATTSON', wattson, 74), (650, 'MUS_GROUNDED_VS_FLANNERY', flannery, 84)]
KERMIS_CHECK = ('roxanne', 'brawly', 'flannery')    # Wattson is goedgekeurd (gabber) en blijft byte-identiek
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
        if r['key'] in KERMIS_CHECK:                      # anti-kermis: eerst meten, alleen schrijven als het schoon is
            lead = next(p for p in r['order'] if p.name == 'lead')      # melodie noot voor noot (na de stemverdeler)
            have = {(x[0], x[2]) for x in lead.notes}
            lost = [x for x in melody_src(src) if (x[0], guitar_octave(x[0], x[2])) not in have]
            assert not lost, 'melodie mist %d noten, bijv. %s' % (len(lost), lost[:3])
            write_song(path + '.tmp', r['bpm'], r['order'] + r['psg'], r['vols'], r['pans'])
            fails = kermis_meter(path + '.tmp', open('sound/voicegroups/%s.inc' % vg.name).read(),
                                 open('sound/voicegroups/drumsets/%s.inc' % kit.name).read(), src,
                                 metal=r.get('metal', False))
            if fails:
                if not os.environ.get('GYM_KEEP_TMP'):
                    os.remove(path + '.tmp')
                sys.exit('KERMIS (%s), niet geschreven:\n  ' % r['leader'] + '\n  '.join(fails))
            os.replace(path + '.tmp', path)
            print('  anti-kermis: OK')
        else:
            write_song(path, r['bpm'], r['order'] + r['psg'], r['vols'], r['pans'])
        register(num, const, r['key'], V)
        print('  ->', path)


if __name__ == '__main__':
    main()
