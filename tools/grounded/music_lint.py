#!/usr/bin/env python3
"""Project Grounded: controleert een MIDI vóór hij in de game of naar Jordi gaat (zie tools/grounded/MUZIEK.md).

Controleert ook het aantal sporen (max. NUM_TRACKS_BGM in sound/music_player_table.inc).
Leest de voicegroup uit midi.cfg (-G_...) en meldt de fouten die we eerder maakten:
  - meer DirectSound-noten tegelijk dan de engine mixt (MAX_CHANS, src/m4a.c) -> noten worden afgekapt ("snips");
    uitklinktijd per instrument uit de release van de voicegroup (musiclib.release_ticks)
  - dubbele noten (zelfde spoor, noot en tick) -> volumepiek/klik + kanaalroof
  - drumnoten die in de drumkit PSG zijn (piepjes) of buiten de kit vallen (stilte)
  - melodische programma's die PSG zijn (vierkant/ruis/golf) -> losse piepjes, alleen bewust gebruiken
  - extreem lage noten (< E1) op DirectSound -> vervormde dreun
Gebruik: python3 tools/grounded/music_lint.py sound/songs/midi/mus_x.mid [...]
Exitcode 1 bij fouten (FOUT); waarschuwingen (LET OP) laten het door."""
import os, re, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import releases, release_ticks

MAX_CHANS = 10          # src/m4a.c mixt 12 kanalen; 2 houden we vrij voor geluidseffecten
# uitzonderingen: legendary-gevechten mogen 11 (1 kanaal vrij voor effecten)
MAX_PER_SONG = {'mus_grounded_vs_regigigas.mid': 11, 'mus_grounded_vs_suicune.mid': 11,
                'mus_grounded_vs_entei.mid': 11, 'mus_grounded_vs_raikou.mid': 11,
                'mus_grounded_vs_jirachi.mid': 11}
CFG = 'sound/songs/midi/midi.cfg'
VG_DIR = 'sound/voicegroups'


def voicegroup_of(mid):
    name = os.path.basename(mid)
    for line in open(CFG):
        if line.startswith(name + ':'):
            m = re.search(r'-G_?(\w+)', line)
            return m.group(1) if m else None
    return None


def load_voices(vg):
    """programma -> 'ds' | 'psg' | 'drums:<kit>'."""
    path = os.path.join(VG_DIR, vg + '.inc')
    if not os.path.exists(path):
        return None
    out, prog = {}, 0
    for line in open(path):
        line = line.strip()
        if not line.startswith('voice_') or line.startswith('voice_group'):   # 'voice_group x' is geen instrument
            continue
        m = re.search(r'@\s*(\d+)', line)
        if m:
            prog = int(m.group(1))
        kind = line.split()[0]
        if kind.startswith('voice_keysplit_all'):
            out[prog] = 'drums:' + line.split('voicegroup_')[1].split()[0]
        elif kind.startswith(('voice_square', 'voice_noise', 'voice_programmable_wave')):
            out[prog] = 'psg'
        else:
            out[prog] = 'ds'
        prog += 1
    return out


def load_kit(kit):
    path = os.path.join(VG_DIR, 'drumsets', kit.replace('_drumset', '') + '.inc')
    if not os.path.exists(path):
        return None
    lines = [l.strip() for l in open(path) if l.strip().startswith(('voice_', 'voice_group'))]
    first = int(lines[0].split(',')[1])
    return {first + i: ('psg' if l.startswith(('voice_square', 'voice_noise', 'voice_programmable')) else 'ds')
            for i, l in enumerate(lines[1:])}


def lint(mid):
    m = mido.MidiFile(mid)
    scale = 96 / m.ticks_per_beat
    vg = voicegroup_of(mid)
    voices = load_voices(vg) if vg else None
    errors, warns = [], []
    # de muziekspeler speelt max. NUM_TRACKS_BGM sporen; de rest wordt stilletjes overgeslagen (Mewtwo v3, Regigigas)
    import re as _re
    maxtr = int(_re.search(r'NUM_TRACKS_BGM,\s*(\d+)', open('sound/music_player_table.inc').read()).group(1))
    ntr = sum(1 for t in m.tracks if any(x.type == 'note_on' for x in t))
    if ntr > maxtr:
        errors.append('%d sporen met noten, de muziekspeler speelt er max. %d (NUM_TRACKS_BGM): de laatste vallen weg' % (ntr, maxtr))
    if voices is None:
        warns.append('voicegroup onbekend (%s); PSG-controle overgeslagen' % vg)
    tempo = next((x.tempo for t in m.tracks for x in t if x.type == 'set_tempo'), 500000)
    sec = lambda tick: tick / m.ticks_per_beat * tempo / 1e6
    rel = releases(vg) if voices else {}
    bpm = 60e6 / tempo
    ds_notes = []
    for ti, t in enumerate(m.tracks):
        tick, on, prog, seen = 0, {}, {}, set()
        for x in t:
            tick += x.time
            if x.type == 'program_change':
                prog[x.channel] = x.program
            if x.type == 'note_on' and x.velocity:
                key = (x.channel, x.note, tick)
                if key in seen:
                    errors.append('dubbele noot spoor %d noot %d op %.2f s' % (ti, x.note, sec(tick)))
                seen.add(key)
                on.setdefault((x.channel, x.note), []).append(tick)
            elif x.type in ('note_on', 'note_off') and on.get((x.channel, x.note)):
                s = on[(x.channel, x.note)].pop(0)
                p = prog.get(x.channel, 0)
                kind = voices.get(p, 'ds') if voices else 'ds'
                if kind.startswith('drums:'):
                    kit = load_kit(kind[6:])
                    if kit is not None:
                        k = kit.get(x.note)
                        if k is None:
                            errors.append('drumnoot %d valt buiten de kit (%s) op %.2f s' % (x.note, kind[6:], sec(s)))
                        elif k == 'psg':
                            errors.append('drumnoot %d is PSG (piepje) op %.2f s' % (x.note, sec(s)))
                            continue
                    ds_notes.append((s, min(tick, s + 2 * m.ticks_per_beat), ti))   # drums: echte lengte (max 2 tellen)
                elif kind == 'psg':
                    warns.append('spoor %d programma %d is PSG (vierkant/ruis): bewust?' % (ti, p))
                else:
                    if x.note < 28:
                        warns.append('spoor %d noot %d (< E1) op %.2f s: vervormde dreun?' % (ti, x.note, sec(s)))
                    ds_notes.append((s, tick + release_ticks(rel.get(p, 200), m.ticks_per_beat, bpm), ti))
    # polyfonie
    starts = sorted(set(n[0] for n in ds_notes))
    over = []
    cap = MAX_PER_SONG.get(os.path.basename(mid), MAX_CHANS)
    for s in starts:
        c = sum(1 for a, b, _ in ds_notes if a <= s < b)
        if c > cap:
            over.append((sec(s), c))
    if over:
        errors.append('%d momenten met meer dan %d DirectSound-noten (max %d), bijv. %s' % (
            len(over), cap, max(c for _, c in over), ', '.join('%.1f s' % t for t, _ in over[:6])))
    # PSG-waarschuwingen ontdubbelen
    warns = sorted(set(warns))
    return errors, warns


if __name__ == '__main__':
    bad = 0
    for f in sys.argv[1:]:
        e, w = lint(f)
        print('%s: %s' % (os.path.basename(f), 'OK' if not e else '%d fout(en)' % len(e)))
        for x in e[:12]:
            print('  FOUT  ', x)
        if len(e) > 12:
            print('  ... en nog %d' % (len(e) - 12))
        for x in w[:8]:
            print('  LET OP', x)
        bad |= bool(e)
    sys.exit(1 if bad else 0)
