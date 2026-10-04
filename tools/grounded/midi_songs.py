#!/usr/bin/env python3
# Project Grounded: maakt de eigen nummers in sound/songs/midi/ uit de originele MIDI's in sound/songs/grounded_src/.
# Draai vanuit de hoofdmap: python3 tools/grounded/midi_songs.py  (vereist: pip install mido)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from prepare_midi import prepare

SRC = 'sound/songs/grounded_src'
DST = 'sound/songs/midi'

# Colress (Pokémon Black 2/White 2): 10 nootsporen. Orchestra Hit (spoor 7) deelt kanaal 1 met Vocals -> kanaal 5.
# Synth Lead 1 (spoor 8) naar programma 81, zodat beide leads niet hetzelfde GBA-blokgolfkanaal gebruiken.
prepare(f'{SRC}/colress_battle.mid', f'{DST}/mus_grounded_vs_colress.mid',
        channel_map={7: 4}, program_map={8: 81})

# Macarena: 13 kanalen -> 10. Weg: fluit (spoor 5, verdubbelt de piccolo), tweede square lead (spoor 13), los effect (spoor 14).
prepare(f'{SRC}/macarena.mid', f'{DST}/mus_grounded_vs_birch.mid',
        drop_tracks=(5, 13, 14))
print('klaar')

# Automatisch voorbereid (groepering per GBA-instrument), zie prepare_auto in prepare_midi.py
from prepare_midi import prepare_auto, write_voicegroup
write_voicegroup()
for src, dst in [
    ('dppt_champion.mid', 'mus_grounded_vs_dppt_champion.mid'),
    ('dppt_cyrus.mid',    'mus_grounded_vs_cyrus.mid'),
    ('bw_n.mid',          'mus_grounded_vs_n.mid'),
    ('bw_ghetsis.mid',    'mus_grounded_vs_ghetsis.mid'),
]:
    prepare_auto(f'{SRC}/{src}', f'{DST}/{dst}')
for src, dst in [
    ('yoshi_castle.mid',      'mus_grounded_vs_yoshi_castle.mid'),
    ('mksc_broken_pier.mid',  'mus_grounded_vs_broken_pier.mid'),
    ('mksc_sunset_wilds.mid', 'mus_grounded_vs_sunset_wilds.mid'),
]:
    prepare_auto(f'{SRC}/{src}', f'{DST}/{dst}')

# Dark Cave is een HGSS-rip met eigen (niet-GM) instrumentnummers: kanaal 2 (shaker, noten 101-111) weg,
# kanaal 7 en 8 zijn baslijnen, en alles boven toonhoogte 84 gaat per octaaf omlaag.
prepare_auto(f'{SRC}/hgss_dark_cave.mid', f'{DST}/mus_grounded_vs_dark_cave.mid',
             drop_channels=(2,), channel_category={7: 'fingered_bass', 8: 'synth_bass'}, max_note=84)

# Giratina: de hoornpartij (kanaal 14) en een paar strijkers zitten op toonhoogte 85-104, veel te hoog voor
# de GBA-samples (piep aan het begin). Alles boven 84 gaat per octaaf omlaag.
prepare_auto(f'{SRC}/pt_giratina.mid', f'{DST}/mus_grounded_vs_giratina.mid', max_note=84,
             # vergeleken met een GBA-soundfont-opname: bas te zwak, midden te sterk
             volume={'strings': 80, 'piano': 80, 'horn': 86, 'trumpet': 86, 'flute': 86, 'square2': 76})

# Zinnia (ORAS, Delta Episode): gevechtsmuziek van Zinnia voor de Sky Pillar
prepare_auto(f'{SRC}/oras_zinnia.mid', f'{DST}/mus_grounded_vs_zinnia.mid', max_note=84)

# Neo Team Plasma (Black 2/White 2), MIDI van Byabbington (onlinesequencer): gevechtsmuziek van de Neo Plasma-deelnemers
# Sinds v2 gemaakt door tools/grounded/neo_plasma_theme.py (echte instrumenten per bronspoor, eigen voicegroup).
# prepare_auto(f'{SRC}/b2w2_neo_plasma.mid', f'{DST}/mus_grounded_vs_neo_plasma.mid', max_note=84)
