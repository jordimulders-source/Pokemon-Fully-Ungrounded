#!/usr/bin/env python3
"""Project Grounded: gevechtsmuziek van Neo Team Plasma (Battle Stadium): "Battle! Neo Team Plasma"
(Pokémon Black 2/White 2). Noten: MIDI van Byabbington (onlinesequencer, sound/songs/grounded_src/b2w2_neo_plasma.mid).
Klank, timing en balans: gemeten aan het origineel (BW2-mp3 van Jordi). Structuur zoals in de game: intro maat 0-9,
loop maat 10-73 (de MIDI speelt die loop twee keer).

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

Gebruik: python3 tools/grounded/neo_plasma_theme.py (samples: tools/grounded/neo_plasma_samples.py)"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, thin, detach, allocate, releases, release_ticks, Song

SRC = 'sound/songs/grounded_src/b2w2_neo_plasma.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_neo_plasma.mid'
VG = 'sound/voicegroups/grounded_neo_plasma.inc'
DRUMSET = 'sound/voicegroups/drumsets/neo_plasma.inc'
KEYSPLIT = 'sound/voicegroups/keysplits/np_trumpet.inc'
TPB, BAR, BEAT, S16 = 384, 1536, 384, 96
BPM = 176
LOOP0, END = 10 * BAR, 74 * BAR
SAW_SHIFT = 17              # sawtooth vanaf maat 5: 17 ticks te vroeg in de bron

# programma's in voicegroup_grounded_neo_plasma
BASS, BRASS, BRASS_LO, ORGAN, LEAD, DRUMS = 38, 62, 63, 17, 80, 127
BODY, SUB, ARPB, DSINE, STAB, PLUCK = 81, 82, 84, 85, 86, 87
VOICES = {
    LEAD:     'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_square_wave, 255, 0, 255, 140',
    BODY:     'voice_square_1 60, 0, 0, 2, 0, 1, 12, 3',
    ARPB:     'voice_square_2 60, 0, 2, 0, 2, 6, 1',
    DSINE:    'voice_directsound 72, 0, DirectSoundWaveData_np_sine, 255, 220, 200, 140',
    STAB:     'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 215, 40, 100',
    PLUCK:    'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_square_wave, 255, 205, 0, 110',
    BASS:     'voice_directsound 60, 0, DirectSoundWaveData_np_synth_bass, 255, 245, 60, 110',
    BRASS:    'voice_keysplit voicegroup_np_trumpet_keysplit, keysplit_trumpet',
    BRASS_LO: 'voice_keysplit voicegroup_np_trumpet_keysplit, keysplit_trumpet',
    ORGAN:    'voice_directsound 60, 0, DirectSoundWaveData_np_organ_sharp, 255, 220, 160, 90',
    SUB:      'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 1',
    DRUMS:    'voice_keysplit_all voicegroup_neo_plasma_drumset',
}
# drumkit (noot -> regel); standaard GBA-samples in de GM-indeling (v8; v7 had 36-43 op een rij)
KICK, SNARE, SNARE_OFF, SNARE24, CHAT, OHAT, CRASH, SPLASH = 36, 38, 39, 40, 42, 46, 49, 55
KITV = {
    KICK:      'voice_directsound 67, 0, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 0',
    SNARE:     'voice_directsound_no_resample 60, 0, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 220',
    SNARE_OFF: 'voice_directsound_no_resample 60, 0, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 180',
    SNARE24:   'voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_synth_snare, 255, 0, 255, 200',
    CHAT:      'voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 255, 0',
    OHAT:      'voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0',
    CRASH:     'voice_directsound_no_resample 60, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',
    SPLASH:    'voice_directsound 67, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 200, 0, 140',
}
# ongebruikte noten in de kit: een stille DirectSound-regel (geen PSG: een verdwaalde noot mag niet piepen)
KIT = [KITV.get(k, 'voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0')
       for k in range(36, max(KITV) + 1)]
# bron-drumnoot -> (kitnoot, lengte in ticks, velocity 0-127); 42/44 = dichte hihat
DRUM_MAP = {36: (KICK, 190, 96), 37: (SNARE_OFF, 160, 127), 38: (SNARE, 192, 120), 46: (OHAT, 192, 70),
            49: (CRASH, 384, 100), 57: (CRASH, 384, 100), 55: (SPLASH, 288, 90)}
HAT_LEN, HAT_ACC, HAT_A, HAT_B = 80, 127, 92, 74   # dichte hihat: 77 ms = 82 ticks; accent op de kwart
BREAK = {34, 35, 36, 64, 65}                # breaks (halftime / zonder bas): geen four-on-the-floor/hihats/stoten
NO_HATS = set(range(0, 10)) | BREAK         # intro en breaks: geen 16e-hihats
ORGAN_BARS = set(range(49, 62)) | set(range(65, 71))    # daar speelt het orgel al 16e-stoten: geen extra stoten
SNARE_LEN, GHOST_VEL, BACK_VEL = 192, 58, 118
UNISONO_BARS = set(range(46, 50))           # unisono-riff (bas + saw): geen akkoordstoten
ARPB_DELAY = 16                             # spoor B van de arpeggio's: 1/24 tel later (±1 frame)

# spoorvolumes (CC7), afgesteld met solo-RMS en balance_orig.py tegen de mp3
# v8: nieuwe samples op dezelfde luidheid als v7 gezet (RMS van de eerste 80 ms per sample), lead en lead-octaaf
# iets terug omdat ze nu aanhouden
VOL = dict(lead=92, body=66, brass=97, brass_lo=81, organ=62, bass=114, sub=96, steel=38, arp=34, arpb=40,
           dsine=40, stab=45, drums=80)
LEGATO_GAP = BEAT           # lead: een noot houdt aan tot de volgende aanslag als de rust ertussen <= 1 tel is


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Neo Team Plasma (BW2) v8. Gegenereerd door tools/grounded/neo_plasma_theme.py.'
    lines[1] = '@ 17 orgel, 38 synth bass, 62/63 synth brass (trompet-keysplit), 80 square-lead, 81 lead-octaaf (PSG), 82 sub (PSG-golf), 84 arp B (PSG), 85 sinus, 86 orgelstoot, 87 square-pluk, 127 drums.'
    lines[2] = 'voice_group grounded_neo_plasma'
    out = []
    for l in lines:
        k = l.rsplit('@', 1)[1].strip() if '@' in l and l.startswith('\tvoice') else None
        if k and k.isdigit() and int(k) in VOICES:
            l = '\t%s  @ %s' % (VOICES[int(k)], k)
        out.append(l)
    open(VG, 'w').write('\n'.join(out))
    open(KEYSPLIT, 'w').write(
        '@ Project Grounded: synth brass voor Battle! Neo Team Plasma v8 (neo_plasma_theme.py) = de GBA-trompetten\n'
        '@ (sc88pro_trumpet_60/72/84, tabel keysplit_trumpet) zoals trumpet.inc, met een korte release (110, v7-brass: 110-120): stoten.\n'
        'voice_group np_trumpet_keysplit\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_trumpet_%d, 255, 0, 193, 110\n' % k for k in (60, 72, 84)))
    open(DRUMSET, 'w').write(
        '@ Project Grounded: drumkit voor Battle! Neo Team Plasma v8 (neo_plasma_theme.py): standaard GBA-samples\n'
        '@ in de GM-indeling: 36 kick (+7 halve tonen), 38 snare (fills), 39 off-beat-clap (909), 40 felle snare\n'
        '@ (2 en 4, ghosts), 42 dichte hihat, 46 open hihat, 49 crash, 55 splash. Alles DirectSound.\n'
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
    return T


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


def stabs(guitar, arp):
    """v7: staccato akkoordstoten (2 stemmen, G3-D5) op elke 'en' (8e off-beat) in de gevechtsmaten zonder orgel.
    De gitaar speelt meestal 16e-octaven (alleen de grondtoon), dus akkoord = een gitaarakkoord met >= 2 toonklassen
    (aanzet <= 2 tellen eerder; geen stoot als het akkoord precies op deze 'en' zelf slaat), anders de
    arpeggiotonen van deze tel. Tweeklank = de twee hoogste tonen met een terts..sext ertussen (geen secundes:
    in de unisono-riffs geeft dat clusters). Geen eigen harmonie: alleen tonen uit de bron."""
    onsets = {}
    for s_, e_, n, v in guitar:
        onsets.setdefault(s_, set()).add(n)
    chords = sorted(t for t, ns in onsets.items() if len({n % 12 for n in ns}) >= 2)
    out = []
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
            if pair:
                out += [[t, t + 72, n, 100] for n in pair]
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
    bass = staccato(mono([g[0] for g in groups(T[3])]), 0.6, 48, 150)
    # (PSG-noten onder C2 klinken in m4a allemaal als C2: MidiKeyToCgbFreq klemt key <= 35. Waar de bas onder C2
    # klinkt (Eb1-B1), speelt de sub de geschreven noot = een octaaf boven de grondtoon, op hetzelfde ritme.)
    sub = [[s_, e_, n - 12 if n - 12 >= 36 else n, 127] for s_, e_, n, v in bass]
    # orgel: zelfde register, kort en scherp (ongewijzigd sinds v5)
    organ = staccato(thin(T[6], 3, 'top'), 0.7, 20, 200)
    stab = stabs(guitar, arp)
    # waar een stoot valt en de brass een octaaf-chug speelt: alleen de bovenste noot van de chug (scheelt een kanaal)
    st = {e[0] for e in stab}
    hi = {}
    for e in brass:
        hi[e[0]] = max(hi.get(e[0], 0), e[2])
    brass = [e for e in brass if e[0] not in st or e[2] == hi[e[0]]]
    parts = {'drums': dr, 'bass': bass, 'brass': brass, 'organ': organ, 'brass_lo': brass_lo, 'steel': T[8],
             'arp': arp, 'stab': stab, 'dsine': T[7] + T[9]}
    parts = {k: dedupe(clip(v)) for k, v in parts.items()}
    parts['lead'] = dedupe(clip(lead))

    voicegroup()
    rel = releases('grounded_neo_plasma')
    # v8: de stemverdeler (en detach) rekent met de releases van v7, zodat élke noot (aanslag, lengte, toonhoogte)
    # exact v7 blijft; alleen de lead wordt daarna legato. ds_check() meet de bezetting met de echte v8-releases.
    rel = dict(rel)
    rel.update({BASS: 120, BRASS: 120, BRASS_LO: 110, LEAD: 140, STAB: 100, PLUCK: 150})
    progs = {'lead': LEAD, 'bass': BASS, 'brass': BRASS, 'organ': ORGAN, 'steel': PLUCK, 'brass_lo': BRASS_LO,
             'arp': PLUCK, 'stab': STAB, 'dsine': DSINE}
    tail = {k: release_ticks(rel[p], TPB, BPM) for k, p in progs.items()}
    tail.update(drums=0)
    for k in progs:                                 # staccato-partijen: release valt binnen de eigen 16e
        parts[k] = detach(parts[k], tail[k])
    order = ['drums', 'lead', 'bass', 'organ', 'brass', 'steel', 'dsine', 'stab', 'arp', 'brass_lo']
    res = allocate(parts, order, tail)
    assert len(res['lead']) == len(parts['lead']), 'lead verliest noten'
    real = releases('grounded_neo_plasma')
    res['lead'] = trim_legato(res, order, {k: 0 if k == 'drums' else release_ticks(real[progs[k]], TPB, BPM)
                                           for k in order})
    body = [[s_, e_, n - 12, 96] for s_, e_, n, v in res['lead'] if n - 12 >= 40]
    ds_check(res, progs, order)
    print('drumnoten buiten de kit (weg): %d, lage sawtooth-noten (basverdubbeling, weg): %d' % (drum_drop, saw_low))
    for k in order:
        n, kept = len(parts[k]), len(res[k])
        print('  %-9s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - kept, 100 * (n - kept) / max(n, 1)))
    p = res
    # arpeggio spoor B (PSG): alle arpeggio's/steel drums (ook wat in A wegviel), 1/24 tel later
    arpb = mono([[s_ + ARPB_DELAY, e_ + ARPB_DELAY, n, v] for s_, e_, n, v in parts['arp'] + parts['steel']])
    psg = {'body': dedupe(clip(body)), 'sub': dedupe(clip(sub)), 'arpb': dedupe(clip(arpb))}
    song = Song(TPB, 500000)
    tempo_map(song, END)
    song.loop = (LOOP0, END)
    tracks = [
        (p['lead'], LEAD, VOL['lead'], 0, 64),
        (psg['body'], BODY, VOL['body'], 1, 64),
        (p['brass'], BRASS, VOL['brass'], 2, 56),
        (p['brass_lo'], BRASS_LO, VOL['brass_lo'], 3, 64),
        (p['organ'], ORGAN, VOL['organ'], 4, 72),
        (p['bass'], BASS, VOL['bass'], 5, 64),
        (psg['sub'], SUB, VOL['sub'], 6, 64),
        (p['arp'], PLUCK, VOL['arp'], 7, 35),
        (p['steel'], PLUCK, VOL['steel'], 8, 35),
        (psg['arpb'], ARPB, VOL['arpb'], 10, 85),
        (p['stab'], STAB, VOL['stab'], 11, 60),
        (p['dsine'], DSINE, VOL['dsine'], 12, 64),
        (p['drums'], DRUMS, VOL['drums'], 9, None),
    ]
    written = 0
    for notes, prog, vol, ch, pan in tracks:
        assert notes, 'lege partij'
        song.add(notes, prog, vol, ch, pan)
        written += len(notes)
    assert written == sum(len(p[k]) for k in order) + sum(len(v) for v in psg.values()), 'niet elke partij staat in de MIDI'
    song.save(OUT, END)
    print('PSG: body %d, sub %d, arp B %d noten' % tuple(len(psg[k]) for k in ('body', 'sub', 'arpb')))
    print(OUT, '(%d sporen, intro %.1f s, loop %.1f s)' % (len(song.tracks), LOOP0 / TPB * 60 / 175.96,
                                                           (END - LOOP0) / TPB * 60 / 175.96))


if __name__ == '__main__':
    build()
