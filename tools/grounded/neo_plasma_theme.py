#!/usr/bin/env python3
"""Project Grounded: gevechtsmuziek van Neo Team Plasma (Battle Stadium): "Battle! Neo Team Plasma"
(Pokémon Black 2/White 2). Noten: MIDI van Byabbington (onlinesequencer, sound/songs/grounded_src/b2w2_neo_plasma.mid).
Klank, timing en balans: gemeten aan het origineel (BW2-mp3 van Jordi). Structuur zoals in de game: intro maat 0-9,
loop maat 10-73 (de MIDI speelt die loop twee keer).

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
TPB, BAR, BEAT, S16 = 384, 1536, 384, 96
BPM = 176
LOOP0, END = 10 * BAR, 74 * BAR
SAW_SHIFT = 17              # sawtooth vanaf maat 5: 17 ticks te vroeg in de bron

# programma's in voicegroup_grounded_neo_plasma
BASS, BRASS, BRASS_LO, ORGAN, LEAD, SINE, TRI, STEEL, DRUMS = 38, 62, 63, 17, 80, 82, 83, 114, 127
VOICES = {
    LEAD:     'voice_directsound 60, 0, DirectSoundWaveData_np_lead_warm, 255, 235, 200, 140',
    BASS:     'voice_directsound 60, 0, DirectSoundWaveData_np_pulse_bass, 255, 210, 140, 120',
    BRASS:    'voice_directsound 60, 0, DirectSoundWaveData_np_brass_full, 255, 215, 150, 120',
    BRASS_LO: 'voice_directsound 60, 0, DirectSoundWaveData_np_brass_full_lo, 255, 210, 150, 110',
    ORGAN:    'voice_directsound 60, 0, DirectSoundWaveData_np_organ_sharp, 255, 220, 160, 90',
    SINE:     'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 1',
    TRI:      'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_2, 0, 7, 15, 1',
    STEEL:    'voice_directsound 60, 0, DirectSoundWaveData_gm_steel_drums, 255, 0, 255, 150',
    DRUMS:    'voice_keysplit_all voicegroup_neo_plasma_drumset',
}
# drumkit (noot -> regel); standaard GBA-samples (rs_drumset e.d.)
KICK, SNARE_OFF, SNARE, OHAT, CRASH, SPLASH, CHAT = 36, 37, 38, 39, 40, 41, 42
KIT = [
    'voice_directsound 67, 0, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 0',
    'voice_directsound_no_resample 60, 0, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 180',
    'voice_directsound_no_resample 60, 0, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 220',
    'voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0',
    'voice_directsound_no_resample 60, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',
    'voice_directsound 67, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 200, 0, 140',
    'voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 255, 0',
]
# bron-drumnoot -> (kitnoot, lengte in ticks, velocity 0-127); 42/44 = dichte hihat
DRUM_MAP = {36: (KICK, 190, 96), 37: (SNARE_OFF, 160, 127), 38: (SNARE, 192, 120), 46: (OHAT, 192, 70),
            49: (CRASH, 384, 100), 57: (CRASH, 384, 100), 55: (SPLASH, 288, 90)}
HAT_LEN, HAT_VEL, HAT_ACC = 80, 96, 127     # dichte hihat: 77 ms = 82 ticks
NO_HATS = set(range(0, 10)) | set(range(34, 38)) | set(range(46, 50)) | {64, 65}   # intro en breaks: geen 16e-hihats

# spoorvolumes (CC7), afgesteld met solo-RMS en balance_orig.py tegen de mp3
VOL = dict(lead=127, brass=72, brass_lo=60, organ=62, bass=121, steel=26, arp=22, sine=16, tri=16, drums=80)


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Neo Team Plasma (BW2) v6. Gegenereerd door tools/grounded/neo_plasma_theme.py.'
    lines[1] = '@ 17 orgel, 38 pulse-bas, 62/63 synth brass, 80 warme pulse-lead, 114 steel drums, 127 drums.'
    lines[2] = 'voice_group grounded_neo_plasma'
    out = []
    for l in lines:
        k = l.rsplit('@', 1)[1].strip() if '@' in l and l.startswith('\tvoice') else None
        if k and k.isdigit() and int(k) in VOICES:
            l = '\t%s  @ %s' % (VOICES[int(k)], k)
        out.append(l)
    open(VG, 'w').write('\n'.join(out))
    open(DRUMSET, 'w').write(
        '@ Project Grounded: drumkit voor Battle! Neo Team Plasma v6 (neo_plasma_theme.py): standaard GBA-samples.\n'
        '@ 36 kick (+7 halve tonen), 37 off-beat-clap (909), 38 snare, 39 open hihat, 40 crash, 41 splash,\n'
        '@ 42 dichte hihat. Alles DirectSound.\n'
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
    out = dedupe(out)
    by = {}
    for e in out:
        by.setdefault(e[2], []).append(e)
    for lst in by.values():                         # een nieuwe slag op dezelfde drumnoot kapt de vorige af
        for a, b in zip(lst, lst[1:]):
            a[1] = min(a[1], b[0])
    # snelle hihats: 16en in de gevechtsdelen (niet op de plekken waar al een snare of hihat staat)
    taken = {e[0] for e in out if e[2] in (SNARE_OFF, SNARE, OHAT)} | {h[0] for h in hats}
    for b in range(10, 74):
        if b in NO_HATS:
            continue
        for i in range(16):
            t = b * BAR + i * S16
            if i % 4 == 0 or t in taken:
                continue
            hats.append([t, t + HAT_LEN, CHAT, HAT_ACC if i % 4 == 2 else HAT_VEL])
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

    # sawtooth: bovenstem = lead (DS, octaaf lager), octaaf eronder (lead2) = unisono met de lead: weg,
    # binnenstemmen >= C3 = arpeggio (steel drums);
    # lage noten (< C3) verdubbelen de bas: weg (de bas speelt ze al)
    lead, lead2, arp, saw_low = [], [], [], 0
    for g in groups(T[4]):
        top = g[-1]
        lead.append(list(top))
        for e in g[:-1]:
            if e[2] == top[2] - 12 and e[2] >= 48:
                lead2.append(list(e))
            elif e[2] >= 48:
                arp.append(list(e))
            else:
                saw_low += 1
    lead = octave_down(mono(quantize_runs(lead)))
    arp = mono(quantize_runs(thin(arp, 1, 'top')))
    # 'gitaar' = synth brass-stoten: akkoorden vanaf C3 (3 bovenste stemmen), daaronder de lage partij (1 stem)
    brass = thin([e for e in T[5] if e[2] >= 48], 3, 'top')
    brass_lo = mono([g[0] for g in groups([e for e in T[5] if e[2] < 48])])
    brass = staccato(brass, 0.85, 60, 9999)
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
    # bas: onderstem, staccato (klinkt een octaaf lager door de sample)
    bass = staccato(mono([g[0] for g in groups(T[3])]), 0.6, 48, 150)
    # orgel: zelfde register, kort en scherp
    organ = staccato(thin(T[6], 3, 'top'), 0.7, 20, 200)
    parts = {'drums': dr, 'bass': bass, 'brass': brass, 'organ': organ, 'brass_lo': brass_lo, 'steel': T[8],
             'arp': arp}
    parts = {k: dedupe(clip(v)) for k, v in parts.items()}
    parts['lead'] = dedupe(clip(lead))
    psg = {'sine': dedupe(clip(T[7])), 'tri': dedupe(clip(T[9]))}

    voicegroup()
    rel = releases('grounded_neo_plasma')
    progs = {'lead': LEAD, 'bass': BASS, 'brass': BRASS, 'organ': ORGAN, 'steel': STEEL, 'brass_lo': BRASS_LO,
             'arp': STEEL}
    tail = {k: release_ticks(rel[p], TPB, BPM) for k, p in progs.items()}
    tail.update(drums=0)
    for k in progs:                                 # staccato-partijen: release valt binnen de eigen 16e
        parts[k] = detach(parts[k], tail[k])
    order = ['drums', 'lead', 'bass', 'organ', 'brass', 'brass_lo', 'steel', 'arp']
    res = allocate(parts, order, tail)
    print('drumnoten buiten de kit (weg): %d, lage sawtooth-noten (basverdubbeling, weg): %d' % (drum_drop, saw_low))
    for k in order:
        n, kept = len(parts[k]), len(res[k])
        print('  %-9s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - kept, 100 * (n - kept) / max(n, 1)))
    p = res
    song = Song(TPB, 500000)
    tempo_map(song, END)
    song.loop = (LOOP0, END)
    tracks = [
        (p['lead'], LEAD, VOL['lead'], 0, 64),
        (p['brass'], BRASS, VOL['brass'], 2, 56),
        (p['brass_lo'], BRASS_LO, VOL['brass_lo'], 3, 64),
        (p['organ'], ORGAN, VOL['organ'], 4, 72),
        (p['bass'], BASS, VOL['bass'], 5, 64),
        (p['arp'], STEEL, VOL['arp'], 6, 80),
        (p['steel'], STEEL, VOL['steel'], 7, 48),
        (psg['sine'], SINE, VOL['sine'], 10, 64),
        (psg['tri'], TRI, VOL['tri'], 11, 64),
        (p['drums'], DRUMS, VOL['drums'], 9, None),
    ]
    written = 0
    for notes, prog, vol, ch, pan in tracks:
        assert notes, 'lege partij'
        song.add(notes, prog, vol, ch, pan)
        written += len(notes)
    assert written == sum(len(p[k]) for k in order) + sum(len(v) for v in psg.values()), 'niet elke partij staat in de MIDI'
    song.save(OUT, END)
    print(OUT, '(%d sporen, intro %.1f s, loop %.1f s)' % (len(song.tracks), LOOP0 / TPB * 60 / 175.96,
                                                           (END - LOOP0) / TPB * 60 / 175.96))


if __name__ == '__main__':
    build()
