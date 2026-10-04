#!/usr/bin/env python3
# Project Grounded: bereidt een General MIDI-bestand voor op mid2agb + voicegroup_grounded_gm.
# - drumkanaal (10) krijgt programma 127 (= drumset in de grounded_gm-voicegroup)
# - sporen/kanalen weglaten (GBA-BGM heeft maximaal 10 sporen)
# - kanalen omzetten (mid2agb maakt één GBA-spoor per MIDI-kanaal)
# - programma's omzetten
# - loop-markers [ en ] rond het hele nummer
# Gebruik: zie tools/grounded/midi_songs.py
import mido

def prepare(src, dst, drop_tracks=(), channel_map=None, program_map=None, loop=True):
    channel_map = channel_map or {}   # {track_index: new_channel}
    program_map = program_map or {}   # {track_index: new_program}
    m = mido.MidiFile(src)
    out = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    end_tick = 0
    for ti, t in enumerate(m.tracks):
        if ti in drop_tracks:
            continue
        nt = mido.MidiTrack(); tick = 0; is_drum = False
        for msg in t:
            tick += msg.time
            if not msg.is_meta and hasattr(msg, 'channel'):
                ch = channel_map.get(ti, msg.channel)
                msg = msg.copy(channel=ch)
                if ch == 9:
                    is_drum = True
                if msg.type == 'program_change':
                    if ch == 9:
                        msg = msg.copy(program=127)
                    elif ti in program_map:
                        msg = msg.copy(program=program_map[ti])
            nt.append(msg)
        end_tick = max(end_tick, tick)
        if is_drum and not any(x.type == 'program_change' for x in nt):
            nt.insert(0, mido.Message('program_change', channel=9, program=127, time=0))
        if ti in program_map and not any(x.type == 'program_change' for x in nt):
            ch = next((x.channel for x in nt if hasattr(x, 'channel')), 0)
            nt.insert(0, mido.Message('program_change', channel=ch, program=program_map[ti], time=0))
        out.tracks.append(nt)
    if loop:
        conductor = out.tracks[0]
        conductor.insert(0, mido.MetaMessage('marker', text='[', time=0))
        # ']' aan het eind van het langste spoor
        total = sum(x.time for x in conductor)
        conductor.append(mido.MetaMessage('marker', text=']', time=max(0, end_tick - total)))
    out.save(dst)


# ---------------------------------------------------------------------------
# Automatische variant: groepeert alle noten per GBA-instrument van voicegroup_grounded_gm,
# zodat ook grote orkest-MIDI's binnen de 10 sporen passen. Volume (CC7/CC11) wordt in de
# velocity verwerkt; pitch bends vallen weg.

VOICES = {
    'piano':         'voice_keysplit voicegroup_piano_keysplit, keysplit_piano',
    'glockenspiel':  'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 242',
    'xylophone':     'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_xylophone, 255, 235, 0, 204',
    'organ':         'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127',
    'square1':       'voice_square_1 60, 0, 0, 2, 0, 0, 15, 0',
    'square2':       'voice_square_2 60, 0, 2, 0, 1, 7, 1',
    'fingered_bass': 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
    'slap_bass':     'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_slap_bass, 255, 235, 128, 99',
    'synth_bass':    'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 252, 0, 115',
    'strings':       'voice_keysplit voicegroup_strings_keysplit, keysplit_strings',
    'harp':          'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 242',
    'timpani':       'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 226',
    'choir':         'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 255, 0, 255, 165',
    'trumpet':       'voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet',
    'tuba':          'voice_keysplit voicegroup_tuba_keysplit, keysplit_tuba',
    'horn':          'voice_keysplit voicegroup_french_horn_keysplit, keysplit_french_horn',
    'oboe':          'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127',
    'flute':         'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127',
    'taiko':         'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 0',
    'cymbal':        'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216',
    'noise':         'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    'drums':         'voice_keysplit_all voicegroup_rs_drumset',
}


def gm_category(program):
    """GM-programma -> (categorie, representatief programma). Bron voor sound/voicegroups/grounded_gm.inc."""
    p = program
    if p in (9, 10, 14): return ('glockenspiel', 9)
    if p in (11, 12, 13): return ('xylophone', 13)
    if p < 16: return ('piano', 0)
    if p < 24: return ('organ', 16)
    if p < 32: return ('square2', 81)
    if p < 36: return ('fingered_bass', 33)
    if p < 38: return ('slap_bass', 36)
    if p < 40: return ('synth_bass', 38)
    if p == 46: return ('harp', 46)
    if p == 47: return ('timpani', 47)
    if p < 52: return ('strings', 48)
    if p < 55: return ('choir', 52)
    if p in (57, 58): return ('tuba', 58)
    if p == 60: return ('horn', 60)
    if p < 64: return ('trumpet', 56)
    if p < 72: return ('oboe', 68)
    if p < 80: return ('flute', 73)
    if p == 80: return ('square1', 80)
    if p < 88: return ('square2', 81)
    if p < 104: return ('strings', 48)
    if p < 112: return ('piano', 0)
    if p in (116, 117, 118): return ('taiko', 116)
    if p < 120: return ('cymbal', 119)
    if p < 127: return ('noise', 121)
    return ('drums', 127)


def write_voicegroup(path='sound/voicegroups/grounded_gm.inc'):
    lines = ["@ Project Grounded: General MIDI-achtige voicegroup voor geïmporteerde MIDI's.",
             "@ Gegenereerd door tools/grounded/prepare_midi.py (write_voicegroup); programma 127 = drumset.",
             "voice_group grounded_gm"]
    for p in range(128):
        lines.append(f"\t{VOICES[gm_category(p)[0]]}  @ {p}")
    open(path, 'w').write('\n'.join(lines) + '\n')


def prepare_auto(src, dst, max_tracks=10, loop=True, report=True,
                 drop_channels=(), channel_category=None, transpose=None, max_note=None,
                 volume=None, min_note=None):
    """drop_channels: MIDI-kanalen die wegvallen; channel_category: {kanaal: categorie} om het instrument
    te overschrijven (bv. rips met niet-GM-programma's); transpose: {kanaal: halve tonen};
    max_note: noten hoger dan dit gaan per octaaf omlaag (tegen piepende hoge tonen);
    min_note: {kanaal: noot}: lagere noten gaan per octaaf omhoog (een sample ver omlaag gestemd = lange 'puuup');
    volume: {categorie: 0-127} spoorvolume (standaard 127), om de balans tussen bas en midden te regelen."""
    channel_category = channel_category or {}
    transpose = transpose or {}
    m = mido.MidiFile(src)
    tempo_events = []                     # (tick, meta)
    notes = {}                            # categorie -> list of (tick, on, note, vel)
    for ti, t in enumerate(m.tracks):
        tick = 0; prog = {}; vol = {}; expr = {}; active = {}
        for msg in t:
            tick += msg.time
            if msg.is_meta:
                if msg.type in ('set_tempo', 'time_signature'):
                    tempo_events.append((tick, msg))
                continue
            ch = getattr(msg, 'channel', None)
            if msg.type == 'program_change':
                prog[ch] = msg.program
            elif msg.type == 'control_change' and msg.control == 7:
                vol[ch] = msg.value
            elif msg.type == 'control_change' and msg.control == 11:
                expr[ch] = msg.value
            elif msg.type in ('note_on', 'note_off') and ch in drop_channels:
                continue
            elif msg.type == 'note_on' and msg.velocity > 0:
                cat = 'drums' if ch == 9 else channel_category.get(ch, gm_category(prog.get(ch, 0))[0])
                v = int(msg.velocity * vol.get(ch, 100) / 127 * expr.get(ch, 127) / 127)
                n = msg.note + transpose.get(ch, 0)
                if max_note is not None and ch != 9:
                    while n > max_note:
                        n -= 12
                while min_note and n < min_note.get(ch, 0):
                    n += 12
                n = max(0, min(127, n))
                notes.setdefault(cat, []).append((tick, 1, n, max(1, min(127, v))))
                active.setdefault((ch, msg.note), []).append((cat, n))
            elif msg.type in ('note_off', 'note_on'):
                stack = active.get((ch, msg.note))
                if stack:
                    cat, n = stack.pop(0)
                    notes[cat].append((tick, 0, n, 0))
    end_tick = max((ev[0] for evs in notes.values() for ev in evs), default=0)
    count = {c: sum(1 for e in evs if e[1]) for c, evs in notes.items()}
    keep = []
    if 'drums' in notes:
        keep.append('drums')
    keep += [c for c in sorted(count, key=lambda c: -count[c]) if c != 'drums'][:max_tracks - len(keep)]
    # Categorieën die niet meer passen, samenvoegen met het meest verwante instrument dat wel een spoor heeft.
    FALLBACK = {
        'choir': ['strings', 'organ', 'horn', 'flute'], 'organ': ['strings', 'choir', 'piano'],
        'oboe': ['flute', 'strings', 'horn'], 'flute': ['oboe', 'strings', 'square1'],
        'tuba': ['horn', 'trumpet', 'fingered_bass'], 'horn': ['trumpet', 'tuba', 'strings'],
        'trumpet': ['horn', 'tuba', 'strings'], 'glockenspiel': ['xylophone', 'piano', 'harp'],
        'xylophone': ['glockenspiel', 'piano', 'harp'], 'harp': ['piano', 'strings'],
        'square1': ['square2', 'flute'], 'square2': ['square1', 'flute'],
        'noise': ['drums', 'cymbal'], 'cymbal': ['drums', 'noise'], 'taiko': ['timpani', 'drums'],
        'timpani': ['taiko', 'drums', 'fingered_bass'], 'piano': ['harp', 'strings'],
        'strings': ['choir', 'organ', 'piano'],
        'fingered_bass': ['synth_bass', 'slap_bass'], 'synth_bass': ['fingered_bass', 'slap_bass'],
        'slap_bass': ['fingered_bass', 'synth_bass'],
    }
    merged = []
    for c in [c for c in notes if c not in keep]:
        target = next((t for t in FALLBACK.get(c, []) if t in keep), None)
        if target:
            notes[target] += notes[c]
            merged.append(f'{c}->{target}')
    dropped = [c for c in notes if c not in keep and not any(m.startswith(c + '->') for m in merged)]

    out = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    cond = mido.MidiTrack(); out.tracks.append(cond)
    evs = sorted(tempo_events, key=lambda e: e[0])
    if loop:
        evs = [(0, mido.MetaMessage('marker', text='['))] + evs + [(end_tick, mido.MetaMessage('marker', text=']'))]
    last = 0
    for tk, msg in evs:
        cond.append(msg.copy(time=tk - last)); last = tk
    free = [c for c in range(16) if c != 9]
    for cat in keep:
        ch = 9 if cat == 'drums' else free.pop(0)
        program = next(gm_category(p)[1] for p in range(128) if gm_category(p)[0] == cat)
        tr = mido.MidiTrack(); out.tracks.append(tr)
        tr.append(mido.Message('program_change', channel=ch, program=program, time=0))
        tr.append(mido.Message('control_change', channel=ch, control=7, value=(volume or {}).get(cat, 127), time=0))
        last = 0
        for tk, on, note, v in sorted(notes[cat], key=lambda e: (e[0], e[1])):
            tr.append(mido.Message('note_on' if on else 'note_off', channel=ch, note=note, velocity=v, time=tk - last)); last = tk
    out.save(dst)
    if report:
        print(f'{dst}: sporen {keep}' + (f' | samengevoegd: {merged}' if merged else '') + (f' | weggelaten: {dropped} ({sum(count[c] for c in dropped)} noten)' if dropped else ''))
