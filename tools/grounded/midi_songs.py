#!/usr/bin/env python3
# Project Grounded: maakt de eigen nummers in sound/songs/midi/ uit de originele MIDI's in sound/songs/grounded_src/.
# Draai vanuit de hoofdmap: python3 tools/grounded/midi_songs.py  (vereist: pip install mido)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from prepare_midi import prepare

SRC = 'sound/songs/grounded_src'
DST = 'sound/songs/midi'

# PSG-drumnoten in rs_drumset (37/44/49/51/52/56/58/61/63 = vaste blokgolftoon, een crash klinkt als een lange
# 'puuup', Ghetsis v0.9.65) -> DirectSound-noot in dezelfde kit. (noot, factor) = ook de velocity schalen.
RS_PSG_FIX = {37: 38, 44: 42, 49: 57, 51: 59, 52: 57}
SIDE_STICK_SOFT = (38, 0.6)   # side stick -> snare, zachter (geen rimshot-sample in de kit)

# Colress (Pokémon Black 2/White 2): 10 nootsporen. Orchestra Hit (spoor 7) deelt kanaal 1 met Vocals -> kanaal 5.
# Synth Lead 1 (spoor 8) naar programma 81, zodat beide leads niet hetzelfde GBA-blokgolfkanaal gebruiken.
# v0.9.67: crash 49 en chinese cymbal 52 (PSG) -> orkestcrash 57.
prepare(f'{SRC}/colress_battle.mid', f'{DST}/mus_grounded_vs_colress.mid',
        channel_map={7: 4}, program_map={8: 81}, drum_map=RS_PSG_FIX)

# Macarena: 13 kanalen -> 10. Weg: fluit (spoor 5, verdubbelt de piccolo), tweede square lead (spoor 13), los effect (spoor 14).
# v0.9.67: pedaal-hihat 44 -> gesloten hihat 42, open hoge conga 63 -> gedempte hoge conga 62 (beide PSG in rs_drumset);
# open triangel 81 valt buiten rs_drumset en leest daar frlg_drumset-noot 52 = ook een PSG-blokgolf -> ride bell 53.
prepare(f'{SRC}/macarena.mid', f'{DST}/mus_grounded_vs_birch.mid',
        drop_tracks=(5, 13, 14), drum_map={44: 42, 63: 62, 81: 53})
print('klaar')

# Automatisch voorbereid (groepering per GBA-instrument), zie prepare_auto in prepare_midi.py
from prepare_midi import prepare_auto, write_voicegroup
write_voicegroup()
for src, dst in [
    ('dppt_champion.mid', 'mus_grounded_vs_dppt_champion.mid'),
    ('dppt_cyrus.mid',    'mus_grounded_vs_cyrus.mid'),
    ('bw_n.mid',          'mus_grounded_vs_n.mid'),
]:
    prepare_auto(f'{SRC}/{src}', f'{DST}/{dst}')
# Ghetsis: de koperpartij (kanaal 6) speelt de 'Ghetsis!'-koorakkoorden twee octaven te laag mee (noot 18-27) en de
# e-piano (kanaal 7) heeft noten 7/13: een trompet-/pianosample zo ver omlaag geeft lange 'puuup'-tonen (Jordi).
# v0.9.65: de 'puuup' vóór de koorstukken (88 s, 92,5 s) was drumnoot 49 = PSG in rs_drumset; nu echte samples.
# Koper terug op min. C2 (v0.9.60; Jordi: de vocalen waren goed).
prepare_auto(f'{SRC}/bw_ghetsis.mid', f'{DST}/mus_grounded_vs_ghetsis.mid', min_note={6: 36, 7: 36},
             drum_map=RS_PSG_FIX)
# v0.9.67 PSG-drums: Yoshi lage bongo 61 -> open lage conga 64; Broken Pier crash 49 -> 57 en side stick 37 -> zachte
# snare; Sunset Wilds side stick 37 -> zachte snare en pedaal-hihat 44 -> gesloten hihat 42.
for src, dst, dm in [
    ('yoshi_castle.mid',      'mus_grounded_vs_yoshi_castle.mid', {61: 64}),
    ('mksc_broken_pier.mid',  'mus_grounded_vs_broken_pier.mid', {**RS_PSG_FIX, 37: SIDE_STICK_SOFT}),
    ('mksc_sunset_wilds.mid', 'mus_grounded_vs_sunset_wilds.mid', {**RS_PSG_FIX, 37: SIDE_STICK_SOFT}),
]:
    prepare_auto(f'{SRC}/{src}', f'{DST}/{dst}', drum_map=dm)

# Dark Cave is een HGSS-rip met eigen (niet-GM) instrumentnummers: kanaal 2 (shaker, noten 101-111) weg,
# kanaal 7 en 8 zijn baslijnen, en alles boven toonhoogte 84 gaat per octaaf omlaag.
prepare_auto(f'{SRC}/hgss_dark_cave.mid', f'{DST}/mus_grounded_vs_dark_cave.mid',
             drop_channels=(2,), channel_category={7: 'fingered_bass', 8: 'synth_bass'}, max_note=84)

# Giratina: de hoornpartij (kanaal 14) en een paar strijkers zitten op toonhoogte 85-104, veel te hoog voor
# de GBA-samples (piep aan het begin). Alles boven 84 gaat per octaaf omlaag.
prepare_auto(f'{SRC}/pt_giratina.mid', f'{DST}/mus_grounded_vs_giratina.mid', max_note=84,
             # vergeleken met een GBA-soundfont-opname: bas te zwak, midden te sterk
             volume={'strings': 80, 'piano': 80, 'horn': 86, 'trumpet': 86, 'flute': 86, 'square2': 76},
             drum_map=RS_PSG_FIX)   # v0.9.67: bekkenroffels (crash 49, china 52, PSG) -> orkestcrash 57

# Zinnia (ORAS, Delta Episode): gevechtsmuziek van Zinnia voor de Sky Pillar
# Knapperen (Jordi): de 8-bit-mixer loopt over (-128 <-> 127) bij strijkersstapels + synthbas + kick (1,7-3,1 s,
# 10 s, 21 s). Strijkers/bas/orgel/drums zachter en -V072 in midi.cfg: 0 overlopen in recpcm, piek 118/127.
prepare_auto(f'{SRC}/oras_zinnia.mid', f'{DST}/mus_grounded_vs_zinnia.mid', max_note=84,
             volume={'strings': 80, 'synth_bass': 85, 'organ': 105, 'drums': 112},
             drum_map=RS_PSG_FIX)   # v0.9.67: crash 49 (PSG) -> orkestcrash 57

# Neo Team Plasma (Black 2/White 2), MIDI van Byabbington (onlinesequencer): gevechtsmuziek van de Neo Plasma-deelnemers
# Sinds v2 gemaakt door tools/grounded/neo_plasma_theme.py (echte instrumenten per bronspoor, eigen voicegroup).
# prepare_auto(f'{SRC}/b2w2_neo_plasma.mid', f'{DST}/mus_grounded_vs_neo_plasma.mid', max_note=84)
