#!/usr/bin/env python3
"""Project Grounded: gevechtsmuziek van Neo Team Plasma (Battle Stadium): "Battle! Neo Team Plasma"
(Pokémon Black 2/White 2). Noten: MIDI van Byabbington (onlinesequencer, sound/songs/grounded_src/b2w2_neo_plasma.mid).
Klank, timing en balans: gemeten aan het origineel (BW2-mp3 van Jordi). Structuur zoals in de game: intro maat 0-9,
loop maat 10-73 (de MIDI speelt die loop twee keer).

v12 (Jordi over v11: 'de noten heb je te pakken, alleen klinken de instrumenten alsof een computer met een kapotte
speaker speelt; haal ze er allemaal af, houd ritme/bpm/noten vast en koppel er logische Emerald-instrumenten aan'):
noten, ritme, tempo, structuur en drumpatroon exact v11 (de stemverdeler rekent met de v11-releases, V11_REL), alleen
programma's/volumes/ADSR nieuw, alles stock-samples uit de vanilla Emerald-voicegroups (zie VOICES), geen eigen
samples meer (de np_*-samples en neo_plasma_samples.py zijn weg), geen pitch bends: de opening-run (maat 2-4) speelt
weer als ladder van gewone noten op de trompet (< C3 synth bass) + PSG-octaaf. Klinkende hoogte gelijk aan v11:
organ2-sporen een octaaf hoger geschreven, de bas een octaaf lager (fingered bass klinkt op de geschreven noot).

v11 (Jordi via Gemini over v10; drums, tempo en de achtergrond-arpeggio's blijven; preview v10 vanaf 0 s, maat =
seconde / 1,364). Elk punt eerst gemeten:
1. 'Theremin / fluittoon met vibrato en pitch-bends op de lead, 0:08-0:18 en 0:45-0:55': de bends van de intro-glide
   gaan op beide sporen (lead + PSG-octaaf) terug naar het midden (BEND c_v+0 op tick 7936) en er zijn geen MOD/LFO-
   controllers. De zweving zat in de samples: sc88pro_square_wave (de lead vanaf maat 22) en np_lead_fat (maat 0-21,
   daaruit opgebouwd) zijn zelf gechorusde blokgolven: 7-10 dB tremolo op 1,7-5 Hz, spectraal zwaartepunt schommelt
   28%, en 90-93% van de energie op de grondtoon (= een fluittoon). Nu np_plead_hi/lo (neo_plasma_samples.pulse_lead):
   zuivere 25%-puls, 0 dB tremolo, felle aanslag, release 60, en elke leadnoot laat een uitklinktijd vóór de volgende
   los (detach: 16en = 60 ticks + 37 uitklink). De glissando (maat 2-4) blijft. Hold-tonen ook op np_plead_hi.
2. 'Valse noten 0:20-0:35, F-E-D-C#-D, D-mineur': F-E-D-C#-D komt in de bron-MIDI, in v11 en in de stem 'other' +
   'vocals' van het origineel (sterkste toon >= C4/C5 per 16e, eerste 100 s) nergens voor; het origineel is C-chromatisch
   (chroma 0-60 s: C, D, C#, E ...), alleen maat 18-21 is D-mineur. De lead-toonklassen in maat 14-25 kloppen met het
   origineel (chroma: 1-4 van 16 zwak per maat, alleen hoge C6/Bb5-tonen); de secunde-wrijving tussen bas en de rest is
   met de nieuwe bas niet gegroeid (maat 14-26: 13,7 -> 13,0 tellen) en zit ook in het origineel (maat 20: A-octaven
   tegen de chromatische bas Ab, beide sterk in de opname). Geen noten veranderd.
3. 'Bas dof, houtachtig tikkend': de 16en klonken 27 ticks (24 ms) op een holle sample = een tik. Nu np_bass_buzz
   (zaagtand + puls + resonantie ±1 kHz, zoals de basstem van het origineel: < 150 Hz 49%, 150-600 30%, 600-2k 12%),
   volle sustain, release 50, noten 85% van de bronlengte (16en 64 ticks; kanaalbezetting gelijk aan v10), CC7 92:
   +3,2 dB t.o.v. v10 (gba_sim, maat 13-42). Een octaaf lager kan niet: de bas klinkt al Eb1-Ab3 (C2-C3 in de riff).
4. rules_check: ook geen bends buiten de intro-run, terug naar 0, geen MOD/LFO, lead zonder zweving en release <= 80.

v10 (Jordi via Gemini over v9; tempo, drumgroove en de achtergrond-arpeggio's blijven; preview v9 begon op 0 s,
dus 0:22 = maat 16, 0:45 = maat 33, 1:08 = maat 50). Feiten gecontroleerd tegen de mp3 (Spleeter-stems, CQT):
1. 'Foute melodienoten 0:22-0:35 en 1:08-1:21': in maat 16-26 klopt elke toonklasse van de lead met het origineel
   (geen consistente fout; de 'F-E-D-C#-D'-lijn komt daar niet voor, de D-mineur-arpeggio's in maat 18-21 wel en die
   speelt v9 al). Wél gevonden: octaaffouten van de transcriptie in het orgeldeel (maat 50-62): orgelakkoorden,
   sawtooth en 8-bit-sinus een octaaf te hoog (OCT_*; fix_octaves). Alle melodische noten <= C6 (cap_top).
2. Intro: de opening-run (maat 2-4) wordt een echte glissando: drie aangehouden noten op een dikke synth brass
   (np_gbrass_lo/hi, velocity 127) met een pitch bend (BENDR 12) die de ladder volgt (gliss()); het octaaf
   eronder (PSG) glijdt mee.
3. Brug: de bas klonk hol (sc88pro_synth_bass heeft maar 17% energie op de grondtoon): np_bass_fat (grondtoon
   erbij), bas en sub CC7 127 (+6% / +32%), vul-stoten in de brug (x . x x . x . x waar de bas zwijgt), de PSG-
   bas-stoten van v9 weg; in de halftime-break 34-36 spelen de 16e-hats door (zoals in het origineel). -V064.
4. Controles (rules_check): geen noot > C6, geen akoestische/strijker/pad-samples, geen trage aanzet, BENDR vóór
   elke bend.

v9 (Jordi over v8: 'het ritme zit er erg goed in, maar de iconische eerste seconden kloppen niet qua instrumentatie
en impact'; ritmische basis van v8 blijft):
1. Opening-run en loopbegin: maat 0-21 (de stijgende chromatische run van de intro, de 64e-loopjes, en het
   arpeggio-thema vanaf het loopbegin) op een vette GBA-lead (np_lead_fat: sc88pro_square_wave x2 ontstemd +
   sc88pro_trumpet = synth brass, harde aanzet; < C4 np_lead_fat_lo zonder trompet). Het arpeggio eronder ook (korte
   release i.p.v. de tokkelende pluk). Lead-CC7 in de run (maat 2-4) en het loopbegin (maat 10-13) 92 -> 115 (+25%).
2. Valse noten in de B-sectie (Jordi 0:22-0:35 = maat 25,7-35,3 van het nummer), gemeten tegen zijn mp3
   (fix_b_section, stabs, held_tones): bron-transcriptiefouten G4 -> A4 (maat 32-33) en G3 weg uit de E-akkoorden
   (maat 22-29); de off-beat-stoten van v7 met een oud akkoord (49 van 79) kregen een tweeklank uit de tonen die dan
   klinken (28) of vervallen (21); aangehouden sawtooth-akkoordtonen (o.a. Bb5/Bb4 in maat 35) die de mono lead
   afkapte, klinken weer (spoor 'hold', 62 tonen).
3. Brug (Jordi 0:48 = maat 44,8): stijgende 16e-arpeggio's (crescendo) op de vette lead + PSG-vierkant 2 en
   staccato bas-stoten in achtsten op de PSG-sub, maat 44 tel 2 t/m 49.

v8 (Jordi over v7: 'ritme en noot-timing perfect, maar de sporen hangen niet aan de juiste instrumenten uit het
GBA-soundfont; laat noten en timing EXACT staan en verander alleen de instrument-toewijzing'). Diff per spoor t.o.v.
v7: aanslagen, toonhoogtes en velocity's identiek; alleen programma's/voices, releases, CC7 en de nootlengtes van
de lead (legato) wijzigen.
1. Lead: de GBA-blokgolf sc88pro_square_wave (DirectSound) met volle sustain (v7: decay naar 200) en release 140, legato:
   elke noot houdt aan tot de volgende aanslag (bij een rust van > 1 tel blijft de bronlengte). De octaaf eronder
   (PSG-vierkant 1) ook legato en met een hoge sustain i.p.v. de korte tik.
2. Bas: sc88pro_synth_bass (strak, kort, veel laag), als np_synth_bass een octaaf hoger gelabeld zodat hij klinkt
   waar de pulse-bas klonk (een octaaf onder de MIDI-noten). Sub op de PSG-golf blijft.
3. Begeleiding/arpeggio's: spoor A (en de steel-drums-partij) = sc88pro_square_wave als zachte pluk (korte decay),
   spoor B blijft het zachte 50%-PSG-vierkant.
4. Akkoorden: de gitaarakkoorden = 'Synth Brass' van het GBA-soundfont (trompet-keysplit sc88pro_trumpet_60/72/84,
   zoals GM 62/63 in grounded_gm), de off-beat-stoten = percussief orgel (sc88pro_organ2, snelle decay).
   Het orgelspoor (np_organ_sharp) blijft ongewijzigd.
5. Drums: eigen kit in de standaard-GM/GBA-indeling: 36 kick (drum_and_percussion_kick, Emerald-kit), 38 snare
   (sc88pro_rnd_snare, fills), 39 handclap (909), 40 felle snare (unknown_synth_snare: backbeat 2/4 + ghosts),
   42 dichte hihat, 46 open hihat, 49 crash, 55 splash. Alles DirectSound, geen PSG-drumnoten. Alleen de
   nootnummers in het drumspoor veranderen (zelfde tijden, lengtes en velocity's).

v7 (Jordi over v6: 'te kaal, dun en los zand'; GBA-productietechnieken voor een vol, gelaagd geluid). Tempo blijft
gemeten 175,96 bpm (Jordi bevestigd: 176; de 150-155 uit de opdracht was een fout), noten/toonsoort uit de bron,
het orgel (sample, ligging, volume, partij) ongewijzigd.
1. Lead op twee sporen: de lead op de bronhoogte (DS-pulse-lead np_lead_pulse, vaste lowpass) + dezelfde melodie een
   octaaf lager op PSG-blokgolf 1 (50%, punchy envelope, velocity 96 = 75%). Kost geen extra DS-kanaal.
2. Sub-bas: de staccato-baslijn op hetzelfde ritme ook op het PSG-golfkanaal (sinus), op de klinkende toonhoogte
   van de bas (de pulse-bas klinkt al een octaaf onder de MIDI; nog een octaaf lager zou < 20 Hz zijn; PSG kan niet
   onder C2, daar een octaaf hoger). De oude
   8-bit-sinuspartij gaat daarom naar een DS-sinus (np_sine). Kick four-on-the-floor in alle gevechtsmaten.
3. Arpeggio's/steel drums gesplitst: spoor A = DS steel drums (pan 35), spoor B = dezelfde noten 16 ticks (±1 frame)
   later op PSG-blokgolf 2 (pan 85). Let op: de game staat standaard op MONO (optiemenu Sound); dan klinkt B als
   een licht verlate verdubbeling (chorus), in STEREO als links/rechts.
4. Off-beat-akkoordstoten (np_stab, 2 stemmen) op elke vrije 'en' in de gevechtsmaten zonder orgelpartij; akkoord =
   het laatste gitaarakkoord van de bron (of de arpeggiotonen van die tel), nooit een eigen harmonie.
5. Drums: kick op 1-2-3-4, scherpe snare (unknown_synth_snare) op 2 en 4, ghost-dubbelslag (16en) aan het eind van
   elke 2e en 4e maat, dichte hihat op alle 16en met accent op elke kwart; clap op de off-beats blijft (bron).

v6 (Jordi over v5: 'te ver doorgeslagen naar een kale, schelle 8-bit sound; hoge tonen snijden in de oren, mist
dynamiek en gelaagdheid'): tempo, noten/timing en het orgel (sample, volume, partij) blijven exact v5.
- Lead een octaaf lager (per maat: alleen waar de hele maat dan nog boven A2 blijft; de lage arpeggio-maten blijven
  staan) op een warme DirectSound-pulse-lead (np_lead_warm: puls 25% + 50% ontstemd, lowpass) i.p.v. de PSG-blokgolf.
  De oude octaafverdubbeling (PSG, lead2) valt daarmee samen: weg.
- Akkoordenspoor: vollere synth brass (np_brass_full: twee ontstemde zaagtanden met filterstoot) en luider.
- Drums: duidelijke GBA-kit, alles DirectSound: kick = drum_and_percussion_kick 7 halve tonen hoger (body ±65 Hz,
  aanzet ±200 Hz, zoals de kick van het origineel), off-beat = TR-909-handclap (fel, 1-8 kHz), snare in fills =
  sc88pro_rnd_snare, dichte hihat (unknown_close_hihat) op de 16en i.p.v. PSG-ruis.
- Arpeggio's (steel drums, binnenstemmen, PSG-sinus/-driehoek) ±6 dB zachter: kruiding, nooit boven de melodie.

v5 (Jordi over v4: 'nog steeds niet echt goed'; melodie strak, tempo exact, scherpe pulse-lead, punchy synth brass,
diepe staccato-bas, zachte steel-drum-arpeggio's, standaard GBA-drumkit, melodie op de voorgrond):
- Tempo: het origineel loopt op 175,96 bpm (kickraster van de mp3 over 136 maten, drift 0,3 ms/maat). De GBA kan
  alleen even tempi (TEMPO = bpm/2) en speelt die 0,45% te traag (59,73 i.p.v. 60 frames/s): 176 klinkt als 175,2.
  Daarom per tel 176 of 178 (Bresenham, 5 op 13 tellen 178) = gemiddeld 175,96, net als het origineel.
- Timing van de bron: het sawtooth-spoor (melodie/arpeggio's) staat vanaf maat 5 17 ticks te vroeg (alle noten op
  x,82 van een 16e; gemeten met toonhoogte-specifieke aanslagen in de mp3: in het origineel vallen ze op het raster),
  het orgel speelt elk akkoord als een 'strum' van 4 ticks per noot, 24 ticks vóór de tel. Beide op het raster gezet.
- Instrumenten (per bronspoor):
    8-Bit Sawtooth, bovenstem   -> lead: PSG-blokgolf 1 (25%, snelle aanzet, korte decay), MIDI-lengtes (niet legato)
    8-Bit Sawtooth, octaaf eronder -> PSG-blokgolf 2 (12,5%, zachter): body onder de lead
    8-Bit Sawtooth, binnenstemmen -> steel drums (arpeggio's, zacht op de achtergrond)
    Electric Guitar (akkoorden) -> synth brass-stoten (np_brass_stab: felle aanzet, geen swell), MIDI-lengtes
    Electric Guitar (< C3)      -> zelfde stoot op een eigen C2-sample (np_brass_stab_lo), één stem
                                   (v6: per octaaf omhoog tot >= C3)
    Slap Bass                   -> diepe pulse-bas een octaaf lager (np_pulse_bass), staccato
    Church Organ                -> scherp drawbar-orgel, zelfde register, korte noten en korte release
    Steel Drums                 -> steel drums (zacht)
    8-Bit Sine / Triangle       -> PSG-golf (zacht)
    drums                       -> standaard GBA-kit (rs_drumset-samples): kick op de tel (sc88pro_rnd_kick),
                                   snare op de achtste off-beats (in het origineel klinkt daar
                                   een felle elektronische snare/clap, 1-8 kHz) en vol in fills, crashes; snelle
                                   hihats op 16en op het PSG-ruiskanaal.

Gebruik: python3 tools/grounded/neo_plasma_theme.py (v12: alleen stock-samples; de v11-samplegenerator staat in de geschiedenis)"""
import collections
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, thin, detach, allocate, releases, release_ticks, Song

SRC = 'sound/songs/grounded_src/b2w2_neo_plasma.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_neo_plasma.mid'
VG = 'sound/voicegroups/grounded_neo_plasma.inc'
DRUMSET = 'sound/voicegroups/drumsets/neo_plasma.inc'
KEYSPLIT = 'sound/voicegroups/keysplits/np_trumpet.inc'
LEAD_KEYSPLIT = 'sound/voicegroups/keysplits/np_lead.inc'     # v12: trompet-lead (eigen bestand: musiclib/lint lezen de release)
TPB, BAR, BEAT, S16 = 384, 1536, 384, 96
BPM = 176
LOOP0, END = 10 * BAR, 74 * BAR
SAW_SHIFT = 17              # sawtooth vanaf maat 5: 17 ticks te vroeg in de bron

# programma's in voicegroup_grounded_neo_plasma
BASS, BRASS, BRASS_LO, ORGAN, LEAD, DRUMS = 38, 62, 63, 17, 80, 127
BODY, SUB, ARPB, DSINE, STAB, PLUCK = 81, 82, 84, 85, 86, 87
FAT_LO, FAT_HI, FARP_LO, FARP_HI, HOLD = 88, 89, 90, 91, 92      # v9
LEAD_REL, BASS_REL = 60, 50                                         # v11: korte releases (afgekapt per noot)
# v12: de stemverdeler (welke noot blijft, hoe lang) rekent met de releases van v11, zodat noten, ritme en lengtes
# exact v11 blijven; de nieuwe stemmen hebben dezelfde (of een kortere) release.
V11_REL = {17: 90, 38: 50, 62: 110, 63: 110, 80: 60, 81: None, 82: None, 84: None, 85: 140, 86: 100, 87: 110,
           88: 60, 89: 60, 90: 40, 91: 40, 92: 100, 127: None}
# v12 (Jordi: 'de noten heb je te pakken, maar de instrumenten klinken alsof een computer met een kapotte speaker
# speelt; gewone Emerald-instrumenten'): alleen stock-samples uit de Emerald-voicegroups, eenvoudige ADSR, geen eigen
# samples, geen bends. Basis = voicegroup vs_gym_leader.
#   lead (>= C3)    trompet-keysplit (sc88pro_trumpet_60/72/84; trumpet_keysplit van vs_gym_leader/vs_elite_four)
#   lead (< C3)     sc88pro_synth_bass (vs_elite_four 38): koper niet onder C3
#   lead-octaaf     PSG-blokgolf 1 (vs_gym_leader 82)
#   akkoordstoten   trompet-keysplit (korte release)
#   orgel, arpeggio's, sinus, hold, orgelstoot   sc88pro_organ2 (vs_frontier_brain 17): zuiver, geen zweving; de
#                   sample klinkt een octaaf lager dan geschreven, dus die sporen staan een octaaf hoger (klinkend = v11)
#   bas             sc88pro_fingered_bass (vs_gym_leader 33), klinkt op de geschreven hoogte: een octaaf lager
#                   geschreven dan in v11 (np_bass_buzz klonk een octaaf onder de geschreven noot); < E1 een octaaf op
#   sub / arp B     PSG-golf / PSG-blokgolf 2 (vs_gym_leader 3)
#   drums           rs_drumset-regels (standaard Emerald-kit), crash = de orkestcrash van rs_drumset 57
ORGAN2 = 'DirectSoundWaveData_sc88pro_organ2'
VOICES = {
    LEAD:     'voice_keysplit voicegroup_np_lead_keysplit, keysplit_trumpet',
    FAT_HI:   'voice_keysplit voicegroup_np_lead_keysplit, keysplit_trumpet',
    FAT_LO:   'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 252, 0, %d' % LEAD_REL,
    BODY:     'voice_square_1 60, 0, 0, 2, 0, 1, 7, 1',
    ARPB:     'voice_square_2 60, 0, 2, 0, 2, 6, 1',
    SUB:      'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 1',
    BRASS:    'voice_keysplit voicegroup_np_trumpet_keysplit, keysplit_trumpet',
    BRASS_LO: 'voice_keysplit voicegroup_np_trumpet_keysplit, keysplit_trumpet',
    BASS:     'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, %d' % BASS_REL,
    ORGAN:    'voice_directsound 60, 0, %s, 255, 0, 255, 90' % ORGAN2,
    STAB:     'voice_directsound 60, 0, %s, 255, 215, 40, 100' % ORGAN2,
    DSINE:    'voice_directsound 60, 0, %s, 255, 220, 200, 140' % ORGAN2,
    PLUCK:    'voice_directsound 60, 0, %s, 255, 205, 0, 110' % ORGAN2,
    FARP_LO:  'voice_directsound 60, 0, %s, 255, 0, 255, 40' % ORGAN2,
    FARP_HI:  'voice_directsound 60, 0, %s, 255, 0, 255, 40' % ORGAN2,
    HOLD:     'voice_directsound 60, 0, %s, 255, 0, 255, 100' % ORGAN2,
    DRUMS:    'voice_keysplit_all voicegroup_neo_plasma_drumset',
}
# organ2 klinkt een octaaf onder de geschreven noot: deze sporen schrijven een octaaf hoger (klinkend = v11; de
# orgelstoot stond in v11 al op organ2 en blijft zoals hij was)
OCT_UP = (ORGAN, DSINE, PLUCK, FARP_LO, FARP_HI, HOLD)
SOUND_OFS = {p: -12 for p in OCT_UP + (STAB,)}
# drumkit (noot -> regel); standaard GBA-samples in de GM-indeling (v8; v7 had 36-43 op een rij)
KICK, SNARE, SNARE_OFF, SNARE24, CHAT, OHAT, CRASH, SPLASH = 36, 38, 39, 40, 42, 46, 49, 55
RS = [l.strip() for l in open('sound/voicegroups/drumsets/rs.inc') if l.startswith('\tvoice')]   # noot 36 = RS[0]
KITV = {k: RS[k - 36] for k in (KICK, SNARE, SNARE_OFF, SNARE24, CHAT, OHAT, SPLASH)}
KITV[CRASH] = RS[57 - 36]           # rs_drumset 49 is PSG: de orkestcrash (57) op 49
# release zoals de v11-kit (kick/hats 0: geen staart die een kanaal bezet; de stemverdeling rekent daarmee)
KIT_REL = {KICK: 0, SNARE: 220, SNARE_OFF: 180, SNARE24: 200, CHAT: 0, OHAT: 0, CRASH: 165, SPLASH: 140}
KITV = {k: v.rsplit(',', 1)[0] + ', %d' % KIT_REL[k] for k, v in KITV.items()}
# ongebruikte noten in de kit: een stille DirectSound-regel (geen PSG: een verdwaalde noot mag niet piepen)
KIT = [KITV.get(k, 'voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0')
       for k in range(36, max(KITV) + 1)]
# bron-drumnoot -> (kitnoot, lengte in ticks, velocity 0-127); 42/44 = dichte hihat
DRUM_MAP = {36: (KICK, 190, 96), 37: (SNARE_OFF, 160, 127), 38: (SNARE, 192, 120), 46: (OHAT, 192, 70),
            49: (CRASH, 384, 100), 57: (CRASH, 384, 100), 55: (SPLASH, 288, 90)}
HAT_LEN, HAT_ACC, HAT_A, HAT_B = 80, 127, 92, 74   # dichte hihat: 77 ms = 82 ticks; accent op de kwart
BREAK = {34, 35, 36, 64, 65}                # breaks (halftime / zonder bas): geen four-on-the-floor/hihats/stoten
# intro en breaks: geen 16e-hihats. v10: in de halftime-break 34-36 spelen de 16e-hats in het origineel door
# (drumstem 5-10 kHz: op elke 16e een aanslag); alleen 64-65 zijn echt kaal
NO_HATS = set(range(0, 10)) | {64, 65}
# v10: octaaffouten in de bron (octcheck tegen de Spleeter-stem 'other': op de noot zelf vs. een octaaf lager,
# gemiddeld per maat, >= 6 dB verschil): het orgel speelt de 16e-akkoorden in maat 50-62 (niet 53) op C4-Eb4-G4 i.p.v. C5
# (10-12 dB), de sawtooth-tonen in maat 52/54/55/61 (9-15 dB) en de 8-bit-sinus in 50/52/54/56/57 (9-16 dB) ook.
OCT_ORGAN = (set(range(50, 63)) - {53})
OCT_SAW = {52, 54, 55, 61}
OCT_SINE = {50, 52, 54, 56, 57}
TOP = 84                                    # v10 (Jordi: 'geen piepjes boven C6'): geen melodische noot > C6
GLISS = (2 * BAR + S16, 5 * BAR)            # de opening-run (E2 -> C6); v12: gewoon noten, geen glissando
BENDR = 12                                  # v12: alleen nog voor de bezettingsberekening (gliss())
ORGAN_BARS = set(range(49, 62)) | set(range(65, 71))    # daar speelt het orgel al 16e-stoten: geen extra stoten
SNARE_LEN, GHOST_VEL, BACK_VEL = 192, 58, 118
UNISONO_BARS = set(range(46, 50))           # unisono-riff (bas + saw): geen akkoordstoten
BASS_LEN = 0.85                             # v11: basnoten 85% van de bronlengte (v10 0,6), dan detach
ARPB_DELAY = 16                             # spoor B van de arpeggio's: 1/24 tel later (±1 frame)

# spoorvolumes (CC7), afgesteld met solo-RMS en balance_orig.py tegen de mp3
# v8: nieuwe samples op dezelfde luidheid als v7 gezet (RMS van de eerste 80 ms per sample), lead en lead-octaaf
# iets terug omdat ze nu aanhouden
# v11: bas 127 -> 92: de nieuwe bas (langere noten, luidere sample) is op 127 2,0x zo luid (RMS, gba_sim maat 13-42);
# op 92 1,45x = +3,2 dB = 'ongeveer 25% luider' (luidheid verdubbelt per ±10 dB)
# v12: de trompet-lead is per sample 8-10 dB zachter dan de pulse-lead van v11 en kan niet boven CC7 127: de lead op
# 127 en de rest x0,65 t.o.v. v11, gecorrigeerd voor het luidheidsverschil van de nieuwe sample (RMS eerste 80 ms;
# organ2 -2,8 dB t.o.v. np_organ_sharp, +4,2 t.o.v. np_sine; fingered bass +1,5 t.o.v. np_bass_buzz; PSG-blokgolf
# sustain 7 i.p.v. 12), -V060 -> -V095
VOL = dict(lead=127, body=74, brass=63, brass_lo=53, organ=29, bass=71, sub=83, steel=23, arp=24, arpb=26,
           dsine=42, stab=29, drums=62)
LEGATO_GAP = BEAT           # lead: een noot houdt aan tot de volgende aanslag als de rust ertussen <= 1 tel is
# v9: vette lead + arpeggio in de intro en het openingsdeel van de loop (maat 0-21: de opening-run en het
# arpeggio-thema), daarna de v8-blokgolf. Leadvolume (CC7) per stuk: de opening-run (maat 2-4) en het loopbegin
# (maat 10-13) +25% (92 -> 115), de rest van maat 0-21 104.
FAT_END = 22 * BAR
# v11: de pulse-lead is in maat 0-21 1,7 dB zachter dan np_lead_fat: daar x1,2 (104 -> 124, 115 -> 127); de glissando
# (eigen sample) blijft 115. Hold: de nieuwe sample is 2,5 dB luider: 46 -> 35
LEAD_VOL = [(0, 127), (LOOP0, 84)]            # v12: 127; v12e: vanaf het loopbegin terug (zie LOOP_VOL)
# v12e (Jordi neuriede de melodie die vanaf 0:14 wegvalt; pyin op de Spleeter-stem 'other' van het origineel: 14,4 s
# lange C, dan G-D#-G#-G, vanaf 25,4 s hetzelfde op D): dat is de elektrische gitaar van de bron (lange octaafnoten +
# achtsten) = de partijen 'brass' en 'brass_lo', die op CC7 63/53 onder de lead (127, sawtooth-16en) verdwenen.
# Vanaf het loopbegin: melodie voor, de 16e-lead terug; de intro blijft zoals hij was.
LOOP_VOL = dict(brass=120, brass_lo=96)
VOL_HOLD = 36
# v9: brug (Jordi '0:48' = maat 44,8 in het nummer): niet stilvallen. Staccato bas-stoten in achtsten op de PSG-sub
# en stijgende arpeggio's (16en, crescendo) op de vette lead (DirectSound) + PSG-vierkant 2 (arp B), van maat 44
# tel 2 tot maat 50.
BRIDGE = (44 * BAR + BEAT, 50 * BAR)
VOL_ARPB_BRIDGE = 47
VOL_BARP = 61               # v9: het brug-arpeggio op DirectSound (vette lead, korte release)


def voicegroup():
    """v12: op basis van de vanilla voicegroup vs_gym_leader; alleen de programma's van VOICES wijken af."""
    base = [l.strip() for l in open('sound/voicegroups/vs_gym_leader.inc') if l.startswith('\tvoice')]
    filler = 'voice_square_1 60, 0, 0, 2, 0, 0, 15, 0'          # zoals de lege plekken in vs_gym_leader
    out = ['@ Project Grounded: Battle! Neo Team Plasma (BW2) v12, op basis van vs_gym_leader (alleen stock-samples).',
           '@ Gegenereerd door tools/grounded/neo_plasma_theme.py. 17 orgel, 38 bas, 62/63 akkoordstoten (trompet),',
           '@ 80/89 lead (trompet), 88 lead < C3 (synth bass), 81 lead-octaaf (PSG), 82 sub (PSG-golf), 84 arp B (PSG),',
           '@ 85 sinus, 86 orgelstoot, 87/90/91 arpeggio, 92 hold (organ2), 127 drums.',
           'voice_group grounded_neo_plasma']
    for k in range(128):
        out.append('\t%s  @ %d' % (VOICES.get(k, base[k] if k < len(base) else filler), k))
    open(VG, 'w').write('\n'.join(out) + '\n')
    ks = lambda name, rel: 'voice_group %s\n' % name + ''.join(
        '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_trumpet_%d, 255, 0, 193, %d\n' % (k, rel)
        for k in (60, 72, 84))
    open(KEYSPLIT, 'w').write(
        '@ Project Grounded: trompetten voor Battle! Neo Team Plasma (neo_plasma_theme.py) = de GBA-trompetten\n'
        '@ (sc88pro_trumpet_60/72/84, tabel keysplit_trumpet) zoals trumpet.inc, met een kortere release:\n'
        '@ akkoordstoten (release 110). De lead staat in np_lead.inc.\n' + ks('np_trumpet_keysplit', 110))
    open(LEAD_KEYSPLIT, 'w').write(
        '@ Project Grounded: trompet-lead voor Battle! Neo Team Plasma v12 (neo_plasma_theme.py): de GBA-trompetten\n'
        '@ (sc88pro_trumpet_60/72/84, tabel keysplit_trumpet) met release %d (afgekapt per noot).\n' % LEAD_REL
        + ks('np_lead_keysplit', LEAD_REL))
    open(DRUMSET, 'w').write(
        '@ Project Grounded: drumkit voor Battle! Neo Team Plasma v12 (neo_plasma_theme.py): de regels van rs_drumset\n'
        '@ (standaard Emerald-kit): 36 kick, 38 snare, 39 clap, 40 orkestsnare, 42 dichte hihat, 46 open hihat,\n'
        '@ 49 crash (rs_drumset 57, want 49 is daar PSG), 55 crash. Alles DirectSound.\n'
        'voice_group neo_plasma_drumset, 36\n' + ''.join('\t%s\n' % k for k in KIT))


def groups(ev):
    g = {}
    for e in ev:
        g.setdefault(e[0], []).append(list(e))
    return [sorted(g[s], key=lambda e: e[2]) for s in sorted(g)]


def fixed_source(m):
    """Bron met de timingcorrecties (zie docstring): sawtooth +17 vanaf maat 5, orgelakkoorden op het raster."""
    T = {i: [[a, b, n, 127] for a, b, n, v in notes_of(m.tracks[i])] for i in range(10)}
    T[4] = [[s + SAW_SHIFT, e + SAW_SHIFT, n, v] if s >= 5 * BAR else [s, e, n, v] for s, e, n, v in T[4]]
    org = []
    for s, e, n, v in T[6]:
        q = ((s - 72) // S16) * S16 + S16 if s % S16 >= 70 else s
        org.append([q, q + (e - s), n, v])
    T[6] = dedupe(org)
    fix_b_section(T)
    fix_octaves(T)
    return T


def fix_octaves(T):
    """v10: octaaffouten van de transcriptie (zie OCT_*): orgelakkoorden (>= 2 tonen tegelijk; de chromatische
    64e-loopjes in maat 49/53/56 kloppen wel) in OCT_ORGAN, sawtooth in OCT_SAW en 8-bit-sinus in OCT_SINE een octaaf
    omlaag."""
    bar = lambda s_: s_ // BAR
    on = {}
    for e in T[6]:
        on[e[0]] = on.get(e[0], 0) + 1
    n = 0
    for i, bars, pred in ((6, OCT_ORGAN, lambda e: on[e[0]] >= 2), (4, OCT_SAW, lambda e: True),
                          (7, OCT_SINE, lambda e: True), (9, OCT_SINE, lambda e: True)):
        for e in T[i]:
            if bar(e[0]) in bars and pred(e):
                e[2] -= 12
                n += 1
        T[i] = dedupe(T[i])
    print('  octaaffix (v10): %d brontonen een octaaf omlaag' % n)


def fix_b_section(T):
    """v9 (Jordi: 'valse noten in de B-sectie, 0:22-0:35' = maat 25,7-35,3 van het nummer). Noot voor noot gemeten
    tegen Jordi's mp3 (harmonische salience op de Spleeter-stem 'other'+'vocals', zie MUZIEK.md):
    - maat 32-33: het gitaarakkoord is D-A-D zoals in maat 30-31 (A4 overal sterk, G4 afwezig); de bron had G4: die
      G4 schuurde twee maten lang tegen de melodie (F#5/A5/C#5) -> A4.
    - maat 22-29: het gitaarakkoord is een kwintakkoord E-B-E (G3 komt in de opname niet voor, F/A wel: de
      tegenlijn G-Bb-A van de lage gitaar); de G3 van de bron gaf met die tegenlijn (G3/Bb3/A3, v6 een octaaf
      omhoog) secundes -> weg."""
    gtr = T[5]
    on = {}
    for e in gtr:
        on.setdefault(e[0], set()).add(e[2])
    out = []
    for e in gtr:
        s_, n = e[0], e[2]
        if 32 * BAR <= s_ < 34 * BAR and n == 67:
            e = [e[0], e[1], 69, e[3]]
        elif 22 * BAR <= s_ < 30 * BAR and n == 55 and {52, 59, 64} <= on[s_]:
            continue
        out.append(e)
    T[5] = out


def quantize_runs(ev, grid=16):
    """mid2agb rekent in 1/24 tel (16 ticks): snelle loopjes (32e/64e) op dat raster zetten, één noot per stap."""
    out, used = [], set()
    for s, e, n, v in sorted(ev):
        q = int(round(s / grid)) * grid
        if q in used:
            continue
        used.add(q)
        out.append([q, max(q + grid, e), n, v])
    return out


def mono(ev):
    """Eén stem: elke noot eindigt uiterlijk bij de volgende aanslag."""
    ev = sorted(ev)
    for a, b in zip(ev, ev[1:]):
        a[1] = min(a[1], b[0])
    return [e for e in ev if e[1] > e[0]]


def legato(ev, gap=LEGATO_GAP):
    """v8: elke noot houdt aan tot de volgende aanslag (aanslagmomenten blijven gelijk), behalve vóór een rust > gap."""
    ev = [list(e) for e in sorted(ev)]
    for a, b in zip(ev, ev[1:]):
        if b[0] - a[1] <= gap:
            a[1] = b[0]
    return ev


def trim_legato(res, order, tails):
    """v8: lead legato (tot de volgende aanslag), maar nooit zo lang dat er ergens meer dan 10 DS-noten tegelijk
    klinken, uitklinktijden (v8-releases) meegerekend: anders stopt de leadnoot eerder (nooit korter dan in v7, dat
    paste al). tails = uitklinktijd per partij in ticks."""
    rest = [(s_, e_ + tails[k]) for k in order if k != 'lead' for s_, e_, n, v in res[k]]
    tl = tails['lead']
    v7, leg = sorted(res['lead']), legato(res['lead'])
    out = []
    for i, ((s_, e7, n, v), (_, eleg, _, _)) in enumerate(zip(v7, leg)):
        # de andere leadnoten tellen ook mee: de vorige met hun nieuwe lengte, de volgende (nog) met die van v7
        others = rest + [(a, b + tl) for a, b, _, _ in out] + [(a, b + tl) for a, b, _, _ in v7[i + 1:]]
        starts = sorted({a for a, b in others})
        end = e7
        # de volgende leadnoot telt mee (zijn eigen kanaal); kandidaat-eindes: het legato-einde of vlak vóór een
        # aanslag die anders geen kanaal heeft
        cands = sorted({eleg} | {t - tl for t in starts if e7 + tl <= t < eleg + tl and t - tl > e7}, reverse=True)
        for E in cands:
            pts = [t for t in starts if s_ <= t < E + tl]
            if all(sum(1 for a, b in others if a <= t < b) < 10 for t in pts):
                end = E
                break
        out.append([s_, max(e7, end), n, v])
    full = sum(b - a for a, b, _, _ in leg) - sum(b - a for a, b, _, _ in v7)
    got = sum(b - a for a, b, _, _ in out) - sum(b - a for a, b, _, _ in v7)
    print('  lead legato: %d van %d noten langer dan in v7; %.0f%% van de volle legato-verlenging (de rest ingekort waar '
          'anders > 10 kanalen klinken)' % (sum(o[1] > e[1] for o, e in zip(out, v7)), len(v7), 100 * got / max(1, full)))
    return out


def ds_check(res, progs, order):
    """v8: DirectSound-bezetting met de echte releases van v8 (lead legato): hoeveel aanslagen vinden geen vrij
    kanaal (max. 10)? Die noten kapen in de game een kanaal (kanaalroof) of vallen weg."""
    real = releases('grounded_neo_plasma')
    iv = []
    for k in order:
        t = 0 if k == 'drums' else release_ticks(real[progs[k]], TPB, BPM)
        iv += [(s_, e_ + t, k) for s_, e_, n, v in res[k]]
    hold = [(s_, e_) for k in order for s_, e_, n, v in res[k]]
    over, hard = {}, 0
    for s_, e_, k in sorted(iv):
        if sum(1 for a, b, _ in iv if a <= s_ < b) > 10:
            over[k] = over.get(k, 0) + 1
        if sum(1 for a, b in hold if a <= s_ < b) > 10:
            hard += 1
    tot = sum(len(res[k]) for k in order)
    print('  bezetting (v8-releases): %d van %d aanslagen met > 10 aangehouden noten (kanaalroof); %d keer wordt alleen '
          'een uitklinkende staart afgekapt (m4a pakt eerst een kanaal in release) %s' % (hard, tot, sum(over.values()), over))


def prog_events(notes, prog_of):
    """v9: programmawissels per noot (alleen bij een wissel), en op het loopbegin opnieuw (de sprong terug)."""
    out, cur, looped = [], None, False
    for s_, e_, n, v in sorted(notes):
        p = prog_of(n, s_)
        if p != cur or (s_ >= LOOP0 and not looped):
            out.append((s_, 'prog', p))
            cur = p
        if s_ >= LOOP0:
            looped = True
    return out


def held_tones(saw, res, order, progs, real):
    """v9: sawtooth-noten >= C3 van >= 3 16en die in de uitvoer (lead/arpeggio's/steel) korter dan 60% op dezelfde
    toonhoogte klinken (de mono lead en het uitgedunde arpeggio kappen aangehouden akkoordtonen af: in maat 34-44 en
    9 klonk zo het halve akkoord niet, bv. de Bb5/Bb4 in maat 35). Alleen waar een DS-kanaal vrij is."""
    out_n = [(a, b, n) for k in ('lead', 'farp', 'arp', 'steel') for a, b, n, v in res[k]]
    cand = []
    for s_, e_, n, v in sorted(saw):
        if n < 48 or e_ - s_ < 3 * S16 or s_ >= END:
            continue
        e_ = min(e_, END)
        cov = sum(max(0, min(e_, b) - max(s_, a)) for a, b, m in out_n if m == n)
        if cov < 0.6 * (e_ - s_):
            cand.append([s_, e_, n - 12 * max(0, -(-(n - TOP) // 12)), 127])
    by = {}
    for e in sorted(dedupe(cand)):
        by.setdefault(e[2], []).append(e)
    for lst in by.values():                     # zelfde toonhoogte mag in één spoor niet overlappen
        for a, b in zip(lst, lst[1:]):
            a[1] = min(a[1], b[0])
    th = release_ticks(100, TPB, BPM)
    cand = detach(sorted(e for lst in by.values() for e in lst if e[1] > e[0]), th)
    busy = []
    for k in order:
        t = 0 if k == 'drums' else release_ticks(real[progs[k]], TPB, BPM)
        busy += [(a, b + t) for a, b, n, v in res[k]]
    kept = allocate({'hold': cand}, ['hold'], {'hold': th}, preset=busy)['hold']
    print('  hold: %d aangehouden akkoordtonen terug, %d passen niet (geen kanaal vrij)' % (len(kept), len(cand) - len(kept)))
    return kept


def bridge_arp(T, bass):
    """v9: stijgende arpeggio's (16en, crescendo) in de brug. Maat 44 (tel 2-4): de tonen van het aangehouden akkoord
    B5/G5/B4 (alleen G en B: de bas loopt er C/Eb onder), per tel een stap hoger. Vanaf maat 45 (unisono-riff en de
    3-3-2-brug in kwinten): bij elke nieuwe basnoot opnieuw stijgend vanaf zijn grondtoon, met de kwint (als die toon in de bron dan klinkt;
    anders octaven), vanaf maat 47 een octaaf hoger: zo volgt het arpeggio de 3-3-2-wissels."""
    src = [(a, b, n) for i in (3, 4, 5) for a, b, n, v in T[i]]
    out = []
    for t in range(BRIDGE[0], BRIDGE[1], S16):
        if t < 45 * BAR:
            tones = [67, 71, 79, 83, 91, 95]                      # G4 B4 G5 B5 G6 B6 (de aangehouden tonen)
            k, i = (t - 44 * BAR) // BEAT - 1, (t % BEAT) // S16
            n = tones[k + i]
        else:
            o, _, r, _ = max([e for e in bass if e[0] <= t], key=lambda e: e[0])
            pcs = {m % 12 for a, b, m in src if a < o + S16 and b > o}
            steps = [0, 7, 12, 19, 24, 31] if (r + 7) % 12 in pcs else [0, 12, 24, 36]
            up = 12 if t >= 47 * BAR else 0
            n = r % 12 + 60 + up + steps[((t - o) // S16) % len(steps)]
        while n > TOP:
            n -= 12
        frac = (t - BRIDGE[0]) / (BRIDGE[1] - BRIDGE[0])
        out.append([t, t + 80, n, int(64 + 60 * frac)])
    return out


def bass_fill(bass):
    """v10: vul-stoten voor de bas in de brug op het raster x . x x . x . x (16en), alleen waar geen basnoot klinkt;
    lengte tot uiterlijk 8 ticks vóór de volgende basnoot (geen overlap van dezelfde toon in één spoor)."""
    out = []
    for t in range(BRIDGE[0], BRIDGE[1], S16):
        if (t // S16) % 8 not in (0, 2, 3, 5, 7):
            continue
        if any(a <= t < b + 8 for a, b, n, v in bass) or any(t <= a < t + S16 for a, b, n, v in bass):
            continue
        prev = max((e for e in bass if e[0] <= t), key=lambda e: e[0])
        nxt = min([e[0] for e in bass if e[0] > t] + [t + 9999])
        end = min(t + 56, nxt - 8)
        if end - t >= 32:
            out.append([t, end, prev[2], 100])
    return out


def bridge_sub(bass):
    """v9: staccato bas-stoten in achtsten op de PSG-sub (maat 45-49) op de toonhoogte van de laatst aangeslagen
    basnoot (zelfde octaaf als de sub), accent waar de bas zelf aanslaat, crescendo."""
    ons = {e[0] for e in bass}
    out = []
    for t in range(45 * BAR, BRIDGE[1], BEAT // 2):
        n = max([e for e in bass if e[0] <= t], key=lambda e: e[0])[2]
        n = n - 12 if n - 12 >= 36 else n
        frac = (t - 45 * BAR) / (BRIDGE[1] - 45 * BAR)
        out.append([t, t + 72, n, 127 if t in ons else int(92 + 24 * frac)])
    return out


def gliss(lead):
    """v10 (Jordi/Gemini: 'geen tokkel die losse nootjes omhoog tikt, maar dikke synth brass met een continue pitch bend
    van laag naar hoog, harde aanslag'): de opening-run (maat 2-4, E2 -> C6, in de bron een chromatische ladder van
    ±1 noot per 16e; in het origineel hoor je doorlopende glijlijnen, CQT van de stem 'other') wordt drie aangehouden
    noten (per maat één, velocity 127) op de glissando-brass, elk op het midden van zijn stuk van de ladder, met een
    pitch bend (BENDR 12) die elke 16 ticks (mid2agb-resolutie) de ladder volgt (lineair tussen de aanslagen).
    Geeft (nieuwe leadnoten, bend-events)."""
    g0, g1 = GLISS
    run = sorted(e for e in lead if g0 <= e[0] < g1)
    rest = [e for e in lead if not g0 <= e[0] < g1]
    nxt = min(e[0] for e in rest if e[0] >= g1)
    pts = [(e[0], e[2]) for e in run]
    segs = [[p for p in pts if b * BAR <= p[0] < (b + 1) * BAR] for b in (2, 3, 4)]
    notes, ev = [], []
    for i, sg in enumerate(segs):
        t0 = sg[0][0]
        t1 = segs[i + 1][0][0] if i + 1 < len(segs) else nxt
        lo, hi = sg[0][1], sg[-1][1]
        c = (lo + hi + 1) // 2
        assert hi - c <= BENDR and c - lo <= BENDR
        notes.append([t0, t1, c, 127])
        # ladder inclusief de eerste toon van het volgende stuk (doorlopend glijden tot de volgende aanslag)
        lad = sg + ([segs[i + 1][0]] if i + 1 < len(segs) else [])
        for t in range(t0, t1, S16 // 6):
            prev = [p for p in lad if p[0] <= t][-1]
            later = [p for p in lad if p[0] > t]
            if later:
                q = later[0]
                pitch = prev[1] + (q[1] - prev[1]) * (t - prev[0]) / (q[0] - prev[0])
            else:
                pitch = prev[1]
            pitch = min(hi, max(lo, pitch)) if i + 1 == len(segs) else min(pitch, c + BENDR)
            ev.append((t, mido.Message('pitchwheel', pitch=max(-8192, min(8191, int(round(8192 * (pitch - c) / BENDR)))))))
    ev.append((nxt, mido.Message('pitchwheel', pitch=0)))
    ev = [(0, mido.Message('control_change', control=20, value=BENDR))] + ev
    print('  glissando: %d ladder-noten -> %d aangehouden noten met %d bend-stappen' % (len(run), len(notes), len(ev) - 2))
    return sorted(rest + notes), ev


def cap_top(ev):
    """v10: geen melodische noot boven C6 (TOP): een octaaf (of meer) omlaag."""
    out = []
    for s_, e_, n, v in ev:
        while n > TOP:
            n -= 12
        out.append([s_, e_, n, v])
    return dedupe(out)


FORBIDDEN = ('flute', 'piano', 'nylon', 'acoustic', 'marimba', 'string', 'pad', 'choir', 'violin', 'cello',
             'harp', 'recorder', 'ocarina', 'xylo', 'oboe', 'bassoon', 'whistle', 'theremin', 'clarinet')
MOD_CCS = {1: 'MOD', 21: 'LFOS', 22: 'MODT', 26: 'LFODL'}     # mid2agb: vibrato/LFO-controllers
LEAD_MAX_TREMOLO, LEAD_MAX_REL = 1.0, 80                       # v11: lead zonder zweving, afgekapt


def sample_tremolo(name, note=72, dur=1.5):
    """v11: amplitudeschommeling (dB, p5-p95 van de RMS per 4 perioden) van de aangehouden sample `name` op toon
    `note`, na de aanslag (0,2 s): een gechorusde/ontstemde sample (sc88pro_square_wave 8 dB, np_lead_fat 10 dB) zweeft
    = 'theremin met vibrato'; een zuivere golf ±0 dB."""
    import numpy as np
    import gba_sim
    a, rate, lab, loop = gba_sim.sample(name)
    sr = gba_sim.MIX
    pos = np.arange(int(dur * sr)) * rate * 2 ** ((note - lab) / 12) / sr
    if loop:
        L = loop[1] - loop[0]
        o = pos >= loop[1]
        pos[o] = loop[0] + (pos[o] - loop[0]) % L
    pos = pos[pos < len(a) - 1]
    y = a[pos.astype(int)][int(0.2 * sr):]
    w = int(round(4 * sr / (440 * 2 ** ((note - 69) / 12))))
    r = np.array([np.sqrt((y[k:k + w] ** 2).mean()) for k in range(0, len(y) - w, max(1, w // 4))])
    return 20 * np.log10(np.percentile(r, 95) / max(1e-9, np.percentile(r, 5)))


def rules_check(path):
    """v12: Jordi's regels als harde controles op de geschreven MIDI + voicegroup:
    1. klinkende hoogte (geschreven + SOUND_OFS) van elke melodische noot tussen E1 en C6;
    2. alleen stock-samples: elke gebruikte DirectSound-sample (ook via keysplits/kit) staat in
       sound/direct_sound_samples/ (niet in grounded/) en in een vanilla voicegroup (niet grounded_*);
       geen akoestische instrumenten/strijkers/pads (FORBIDDEN);
    3. geen trage aanzet: attack 255 (DirectSound) of <= 1 (PSG);
    4. geen pitch bends, geen BENDR, geen MOD/LFO-controllers;
    5. de lead (MIDI-kanaal 0) gebruikt alleen samples zonder zweving (tremolo < LEAD_MAX_TREMOLO dB) en een release
       <= LEAD_MAX_REL.
    Faalt met een AssertionError."""
    import re, glob
    m = mido.MidiFile(path)
    vg = {}
    for l in open(VG):
        mm = re.match(r'\t(voice_\w+) (.*?)\s+@ (\d+)', l)
        if mm:
            vg[int(mm.group(3))] = (mm.group(1), mm.group(2))
    groups_ = {}
    for f in (KEYSPLIT, LEAD_KEYSPLIT, DRUMSET):
        cur = None
        for l in open(f):
            if l.startswith('voice_group'):
                cur = l.split()[1].rstrip(',')
                groups_[cur] = []
            elif l.startswith('\tvoice'):
                groups_[cur].append(tuple(l.strip().split(' ', 1)))
    vanilla = set()
    for f in glob.glob('sound/voicegroups/**/*.inc', recursive=True):
        if 'grounded' in f or f in (VG, KEYSPLIT, LEAD_KEYSPLIT, DRUMSET):
            continue
        vanilla |= set(re.findall(r'DirectSoundWaveData_(\w+)', open(f).read()))

    def lines_of(prog):
        kind, args = vg[prog]
        if kind.startswith('voice_keysplit'):
            return groups_[args.split(',')[0].strip().replace('voicegroup_', '')]
        return [(kind, args)]
    bad = []
    for i, t in enumerate(m.tracks):
        drum = any(x.channel == 9 for x in t if x.type == 'note_on')
        tt, cur, used = 0, None, set()
        for x in t:
            tt += x.time
            if x.type == 'program_change':
                cur = x.program
            if x.type == 'note_on' and x.velocity:
                used.add(cur)
                snd = x.note + SOUND_OFS.get(cur, 0)
                if not drum and not 28 <= snd <= TOP:
                    bad.append('spoor %d: klinkende noot %d buiten E1-C6 (tick %d)' % (i, snd, tt))
            if x.type == 'pitchwheel' or (x.type == 'control_change' and x.control == 20):
                bad.append('spoor %d: pitch bend/BENDR op tick %d' % (i, tt))
            if x.type == 'control_change' and x.control in MOD_CCS:
                bad.append('spoor %d: %s (CC%d) op tick %d' % (i, MOD_CCS[x.control], x.control, tt))
        for p in used:
            for kind, args in lines_of(p):
                a = [x.strip() for x in args.split(',')]
                if kind.startswith('voice_directsound'):
                    smp = a[2].replace('DirectSoundWaveData_', '')
                    if not os.path.exists('sound/direct_sound_samples/%s.wav' % smp) or smp not in vanilla:
                        bad.append('spoor %d prog %d: geen stock-sample %s' % (i, p, smp))
                    words = re.split(r'[_\d]+', smp.lower())
                    if any(w.startswith(f) for w in words for f in FORBIDDEN):
                        bad.append('spoor %d prog %d: sample %s' % (i, p, smp))
                    if int(a[3]) != 255 and int(a[5]) > 0:
                        bad.append('spoor %d prog %d: trage aanzet (attack %s)' % (i, p, a[3]))
                    if i == 1 or any(x.channel == 0 for x in t if x.type == 'note_on'):
                        tr = sample_tremolo(smp, 60 if smp.endswith('_60') or 'bass' in smp else 72)
                        if tr >= LEAD_MAX_TREMOLO:
                            bad.append('lead prog %d: sample %s zweeft (%.1f dB tremolo)' % (p, smp, tr))
                        if int(a[6]) > LEAD_MAX_REL:
                            bad.append('lead prog %d: release %s > %d' % (p, a[6], LEAD_MAX_REL))
                elif kind.startswith(('voice_square', 'voice_programmable', 'voice_noise')):
                    if drum:
                        bad.append('spoor %d: PSG-drumnoot (prog %d)' % (i, p))
                    att = int(a[-4])
                    if att > 1:
                        bad.append('spoor %d prog %d: PSG-attack %d' % (i, p, att))
    assert not bad, 'regels van Jordi geschonden: ' + '; '.join(bad)
    print('  regels: klinkend E1-C6, alleen stock-samples, geen akoestische/trage samples, geen bends/MOD/LFO, '
          'lead zonder zweving (< %.0f dB) en release <= %d: OK' % (LEAD_MAX_TREMOLO, LEAD_MAX_REL))


def staccato(ev, f, lo, hi):
    return [[s, s + max(lo, min(hi, int((e - s) * f))), n, v] for s, e, n, v in ev]


def drums(T):
    out, hats, dropped = [], [], 0
    src = sorted(T[0] + T[1] + T[2])
    snares = sorted(s for s, e, n, v in src if n == 38)
    for s, e, n, v in src:
        if n in (42, 44):
            hats.append([s, s + HAT_LEN, CHAT, HAT_ACC])
            continue
        if n not in DRUM_MAP:
            dropped += 1
            continue
        n2, ln, vel = DRUM_MAP[n]
        q = s - s % S16 if n == 36 and s % S16 in (6, 12) else s       # 909-flams (offset 6/12) op de tel
        out.append([q, q + ln, n2, vel])
    # v7: four-on-the-floor (kick op elke tel), scherpe snare op 2 en 4, ghost-dubbelslag aan het eind van elke 2e en
    # 4e maat (16en 3e en 4e van tel 4), in alle gevechtsmaten behalve de breaks
    kicks = {e[0] for e in out if e[2] == KICK}
    fills = {e[0] // S16 for e in out if e[2] == SNARE}
    for b in range(10, 74):
        if b in BREAK:
            continue
        for beat in range(4):
            t = b * BAR + beat * BEAT
            if t not in kicks:
                out.append([t, t + DRUM_MAP[36][1], KICK, DRUM_MAP[36][2]])
            if beat in (1, 3) and t // S16 not in fills:
                out.append([t, t + SNARE_LEN, SNARE24, BACK_VEL])
        if (b - 10) % 2 == 1:
            for i in (14, 15):
                t = b * BAR + i * S16
                if t // S16 not in fills:
                    out.append([t, t + S16, SNARE24, GHOST_VEL])
    out = dedupe(out)
    by = {}
    for e in out:
        by.setdefault(e[2], []).append(e)
    for lst in by.values():                         # een nieuwe slag op dezelfde drumnoot kapt de vorige af
        lst.sort()
        for a, b in zip(lst, lst[1:]):
            a[1] = min(a[1], b[0])
    # constante hihats op alle 16en in de gevechtsdelen, accent op elke kwart, daartussen om en om (niet waar de bron
    # zelf een (open) hihat heeft, of waar de clap/snare al de hoge tik geeft: scheelt een DS-kanaal)
    taken = {e[0] for e in out if e[2] in (OHAT, SNARE_OFF, SNARE, SNARE24)} | {h[0] for h in hats}
    for b in range(10, 74):
        if b in NO_HATS:
            continue
        for i in range(16):
            t = b * BAR + i * S16
            if t in taken:
                continue
            hats.append([t, t + HAT_LEN, CHAT, HAT_ACC if i % 4 == 0 else (HAT_A if i % 2 == 0 else HAT_B)])
    return sorted(out + dedupe(hats)), dropped


def octave_down(ev):
    """Lead een octaaf lager, per maat (loopjes blijven heel) als de hele maat daarna nog >= C2 ligt; in maten met
    lage arpeggio's/sprongen (intro, maat 30-33, 62) alleen de hoge noten (>= Bb4)."""
    by = {}
    for e in ev:
        by.setdefault(e[0] // BAR, []).append(e)
    out = []
    for b, lst in sorted(by.items()):
        whole = min(e[2] for e in lst) - 12 >= 36
        out += [[s, e, n - 12 if whole or n >= 70 else n, v] for s, e, n, v in lst]
    return out


def stabs(guitar, arp, src=None):
    """v7: staccato akkoordstoten (2 stemmen, G3-D5) op elke 'en' (8e off-beat) in de gevechtsmaten zonder orgel.
    De gitaar speelt meestal 16e-octaven (alleen de grondtoon), dus akkoord = een gitaarakkoord met >= 2 toonklassen
    (aanzet <= 2 tellen eerder; geen stoot als het akkoord precies op deze 'en' zelf slaat), anders de
    arpeggiotonen van deze tel. Tweeklank = de twee hoogste tonen met een terts..sext ertussen (geen secundes:
    in de unisono-riffs geeft dat clusters). Geen eigen harmonie: alleen tonen uit de bron."""
    onsets = {}
    for s_, e_, n, v in guitar:
        onsets.setdefault(s_, set()).add(n)
    chords = sorted(t for t, ns in onsets.items() if len({n % 12 for n in ns}) >= 2)
    out, skipped, replaced = [], 0, 0
    for b in range(10, 74):
        if b in BREAK or b in ORGAN_BARS or b in UNISONO_BARS:
            continue
        for beat in range(4):
            t0 = b * BAR + beat * BEAT
            t = t0 + BEAT // 2
            prev = [g for g in chords if t - 2 * BEAT <= g <= t]
            if prev and prev[-1] == t:
                continue                            # het gitaarakkoord slaat hier al
            if prev:
                pcs = onsets[prev[-1]]
            else:
                pcs = {n for s_, e_, n, v in arp if t0 <= s_ < t0 + BEAT}
            voiced = {}
            for n in pcs:
                while n > 74:
                    n -= 12
                while n < 55:
                    n += 12
                voiced[n % 12] = n
            vs = sorted(voiced.values(), reverse=True)
            pair = next(((hi, lo) for i, hi in enumerate(vs) for lo in vs[i + 1:] if 3 <= hi - lo <= 9), None)
            if pair and src is not None:
                # v9: een stoot mag alleen tonen bevatten die de bron op dat moment (t .. t + 72) laat klinken, en
                # geen kleine secunde maken met een brontoon: v7 nam het laatste akkoord tot 2 tellen
                # terug, en dat schuurde (C4 tegen C#/D in maat 25/27/29, C#4 tegen D in maat 18-21, F4/A3 tegen Em
                # in maat 42). Is de v7-tweeklank fout, dan een tweeklank uit de tonen die nu klinken; anders geen.
                now = {n % 12 for a, b, n in src if a < t + 72 and b > t}
                ok = lambda n: n % 12 in now and not any((n - m) % 12 in (1, 11) for m in now)
                if not all(ok(n) for n in pair):
                    vs2 = sorted({n % 12: 55 + (n - 55) % 12 for n in now if ok(n)}.values(), reverse=True)
                    pair = next(((hi, lo) for i, hi in enumerate(vs2) for lo in vs2[i + 1:] if 3 <= hi - lo <= 9), None)
                    replaced += pair is not None
                    skipped += pair is None
            if pair:
                out += [[t, t + 72, n, 100] for n in pair]
    print('  stoten: %d (v9: %d met een andere tweeklank, %d weggelaten: geen passende tonen)' % (len(out) // 2, replaced,
                                                                                               skipped))
    return out


def tempo_map(song, end):
    """Per tel 176 of 178 (mid2agb: TEMPO = bpm/2, alleen even waarden), gemiddeld 176,76 'GBA-bpm' = 175,96 echte bpm
    (de GBA draait op 59,7275 Hz i.p.v. 60). Bresenham: 5 op 13 tellen 178."""
    want = 175.96 * 60 / 59.7275            # GBA-tempowaarde die precies 175,96 bpm geeft
    p = (1 / 176 - 1 / want) / (1 / 176 - 1 / 178)     # aandeel tellen op 178 (tijd per tel ~ 1/tempo)
    acc, last = 0.0, None
    for beat in range(end // BEAT):
        acc += p
        bpm = 176
        if acc >= 1:
            acc -= 1
            bpm = 178
        if bpm != last:
            song.tempo(beat * BEAT, bpm / 120)
            last = bpm


def build():
    m = mido.MidiFile(SRC)
    assert m.ticks_per_beat == TPB
    T = fixed_source(m)
    clip = lambda ev: [[s, min(e, END), n, v] for s, e, n, v in ev if s < END]
    dr, drum_drop = drums(T)

    # sawtooth: bovenstem = lead (bronhoogte) + dezelfde melodie een octaaf lager (PSG, body; vervangt de
    # octaafverdubbeling uit de bron), binnenstemmen >= C3 = arpeggio (steel drums A + PSG B);
    # lage noten (< C3) verdubbelen de bas: weg (de bas speelt ze al)
    lead, arp, saw_low = [], [], 0
    for g in groups(T[4]):
        top = g[-1]
        lead.append(list(top))
        for e in g[:-1]:
            if e[2] == top[2] - 12 and e[2] >= 48:
                pass                                # = body (staat hieronder als eigen laag)
            elif e[2] >= 48:
                arp.append(list(e))
            else:
                saw_low += 1
    lead = mono(quantize_runs(lead))
    arp = mono(quantize_runs(thin(arp, 1, 'top')))
    # 'gitaar' = synth brass-stoten: akkoorden vanaf C3 (3 bovenste stemmen), daaronder de lage partij (1 stem)
    guitar = thin([e for e in T[5] if e[2] >= 48], 3, 'top')
    brass = staccato(guitar, 0.85, 60, 9999)
    brass_lo = mono([g[0] for g in groups([e for e in T[5] if e[2] < 48])])
    brass_lo = staccato(brass_lo, 0.7, 50, 9999)
    # v6: koper niet onder C3 (de lage partij E1-B2 gaf een subdreun op 30-60 Hz): per octaaf omhoog tot >= C3, en
    # weg waar de akkoordpartij die toon op die tel al speelt
    have = {(e[0], e[2]) for e in brass}
    lifted = []
    for s_, e_, n, v in brass_lo:
        while n < 48:
            n += 12
        if (s_, n) not in have:
            lifted.append([s_, e_, n, v])
    brass_lo = lifted
    # bas: onderstem, staccato (klinkt een octaaf lager door de sample); sub = zelfde ritme op de PSG-golf, op de
    # klinkende toonhoogte van de bas
    bass = staccato(mono([g[0] for g in groups(T[3])]), BASS_LEN, 64, 300)
    # (PSG-noten onder C2 klinken in m4a allemaal als C2: MidiKeyToCgbFreq klemt key <= 35. Waar de bas onder C2
    # klinkt (Eb1-B1), speelt de sub de geschreven noot = een octaaf boven de grondtoon, op hetzelfde ritme.)
    sub = [[s_, e_, n - 12 if n - 12 >= 36 else n, 127] for s_, e_, n, v in bass]
    # orgel: zelfde register, kort en scherp (ongewijzigd sinds v5)
    organ = staccato(thin(T[6], 3, 'top'), 0.7, 20, 200)
    srcmel = [(a, b, n) for i in range(3, 10) for a, b, n, v in T[i]]
    stab = stabs(guitar, arp, srcmel)
    # waar een stoot valt en de brass een octaaf-chug speelt: alleen de bovenste noot van de chug (scheelt een kanaal)
    st = {e[0] for e in stab}
    hi = {}
    for e in brass:
        hi[e[0]] = max(hi.get(e[0], 0), e[2])
    brass = [e for e in brass if e[0] not in st or e[2] == hi[e[0]]]
    parts = {'drums': dr, 'bass': bass, 'brass': brass, 'organ': organ, 'brass_lo': brass_lo, 'steel': T[8],
             'arp': arp, 'stab': stab, 'dsine': T[7] + T[9]}
    parts = {k: cap_top(clip(v)) for k, v in parts.items()}
    parts['lead'] = cap_top(clip(lead))

    voicegroup()
    rel = dict(V11_REL)              # v12: notenberekening met de v11-releases (noten exact v11)
    # v8: de stemverdeler (en detach) rekent met de releases van v7, zodat élke noot (aanslag, lengte, toonhoogte)
    # exact v7 blijft; alleen de lead wordt daarna legato. ds_check() meet de bezetting met de echte v8-releases.
    rel = dict(rel)
    rel.update({BASS: 120, BRASS: 120, BRASS_LO: 110, LEAD: 140, STAB: 100, PLUCK: 150})
    rel[BASS] = BASS_REL            # v11: de bas rekent met zijn echte (korte) release; zie BASS_LEN
    progs = {'lead': LEAD, 'bass': BASS, 'brass': BRASS, 'organ': ORGAN, 'steel': PLUCK, 'brass_lo': BRASS_LO,
             'arp': PLUCK, 'stab': STAB, 'dsine': DSINE}
    # v9: het arpeggio in de opening (maat 0-21) op de vette lead met een korte release (FARP: aanhouden en snel los
    # i.p.v. de tokkel van de blokgolf-pluk): een eigen partij met een eigen uitklinktijd, vlak vóór 'arp'
    parts['farp'] = [e for e in parts['arp'] if e[0] < FAT_END]
    parts['arp'] = [e for e in parts['arp'] if e[0] >= FAT_END]
    progs['farp'] = FARP_LO
    rel[FARP_LO] = 40
    tail = {k: release_ticks(rel[p], TPB, BPM) for k, p in progs.items()}
    tail.update(drums=0)
    for k in progs:                                 # staccato-partijen: release valt binnen de eigen 16e
        parts[k] = detach(parts[k], tail[k])
    order = ['drums', 'brass', 'lead', 'bass', 'brass_lo', 'organ', 'steel', 'dsine', 'stab', 'farp', 'arp']   # v12e: melodie eerst
    res = allocate(parts, order, tail)
    assert len(res['lead']) == len(parts['lead']), 'lead verliest noten'
    real = V11_REL
    res['lead'] = trim_legato(res, order, {k: 0 if k == 'drums' else release_ticks(real[progs[k]], TPB, BPM)
                                           for k in order})
    # v11: afgekapt per noot: elke leadnoot laat los een uitklinktijd vóór de volgende aanslag (geen staart die over
    # de volgende noot heen 'glijdt'); de glissando-noten hieronder houden hun eigen lengte
    res['lead'] = detach(res['lead'], release_ticks(LEAD_REL, TPB, BPM))
    # v12: de opening-run speelt weer als ladder (gewone noten, geen bends); de stemverdeling hieronder rekent nog met
    # de 3 glijnoten van v11 (zelfde bezetting: hold/brug/basvulling blijven exact v11)
    ladder = res['lead']
    res['lead'], _ = gliss(res['lead'])
    parts['lead'] = res['lead']
    body = [[s_, e_, n - 12, 96] for s_, e_, n, v in ladder if n - 12 >= 40]
    # v9: aangehouden sawtooth-akkoordtonen (>= 3 16en, >= C3) die nergens meer klinken: eigen spoor 'hold', alleen
    # waar een kanaal vrij is (uitklinktijden van alle andere partijen meegerekend)
    res['hold'] = held_tones(T[4], res, order, progs, real)
    order.append('hold')
    progs['hold'] = HOLD
    parts['hold'] = res['hold']
    # v9: het brug-arpeggio ook op DirectSound (vette lead, release 40: 1 kanaal), waar een kanaal vrij is; de
    # PSG-kopie op arp B klinkt 1/24 tel later (zoals elders in het nummer)
    barp = [[s_, s_ + 64, n, v] for s_, e_, n, v in bridge_arp(T, res['bass'])]
    busy = []
    for k in order:
        t_ = 0 if k == 'drums' else release_ticks(real[progs[k]], TPB, BPM)
        busy += [(a, b + t_) for a, b, n, v in res[k]]
    res['barp'] = allocate({'barp': barp}, ['barp'], {'barp': release_ticks(40, TPB, BPM)}, preset=busy)['barp']
    order.append('barp')
    progs['barp'] = FARP_HI
    parts['barp'] = barp
    # v10: brug: de bas drukt door (Gemini 'x . x x . x . x' per 16e): vul-stoten op de dikke bas waar de bas zelf
    # zwijgt, op de toon van de laatste basnoot, zachter dan de basnoten zelf (de 3-3-2 van de riff blijft hoorbaar)
    busy = []
    for k in order:
        t_ = 0 if k == 'drums' else release_ticks(real[progs[k]], TPB, BPM)
        busy += [(a, b + t_) for a, b, n, v in res[k]]
    bf = bass_fill(res['bass'])
    res['bfill'] = allocate({'bfill': bf}, ['bfill'], {'bfill': release_ticks(real[BASS], TPB, BPM)}, preset=busy)['bfill']
    order.append('bfill')
    progs['bfill'] = BASS
    parts['bfill'] = bf
    ds_check(res, progs, order)
    print('drumnoten buiten de kit (weg): %d, lage sawtooth-noten (basverdubbeling, weg): %d' % (drum_drop, saw_low))
    for k in order:
        n, kept = len(parts[k]), len(res[k])
        print('  %-9s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - kept, 100 * (n - kept) / max(n, 1)))
    res['lead'] = parts['lead'] = ladder
    p = res
    # arpeggio spoor B (PSG): alle arpeggio's/steel drums (ook wat in A wegviel), 1/24 tel later
    arpb = mono([[s_ + ARPB_DELAY, e_ + ARPB_DELAY, n, v] for s_, e_, n, v in parts['farp'] + parts['arp'] + parts['steel']])
    # v9: brug: stijgende arpeggio's op arp B en staccato bas-stoten in achtsten op de sub
    arpb = [e for e in arpb if not BRIDGE[0] <= e[0] < BRIDGE[1]] + \
        [[s_ + ARPB_DELAY, e_ + ARPB_DELAY, n, v] for s_, e_, n, v in bridge_arp(T, res['bass'])]
    # v10: de PSG-bas-stoten van v9 in de brug ('zacht, hol piepje') weg: de sub speelt weer zoals in v8
    psg = {'body': dedupe(clip(body)), 'sub': dedupe(clip(sorted(sub))), 'arpb': dedupe(clip(sorted(arpb)))}
    song = Song(TPB, 500000)
    tempo_map(song, END)
    song.loop = (LOOP0, END)
    # v12: lead op de trompet; < C3 op de synth bass (koper niet onder C3)
    lead_prog = lambda n, s_: FAT_LO if n < 48 else LEAD
    arp_prog = lambda n, s_: (FARP_HI if n >= 60 else FARP_LO) if s_ < FAT_END else PLUCK
    # v12f (Jordi: 'de melodie valt daarna meermaals kort weg'): de melodie wisselt in de bron tussen de gitaar (brass) en
    # de sawtooth-lead; de lead alleen terug in de maten waar de gitaar hem speelt (>= 4 aanslagen per maat), elders 127
    gtr = collections.Counter(s_ // BAR for s_, e_, n, v in p['brass'] + p['brass_lo'])
    lead_vol = [(0, 127)]
    for b_ in range(LOOP0 // BAR, END // BAR):
        v_ = 84 if gtr[b_] >= 4 else 127
        if v_ != lead_vol[-1][1]:
            lead_vol.append((b_ * BAR, v_))
    lead_cc = prog_events(p['lead'], lead_prog) + [(t, 7, v) for t, v in lead_vol]
    arp_notes = sorted(p['farp'] + p['arp'])
    arpb_cc = [(BRIDGE[0], 7, VOL_ARPB_BRIDGE), (BRIDGE[1], 7, VOL['arpb'])]
    tracks = [
        (p['lead'], lead_prog(p['lead'][0][2], 0), LEAD_VOL[0][1], 0, 64, lead_cc),
        (psg['body'], BODY, VOL['body'], 1, 64),
        (p['brass'], BRASS, VOL['brass'], 2, 56, [(LOOP0, 7, LOOP_VOL['brass'])]),
        (p['brass_lo'], BRASS_LO, VOL['brass_lo'], 3, 64, [(LOOP0, 7, LOOP_VOL['brass_lo'])]),
        (p['organ'], ORGAN, VOL['organ'], 4, 72),
        (sorted(p['bass'] + p['bfill']), BASS, VOL['bass'], 5, 64),
        (psg['sub'], SUB, VOL['sub'], 6, 64),
        (arp_notes, arp_prog(arp_notes[0][2], 0), VOL['arp'], 7, 35, prog_events(arp_notes, arp_prog)),
        (p['steel'], PLUCK, VOL['steel'], 8, 35),
        (psg['arpb'], ARPB, VOL['arpb'], 10, 85, arpb_cc),
        (p['stab'], STAB, VOL['stab'], 11, 60),
        (p['dsine'], DSINE, VOL['dsine'], 12, 64),
        (p['drums'], DRUMS, VOL['drums'], 9, None),
        (p['hold'], HOLD, VOL_HOLD, 13, 92),
        (p['barp'], FARP_HI, VOL_BARP, 14, 40),
    ]
    written = 0
    for notes, prog, vol, ch, pan, *cc in tracks:
        assert notes, 'lege partij'
        # v12: klinkende hoogte = v11 (organ2 klinkt een octaaf onder de geschreven noot; de fingered bass op de
        # geschreven noot, np_bass_buzz klonk een octaaf lager)
        if prog in OCT_UP:
            notes = [[s_, e_, n + 12, v] for s_, e_, n, v in notes]
        elif prog == BASS:
            notes = [[s_, e_, n - 12 if n - 12 >= 28 else n, v] for s_, e_, n, v in notes]
        song.add(notes, prog, vol, ch, pan, extra=cc[1] if len(cc) > 1 else (), ccs=cc[0] if cc else ())
        written += len(notes)
    assert written == sum(len(p[k]) for k in order) + sum(len(v) for v in psg.values()), 'niet elke partij staat in de MIDI'
    song.save(OUT, END)
    rules_check(OUT)
    print('PSG: body %d, sub %d, arp B %d noten' % tuple(len(psg[k]) for k in ('body', 'sub', 'arpb')))
    print(OUT, '(%d sporen, intro %.1f s, loop %.1f s)' % (len(song.tracks), LOOP0 / TPB * 60 / 175.96,
                                                           (END - LOOP0) / TPB * 60 / 175.96))


if __name__ == '__main__':
    build()
