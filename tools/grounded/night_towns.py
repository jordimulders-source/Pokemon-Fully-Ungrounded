#!/usr/bin/env python3
"""Project Grounded: nachtversies van de stads- en dorpsthema's (zoals in Diamond/Pearl). Jordi (11 okt): "Is het ook
niet zoveel moeite om de city themes een nacht thema van te maken? Zoals in Diamond en Pearl. Gewoon lichte remixes."

Lichte remix = het origineel 1-op-1 (sporen, noten, CC7-swells, loop, vorm, harmonie), alleen het karakter verandert:
  - tempo x ±0,88 (per stad, afgerond op even bpm: de m4a-tempobyte is bpm/2);
  - instrumenten zachter (in een eigen voicegroup per stad = kopie van de originele voicegroup met vervangen slots):
      piano / orgel / accordeon  -> elektrische piano (sd90 detuned EP, keysplit `night_ep`)
      trompet                     -> hoorn (of fluit als de partij onder C3 komt: koper klinkt daar als 'puuup')
      tuba                        -> fretless bas (als de partij onder C3 komt) of hoorn (melodie)
      fingered/slap/synth bass    -> fretless bas
      xylofoon                    -> harp
      PSG-blokgolven              -> 50%-blokgolf (de ronde, holle klank i.p.v. de schelle 12,5/25%), iets zachter
      PSG-ruis (hihat)            -> zachter
  - percussie als 'brushes': bekkens weg, open hihat -> gesloten, snare/clap heel zacht, kick/hats/tamboerijn zachter;
  - per stad nog een paar velocity-correcties (glockenspiel/buisklokken zachter, sleebellen in Ashfrost zachter).
Alleen stock-samples (de EP komt uit de FRLG-voicegroups); geen nieuwe samples. Het arrangeerscript meldt per stad
het maximale aantal DirectSound-noten tegelijk (origineel en nacht, inclusief uitklinktijd).

Nummers 712-725 (MUS_GROUNDED_NIGHT_*). Koppeling: src/overworld.c, GetLocationMusic (nacht + buitenkaart).
Gebruik: python3 tools/grounded/night_towns.py [--info]"""
import os, re, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import releases, release_ticks

MID = 'sound/songs/midi'
FIRST = 712
# (bronbestand, naam, tempofactor, extra velocity per programma {prog: factor}, vaste vervangingen {prog: voice-regel})
SONGS = [
    ('mus_littleroot',        'LITTLEROOT', 0.89, {}, {}),
    ('mus_oldale',            'OLDALE',     0.88, {}, {}),
    ('mus_petalburg',         'PETALBURG',  0.87, {}, {}),
    ('mus_rustboro',          'RUSTBORO',   0.88, {}, {}),
    ('mus_dewford',           'DEWFORD',    0.90, {}, {}),
    # v2 (Jordi 11 okt: "slateport en lilycove nog iets langzamer en relaxter, zodat het echt een nachtgevoel geeft"):
    # trager, brushes (alleen kick + snare op de 8e-tellen, heel zacht), PSG-hats en -akkoordstoten zachter en dunner
    ('mus_slateport',         'SLATEPORT',  0.80, {14: 0.7, 5: 0.75, 6: 0.75, 80: 0.75, 81: 0.75, 83: 0.75,
                                                   126: 0.6, 127: 0.6}, {},
     {'drums': {'snare': 0.22, 'kick': 0.4}, 'grid': {0: 12, 126: 12, 127: 12}, 'legato': {7}}),
    ('mus_verdanturf',        'VERDANTURF', 0.92, {}, {}),
    ('mus_fallarbor',         'FALLARBOR',  0.88, {9: 0.75}, {}),
    ('mus_fortree',           'FORTREE',    0.88, {}, {}),
    # v2: trager, begeleiding (strijkers/bas/PSG) legato: de zachte 'echo'-aanslag wordt één langere noot (rustiger
    # en minder DS-noten tegelijk), harp korter uitklinken, strijkers iets zachter
    ('mus_lilycove',          'LILYCOVE',   0.80, {48: 0.85}, {},
     {'legato': {2, 3, 6}, 'rel_cap': 200}),
    ('mus_sootopolis',        'SOOTOPOLIS', 0.88, {}, {}),
    ('mus_ever_grande',       'EVER_GRANDE', 0.88, {14: 0.8}, {}),
    ('mus_grounded_ashfrost', 'ASHFROST',   0.88, {9: 0.75, 89: 0.5}, {}),
    ('mus_rg_celadon',        'CELADON',    0.88, {}, {}),
]

EP = 'voice_keysplit voicegroup_night_ep_keysplit, keysplit_night_ep'
HORN = 'voice_keysplit voicegroup_french_horn_keysplit, keysplit_french_horn'
FLUTE = 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 0, 255, 165'
HARP = 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 226'
FRETLESS = 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 253, 0, %d'
EP_KEYSPLIT = ('voice_group night_ep_keysplit\n'
               '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_detuned_ep1_low, 255, 188, 128, 210\n'
               '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_detuned_ep1_high, 255, 204, 77, 210\n')
EP_TABLE = ('@ Project Grounded: elektrische piano voor de nachtversies van de stadsthema\'s (night_towns.py).\n'
            'keysplit night_ep, 24\n\tsplit 0, 65\n\tsplit 1, 120\n')

# percussie per sample in de drumkit: None = weg, (noot, factor) = vervangen, factor = alleen zachter
def drum_rule(line, kit_lines, over=None):
    if 'cymbal_crash' in line:
        return None
    if 'open_hihat' in line:
        close = [k for k, l in kit_lines.items() if 'close_hihat' in l]
        return (close[0], 0.5) if close else None
    over = over or {}
    for key, f in (('snare', 0.4), ('hand_clap', 0.35), ('kick', 0.6), ('tom', 0.6), ('close_hihat', 0.55),
                   ('tambourine', 0.45), ('timpani', 0.5), ('conga', 0.7), ('ride_bell', 0.5), ('cowbell', 0.5)):
        if key in line:
            return over.get(key, f)
    return 0.7


def parse_vg(path):
    """voicegroup-bestand -> (naam, beginnoot, [regels per programma])"""
    name, start, out = None, 0, []
    for l in open(path):
        s = l.strip()
        if s.startswith('voice_group'):
            parts = s.split(None, 1)[1].split(',')
            name = parts[0].strip()
            start = int(parts[1]) if len(parts) > 1 else 0
        elif s.startswith('voice_'):
            out.append(s.split('@')[0].strip())
    return name, start, out


def find_vg(name):
    for d in ('sound/voicegroups', 'sound/voicegroups/drumsets'):
        for f in os.listdir(d):
            if f.endswith('.inc'):
                p = os.path.join(d, f)
                with open(p) as fh:
                    head = fh.read(4000)
                if re.search(r'^voice_group %s\b' % name, head, re.M):
                    return p
    raise SystemExit('voicegroup niet gevonden: ' + name)


def cfg_of(src):
    for l in open(os.path.join(MID, 'midi.cfg')):
        if l.startswith(src + '.mid:'):
            return l.split(':', 1)[1].split()
    raise SystemExit('geen midi.cfg-regel voor ' + src)


def ranges(mid):
    """programma -> (laagste, hoogste) noot over alle sporen"""
    out = {}
    for t in mid.tracks:
        prog = 0
        for m in t:
            if m.type == 'program_change':
                prog = m.program
            elif m.type == 'note_on' and m.velocity:
                lo, hi = out.get(prog, (127, 0))
                out[prog] = (min(lo, m.note), max(hi, m.note))
    return out


def soften_square(line):
    # voice_square_1[_alt] key, pan, sweep, duty, a, d, s, r  |  voice_square_2[_alt] key, pan, duty, a, d, s, r
    kind, args = line.split(None, 1)
    a = [x.strip() for x in args.split(',')]
    di = 3 if kind.startswith('voice_square_1') else 2
    a[di] = '2'
    return '%s %s' % (kind, ', '.join(a))


def night_voice(prog, line, rng, rel_cap=None):
    """(nieuwe regel, velocityfactor) voor één programma"""
    lo, hi = rng.get(prog, (60, 60))
    if 'piano_keysplit' in line or 'sc88pro_organ2' in line or 'sc88pro_accordion' in line:
        return EP, 0.9
    if 'trumpet_keysplit' in line:
        return (HORN, 1.0) if lo >= 48 else (FLUTE, 1.0)
    if 'tuba_keysplit' in line:
        return (FRETLESS % 188, 1.0) if lo < 48 else (HORN, 1.0)
    if re.search(r'(fingered|slap|synth)_bass', line):
        rel = int(line.split(',')[-1])
        return FRETLESS % rel, 1.0
    if 'sc88pro_xylophone' in line:
        return HARP, 0.9
    if line.startswith('voice_square'):
        return soften_square(line), 0.8
    if line.startswith('voice_noise'):
        return line, 0.45
    cap = rel_cap or REL_CAP
    if line.startswith('voice_directsound ') and int(line.split(',')[-1]) > cap:
        # lange uitklinktijd (harp 242, glockenspiel 249): korter, zodat de stemverdeling binnen 10 DS-noten blijft
        return line.rsplit(',', 1)[0] + ', %d' % cap, 1.0
    return line, 1.0


REL_CAP = 220


def even_tempo(us, f):
    bpm = 60e6 / us * f
    return int(round(60e6 / (max(2, round(bpm / 2) * 2))))


def legato_echoes(track, maxvel=40):
    """Zachte 'echo' (zelfde toon, velocity <= maxvel, direct na het einde van de vorige noot) samenvoegen met die
    vorige noot: één langere, rustige noot i.p.v. aanslag + naklank."""
    ev, t = [], 0
    for m in track:
        t += m.time
        ev.append([t, m])
    off_at = {}   # (noot, tick) -> index van de note-off van de vorige noot
    drop = set()
    for i, (t, m) in enumerate(ev):
        if m.type == 'note_off' or (m.type == 'note_on' and m.velocity == 0):
            off_at[(m.note, t)] = i
        elif m.type == 'note_on' and m.velocity <= maxvel and (m.note, t) in off_at:
            j = off_at.pop((m.note, t))
            if j in drop:
                continue
            drop.update((i, j))
    out, last = mido.MidiTrack(), 0
    for i, (t, m) in enumerate(ev):
        if i in drop:
            continue
        out.append(m.copy(time=t - last))
        last = t
    return out, len(drop) // 2


def build(idx, src, key, tf, velx, fixed, opts=None, info=False):
    opts = opts or {}
    num = FIRST + idx
    low = 'mus_grounded_night_' + key.lower()
    vgname = 'grounded_night_' + key.lower()
    mid = mido.MidiFile(os.path.join(MID, src + '.mid'))
    cfg = cfg_of(src)
    gopt = [c for c in cfg if c.startswith('-G')][0]
    ovg = gopt[2:].lstrip('_')
    vol = int([c for c in cfg if c.startswith('-V')][0][2:])
    _, _, lines = parse_vg(find_vg(ovg))
    rng = ranges(mid)
    used = sorted(rng)
    new_lines, vel = list(lines), {}
    while len(new_lines) < 128:
        new_lines.append('voice_square_1 60, 0, 0, 2, 0, 0, 15, 0')
    report = []
    for p in used:
        nl, f = night_voice(p, lines[p], rng, opts.get('rel_cap'))
        if p in fixed:
            nl = fixed[p]
        new_lines[p] = nl
        vel[p] = f * velx.get(p, 1.0)
        if nl != lines[p] or vel[p] != 1.0:
            report.append('  %3d %-62s -> %-62s x%.2f  noten %d-%d' % (p, lines[p][:62], nl[:62], vel[p], *rng[p]))
    # drumkits
    kits = {}
    for p in used:
        m = re.match(r'voice_keysplit_all voicegroup_(\w+)', lines[p])
        if m:
            kn, ks, kl = parse_vg(find_vg(m.group(1)))
            kits[p] = {ks + i: l for i, l in enumerate(kl)}
    # MIDI
    out = mido.MidiFile(type=mid.type, ticks_per_beat=mid.ticks_per_beat)
    dropped = kept = merged = 0
    tempi = []
    grid = opts.get('grid', {})
    for ti, t in enumerate(mid.tracks):
        nt, prog, carry, skip, at = mido.MidiTrack(), 0, 0, {}, 0
        for m in t:
            at += m.time
            m = m.copy(time=m.time + carry)
            carry = 0
            if m.type == 'set_tempo':
                m = m.copy(tempo=even_tempo(m.tempo, tf))
                tempi.append(round(60e6 / m.tempo))
            elif m.type == 'program_change':
                prog = m.program
            elif m.type in ('note_on', 'note_off'):
                on = m.type == 'note_on' and m.velocity > 0
                if not on:
                    if skip.get(m.note):
                        skip[m.note] -= 1
                        carry = m.time
                        continue
                    if prog in kits and m.note in kits[prog].get('_map', {}):
                        m = m.copy(note=kits[prog]['_map'][m.note])
                else:
                    f = vel.get(prog, 1.0)
                    if prog in grid and at % grid[prog]:
                        # minder druk: alleen aanslagen op het raster (bijv. 8e-tellen)
                        skip[m.note] = skip.get(m.note, 0) + 1
                        carry = m.time
                        dropped += 1
                        continue
                    if prog in kits:
                        r = drum_rule(kits[prog].get(m.note, ''), kits[prog], opts.get('drums'))
                        if r is None:
                            skip[m.note] = skip.get(m.note, 0) + 1
                            carry = m.time
                            dropped += 1
                            continue
                        if isinstance(r, tuple):
                            kits[prog].setdefault('_map', {})[m.note] = r[0]
                            m = m.copy(note=r[0])
                            r = r[1]
                        f = r
                    kept += 1
                    m = m.copy(velocity=max(1, min(127, int(round(m.velocity * f)))))
            nt.append(m)
        if ti in opts.get('legato', ()):
            nt, n = legato_echoes(nt)
            merged += n
        out.tracks.append(nt)
    path = os.path.join(MID, low + '.mid')
    out.save(path)
    # voicegroup
    vgp = 'sound/voicegroups/%s.inc' % vgname
    with open(vgp, 'w') as fh:
        fh.write('@ Project Grounded: nachtversie van %s (%s), gegenereerd door tools/grounded/night_towns.py.\n' % (src, ovg))
        fh.write('@ Kopie van voicegroup_%s met zachtere instrumenten (EP, hoorn, fretless, harp, 50%%-blokgolven).\n' % ovg)
        fh.write('voice_group %s\n' % vgname)
        for i, l in enumerate(new_lines):
            fh.write('\t%s  @ %d\n' % (l, i) if i % 8 == 0 else '\t%s\n' % l)
    # stemmen tellen (origineel vs. nacht)
    def peak(m, vg, bpm):
        from musiclib import ds_occupancy
        rel = releases(vg)
        occ = []
        for t in m.tracks:
            occ += ds_occupancy(t, rel, m.ticks_per_beat, bpm, drum_len=m.ticks_per_beat // 2)
        ev = sorted([(s, 1) for s, e in occ] + [(e, -1) for s, e in occ], key=lambda x: (x[0], x[1]))
        cur = mx = 0
        for _, d in ev:
            cur += d
            mx = max(mx, cur)
        return mx
    obpm = 60e6 / next(m.tempo for tr in mid.tracks for m in tr if m.type == 'set_tempo')
    po, pn = peak(mid, ovg, obpm), peak(out, vgname, tempi[0])
    print('%d %s: %s, %s bpm (was %d), DS-noten max %s -> %d, drumnoten weg %d%s' % (
        num, low, ovg, sorted(set(tempi)), round(obpm), po, pn, dropped,
        ', echo\'s legato %d' % merged if merged else ''))
    if info:
        print('\n'.join(report))
    other = ' '.join(c for c in cfg if not c.startswith(('-G', '-V')))
    return num, low, vgname, '%s.mid: %s -G_%s -V%03d' % (low, other, vgname, VOLS.get(key, vol))


# -V per nachtversie (na meting met batchrec: piek <= 110-120/127 en een RMS die niet ver onder het origineel zakt)
VOLS = {'SLATEPORT': 84}   # v2: brushes en dunnere begeleiding maken hem zachter (RMS 1750 bij -V070)


def register(entries):
    h = open('include/constants/songs.h').read()
    t = open('sound/song_table.inc').read()
    # plaatshouders voor 704-711 (nummers van andere agents) zodat constante = index blijft
    tab = [l for l in t.split('\n') if re.match(r'\s*song ', l)]
    n_tab = len(tab)
    add_t = ''
    while n_tab < FIRST:
        add_t += '\n\tsong mus_dummy, MUSIC_PLAYER_BGM, 0 @ Project Grounded: plaatshouder %d (ander muzieknummer)\n' % n_tab
        n_tab += 1
    add_h = ''
    for num, low, vgname, line in entries:
        const = low.upper()
        if '#define %s ' % const not in h:
            add_h += '#define %s %d // Project Grounded: nachtversie van een stadsthema (tools/grounded/night_towns.py)\n' % (const, num)
        if '\tsong %s,' % low not in t:
            assert n_tab == num, (n_tab, num)
            add_t += '\n\tsong %s, MUSIC_PLAYER_BGM, 0\n' % low
            n_tab += 1
    if add_h:
        last = list(re.finditer(r'^#define MUS_GROUNDED_\w+\s+\d+.*$', h, re.M))[-1]
        i = last.end() + 1
        h = h[:i] + add_h + h[i:]
        open('include/constants/songs.h', 'w').write(h)
    if add_t:
        i = t.index('\n\t.align 2\ndummy_song_header:')
        t = t[:i].rstrip('\n') + '\n' + add_t + t[i:]
        open('sound/song_table.inc', 'w').write(t)
    c = open(os.path.join(MID, 'midi.cfg')).read().rstrip('\n').split('\n')
    for num, low, vgname, line in entries:
        hit = [i for i, l in enumerate(c) if l.startswith(low + '.mid:')]
        if hit:
            c[hit[0]] = line
        else:
            c.append(line)
    open(os.path.join(MID, 'midi.cfg'), 'w').write('\n'.join(c) + '\n')
    v = open('sound/voice_groups.inc').read()
    incs = ['keysplits/night_ep.inc'] + ['%s.inc' % e[2] for e in entries]
    for inc in incs:
        if '"sound/voicegroups/%s"' % inc not in v:
            v = v.rstrip('\n') + '\n.include "sound/voicegroups/%s"\n' % inc
    open('sound/voice_groups.inc', 'w').write(v)
    k = open('sound/keysplit_tables.inc').read()
    if 'keysplit night_ep,' not in k:
        open('sound/keysplit_tables.inc', 'w').write(k.rstrip('\n') + '\n\n' + EP_TABLE)


def main():
    info = '--info' in sys.argv
    with open('sound/voicegroups/keysplits/night_ep.inc', 'w') as fh:
        fh.write(EP_KEYSPLIT)
    entries = [build(i, *s, info=info) for i, s in enumerate(SONGS)]
    register(entries)


if __name__ == '__main__':
    main()
