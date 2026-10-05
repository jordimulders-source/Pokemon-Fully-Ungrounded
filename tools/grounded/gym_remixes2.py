#!/usr/bin/env python3
"""Project Grounded: vier remixes van het Emerald-gymleiderthema (mus_vs_gym_leader.mid) voor de gymleiders 5-8.

Jordi: 'Gymleiders allemaal een remix van het originele gym leader theme; echt duidelijk te herkennen, zelfde
melodie, andere instrumenten.' Dus: de sporen van het origineel worden 1-op-1 gekopieerd (noten, vibrato, CC7-dips,
panning, programmawissels, loop maat 10-62), alleen de instrumenten wisselen per genre; de ritmesectie (drums,
bas-ritme) en lagen erbovenop zijn nieuw, maar volgen de originele bas (grondtonen/kwinten), de snare-posities
(tel 2 en 4) en het pauken-ritme (1, 2-en, 4-en) van het origineel.

  651 MUS_GROUNDED_VS_NORMAN     blockbuster-tv-orkest (188 bpm): cello-melodie, strijkersostinato, taiko/concert-
                                 basdrum, koper-'braam' op de sectiebegins, koor in de opbouw
  652 MUS_GROUNDED_VS_WINONA     bubblegum-dancepop (168 bpm): glanzende synthleads, four-on-the-floor, claps,
                                 offbeat-hihats, synthbrass-stoten op het pauken-ritme, huppelende synthbas
  653 MUS_GROUNDED_VS_TATE_LIZA  psytrance (144 bpm): rollende 16e-bas tussen de kicks, tweestemmige leads (Tate links:
                                 acid-zaagtand, Liza rechts: holle blokgolf), acid-lijnen in de rustige delen, zaps
  654 MUS_GROUNDED_VS_WALLACE    Franse lounge/bossa (156 bpm): vibrafoon + accordeon (musette), bugel, Rhodes-
                                 akkoorden in bossa-ritme, contrabas, brushes/cross-stick, fluit, nylon

Eén voicegroup voor alle vier: voicegroup_grounded_gym2 = voicegroup_vs_gym_leader (het origineel) + de extra
instrumenten op 92-122 + vier drumkits (123-126, sound/voicegroups/drumsets/gym2_*.inc).
Samples: tools/grounded/gym2_samples.py (voorvoegsel gym2_). Stemverdeler: max. 10 DirectSound-noten, melodie eerst.
Gebruik: python3 tools/grounded/gym_remixes2.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import releases, release_ticks, dedupe, MAX_VOICES
from music_lint import load_voices

SRC = 'sound/songs/midi/mus_vs_gym_leader.mid'
VG = 'grounded_gym2'
TPB, BAR, LOOP, END = 24, 96, 10, 62
NOTE_NAMES = 'C C# D Eb E F F# G Ab A Bb B'.split()

# ---- extra instrumenten (programma: regel) -------------------------------------------------------------------
P = dict(CELLO=92, OSTINATO=93, BRAAM=94, CHOIR=95, HARP=96, POPLEAD=97, SQUARE=98, POPBRASS=99, POPPLUCK=100,
         POPSTAB=101, POPSTAB5=102, SYNTHBASS=103, GLOCK=104, LEAD_A=105, LEAD_B=106, PSYBASS=107, ACID=108,
         VIBES=109, RHODES=110, RH_DOM=111, RH_MAJ=112, RH_MIN=113, RH_SUS=114, UPRIGHT=115, FLUGEL=116,
         ACCORDION=117, FLUTE=118, NYLON=119, NOISE_HAT=120, NOISE_RISE=121, PIZZ=122, PIANO_HI=88, STR_SHORT=89, PIANO_MID=87,
         KIT_NORMAN=123, KIT_WINONA=124, KIT_TATE=125, KIT_WALLACE=126)
STRINGS, TRUMPET, HORN, PIANO, TIMPANI = 48, 56, 60, 1, 47
ds = lambda s, rel, key=60, adsr='255, 0, 255': 'voice_directsound %d, 0, DirectSoundWaveData_%s, %s, %d' % (key, s, adsr, rel)
EXTRA = {
    'CELLO': ds('gym2_cello', 170), 'OSTINATO': ds('gym2_ostinato', 120), 'BRAAM': ds('gym2_braam', 200),
    'CHOIR': ds('classical_choir_voice_ahhs', 165), 'HARP': ds('sc88pro_harp', 200, adsr='255, 242, 51'),
    'POPLEAD': ds('gym2_pop_lead', 150), 'SQUARE': ds('sc88pro_square_wave', 140), 'POPBRASS': ds('gym2_pop_brass', 150),
    'POPPLUCK': ds('gym2_pop_pluck', 150), 'POPSTAB': ds('gym2_pop_stab', 140), 'POPSTAB5': ds('gym2_pop_stab5', 140),
    'SYNTHBASS': ds('sc88pro_synth_bass', 115, adsr='255, 252, 0'), 'GLOCK': ds('sc88pro_glockenspiel', 190, adsr='255, 165, 51'),
    'LEAD_A': ds('gym2_psy_lead_a', 150), 'LEAD_B': ds('gym2_psy_lead_b', 150), 'PSYBASS': ds('gym2_psy_bass', 60),
    'ACID': ds('gym2_psy_acid', 80), 'VIBES': ds('gym2_vibes', 190), 'RHODES': ds('gym2_rhodes', 180),
    'RH_DOM': ds('gym2_rh_dom', 165), 'RH_MAJ': ds('gym2_rh_maj', 165), 'RH_MIN': ds('gym2_rh_min', 165),
    'RH_SUS': ds('gym2_rh_sus', 165), 'UPRIGHT': ds('gym2_upright', 130), 'FLUGEL': ds('gym2_flugel', 140),
    'ACCORDION': ds('sc88pro_accordion', 150), 'FLUTE': ds('sc88pro_flute', 150),
    'NYLON': ds('sc88pro_nylon_str_guitar', 76, adsr='255, 249, 25'),
    'NOISE_HAT': 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0', 'NOISE_RISE': 'voice_noise 60, 0, 0, 7, 0, 15, 2',
    'PIZZ': ds('sc88pro_pizzicato_strings', 165, adsr='255, 216, 0'),
    # intro (maat 0-1): pianotriller en strijkersloopjes in 16en; met de lange release van de keysplits (239/196)
    # klonken er in het origineel tot 17 noten tegelijk -> eigen korte versies
    'PIANO_HI': ds('sc88pro_piano1_84', 150, adsr='255, 250, 0'), 'STR_SHORT': ds('sc88pro_string_ensemble_72', 140),
    'PIANO_MID': ds('sc88pro_piano1_60', 200, adsr='255, 250, 0'),     # piano-melodie (maat 22-25, 34-36): release 239 -> 200
}
nr = lambda s, rel, adsr='255, 0, 255': 'voice_directsound_no_resample 60, 0, DirectSoundWaveData_%s, %s, %d' % (s, adsr, rel)
# drumkits: noot -> regel (vanaf 36; gaten worden met de eerste regel gevuld, die noten gebruiken we niet)
KITS = {
    # ronde 2 (v2): de drie kits hieronder horen bij grounded_gym2_<leider> (programma 127); grounded_gym2 (Wallace)
    # verwijst er ook nog naar op 123-125, maar Wallace speelt ze niet.
    'norman': ('TV-orkest/big band (v2): 36 kick, 38 orkestsnare, 41/45 toms, 42 dichte hihat, 49 orkestcrash, 51 ride',
               {36: nr('sc88pro_rnd_kick', 100), 38: nr('sc88pro_orchestra_snare', 200),
                41: 'voice_directsound 64, 0, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 200',
                42: nr('unknown_close_hihat', 150, '255, 127, 0'),
                45: 'voice_directsound 72, 0, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 200',
                49: ds('sc88pro_orchestra_cymbal_crash', 216, adsr='255, 246, 0'),
                51: nr('dance_drums_ride_bell', 180, '255, 165, 103')}),
    'winona': ('girly pop (v2): 36 Emerald-dance-kick, 38 synthsnare, 39 909-clap, 42 dichte hihat, 46 open hihat, 49 crash, 54 tamboerijn',
               {36: nr('drum_and_percussion_kick', 120), 38: nr('unknown_synth_snare', 120), 39: nr('sc88pro_tr909_hand_clap', 127, '255, 255, 255'),
                42: nr('unknown_close_hihat', 150, '255, 127, 0'), 46: nr('unknown_open_hihat', 60, '255, 242, 141'),
                49: nr('trinity_cymbal_crash', 165, '255, 235, 0'), 54: nr('sc88pro_tambourine', 150, '255, 127, 77')}),
    'tate': ('psytrance (v2): 36 Emerald-dance-kick (kort), 38 snare (rolls), 39 909-clap, 42 dichte hihat, 46 open hihat, 49 crash, 50 zap',
             {36: nr('drum_and_percussion_kick', 110), 38: nr('unknown_synth_snare', 100), 39: nr('sc88pro_tr909_hand_clap', 127, '255, 255, 255'),
              42: nr('unknown_close_hihat', 150, '255, 127, 0'), 46: nr('unknown_open_hihat', 40, '255, 242, 141'),
              49: nr('trinity_cymbal_crash', 165, '255, 235, 0'), 50: nr('gym2_psy_zap', 60)}),
    'wallace': ('lounge/bossa: 36 zachte kick, 37 cross-stick, 38 brush-tik, 40 brush-swirl, 49 ride (als crash), 51 ride',
                {36: nr('gym2_soft_kick', 100), 37: nr('gym2_side_stick', 90), 38: nr('gym2_brush_tap', 120),
                 40: nr('gym2_brush_swirl', 150), 49: nr('gym2_ride', 200), 51: nr('gym2_ride', 160)}),
}
KICK, SNARE, CLAP, CHAT, OHAT, CRASH, TAMB, LOTOM, TAIKO, ZAP = 36, 38, 39, 42, 46, 49, 54, 41, 43, 50
XSTICK, BRUSH, SWIRL, RIDE = 37, 38, 40, 51


def write_voicegroup():
    src = [l.strip() for l in open('sound/voicegroups/vs_gym_leader.inc') if l.strip().startswith('voice_')
           and not l.strip().startswith('voice_group')]
    assert len(src) == 91, len(src)
    src.append(src[80])                                               # 91: opvulling
    src[TIMPANI] = ds('sc88pro_timpani', 190, adsr='255, 246, 0')      # 226 klonk ±1 s na (3 kanalen per maat)
    lines = ['@ Project Grounded: voicegroup_vs_gym_leader + instrumenten voor de gymleider-remixes 651-654.',
             '@ Gegenereerd door tools/grounded/gym_remixes2.py (samples: gym2_samples.py). Pauken (47) korter.',
             'voice_group %s' % VG]
    lines += ['\t%s  @ %d' % (l, i) for i, l in enumerate(src)]
    names = {v: k for k, v in P.items()}
    for p in [87, 88, 89] + list(range(92, 127)):
        k = names[p]
        if k.startswith('KIT_'):
            line = 'voice_keysplit_all voicegroup_gym2_%s_drumset' % k[4:].lower()
        else:
            line = EXTRA[k]
        if p < 92:
            lines[3 + p] = '\t%s  @ %d' % (line, p)
        else:
            lines.append('\t%s  @ %d' % (line, p))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(lines) + '\n')
    for kit, (doc, voices) in KITS.items():
        out = ['@ Project Grounded: drumkit voor %s (gym_remixes2.py).' % doc, 'voice_group gym2_%s_drumset, 36' % kit]
        for n in range(36, max(voices) + 1):
            out.append('\t' + voices.get(n, voices[36]))
        open('sound/voicegroups/drumsets/gym2_%s.inc' % kit, 'w').write('\n'.join(out) + '\n')
    inc = open('sound/voice_groups.inc').read()
    for kit in KITS:
        line = '.include "sound/voicegroups/drumsets/gym2_%s.inc"' % kit
        if line not in inc:
            anchor = '.include "sound/voicegroups/drumsets/victini.inc"'
            inc = inc.replace(anchor, anchor + '\n' + line) if anchor in inc else line + '\n' + inc
    line = '.include "sound/voicegroups/%s.inc"' % VG
    if line not in inc:
        inc = inc.rstrip('\n') + '\n' + line + '\n'
    open('sound/voice_groups.inc', 'w').write(inc)


# ---- het origineel ---------------------------------------------------------------------------------------------
def load_source():
    m = mido.MidiFile(SRC)
    assert m.ticks_per_beat == TPB
    tracks = {}
    for i in range(1, 9):
        tick, prog, on, notes, other = 0, None, {}, [], []
        ch = next(x.channel for x in m.tracks[i] if hasattr(x, 'channel'))
        for x in m.tracks[i]:
            tick += x.time
            if x.type == 'program_change':
                prog = x.program
            if x.type == 'note_on' and x.velocity:
                on.setdefault(x.note, []).append((tick, x.velocity, prog))
            elif x.type in ('note_on', 'note_off'):
                if on.get(x.note):
                    s, v, p = on[x.note].pop(0)
                    notes.append([s, tick, x.note, v, p])
            elif not x.is_meta:
                other.append((tick, x))
        seen, uniq = set(), []
        for n in sorted(notes):
            if (n[0], n[2]) not in seen:
                seen.add((n[0], n[2]))
                uniq.append(n)
        tracks[i] = (uniq, other, ch)
    return tracks


SRC_T = load_source()
BASS = SRC_T[3][0]
SNARE_POS = [n[0] for n in SRC_T[7][0]]
TIMP = SRC_T[8][0]


def bass_at(tick):
    """Originele basnoot die op `tick` begint (of klinkt)."""
    last = None
    for s, e, n, v, p in BASS:
        if s <= tick < e:
            return n
        if s <= tick:
            last = n
    return last                       # in een rust (maat 25): de laatst gespeelde basnoot


def root_pc(bar, half):
    if bar < 10:
        return 0
    t0 = bar * BAR + half * 48
    return min(n for s, e, n, v, p in BASS if t0 <= s < t0 + 48) % 12   # laagste basnoot (maat 13: G2-C2-D2-C2 = C)


def ctype(bar, half):
    """Akkoordtype per halve maat, afgelezen uit het origineel (bas + alle melodiestemmen; zie het rapport):
    A-deel: C-mixolydisch (C13 / Bb/C = C9sus) en Bb-lydisch (Bbmaj13, #11 in de melodie); B-deel C-Db-Eb.
    Gecontroleerd: geen kleine secunde tussen een akkoordtoon en een melodietoon van >= een achtste (behalve maat 59)."""
    if bar < 10:
        return '5'
    if bar < 34:
        r = (bar - 10) % 12
        if r in (4, 5, 8, 9):
            return 'maj'
        if r == 0:
            return 'sus' if (bar, half) == (10, 1) else 'dom'     # maat 10: Bb/F boven C; maat 22: E-D-C
        if r == 1:
            return 'sus'
        return 'dom'
    if bar <= 36:
        return 'dom' if bar == 35 else 'sus'
    if bar <= 47:
        return 'min' if root_pc(bar, half) == 0 else 'maj'
    if bar <= 52:
        return 'sus'
    if bar == 53:
        return 'maj'
    if bar <= 55:
        return 'sus'
    if bar <= 57:
        return 'dom'
    if bar <= 59:
        return 'min'
    return 'dom'


def chord_note(bar, half, center=60):
    """Toets waarop een akkoordsample (gelabeld op C) de grondtoon van deze halve maat speelt: -6..+5 rond C."""
    return center + ((root_pc(bar, half) + 6) % 12) - 6


def bars(a, b):
    return range(a, b + 1)


# ---- bouwstenen ----------------------------------------------------------------------------------------------
class Part:
    """Een partij: noten [start, eind, toets, velocity, programma] + overige events; `track` = uitvoerspoor."""
    def __init__(self, name, track, notes=(), drums=False):
        self.name, self.track, self.notes, self.drums = name, track, [list(n) for n in notes], drums


class Track:
    def __init__(self, ch, prog=None, vol=None, pan=None, other=()):
        self.ch, self.prog, self.vol, self.pan, self.other = ch, prog, vol, pan, list(other)
        self.notes = []


def copy_track(i, progmap, vol=1.0, pan=None):
    """Spoor i van het origineel: noten en events gelijk, programma's via progmap(prog, tick), CC7 x vol."""
    notes, other, ch = SRC_T[i]
    out = []
    for t, x in other:
        if x.type == 'program_change':
            x = x.copy(program=progmap(x.program, t))
        elif x.type == 'control_change' and x.control == 7:
            x = x.copy(value=max(1, min(127, round(x.value * vol))))
        elif x.type == 'control_change' and x.control == 10 and pan is not None:
            x = x.copy(value=max(0, min(127, pan + (x.value - 64) // 3)))
        out.append((t, x))
    tr = Track(ch, other=out)
    return tr, [[s, e, n, v, progmap(p, s)] for s, e, n, v, p in notes]


def hit(out, t, note, vel, length, prog):
    out.append([int(t), int(t + length), note, max(1, min(127, int(vel))), prog])


def snare_roll(out, b0, b1, prog, note, v0=50, v1=118, step=6, start=0):
    """16e-roffel van maat b0 (tel `start`) t/m b1 met crescendo."""
    t0, t1 = b0 * BAR + start, (b1 + 1) * BAR
    n = (t1 - t0) // step
    for k in range(n):
        hit(out, t0 + k * step, note, v0 + (v1 - v0) * k / max(1, n - 1), step, prog)


def crash_at(out, barlist, prog, vel=110):
    for b in barlist:
        hit(out, b * BAR, CRASH, vel, 48, prog)


def timp_positions(bar):
    return [s - bar * BAR for s, e, n, v, p in TIMP if bar * BAR <= s < (bar + 1) * BAR]


# ---- per leider ----------------------------------------------------------------------------------------------
A1, A2, B1, B2, BRK, BUILD = bars(10, 21), bars(22, 33), bars(34, 36), bars(37, 48), bars(49, 53), bars(54, 61)


# ---- ronde 2 (v2): Norman, Winona, Tate & Liza, elk met een eigen voicegroup -------------------------------------
# Wallace (goedgekeurd) houdt voicegroup_grounded_gym2 en zijn kit byte-identiek; de andere drie krijgen
# grounded_gym2_<leider>: dezelfde basis (0-91: het origineel + korte intro-varianten op 87-89 + kortere pauken)
# en hun eigen instrumenten op 92-126, drumkit op 127.
PIANO_MID_, PIANO_HI_, STR_SHORT_ = P['PIANO_MID'], P['PIANO_HI'], P['STR_SHORT']
HITOM = 45


def base_lines():
    src = [l.strip() for l in open('sound/voicegroups/vs_gym_leader.inc') if l.strip().startswith('voice_')
           and not l.strip().startswith('voice_group')]
    src.append(src[80])
    src[TIMPANI] = ds('sc88pro_timpani', 190, adsr='255, 246, 0')
    src[87], src[88], src[89] = EXTRA['PIANO_MID'], EXTRA['PIANO_HI'], EXTRA['STR_SHORT']
    return src


FILL = 'voice_square_1 60, 0, 0, 2, 0, 0, 15, 0'
PSG_LEAD = 'voice_square_1 60, 0, 0, 2, 0, 1, 11, 2'      # blokgolf 50% (25% was 'schel' bij Neo Plasma v5)
NOISE_HAT_L = 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0'
NOISE_RISE_L = 'voice_noise 60, 0, 0, 7, 0, 15, 2'
TYPES = ('dom', 'maj', 'min', 'sus', '5')
NORMAN = dict(BASS_F=92, BASS_FL=93, **{'NB_' + t: 94 + i for i, t in enumerate(TYPES)},
              **{'NP_' + t: 99 + i for i, t in enumerate(TYPES)}, KIT=127)
WINONA = dict(LEAD_SQ=92, CELESTA=93, **{'PAD_' + t: 94 + i for i, t in enumerate(TYPES)}, SYNTHBASS=99,
              POPPLUCK=100, TUBBELL=101, NOISE_HAT=102, KIT=127)
TATE = dict(LEAD_A=92, LEAD_B=93, PSYBASS=94, ACID=95, POPPLUCK=96, NOISE_HAT=97, NOISE_RISE=98, DRONE=99, KIT=127)
LEADER_VG = {
    'norman': ('grounded_gym2_norman', {
        92: ds('sc88pro_fingered_bass', 140, adsr='255, 253, 0'),     # walking bass (Emerald finger bass)
        93: ds('sc88pro_fretless_bass', 150, adsr='255, 253, 0'),     # B-deel en break: fretless
        **{94 + i: ds('gym2_nb_' + t, 110) for i, t in enumerate(TYPES)},   # brass-section-stoten (trompet + hoorn)
        **{99 + i: ds('gym2_np_' + t, 90) for i, t in enumerate(TYPES)},    # pizzicato-akkoorden
        127: 'voice_keysplit_all voicegroup_gym2_norman_drumset'}),
    'winona': ('grounded_gym2_winona', {
        92: PSG_LEAD, 93: ds('gym2_celesta', 175),
        **{94 + i: ds('gym2_wpad_' + t, 140) for i, t in enumerate(TYPES)},
        99: ds('sc88pro_synth_bass', 100, adsr='255, 252, 0'), 100: ds('gym2_pop_pluck', 150),
        101: ds('sc88pro_tubular_bell', 190, adsr='255, 165, 90'), 102: NOISE_HAT_L,
        127: 'voice_keysplit_all voicegroup_gym2_winona_drumset'}),
    'tate_liza': ('grounded_gym2_tate', {
        92: ds('gym2_psy_lead_a', 110), 93: ds('gym2_psy_lead_b', 110),
        94: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_gym2_saw, 0, 0, 15, 0',   # psy-bas (PSG-golf)
        95: ds('gym2_psy_acid', 80), 96: ds('gym2_pop_pluck', 150), 97: NOISE_HAT_L, 98: NOISE_RISE_L,
        99: ds('gym2_psy_lead_b', 150),
        127: 'voice_keysplit_all voicegroup_gym2_tate_drumset'}),
}


def write_leader_voicegroups():
    inc = open('sound/voice_groups.inc').read()
    for leader, (vg, extra) in LEADER_VG.items():
        lines = base_lines() + [FILL] * (128 - 92)
        for p, l in extra.items():
            lines[p] = l
        out = ['@ Project Grounded: gymleider-remix v2 (%s): voicegroup_vs_gym_leader + eigen instrumenten op 92-127.' % leader,
               '@ Gegenereerd door tools/grounded/gym_remixes2.py (samples: gym2_samples.py).', 'voice_group %s' % vg]
        out += ['\t%s  @ %d' % (l, i) for i, l in enumerate(lines)]
        open('sound/voicegroups/%s.inc' % vg, 'w').write('\n'.join(out) + '\n')
        line = '.include "sound/voicegroups/%s.inc"' % vg
        if line not in inc:
            anchor = '.include "sound/voicegroups/%s.inc"' % VG
            inc = inc.replace(anchor, anchor + '\n' + line)
    open('sound/voice_groups.inc', 'w').write(inc)


def section(b):
    for name, rng in (('A1', A1), ('A2', A2), ('B1', B1), ('B2', B2), ('BRK', BRK), ('BUILD', BUILD)):
        if b in rng:
            return name
    return 'INTRO'


WALK = {'dom': [0, 7, 9, 10], 'sus': [0, 5, 7, 10], 'min': [0, 3, 7, 10], 'maj': [0, 4, 7, 9], '5': [0, 7, 10, 12]}


def place(pc, near, lo=33, hi=47):
    """Toets met toonklasse pc tussen lo en hi, zo dicht mogelijk bij `near`."""
    return min((n for n in range(lo, hi + 1) if n % 12 == pc), key=lambda n: (abs(n - near), n))


def walking_bass(barlist, prog_of, vel_of):
    """Dynamische walking bass in kwarten: 1 = grondtoon, 2-3 = akkoordtonen (kwint, octaafsprong, septiem/sext),
    4 = chromatische nadering (halve toon boven/onder) van de grondtoon van de volgende maat; elke 4e maat een
    achtste-'skip' op tel 4 en naar elke nieuwe sectie een chromatische loop omhoog in achtsten."""
    out, prev = [], 36
    for b in barlist:
        typ = ctype(b, 0)
        tones = WALK[typ]
        r0 = place(root_pc(b, 0), prev)
        nb = b + 1 if b + 1 < END else LOOP
        nroot = place(root_pc(nb, 0), r0)
        appr = nroot + (1 if b % 2 else -1)
        if appr > 47:
            appr -= 2
        v = b % 4
        up = r0 + 12 if r0 + 12 <= 50 else r0 - 5
        if v == 0:
            line = [r0, r0 + 7, r0 + tones[2], appr]
        elif v == 1:
            line = [r0, up, r0 + 7, appr]
        elif v == 2:
            line = [r0, r0 + tones[1], r0 + tones[3], appr]
        else:
            line = [r0, r0 + 7, up, None]
        if root_pc(b, 1) != root_pc(b, 0):
            line[2] = place(root_pc(b, 1), r0)
        base = vel_of(b)
        acc = [0, -16, -6, -10]
        prog = prog_of(b)
        mine = []
        for k, n in enumerate(line):
            if n is not None:
                hit(mine, b * BAR + 24 * k, n, base + acc[k], 22, prog)
        if line[3] is None:                                   # 'skip': twee achtsten op tel 4
            hit(mine, b * BAR + 72, r0 + tones[3] if r0 + tones[3] <= 50 else r0 + tones[1], base - 14, 10, prog)
            hit(mine, b * BAR + 84, appr, base - 4, 10, prog)
        if b in (21, 33, 36, 48, 61):                         # chromatische loop omhoog naar de nieuwe sectie
            mine = [n for n in mine if n[0] < b * BAR + 48]
            for k in range(4):
                hit(mine, b * BAR + 48 + 12 * k, nroot - 4 + k, base - 8 + 4 * k, 10, prog)
        out += mine
        prev = r0
    return out


def norman():
    """TV-orkest (Jordi ronde 2): walking bass op de Emerald finger/fretless bass, ride (Emerald ride bell) en
    hihat-voet op 2 en 4, gelaagde brass-section-stoten (Emerald trompet + hoorn als één sample per akkoord) op het
    pauken-ritme met snare/kick die ze 'vangen' (big band), pizzicato-akkoorden (Emerald pizzicato) als staccato
    opvulling op de achtste-en. De melodie staat weer op de originele instrumenten (hoorn, strijkers, trompet,
    piano); de PSG-tegenmelodieën worden strijkers, de originele pauken blijven."""
    N = NORMAN
    K = N['KIT']
    tr, parts = {}, []
    t1, n1 = copy_track(1, lambda p, t: PIANO_MID_ if p == PIANO else (STR_SHORT_ if p == STRINGS and t < 2 * BAR else p), 1.0)
    t2, n2 = copy_track(2, lambda p, t: (PIANO_HI_ if t < 2 * BAR else PIANO_MID_) if p == PIANO else p, 0.92)
    t4, n4 = copy_track(4, lambda p, t: STRINGS if p in (80, 84) else p, 0.60)
    t5, n5 = copy_track(5, lambda p, t: STRINGS if p == 80 else p, 0.60)
    t6, n6 = copy_track(6, lambda p, t: p, 0.70)
    t8, n8 = copy_track(8, lambda p, t: p, 0.78)
    for k, (t, n) in {'mel2': (t2, n2), 'mel1': (t1, n1), 'cnt4': (t4, n4), 'cnt5': (t5, n5), 'wave': (t6, n6),
                      'timp': (t8, n8)}.items():
        tr[k] = t
        parts.append(Part(k, k, n))
    # --- bas: intro en break = de originele baslijn, de rest walking
    sec_vel = {'A1': 106, 'A2': 118, 'B1': 112, 'B2': 104, 'BUILD': 122, 'BRK': 100, 'INTRO': 110}
    bass = []
    for s, e, n, v, p in BASS:
        b = s // BAR
        if b < 10 or b in bars(49, 53):
            hit(bass, s, n, 112 if s % 24 == 0 else 96, min(e - s, 10), N['BASS_FL'] if b >= 49 else N['BASS_F'])
    walk_bars = list(bars(10, 48)) + list(bars(54, END - 1))
    bass += walking_bass(walk_bars, lambda b: N['BASS_FL'] if b in B2 else N['BASS_F'], lambda b: sec_vel[section(b)])
    tr['bass'] = Track(2, N['BASS_F'], 118, 64)
    parts.append(Part('bass', 'bass', bass))
    # --- brass-stoten en pizzicato
    brass, pizz = [], []
    big = (10, 22, 26, 30, 34, 37, 41, 45, 54, 58)
    for b in bars(10, END - 1):
        sec = section(b)
        for pos in timp_positions(b):
            half = 0 if pos < 48 else 1
            prog, note = N['NB_' + ctype(b, half)], chord_note(b, half)
            if (b, pos) == (59, 84):
                continue                              # melodie E4 tegen de F van Bb-mineur (zie ctype)
            if pos == 0 and b in big:
                hit(brass, b * BAR, note, 124, 30, prog)
            elif sec in ('A2', 'B1', 'BUILD') and pos:
                hit(brass, b * BAR + pos, note, 110 if pos != 84 else 116, 8, prog)
            elif sec == 'A1' and pos == 84 and b % 2:
                hit(brass, b * BAR + pos, note, 100, 8, prog)
        if b == 53:
            for k, pos in enumerate((0, 24, 48, 72)):
                hit(brass, b * BAR + pos, chord_note(b, pos // 48), 96 + 9 * k, 8, N['NB_' + ctype(b, pos // 48)])
        if sec == 'BRK':
            if b <= 52:
                for k, pos in enumerate((0, 24, 48, 72)):
                    hit(pizz, b * BAR + pos, chord_note(b, pos // 48), 72 + 6 * (b - 49) + 2 * k, 8,
                        N['NP_' + ctype(b, pos // 48)])
            continue
        offs = (12, 36, 60, 84) if sec == 'B2' else (12, 60)
        for pos in offs:
            half = 0 if pos < 48 else 1
            hit(pizz, b * BAR + pos, chord_note(b, half), 96 if sec != 'A1' else 88, 8, N['NP_' + ctype(b, half)])
    tr['brass'] = Track(10, N['NB_dom'], 104, 64)
    tr['pizz'] = Track(11, N['NP_dom'], 92, 72)
    parts.append(Part('brass', 'brass', brass))
    parts.append(Part('pizz', 'pizz', pizz))
    # --- drums
    kick, snare, ride, hat, crash, perc = [], [], [], [], [], []
    swing = [(0, 100), (24, 80), (36, 64), (48, 96), (72, 80), (84, 64)]
    for b in bars(2, END - 1):
        sec = section(b)
        loud = sec in ('A2', 'BUILD')
        if b < 10:
            for k in range(8):
                hit(hat, b * BAR + 12 * k, CHAT, 74 if k % 2 == 0 else 52, 6, K)
        elif sec == 'BRK':
            if b <= 52:
                for k in range(4):
                    hit(hat, b * BAR + 24 * k, CHAT, 60 + 6 * (b - 49), 6, K)
        else:
            for pos, v in swing:
                hit(ride, b * BAR + pos, RIDE, v + (8 if loud else 0) - (10 if sec == 'B2' else 0), 12, K)
            for pos in (24, 72):
                hit(hat, b * BAR + pos, CHAT, 66, 6, K)
            hit(kick, b * BAR, KICK, 96 if not loud else 108, 12, K)
        for s in (b * BAR + 24, b * BAR + 72):
            if s in SNARE_POS and (sec != 'BRK' or b >= 52):
                hit(snare, s, SNARE, 92 if loud else 78, 12, K)
    for s, e, n, v, p in brass:                       # de drummer 'vangt' de stoten (snare + kick, big band)
        if s % BAR:
            hit(snare, s, SNARE, min(127, v - 4), 12, K)
            hit(kick, s, KICK, 112, 12, K)
        else:
            hit(kick, s, KICK, 124, 12, K)
    crash_at(crash, (2,) + big, K, 112)
    snare_roll(snare, 9, 9, K, SNARE, 50, 110, start=48)
    snare_roll(snare, 33, 33, K, SNARE, 60, 118, start=48)
    snare_roll(snare, 53, 53, K, SNARE, 40, 120)
    snare_roll(snare, 61, 61, K, SNARE, 60, 122, start=48)
    for b in (21, 36, 48):
        for k, pos in enumerate((48, 60, 72, 84)):
            hit(perc, b * BAR + pos, (HITOM, HITOM, LOTOM, LOTOM)[k], 92 + 8 * k, 12, K)
    tr['drums'] = Track(9, K, 116, 64)
    for k, notes in (('kick', kick), ('snare', snare), ('ride', ride), ('hat', hat), ('crash', crash), ('perc', perc)):
        parts.append(Part(k, 'drums', notes, drums=True))
    order = ['mel2', 'mel1', 'bass', 'kick', 'snare', 'brass', 'cnt4', 'ride', 'crash', 'pizz', 'cnt5', 'timp',
             'hat', 'perc']
    return dict(bpm=188, tracks=tr, parts=parts, order=order, vg=LEADER_VG['norman'][0])


def winona():
    """Girly pop (Jordi ronde 2): géén koper meer. Bovenstem (spoor 2) = PSG-blokgolf (50%), onderstem (spoor 1) =
    celesta, de PSG-tegenmelodieën op blokgolf 1 (die de lead nu gebruikt) -> synthpluk; polysynth-pad-akkoorden
    (één sample per voicing) als 2-tels-pad in de rustige delen en als off-beat-stoten (pomp) in A2/opbouw,
    buisklokken op de sectiebegins. Strakke synthbas (Emerald) op de originele achtsten, Emerald-dance-kick op
    elke tel, 909-clap op 2 en 4, open hihat op de en, tamboerijn, PSG-ruis-16en."""
    W = WINONA
    K = W['KIT']
    tr, parts = {}, []
    t1, n1 = copy_track(1, lambda p, t: PIANO_MID_ if p == PIANO else W['CELESTA'], 0.84, pan=44)
    t2, n2 = copy_track(2, lambda p, t: W['LEAD_SQ'], 0.74)
    sq1 = (5, 7, 82, 83, 85, 86)                      # blokgolf 1 = de lead; die tegenstemmen worden synthpluk
    t4, n4 = copy_track(4, lambda p, t: W['POPPLUCK'] if p in sq1 else p, 0.78)
    t5, n5 = copy_track(5, lambda p, t: W['POPPLUCK'] if p in sq1 else p, 0.78)
    t6, n6 = copy_track(6, lambda p, t: p, 0.80)
    for k, (t, n) in {'mel2': (t2, n2), 'mel1': (t1, n1), 'cnt4': (t4, n4), 'cnt5': (t5, n5), 'wave': (t6, n6)}.items():
        tr[k] = t
        parts.append(Part(k, k, n))
    bass = []
    for s, e, n, v, p in BASS:
        hit(bass, s, n, 122 if (s % 24) == 0 else 104, min(e - s, 8), W['SYNTHBASS'])
    tr['bass'] = Track(2, W['SYNTHBASS'], 112, 64)
    parts.append(Part('bass', 'bass', bass))
    kick, clap, hat, crash, perc = [], [], [], [], []
    for b in bars(0, END - 1):
        four = 2 <= b and b not in BRK
        for beat in range(4):
            t = b * BAR + beat * 24
            if four:
                hit(kick, t, KICK, 124 if beat in (0, 2) else 116, 12, K)
            if (b >= 10 and b not in BRK) or b in bars(6, 9):
                hit(hat, t + 12, OHAT, 92 if b >= 10 else 70, 12, K)
            if b in BRK and b <= 51:
                hit(clap, t, CLAP, 70 + 10 * (b - 49), 12, K)
        for s in (b * BAR + 24, b * BAR + 72):
            if s in SNARE_POS and b not in BRK:
                hit(clap, s, CLAP, 120, 12, K)
        if b in A2 or b in BUILD:
            for s in (b * BAR + 24, b * BAR + 72):
                hit(perc, s + 6, TAMB, 64, 6, K)
    snare_roll(clap, 52, 52, K, SNARE, 60, 100, step=12)
    snare_roll(clap, 53, 53, K, SNARE, 70, 122)
    snare_roll(clap, 1, 1, K, CLAP, 50, 110, step=12)
    snare_roll(clap, 61, 61, K, SNARE, 70, 120, start=48)
    crash_at(crash, (2, 10, 14, 18, 22, 26, 30, 34, 37, 41, 45, 54, 58), K, 104)
    tr['drums'] = Track(9, K, 116, 64)
    for k, notes in (('kick', kick), ('clap', clap), ('hat', hat), ('crash', crash), ('perc', perc)):
        parts.append(Part(k, 'drums', notes, drums=True))
    # pads: 2 tellen per halve maat (rustig) of off-beat-stoten (pomp)
    pad = []
    for b in bars(10, END - 1):
        sec = section(b)
        if sec == 'BRK' and b < 52:
            continue
        for half in (0, 1):
            prog, note = W['PAD_' + ctype(b, half)], chord_note(b, half)
            if sec in ('A2', 'BUILD', 'BRK'):
                for pos in (12, 36):
                    if (b, half * 48 + pos) == (59, 84):
                        continue                      # melodie E4 tegen de F van Bb-mineur
                    hit(pad, b * BAR + half * 48 + pos, note, 88 if sec != 'BRK' else 70 + 8 * (b - 52), 9, prog)
            else:
                hit(pad, b * BAR + half * 48, note, 78, 44, prog)
    tr['pad'] = Track(10, W['PAD_dom'], 84, 64)
    parts.append(Part('pad', 'pad', pad))
    # buisklokken op de sectiebegins: de melodienoot van dat moment
    bell = []
    for b in (10, 22, 34, 37, 45, 54, 58):
        m = [n for s, e, n, v, p in SRC_T[2][0] if s == b * BAR] or [72 + root_pc(b, 0)]
        hit(bell, b * BAR, m[0], 104, 40, W['TUBBELL'])
    tr['bell'] = Track(11, W['TUBBELL'], 80, 76)
    parts.append(Part('bell', 'bell', bell))
    nh = []
    for b in bars(2, END - 1):
        if b in BRK and b < 52:
            continue
        for k in range(16):
            if k % 4 == 2:
                continue
            hit(nh, b * BAR + 6 * k, 72, 70 if k % 4 == 0 else 46, 3, W['NOISE_HAT'])
    tr['nhat'] = Track(12, W['NOISE_HAT'], 40, 64)
    parts.append(Part('nhat', 'nhat', nh))
    order = ['mel2', 'mel1', 'bass', 'kick', 'clap', 'hat', 'pad', 'bell', 'crash', 'perc', 'cnt4', 'cnt5']
    return dict(bpm=168, tracks=tr, parts=parts, order=order, vg=LEADER_VG['winona'][0])


ARP = {'dom': (0, 7, 10), 'sus': (0, 5, 10), 'min': (0, 3, 7), 'maj': (0, 4, 7), '5': (0, 7)}


def arp_tones(m, b, half, down):
    """Twee akkoordtonen onder (down) of boven de melodienoot, minstens een kleine terts ertussen."""
    root = root_pc(b, half)
    pcs = {(root + i) % 12 for i in ARP[ctype(b, half)]}
    out, cur = [], m
    for _ in range(2):
        rng = range(cur - 3, cur - 13, -1) if down else range(cur + 3, cur + 13)
        nxt = next((n for n in rng if n % 12 in pcs), cur - 12 if down else cur + 12)
        out.append(nxt)
        cur = nxt
    return out


def arpeggiate(notes, down, bends):
    """Melodie -> 16e-arpeggio's (Jordi: 'verdeel het thema in snelle zestiende-noot arpeggio's'): elke melodienoot
    blijft op zijn eigen tick en toonhoogte staan (met zijn velocity), de 16en daarna lopen langs twee akkoordtonen
    eronder (Liza) of erboven (Tate) en op elke tel van de noot terug naar de melodienoot. Intro (maat 2-9):
    octaafflutter. `bends`: pitch-bend-sweeps (BENDR 2): lange noten glijden erin (scoop van onder bij Liza, van
    boven bij Tate), frase-einden (>= 90 ticks) zweven in de laatste tel weg (tegengesteld)."""
    out = []
    sign = -1 if down else 1
    for s, e, n, v, p in notes:
        b = s // BAR
        L = e - s
        if b < 2 or L < 12:
            out.append([s, e, n, v, p])
            bends.append((s, 0.0))
            continue
        if b < 10:
            seq = [n, n - 12 if down else n + 12] * 2
        else:
            c1, c2 = arp_tones(n, b, 1 if (s % BAR) >= 48 else 0, down)
            seq = [n, c1, c2, c1]
        for k, t in enumerate(range(s, e - 2, 6)):
            x = n if (t - s) % 24 == 0 else seq[k % 4]
            x = max(48, min(96, x))
            out.append([t, t + 4, x, v if (t - s) % 24 == 0 else max(1, int(v * 0.8)), p])
        if L >= 36:
            for i in range(7):
                bends.append((s + 2 * i, sign * 2.0 * (1 - i / 6)))
        else:
            bends.append((s, 0.0))
        if L >= 90:
            for i in range(1, 9):
                bends.append((e - 24 + 3 * i, -sign * 2.0 * (i / 8) ** 1.5))
    return out


def bend_events(bends, ch):
    ev = [(0, mido.Message('control_change', channel=ch, control=20, value=2))]
    last = {}
    for t, semis in sorted(bends):
        last[t] = semis
    last[LOOP * BAR] = last.get(LOOP * BAR, 0.0)        # op het loopbegin altijd zuiver
    val = None
    for t in sorted(last):
        pw = max(-8192, min(8191, int(round(8192 * last[t] / 2))))
        if pw != val or t == LOOP * BAR:
            ev.append((t, mido.Message('pitchwheel', channel=ch, pitch=pw)))
            val = pw
    return [(t, x) for t, x in ev if t < END * BAR]


def tate_liza():
    """Psytrance (Jordi ronde 2), 144 bpm: Emerald-dance-kick op elke tel; rollende psy-bas op het PSG-golfkanaal
    (eigen 4-bit-zaagtand, één periode = een octaaf lager dan genoteerd) in 16en tussen de kicks: grondtoon /
    originele off-beat-noot (accent) / grondtoon; de melodie (Tate links = acid-zaagtand, Liza rechts = holle
    blokgolf) als 16e-arpeggio's met pitch-bend-sweeps. Clap op 2 en 4, open hihat op de en, PSG-ruis-16en,
    zaps op het pauken-ritme, acid-lijnen in de rustige delen, ruis-risers naar de drops."""
    T = TATE
    K = T['KIT']
    tr, parts = {}, []
    t1, n1 = copy_track(1, lambda p, t: T['LEAD_A'], 0.84, pan=30)
    t2, n2 = copy_track(2, lambda p, t: T['POPPLUCK'] if (p == PIANO and t < 2 * BAR) or p == 45 else T['LEAD_B'], 0.88, pan=98)
    b1, b2 = [], []
    n1, n2 = arpeggiate(n1, False, b1), arpeggiate(n2, True, b2)
    t1.other += bend_events(b1, t1.ch)
    t2.other += bend_events(b2, t2.ch)
    t4, n4 = copy_track(4, lambda p, t: p, 0.78)
    t5, n5 = copy_track(5, lambda p, t: p, 0.78)
    # origineel golfspoor: maat 0-1 blijft PSG (de bas begint pas in maat 2); daarna botst het met de psy-bas op het
    # golfkanaal -> DirectSound-drone; maat 37-44 = de grondtonen van de bas (C2/C#2/Eb2), die speelt de psy-bas al
    t6, n6 = copy_track(6, lambda p, t: p if t < 2 * BAR else T['DRONE'], 0.62)
    n6 = [n for n in n6 if not (37 * BAR <= n[0] < 45 * BAR)]
    for k, (t, n) in {'mel2': (t2, n2), 'mel1': (t1, n1), 'cnt4': (t4, n4), 'cnt5': (t5, n5), 'drone': (t6, n6)}.items():
        tr[k] = t
        parts.append(Part(k, k, n))
    nobass = set(bars(49, 52))
    bass, kick, hat, clap, crash, fx, acid = [], [], [], [], [], [], []
    for b in bars(0, END - 1):
        for beat in range(4):
            t = b * BAR + beat * 24
            if b < 2:
                continue
            if b not in nobass:
                hit(kick, t, KICK, 124, 5, K)
                root, off = bass_at(t), bass_at(t + 12)
                for k, n in ((1, root), (2, off), (3, root)):
                    hit(bass, t + 6 * k, n + 12, (84, 127, 100)[k - 1], 4, T['PSYBASS'])
            if (b >= 6 and b not in nobass):
                hit(hat, t + 12, OHAT, 96 if b >= 10 else 72, 12, K)
        if b >= 10 and b not in nobass:
            for s in (b * BAR + 24, b * BAR + 72):
                if s in SNARE_POS:
                    hit(clap, s, CLAP, 84, 12, K)
        if b in A2 or b in B2 or b in BUILD:
            for pos in timp_positions(b):
                if pos:
                    hit(fx, b * BAR + pos, ZAP, 80, 8, K)
    snare_roll(clap, 52, 53, K, SNARE, 40, 124, step=12)
    snare_roll(clap, 53, 53, K, SNARE, 70, 124)
    snare_roll(clap, 61, 61, K, SNARE, 50, 124)
    snare_roll(clap, 9, 9, K, SNARE, 50, 110, start=48)
    crash_at(crash, (2, 10, 22, 34, 37, 54), K, 110)
    pat = [0, 0, 12, 0, 7, 0, 12, 0, 0, 12, 0, 7, 0, 0, 10, 12]
    acc = [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0]
    for b in list(bars(37, 39)) + list(bars(49, 53)):
        for k in range(16):
            r = bass_at(b * BAR + 6 * k) % 12
            n = 36 + r + pat[k]
            n = n + 12 if n < 40 else n
            hit(acid, b * BAR + 6 * k, n, 118 if acc[k] else 84, 4, T['ACID'])
    tr['bass'] = Track(2, T['PSYBASS'], 66, 64)
    tr['drums'] = Track(9, K, 116, 64)
    tr['acid'] = Track(10, T['ACID'], 92, 76)
    parts.append(Part('bass', 'bass', bass))
    for k, notes in (('kick', kick), ('clap', clap), ('hat', hat), ('crash', crash), ('fx', fx)):
        parts.append(Part(k, 'drums', notes, drums=True))
    parts.append(Part('acid', 'acid', acid))
    nh, ccs = [], []
    risers = {(0, 1), (8, 9), (52, 53), (60, 61)}
    rbars = {b for r in risers for b in bars(*r)}
    for b in bars(0, END - 1):
        if b in rbars or b < 2 or b in nobass:
            continue
        for k in range(16):
            if k % 4 == 2:
                continue
            hit(nh, b * BAR + 6 * k, 74, 76 if k % 2 == 0 else 50, 3, T['NOISE_HAT'])
    for r0, r1 in sorted(risers):
        s, e = r0 * BAR, (r1 + 1) * BAR
        hit(nh, s, 60, 100, e - s - 2, T['NOISE_RISE'])
        for k in range(17):
            ccs.append((s + (e - s) * k // 16, 7, 6 + 34 * k // 16))
        ccs.append((e, 7, 38))
    tr['nhat'] = Track(12, T['NOISE_HAT'], 38, 64)
    tr['nhat'].other = [(t, mido.Message('control_change', channel=12, control=7, value=v)) for t, c, v in ccs]
    parts.append(Part('nhat', 'nhat', nh))
    order = ['mel2', 'mel1', 'kick', 'clap', 'hat', 'acid', 'crash', 'fx', 'drone']
    return dict(bpm=144, tracks=tr, parts=parts, order=order, vg=LEADER_VG['tate_liza'][0])


def wallace():
    """Franse lounge/bossa: bovenstem (spoor 2) op vibrafoon, onderstem (spoor 1) op accordeon (musette), trompet ->
    bugel, piano -> Rhodes, pizzicato -> nylongitaar; de PSG-tegenmelodieën (80/84) op fluit, de PSG-arpeggio's en
    -ostinato's op nylon. Rhodes-akkoorden (één sample per voicing: C13, maj9, m9, 9sus) in het bossa-ritme
    (3-3-4-3-3), contrabas op de bossa-figuur (grondtoon + de originele kwint op 2-en/4-en), zachte kick, cross-stick
    op het pauken-ritme (clave), brush-swirls, brush-tik op 2 en 4, ride in het donkere B-deel, PSG-shaker."""
    K = P['KIT_WALLACE']
    tr, parts = {}, []
    t1, n1 = copy_track(1, lambda p, t: {STRINGS: P['ACCORDION'], HORN: P['ACCORDION'], TRUMPET: P['FLUGEL'],
                                         PIANO: P['RHODES']}.get(p, p), 0.80, pan=46)
    t2, n2 = copy_track(2, lambda p, t: {STRINGS: P['VIBES'], HORN: P['VIBES'], TRUMPET: P['FLUGEL'], 45: P['NYLON'],
                                         PIANO: P['VIBES'] if t < 2 * BAR else P['RHODES']}.get(p, p), 0.96, pan=82)
    cnt = lambda p, t: P['FLUTE'] if p in (80, 84) else (P['NYLON'] if p in (4, 5, 6, 7, 82, 83, 86) else p)
    t4, n4 = copy_track(4, cnt, 0.62, pan=64)
    t5, n5 = copy_track(5, cnt, 0.62, pan=64)
    t6, n6 = copy_track(6, lambda p, t: p, 0.62)
    for k, (t, n) in {'mel2': (t2, n2), 'mel1': (t1, n1), 'cnt4': (t4, n4), 'cnt5': (t5, n5), 'wave': (t6, n6)}.items():
        tr[k] = t
        parts.append(Part(k, k, n))
    bass = []
    for b in bars(0, END - 1):
        if b < 2:
            for s, e, n, v, p in BASS:
                if b * BAR <= s < (b + 1) * BAR:
                    hit(bass, s, n, v, e - s - 4, P['UPRIGHT'])
            continue
        for half in (0, 1):
            t = b * BAR + half * 48
            hit(bass, t, bass_at(t), 120, 30, P['UPRIGHT'])
            hit(bass, t + 36, bass_at(t + 36), 104, 8, P['UPRIGHT'])
    tr['bass'] = Track(2, P['UPRIGHT'], 118, 64)
    parts.append(Part('bass', 'bass', bass))
    kick, stick, brush, swirl, ride = [], [], [], [], []
    for b in bars(2, END - 1):
        for half in (0, 1):
            t = b * BAR + half * 48
            hit(kick, t, KICK, 100, 12, K)
            hit(kick, t + 36, KICK, 76, 8, K)
            if b >= 10 and b not in B2 and half:
                hit(swirl, t, SWIRL, 70, 20, K)          # swirl op 3 (waar de cross-stick zwijgt), brush-tik op 2 en 4
        for pos in timp_positions(b) + ([60] if b % 2 else []):
            hit(stick, b * BAR + pos, XSTICK, 96, 6, K)
        if b >= 10:
            for s in (b * BAR + 24, b * BAR + 72):
                if s in SNARE_POS:
                    hit(brush, s, BRUSH, 78, 12, K)
        if b in B2:
            for beat in range(4):
                hit(ride, b * BAR + beat * 24, RIDE, 84 if beat % 2 else 70, 12, K)
    for b in (10, 22, 37, 54):
        hit(ride, b * BAR, CRASH, 96, 48, K)
    tr['drums'] = Track(9, K, 110, 64)
    for k, notes in (('kick', kick), ('stick', stick), ('brush', brush), ('swirl', swirl), ('ride', ride)):
        parts.append(Part(k, 'drums', notes, drums=True))
    # Rhodes-comping: bossa-figuur 3-3-4-3-3 (16en 0, 3, 6, 10, 13) met het akkoord van die halve maat
    rh = []
    types = {'dom': P['RH_DOM'], 'maj': P['RH_MAJ'], 'min': P['RH_MIN'], 'sus': P['RH_SUS'], '5': P['RH_SUS']}
    for b in bars(10, END - 1):
        for k16 in (0, 3, 6, 10, 13):
            pos = 6 * k16
            half = 0 if pos < 48 else 1
            hit(rh, b * BAR + pos, chord_note(b, half), 92 if k16 in (0, 10) else 78, 8, types[ctype(b, half)])
    tr['rhodes'] = Track(10, P['RH_DOM'], 84, 58)
    parts.append(Part('rhodes', 'rhodes', rh))
    # PSG-shaker: 16en, accent op de tellen
    nh = []
    for b in bars(6, END - 1):
        for k in range(16):
            hit(nh, b * BAR + 6 * k, 84, 60 if k % 4 == 0 else (44 if k % 2 == 0 else 32), 3, P['NOISE_HAT'])
    tr['nhat'] = Track(12, P['NOISE_HAT'], 30, 64)
    parts.append(Part('nhat', 'nhat', nh))
    order = ['mel2', 'mel1', 'bass', 'cnt4', 'kick', 'stick', 'rhodes', 'brush', 'cnt5', 'swirl', 'ride']
    return dict(bpm=156, tracks=tr, parts=parts, order=order, vg=VG)


LEADERS = [
    ('norman', 651, 'mus_grounded_vs_norman', norman, 80),          # laatste getal: -V in midi.cfg (nog niet gemeten)
    ('winona', 652, 'mus_grounded_vs_winona', winona, 78),
    ('tate_liza', 653, 'mus_grounded_vs_tate_liza', tate_liza, 76),
    ('wallace', 654, 'mus_grounded_vs_wallace', wallace, 90),
]


# ---- stemverdeler en wegschrijven ----------------------------------------------------------------------------
def occupancy(note, kinds, rel, bpm, drums):
    s, e, n, v, p = note
    kind = kinds.get(p, 'ds')
    if drums or kind.startswith('drums:'):
        return min(e, s + 2 * TPB)
    if kind == 'psg':
        return None
    return e + release_ticks(rel.get(p, 200), TPB, bpm) + 2


LOST = {}


def tail_of(prog, kinds, rel, bpm):
    return 0 if kinds.get(prog, 'ds') != 'ds' else release_ticks(rel.get(prog, 200), TPB, bpm) + 2


def detach_part(notes, kinds, rel, bpm):
    """Legato: elke noot laat een uitklinktijd vóór de volgende aanslag in dezelfde partij los (MUZIEK.md), anders
    bezet de release van de vorige noot een tweede kanaal. De aanslagen en toonhoogtes veranderen niet."""
    starts = sorted(set(n[0] for n in notes))
    out = []
    for s, e, n, v, p in sorted(notes):
        k = next((t for t in starts if t > s), None)
        tl = tail_of(p, kinds, rel, bpm)
        if k is not None and tl and e > k - tl:
            e = max(s + 3, min(e, k - tl))
        out.append([s, e, n, v, p])
    return out


def arrange(spec):
    vg = spec.get('vg', VG)
    kinds, rel = load_voices(vg), releases(vg)
    busy, report = [], []
    by_name = {p.name: p for p in spec['parts']}
    for part in spec['parts']:
        if not part.drums:
            part.notes = detach_part(part.notes, kinds, rel, spec['bpm'])
    order = spec['order'] + [p.name for p in spec['parts'] if p.name not in spec['order']]
    for name in order:
        part = by_name[name]
        kept, lost = [], 0
        for note in sorted(part.notes):
            en = occupancy(note, kinds, rel, spec['bpm'], part.drums)
            if en is None:
                kept.append(note)
                continue
            s = note[0]
            pts = [s] + [b0 for b0, b1 in busy if s < b0 < en]
            if all(sum(1 for b0, b1 in busy if b0 <= q < b1) < MAX_VOICES for q in pts):
                kept.append(note)
                busy.append((s, en))
            else:
                lost += 1
                LOST.setdefault(name, []).append(s // BAR)
        dsn = sum(1 for n in part.notes if occupancy(n, kinds, rel, spec['bpm'], part.drums) is not None)
        report.append((name, len(part.notes), dsn, lost))
        part.notes = kept
    return report


def write_midi(spec, path):
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    cond.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    cond.append(mido.MetaMessage('set_tempo', tempo=int(round(60e6 / spec['bpm'])), time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=LOOP * BAR))
    cond.append(mido.MetaMessage('marker', text=']', time=(END - LOOP) * BAR))
    cond.append(mido.MetaMessage('end_of_track', time=0))
    out.tracks.append(cond)
    notes_by_track = {}
    for p in spec['parts']:
        notes_by_track.setdefault(p.track, []).extend(p.notes)
    used = set()
    for key, tr in spec['tracks'].items():
        notes = dedupe_prog(notes_by_track.get(key, []))
        if not notes:
            continue
        assert tr.ch not in used, (key, tr.ch)
        used.add(tr.ch)
        ev = []
        if tr.prog is not None:
            ev.append((0, 0, 0, mido.Message('program_change', channel=tr.ch, program=tr.prog)))
            ev.append((0, 0, 1, mido.Message('control_change', channel=tr.ch, control=7, value=tr.vol)))
            ev.append((0, 0, 2, mido.Message('control_change', channel=tr.ch, control=10, value=tr.pan)))
        for k, (t, x) in enumerate(tr.other):
            ev.append((t, 1, k, x.copy(channel=tr.ch)))
        prog_now = tr.prog
        progs = sorted(set((n[0], n[4]) for n in notes))
        # generated sporen met meerdere programma's (stoten, Rhodes-voicings, ruis-hat/riser): wissel vóór de noot
        if tr.prog is not None:
            last = tr.prog
            for t, p in progs:
                if p != last:
                    ev.append((t, 1, -1, mido.Message('program_change', channel=tr.ch, program=p)))
                    last = p
        for s, e, n, v, p in notes:
            ev.append((s, 2, n, mido.Message('note_on', channel=tr.ch, note=n, velocity=v)))
            ev.append((e, 0, n, mido.Message('note_off', channel=tr.ch, note=n, velocity=0)))
        ev.sort(key=lambda x: (x[0], x[1], x[2]))
        t = mido.MidiTrack()
        last = 0
        for tick, _, _, x in ev:
            t.append(x.copy(time=tick - last))
            last = tick
        t.append(mido.MetaMessage('end_of_track', time=max(0, END * BAR - last)))
        out.tracks.append(t)
    assert len(out.tracks) - 1 <= 16, len(out.tracks)
    out.save(path)


def dedupe_prog(notes):
    """Ontdubbelen (zelfde tick + toets) en dezelfde toets in één spoor niet laten overlappen."""
    seen, out = set(), []
    for n in sorted(notes):
        if (n[0], n[2]) in seen:
            continue
        seen.add((n[0], n[2]))
        out.append(list(n))
    last = {}
    for n in out:
        prev = last.get(n[2])
        if prev is not None and prev[1] > n[0]:
            prev[1] = max(prev[0] + 1, n[0])
        last[n[2]] = n
    return out


FAILS = []


def check_unchanged(spec, leader):
    """Controle: de melodiesporen (1 en 2) hebben exact de noten van het origineel (toets, start, lengte)."""
    for name, i in (('mel1', 1), ('mel2', 2)):
        part = next(p for p in spec['parts'] if p.name == name)
        # aanslag en toonhoogte exact; de lengte mag alleen een uitklinktijd korter zijn (detach)
        a = sorted((s, n) for s, e, n, v, p in part.notes)
        b = sorted((s, n) for s, e, n, v, p in SRC_T[i][0])
        orig = {(s, n): e for s, e, n, v, p in SRC_T[i][0]}
        assert all(e <= orig[(s, n)] for s, e, n, v, p in part.notes if (s, n) in orig), leader
        if leader == 'tate_liza':                    # arpeggio's: elke melodienoot staat nog op zijn tick
            a = sorted(set(a) & set(b))
        if a != b:
            lost = sorted(set(b) - set(a))
            print('!! %s: %s wijkt af van het origineel (%d vs %d noten), bijv. %s' % (leader, name, len(a), len(b), lost[:6]))
            FAILS.append(leader)


def set_cfg(song, vol, vg=VG):
    cfg = 'sound/songs/midi/midi.cfg'
    lines = open(cfg).read().rstrip('\n').split('\n')
    line = '%s.mid: -E -R50 -G_%s -V%03d' % (song, vg, vol)
    lines = [line if l.startswith(song + '.mid:') else l for l in lines]
    if line not in lines:
        lines.append(line)
    open(cfg, 'w').write('\n'.join(lines) + '\n')


def main():
    write_voicegroup()
    write_leader_voicegroups()
    for leader, num, song, fn, vol in LEADERS:
        spec = fn()
        rep = arrange(spec)
        check_unchanged(spec, leader)
        path = 'sound/songs/midi/%s.mid' % song
        write_midi(spec, path)
        set_cfg(song, vol, spec['vg'])
        dur = END * BAR / TPB * 60 / spec['bpm']
        print('%s (%d): %d bpm, %.1f s (intro %.1f s + loop %.1f s) -> %s' % (
            leader, num, spec['bpm'], dur, LOOP * 4 * 60 / spec['bpm'], (END - LOOP) * 4 * 60 / spec['bpm'], path))
        for name, n, dsn, lost in rep:
            print('   %-6s %4d noten (%4d DS), %3d weg (%.1f%%)' % (name, n, dsn, lost, 100.0 * lost / max(1, dsn)))
        if os.environ.get('GYM2_DEBUG'):
            from collections import Counter
            for k, v in LOST.items():
                print('      weg %-6s per maat: %s' % (k, dict(sorted(Counter(v).items()))))
        LOST.clear()
    assert not FAILS, FAILS


if __name__ == '__main__':
    main()
