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
Gebruik: python3 tools/grounded/music_lint.py sound/songs/midi/mus_x.mid [...] [--genre stoner [--tonic C]]
Exitcode 1 bij fouten (FOUT); waarschuwingen (LET OP) laten het door."""
import os, re, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import releases, release_ticks

MAX_CHANS = 10          # src/m4a.c mixt 12 kanalen; 2 houden we vrij voor geluidseffecten
# uitzonderingen: legendary-gevechten mogen 11 (1 kanaal vrij voor effecten)
MAX_PER_SONG = {'mus_grounded_yi_athletic.mid': 11,   # SPC-rip: 8 SNES-stemmen + uitklinkstaartjes (5 momenten)
                'mus_grounded_vs_regigigas.mid': 11, 'mus_grounded_vs_suicune.mid': 11,
                'mus_grounded_vs_entei.mid': 11, 'mus_grounded_vs_raikou.mid': 11,
                'mus_grounded_vs_jirachi.mid': 11,
                'mus_grounded_vs_heatran.mid': 11,
                'mus_grounded_vs_shaymin.mid': 11,
                'mus_grounded_vs_rayquaza.mid': 11,
                'mus_grounded_vs_genesect.mid': 11,
                'mus_grounded_vs_victini.mid': 11,
                'mus_grounded_vs_darkrai.mid': 11,
                'mus_grounded_vs_tapu.mid': 11,
                'mus_grounded_vs_ho_oh.mid': 11,
                'mus_grounded_vs_lugia.mid': 11,
                'mus_grounded_vs_tornadus.mid': 11, 'mus_grounded_vs_thundurus.mid': 11,
                'mus_grounded_vs_landorus.mid': 11, 'mus_grounded_vs_hoopa.mid': 11,
                'mus_grounded_vs_ruinous.mid': 11,
                'mus_grounded_vs_zacian.mid': 11, 'mus_grounded_vs_xerneas.mid': 11,
                'mus_grounded_vs_lake_trio.mid': 11, 'mus_grounded_vs_legendary.mid': 11,

                'mus_grounded_vs_ultra_beast.mid': 11,
                'mus_grounded_vs_area_zero.mid': 11}
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


STONER_HELP = """--genre stoner [--tonic C]: extra controles voor stoner/desert rock (Heatran, zie MUZIEK.md 'Heatran v6/v7').
Anti-ska / anti-vrolijk (v1-v5 klonken als ska-punk/'Bowser's Castle'):
  - geen open hihat op de 'en', hihat-accent op de tel
  - geen chromatische Mario-loopjes (4+ noten in halve tonen dezelfde kant op) in melodische sporen
  - geen 'skank': aanslag naast de tel terwijl het spoor op die tel stil was (max. 5%)
  - met --tonic: geen grote terts boven de grondtoon (alleen mineur/pentatonisch/blues)
Niet saai (v6 was 'saai, statisch, eentonig': lange akkoorden, één riff); gemeten binnen de loop ([ ]):
  - minstens 2 tempowissels per loop (incl. de terugsprong)
  - minstens 6 verschillende maatpatronen in het laagste spoor, geen patroon in > 40% van de maten
  - vóór elke riffwissel (maatpatronen van de volgende 2 maten komen in de 4 ervoor niet voor) een stop (alle
    melodische sporen >= een 8e stil in de laatste tel) of een fill (>= 3 tom-/snareklappen in de laatste tel),
    vlak vóór de wisselmaat of aan het eind ervan (slotvariant)
  - palm-mute (programma met een '_pm_'/'mute'-sample): >= 40% van de snelle (8e/16e) aanslagen van het
    slaggitaarspoor (het spoor met het hoogste aandeel)
  - max. 15% van de tijd van het laagste spoor in noten van meer dan 2 tellen"""
NOTE_PC = {'C': 0, 'Db': 1, 'C#': 1, 'D': 2, 'Eb': 3, 'D#': 3, 'E': 4, 'F': 5, 'Gb': 6, 'F#': 6, 'G': 7, 'Ab': 8,
           'G#': 8, 'A': 9, 'Bb': 10, 'A#': 10, 'B': 11}


def kit_lines(mid):
    """drumnoot -> regel uit de drumkit van de voicegroup (samplenaam), of None."""
    vg = voicegroup_of(mid)
    voices = load_voices(vg) if vg else None
    kit = next((k[6:] for k in (voices or {}).values() if k.startswith('drums:')), None)
    path = os.path.join(VG_DIR, 'drumsets', (kit or '').replace('_drumset', '') + '.inc')
    if kit and os.path.exists(path):
        lines = [l.strip() for l in open(path) if l.strip().startswith(('voice_', 'voice_group'))]
        first = int(lines[0].split(',')[1])
        return {first + i: l for i, l in enumerate(lines[1:])}
    return None


def kit_hats(mid):
    """drumnoten -> 'hat' / 'ohat' uit de drumkit van de voicegroup (samplenaam), anders GM-nummers."""
    kl = kit_lines(mid)
    if kl is None:
        return {42: 'hat', 44: 'hat', 46: 'ohat'}
    out = {}
    for k, l in kl.items():
        if 'open_hihat' in l or 'open_hi_hat' in l:
            out[k] = 'ohat'
        elif 'hihat' in l or 'hi_hat' in l:
            out[k] = 'hat'
    return out


def kit_kind(mid, names, gm):
    kl = kit_lines(mid)
    if kl is None:
        return set(gm)
    return {k for k, l in kl.items() if any(x in l for x in names)}


def pm_programs(mid):
    """programma's waarvan de sample(s) palm-mute zijn ('_pm_' of 'mute' in de samplenaam, ook in een keysplit)."""
    vg = voicegroup_of(mid)
    path = os.path.join(VG_DIR, (vg or '') + '.inc')
    out, prog = set(), 0
    if not vg or not os.path.exists(path):
        return out
    for line in open(path):
        line = line.strip()
        if not line.startswith('voice_') or line.startswith('voice_group'):
            continue
        mm = re.search(r'@\s*(\d+)', line)
        if mm:
            prog = int(mm.group(1))
        text = line.lower()
        if line.startswith('voice_keysplit') and not line.startswith('voice_keysplit_all'):
            sub = os.path.join(VG_DIR, 'keysplits', line.split('voicegroup_')[1].split('_keysplit')[0] + '.inc')
            if os.path.exists(sub):
                text = open(sub).read().lower()
        if '_pm_' in text or 'mute' in text:
            out.add(prog)
        prog += 1
    return out


def stoner_lint(mid, tonic=None):
    m = mido.MidiFile(mid)
    tpb = m.ticks_per_beat
    tempo, tracks, loop = [], [], [None, None]
    for t in m.tracks:
        tick, on, ns, ch, prog = 0, {}, [], None, 0
        for x in t:
            tick += x.time
            if x.type == 'set_tempo':
                tempo.append((tick, x.tempo))
            if x.type == 'marker' and x.text in ('[', ']'):
                loop['[]'.index(x.text)] = tick
            if x.type == 'program_change':
                prog = x.program
            if x.type == 'note_on' and x.velocity:
                on[x.note] = (tick, x.velocity, prog)
                ch = x.channel
            elif x.type in ('note_on', 'note_off') and x.note in on:
                s, v, pr = on.pop(x.note)
                ns.append((s, tick, x.note, v, pr))
        if ns:
            tracks.append((ch, sorted(ns)))
    tempo.sort()
    errors = []
    hatmap = kit_hats(mid)
    drums = [n for ch, ns in tracks if ch == 9 for n in ns]
    hats = [n for n in drums if n[2] in hatmap]
    end = max(n[1] for ch, ns in tracks for n in ns)
    ls, le = loop[0] or 0, loop[1] or end
    # ===== anti-ska / anti-vrolijk =====
    oh = [n for n in hats if hatmap[n[2]] == 'ohat' and n[0] % tpb]
    if oh:
        errors.append('stoner: %d open hihats naast de tel (ska/disco)' % len(oh))
    on_v = [n[3] for n in hats if n[0] % tpb == 0]
    off_v = [n[3] for n in hats if n[0] % tpb]
    if on_v and off_v and sum(off_v) / len(off_v) >= sum(on_v) / len(on_v):
        errors.append('stoner: hihat op de en gemiddeld even hard als op de tel (off-beat-accent)')
    mel = [ns for ch, ns in tracks if ch != 9]
    for i, ns in enumerate(mel):
        starts = sorted(set(n[0] for n in ns))
        line = [min(n[2] for n in ns if n[0] == s) for s in starts]
        st = [b - a for a, b in zip(line, line[1:]) if b != a]
        runs = sum(1 for x, y, z in zip(st, st[1:], st[2:]) if abs(x) == 1 and x == y == z)
        if runs:
            errors.append('stoner: melodisch spoor %d heeft %d chromatische loopjes van 4+ noten' % (i, runs))
        sounding = lambda t: any(n[0] <= t < n[1] for n in ns)
        skank = sum(1 for s in starts if s % tpb and not sounding(s - s % tpb))
        if skank > 0.05 * len(starts):
            errors.append('stoner: melodisch spoor %d: %d off-beat-stoten na een stille tel (skank)' % (i, skank))
        if tonic is not None and any(n[2] % 12 == (tonic + 4) % 12 for n in ns):
            errors.append('stoner: melodisch spoor %d speelt de grote terts boven de grondtoon' % i)
    if not mel:
        return errors
    # ===== niet saai =====
    bar = 4 * tpb
    tl = [tp for t, tp in tempo if ls <= t < le]
    t0 = [tp for t, tp in tempo if t <= ls]
    if t0 and (not tl or tl[0] != t0[-1] or [t for t, tp in tempo if t == ls] == []):
        tl = [t0[-1]] + tl
    seq = [x for i, x in enumerate(tl) if i == 0 or x != tl[i - 1]]
    changes = len(seq) - 1 + (1 if len(seq) > 1 and seq[-1] != seq[0] else 0)
    if changes < 2:
        errors.append('stoner/saai: maar %d tempowissels per loop (min. 2: traag <-> snel)' % changes)
    lowest = min(mel, key=lambda ns: sum(n[2] for n in ns) / len(ns))
    bars = {}
    for b in range(ls // bar, (le + bar - 1) // bar):
        bars[b] = tuple(sorted((n[0] - b * bar, n[2]) for n in lowest if b * bar <= n[0] < (b + 1) * bar))
    pats = [p for p in bars.values() if p]
    if len(set(pats)) < 6:
        errors.append('stoner/saai: maar %d verschillende maatpatronen in het laagste spoor (één riff?)' % len(set(pats)))
    if pats and max(pats.count(p) for p in set(pats)) > 0.4 * len(pats):
        errors.append('stoner/saai: één maatpatroon in %.0f%% van de maten' % (100 * max(pats.count(p) for p in set(pats)) / len(pats)))
    toms = kit_kind(mid, ('_tom',), (41, 43, 45, 47, 48, 50))
    snares = kit_kind(mid, ('snare',), (38, 40))
    allmel = [n for ns in mel for n in ns]
    bl = sorted(bars)
    for i, b in enumerate(bl[1:], 1):
        nxt = {bars.get(b), bars.get(b + 1)} - {()}
        prev = {bars.get(x) for x in range(b - 4, b)} - {(), None}
        if not nxt or not prev or nxt & prev:
            continue
        ok = False
        for w1 in (b * bar, (b + 1) * bar):          # vlak vóór de wisselmaat, of aan het eind ervan (slotvariant)
            w0 = w1 - tpb
            sil = sum(1 for j in range(w0, w1, tpb // 4) if not any(n[0] <= j < n[1] for n in allmel))
            hits = len({n[0] for n in drums if n[2] in toms | snares and w0 <= n[0] < w1})
            ok |= sil >= 2 or hits >= 3
        if not ok:
            errors.append('stoner/saai: riffwissel op maat %d zonder stop of fill ervoor' % b)
    pmp = pm_programs(mid)
    share = 0.0
    for ns in mel:                                    # het slaggitaarspoor (het beste spoor) telt
        starts = sorted(set(n[0] for n in ns))
        nx = {s: b for s, b in zip(starts, starts[1:])}
        quick = [n for n in ns if ls <= n[0] < le and nx.get(n[0], 1 << 30) - n[0] <= tpb // 2]
        if len(quick) >= 20:
            share = max(share, sum(1 for n in quick if n[4] in pmp) / len(quick))
    if not pmp:
        errors.append('stoner/saai: geen palm-mute-instrument in de voicegroup')
    else:
        if share < 0.4:
            errors.append('stoner/saai: maar %.0f%% van de 8e/16e-aanslagen palm-muted (min. 40%%)' % (100 * share))
    lo = [n for n in lowest if ls <= n[0] < le]
    tot = sum(n[1] - n[0] for n in lo)
    lng = sum(n[1] - n[0] for n in lo if n[1] - n[0] > 2 * tpb)
    if tot and lng > 0.15 * tot:
        errors.append('stoner/saai: %.0f%% van het laagste spoor in noten > 2 tellen (lange akkoorden)' % (100 * lng / tot))
    return errors


if __name__ == '__main__':
    args = sys.argv[1:]
    genre = tonic = None
    if '--genre' in args:
        i = args.index('--genre'); genre = args[i + 1]; del args[i:i + 2]
    if '--tonic' in args:
        i = args.index('--tonic'); tonic = NOTE_PC[args[i + 1]]; del args[i:i + 2]
    if genre not in (None, 'stoner'):
        sys.exit('onbekend genre %s\n%s' % (genre, STONER_HELP))
    bad = 0
    for f in args:
        e, w = lint(f)
        if genre == 'stoner':
            e += stoner_lint(f, tonic)
        print('%s: %s' % (os.path.basename(f), 'OK' if not e else '%d fout(en)' % len(e)))
        for x in e[:12]:
            print('  FOUT  ', x)
        if len(e) > 12:
            print('  ... en nog %d' % (len(e) - 12))
        for x in w[:8]:
            print('  LET OP', x)
        bad |= bool(e)
    sys.exit(1 if bad else 0)
