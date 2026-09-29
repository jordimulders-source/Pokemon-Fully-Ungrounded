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
