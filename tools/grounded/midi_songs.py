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
