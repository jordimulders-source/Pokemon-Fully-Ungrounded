#!/usr/bin/env python3
"""Project Grounded: acht remixes van het Hoenn-trainerthema (MUS_VS_TRAINER, mus_vs_trainer.mid), één per groep
trainerklassen (Jordi: 'remixes van het trainer battle theme per soort trainer'). Melodie, harmonie en vorm blijven
herkenbaar (melodie = spoor 2 van het origineel noot voor noot, tweede stem = spoor 1, bas = de noten van spoor 3 in
een ander ritme, de akkoorden per halve maat uit alle sporen); kleur, groove en instrumenten wisselen.

  696 MUS_GROUNDED_VS_TRAINER_SEA       calypso: steel drum (rolls op lange noten), marimba-xylofoon, nylon-strums,
                                        conga's/cowbell, golvende PSG-arpeggio's (188 bpm)
  697 MUS_GROUNDED_VS_TRAINER_MOUNTAIN  zwaar: half-time, odaiko/taiko, gongs, hoorns, strijkers, taikosolo i.p.v.
                                        de paukensolo (168 bpm)
  698 MUS_GROUNDED_VS_TRAINER_NATURE    folk: fluit, tin whistle, nylon-strums in achtsten, pizzicato, bodhrán-toms,
                                        tamboerijn (192 bpm)
  699 MUS_GROUNDED_VS_TRAINER_MYSTIC    zwevend: fluitje met vibrato, koor, vibrafoon-arpeggio's, fretless, sparse
                                        Japanse percussie, half-time (176 bpm)
  700 MUS_GROUNDED_VS_TRAINER_CHIC      jazz-lounge swing: vibrafoon/trompet, Rhodes, walking bass, Charleston-piano,
                                        ride (swing 2:1) (200 bpm)
  701 MUS_GROUNDED_VS_TRAINER_ROCK      rock: distortion-lead, overdrive-tweede stem, powerchords in achtsten, rockkit,
                                        tomsolo (216 bpm)
  702 MUS_GROUNDED_VS_TRAINER_ELITE     episch: trompetten/hoorns, strijkersostinato, koor, pauken van het origineel,
                                        orkestsnare en bekkens (204 bpm)
  703 MUS_GROUNDED_VS_TRAINER_KIDS      speels: xylofoon, glockenspiel, pizzicato, PSG-blokgolf, stuiterbas, claps,
                                        fietsbel (208 bpm)

Vorm (maten van het origineel, tpb 24): intro 0-1, riff 2-9, A 10-19, B 20-27, C 28-35, C' 36-39, D 40-43,
E 44-53 (paukensolo), F 54-57, G 58-65, riff 66-73; loop maat 10-74 (zoals het origineel).
Eén voicegroup voor alle acht (grounded_trclass: de PSG-stemmen van vs_trainer op hun eigen nummers, eigen instrumenten
per sample) en één drumkit (drumsets/trclass.inc). Eigen samples: alleen trclass_steel en trclass_vibes
(tools/grounded/trclass_samples.py, 11 kHz, DPCM); verder stock. Stemverdeler max. 10 DirectSound-noten.
Gebruik: python3 tools/grounded/trclass_theme.py"""
import math, os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import Song, release_ticks, MAX_VOICES

SRC = 'sound/songs/midi/mus_vs_trainer.mid'
VG = 'grounded_trclass'
KIT = 'trclass'
TPB, BAR, S = 24, 96, 6
NBARS = 74
LOOP = (10 * BAR, NBARS * BAR)
SECS = [('intro', 0, 2), ('riff', 2, 10), ('A', 10, 20), ('B', 20, 28), ('C', 28, 36), ('C2', 36, 40),
        ('D', 40, 44), ('E', 44, 54), ('F', 54, 58), ('G', 58, 66), ('riff2', 66, 74)]
SEC_START = {a for _, a, _ in SECS}
SEC_END = {z - 1 for _, _, z in SECS}
ENERGY = {'intro': 3, 'riff': 2, 'A': 3, 'B': 1, 'C': 2, 'C2': 3, 'D': 3, 'E': 0, 'F': 2, 'G': 3, 'riff2': 2}
PSG_SLOTS = {4, 5, 6, 7, 80, 81, 82, 83, 85, 90}     # PSG-stemmen van vs_trainer die de PSG-kopieën gebruiken
TIMPANI_PROG = 47


def sec(bar):
    return next(k for k, a, z in SECS if a <= bar < z)


def place(pc, lo):
    return lo + (pc - lo) % 12


# ---- het origineel ---------------------------------------------------------------------------------------------------
class Src:
    def __init__(self):
        m = mido.MidiFile(SRC)
        assert m.ticks_per_beat == TPB
        self.notes, self.other = {}, {}
        for i in range(1, 9):
            tick, prog, on, ev, other, seen = 0, 0, {}, [], [], set()
            for x in m.tracks[i]:
                tick += x.time
                if x.type == 'program_change':
                    prog = x.program
                    other.append((tick, x))
                elif x.type == 'note_on' and x.velocity:
                    on.setdefault(x.note, []).append((tick, x.velocity, prog))
                elif x.type in ('note_on', 'note_off'):
                    if on.get(x.note):
                        s, v, p = on[x.note].pop(0)
                        if (s, x.note) not in seen:
                            seen.add((s, x.note))
                            ev.append([s, tick, x.note, v, p])
                elif not x.is_meta:
                    other.append((tick, x))
            self.notes[i] = sorted(ev)
            self.other[i] = other
        self.lead = self.notes[2]
        self.harm = [x for x in self.notes[1] if x[4] != TIMPANI_PROG]
        self.timp = sorted([x for x in self.notes[1] if x[4] == TIMPANI_PROG] + self.notes[8])
        self.bass = self.notes[3]
        # akkoorden per halve maat: grondtoon = laagste basnoot, toonklassen gewogen naar duur over alle toonsporen
        self.chords = {}
        for h in range(NBARS * 2):
            a, z = h * 48, h * 48 + 48
            bn = [n for s, e, n, v, p in self.bass if a <= s < z]
            root = (min(bn) if bn else 36) % 12
            w = [0.0] * 12
            for i in (1, 2, 3, 4, 5, 6):
                for s, e, n, v, p in self.notes[i]:
                    if p == TIMPANI_PROG:
                        continue
                    ov = min(e, z) - max(s, a)
                    if ov > 0:
                        w[n % 12] += ov * (1.5 if i == 3 else 1.0)
            self.chords[h] = (root, w)

    def chord(self, t, n=3, add7=False, strict=False):
        """Toonklassen van het akkoord op tick t: grondtoon + de zwaarste andere tonen (geen kleine secunden)."""
        if t >= NBARS * BAR:                      # na het einde: de loop begint weer in maat 10
            t = LOOP[0] + t - NBARS * BAR
        root, w = self.chords[t // 48]
        pcs = [root]
        for pc in sorted(range(12), key=lambda k: -w[k]):
            if len(pcs) >= n:
                break
            if pc in pcs or w[pc] < 0.12 * max(w):
                continue
            if any((pc - q) % 12 in (1, 11) for q in pcs):
                continue
            pcs.append(pc)
        if len(pcs) < 3 and (root + 7) % 12 not in pcs and not strict:
            pcs.append((root + 7) % 12)
        if add7:
            sev = (root + 10) % 12
            if sev not in pcs and (root + 11) % 12 not in pcs and not any((sev - q) % 12 in (1, 11) for q in pcs):
                pcs.append(sev)
        return root, pcs

    def bass_at(self, t):
        """Originele basnoot die op tick t klinkt (of de laatste ervoor)."""
        c = [x for x in self.bass if x[0] <= t]
        return c[-1][2] if c else 36

    def half_root(self, t):
        a = t // 48 * 48
        bn = [n for s, e, n, v, p in self.bass if a <= s < a + 48]
        return min(bn) if bn else self.bass_at(t)

    def half_top(self, t):
        a = t // 48 * 48
        bn = [n for s, e, n, v, p in self.bass if a <= s < a + 48]
        return max(bn) if bn else self.bass_at(t)


# ---- instrumenten ---------------------------------------------------------------------------------------------------
def ds(sample, att=255, dec=0, sus=255, rel=165):
    return 'voice_directsound 60, 0, DirectSoundWaveData_%s, %d, %d, %d, %d' % (sample, att, dec, sus, rel)


# naam -> [(vanaf geschreven noot, regel, verschuiving)]: de sample klinkt op toets 60 als C4 + verschuiving
# (gemeten met autocorrelatie/spectrum: fluitje C6, shakuhachi C5, ep_high C5, low distortion C3, powerchord C2)
INST = {
    'piano':   [(0, ds('sc88pro_piano1_48', 255, 252, 0, 150), 0), (54, ds('sc88pro_piano1_60', 255, 250, 0, 150), 0),
                (66, ds('sc88pro_piano1_72', 255, 250, 0, 150), 0), (78, ds('sc88pro_piano1_84', 255, 247, 0, 150), 0)],
    'strings': [(0, ds('sc88pro_string_ensemble_60', rel=180), 0), (66, ds('sc88pro_string_ensemble_72', rel=180), 0),
                (78, ds('sc88pro_string_ensemble_84', rel=180), 0)],
    'stac':    [(0, ds('sc88pro_string_ensemble_60', rel=140), 0), (66, ds('sc88pro_string_ensemble_72', rel=140), 0)],
    'trumpet': [(0, ds('sc88pro_trumpet_60', 255, 0, 193, 150), 0), (66, ds('sc88pro_trumpet_72', 255, 0, 193, 150), 0),
                (78, ds('sc88pro_trumpet_84', 255, 0, 193, 150), 0)],
    'horn':    [(0, ds('sc88pro_french_horn_60', 255, 0, 224, 165), 0), (66, ds('sc88pro_french_horn_72', 255, 0, 224, 165), 0)],
    'pizz':    [(0, ds('sc88pro_pizzicato_strings', 255, 216, 0, 140), 0)],
    'flute':   [(0, ds('sc88pro_flute', 255, 127, 231, 150), 0)],
    'whistle': [(0, ds('sd90_classical_whistle', 255, 0, 255, 160), 24)],
    'shaku':   [(0, ds('sd90_classical_shakuhachi', 255, 0, 255, 170), 12)],
    'oboe':    [(0, ds('sd90_classical_oboe', 255, 165, 154, 150), 0)],
    'nylon':   [(0, ds('sc88pro_nylon_str_guitar', 255, 249, 25, 90), 0)],
    'harp':    [(0, ds('sc88pro_harp', 255, 242, 51, 180), 0)],
    'xylo':    [(0, ds('sc88pro_xylophone', 255, 235, 0, 160), 0)],
    'glock':   [(0, ds('sc88pro_glockenspiel', 255, 165, 51, 190), 0)],
    'tbell':   [(0, ds('sc88pro_tubular_bell', 255, 165, 90, 200), 0)],
    'choir':   [(0, ds('classical_choir_voice_ahhs', 200, 0, 255, 175), 0)],
    'epiano':  [(0, ds('sd90_classical_detuned_ep1_low', 255, 249, 0, 165), 0),
                (66, ds('sd90_classical_detuned_ep1_high', 255, 249, 0, 165), 12)],
    'odrive':  [(0, ds('sd90_classical_overdrive_guitar', 255, 0, 255, 150), 0)],
    'dist':    [(0, ds('sd90_classical_distortion_guitar_high', 255, 0, 255, 150), 0)],
    'power':   [(0, ds('unused_guitar_separates_power_chord', 255, 165, 206, 110), -24)],
    'koto':    [(0, ds('unknown_koto_high', 255, 0, 206, 170), 0)],
    'fbass':   [(0, ds('sc88pro_fingered_bass', 255, 253, 0, 120), 0)],
    'fretless': [(0, ds('sc88pro_fretless_bass', 255, 253, 0, 150), 0)],
    'slap':    [(0, ds('sc88pro_slap_bass', 255, 235, 128, 99), 0)],
    'synbass': [(0, ds('sc88pro_synth_bass', 255, 252, 0, 115), 0)],
    'tuba':    [(0, ds('sc88pro_tuba_39', 255, 0, 255, 140), 0), (45, ds('sc88pro_tuba_51', 255, 0, 255, 140), 0)],
    'timpani': [(0, ds('sc88pro_timpani', 255, 246, 0, 200), 0)],
    'steel':   [(0, ds('trclass_steel', 255, 0, 255, 175), 0)],   # v2: laten naklinken (alleen SEA)
    'vibes':   [(0, ds('trclass_vibes', 255, 0, 255, 175), 0)],
    # eigen PSG-stemmen (kosten geen DirectSound-kanaal)
    'sq_lead': [(0, 'voice_square_1 60, 0, 0, 2, 0, 1, 9, 1', 0)],
    'sq_arp':  [(0, 'voice_square_2 60, 0, 1, 0, 2, 5, 1', 0)],
    'wave':    [(0, 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_3, 0, 7, 15, 2', 0)],
    'noise':   [(0, 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0', 0)],
    # v2 (achteraan, zodat de goedgekeurde nummers byte-identiek blijven)
    'brush':   [(0, 'voice_noise_alt 60, 0, 0, 0, 2, 0, 0', 0)],              # CHIC: brush-ride op PSG-ruis
    'dist_low': [(0, ds('sd90_classical_distortion_guitar_low', 255, 0, 255, 150), -12)],  # ROCK: powerchords
}
PSG_INST = {'sq_lead', 'sq_arp', 'wave', 'noise', 'brush'}

KITV = [  # drumkit vanaf toets 36 (voice_directsound, niet _no_resample: speelt op de rate van de sample)
    ('kick',    'voice_directsound 67, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 160'),
    ('snare',   'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170'),
    ('osnare',  'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 165'),
    ('clap',    'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 160'),
    ('crash',   'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
    ('ocrash',  'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 240, 0, 190'),
    ('tom_l',   'voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 170'),
    ('tom_m',   'voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 170'),
    ('tom_h',   'voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 170'),
    ('taiko',   'voice_directsound 63, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
    ('odaiko',  'voice_directsound 53, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 200'),
    ('gong',    'voice_directsound 47, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 250, 0, 225'),
    ('tamb',    'voice_directsound 60, 80, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 150'),
    ('conga_h', 'voice_directsound 60, 76, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 150'),
    ('conga_l', 'voice_directsound 60, 52, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 160'),
    ('cowbell', 'voice_directsound 60, 72, DirectSoundWaveData_sd90_cowbell, 255, 0, 255, 150'),
    ('triangle', 'voice_directsound 60, 84, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 200'),
    ('wood',    'voice_directsound 60, 64, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 140'),
    ('kotsu',   'voice_directsound 64, 84, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 160'),
    ('ohtsu',   'voice_directsound 60, 44, DirectSoundWaveData_ethnic_flavours_ohtsuzumi, 255, 0, 255, 170'),
    ('ride',    'voice_directsound 60, 80, DirectSoundWaveData_dance_drums_ride_bell, 255, 0, 255, 170'),
    ('jingle',  'voice_directsound 60, 72, DirectSoundWaveData_sc88pro_jingle_bell, 255, 0, 255, 170'),
    ('bike',    'voice_directsound 60, 64, DirectSoundWaveData_bicycle_bell, 255, 0, 255, 190'),
    ('skick',   'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 150'),
    ('ssnare',  'voice_directsound 60, 64, DirectSoundWaveData_sd90_solo_snare, 255, 0, 255, 160'),
    ('atom',    'voice_directsound 60, 64, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 190'),
    ('hat',     'voice_directsound 60, 72, DirectSoundWaveData_unknown_close_hihat, 255, 0, 255, 120'),
    ('ohat',    'voice_directsound 60, 72, DirectSoundWaveData_unknown_open_hihat, 255, 0, 255, 170'),
    ('idrum',   'voice_directsound 60, 64, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 170'),
]
DK = {nm: 36 + i for i, (nm, _) in enumerate(KITV)}
DREL = {36 + i: int(l.rsplit(',', 1)[1]) for i, (nm, l) in enumerate(KITV)}
DLEN = {'crash': 4 * S, 'ocrash': 4 * S, 'gong': 8 * S, 'triangle': 3 * S, 'ride': 2 * S, 'ohat': 2 * S}
assert len(KITV) <= 29


class VGroup:
    def __init__(self):
        free = [p for p in range(1, 127) if p not in PSG_SLOTS]
        self.prog, self.lines, self.rel = {}, {}, {}
        for nm, samples in INST.items():
            for i, (lo, line, shift) in enumerate(samples):
                p = free.pop(0)
                self.prog[(nm, i)] = p
                self.lines[p] = line
                self.rel[p] = None if nm in PSG_INST else int(line.rsplit(',', 1)[1])
        src = [l.strip() for l in open('sound/voicegroups/vs_trainer.inc')
               if l.strip().startswith('voice_') and not l.strip().startswith('voice_group')]
        for p in PSG_SLOTS:
            self.lines[p] = src[p]
            self.rel[p] = None
        self.lines[127] = 'voice_keysplit_all voicegroup_%s_drumset' % KIT
        self.lines[0] = self.lines[127]

    def pick(self, inst, n):
        """(programma, toets) voor geschreven noot n op instrument inst."""
        if inst == 'kit':
            return 127, n
        samples = INST[inst]
        i = max(k for k, (lo, line, sh) in enumerate(samples) if n >= lo or k == 0)
        return self.prog[(inst, i)], n - samples[i][2]

    def write(self):
        out = ['@ Project Grounded: voicegroup voor de trainerklasse-remixes van MUS_VS_TRAINER.',
               '@ Gegenereerd door tools/grounded/trclass_theme.py. PSG-stemmen 4-7/80-90 = vs_trainer; 127 = drumkit.',
               'voice_group %s' % VG]
        dummy = 'voice_square_1 60, 0, 0, 2, 0, 0, 15, 0'
        for p in range(128):
            out.append('\t%s  @ %d' % (self.lines.get(p, dummy), p))
        open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out) + '\n')
        kit = ['@ Project Grounded: drumkit voor de trainerklasse-remixes (tools/grounded/trclass_theme.py). Alles DirectSound.',
               '@ ' + ', '.join('%d %s' % (DK[nm], nm) for nm, _ in KITV) + '.',
               'voice_group %s_drumset, 36' % KIT] + ['\t' + l for _, l in KITV]
        open('sound/voicegroups/drumsets/%s.inc' % KIT, 'w').write('\n'.join(kit) + '\n')


# ---- partijen -------------------------------------------------------------------------------------------------------
class Part:
    def __init__(self, name, ds=True, vol=100, pan=64):
        self.name, self.ds, self.vol, self.pan = name, ds, vol, pan
        self.notes = []       # [start, eind, noot, velocity, instrument]
        self.ccs = []         # (tick, controller, waarde)
        self.extra = []       # (tick, mido-bericht) (PSG-kopieën: programmawissels/XCMD's van het origineel)
        self.raw_prog = None  # PSG-kopie: vaste programmanummers van het origineel

    def add(self, s, e, n, v, inst):
        s, e = int(s), int(e)
        if e > s:
            self.notes.append([s, e, int(n), max(1, min(127, int(v))), inst])


# laagste geschreven noot per instrument (lager klinkt dof of dreunt): een octaaf erbij
MINN = {'whistle': 67, 'shaku': 60, 'flute': 60, 'steel': 55, 'xylo': 53, 'glock': 67, 'vibes': 53, 'trumpet': 52,
        'horn': 48, 'dist': 52, 'odrive': 45, 'oboe': 58, 'choir': 48, 'koto': 55, 'pizz': 43, 'epiano': 45}


def route(part, notes, rule, vel=None):
    """rule(bar) -> (instrument, verschuiving) of None; noten van het origineel naar een nieuw instrument."""
    for s, e, n, v, p in notes:
        r = rule(s // BAR)
        if r:
            inst, sh = r[0], r[1]
            n += sh
            while n < MINN.get(inst, 0):
                n += 12
            part.add(s, e, n, vel if vel else 110, inst)


def by_sec(table):
    """{sectie: (instrument, verschuiving)} -> rule(bar)."""
    return lambda b: table.get(sec(b))


def roll(part, insts=None, minlen=4 * S, step=S, accent=(118, 96)):
    """Lange noten als tremolo (steel drum, marimba): herhalingen per `step` ticks tot het einde."""
    out = []
    for x in part.notes:
        s, e, n, v, inst = x
        if (insts is None or inst in insts) and e - s >= minlen:
            t, k = s, 0
            while t < e - 2:
                out.append([t, min(e, t + step - 1), n, accent[0] if k == 0 else accent[1] - (k % 2) * 6, inst])
                t += step
                k += 1
        else:
            out.append(x)
    part.notes = out


def vibrato(part, depth, delay=12, min_len=30, speed=22):
    part.ccs.append((0, 21, speed))
    part.ccs.append((0, 1, 0))
    notes = sorted(part.notes)
    for i, (s, e, n, v, inst) in enumerate(notes):
        if e - s >= min_len:
            part.ccs.append((s + delay, 1, depth))
            part.ccs.append((e, 1, 0))


def drum(part, bar, pos16, name, vel, length=None):
    t = bar * BAR + pos16 * S
    part.add(t, t + (length or DLEN.get(name, S)), DK[name], vel, 'kit')


def pattern(part, bar, pat, vel=110):
    """pat: {drum: [16e-posities]} of {drum: [(positie, velocity)]}"""
    for name, ps in pat.items():
        for q in ps:
            p, v = (q, vel) if not isinstance(q, tuple) else q
            drum(part, bar, p, name, v)


def fill(part, bar, kind, vel=112):
    """Fill in de tweede helft van de maat."""
    seqs = {'toms': ['tom_h', 'tom_h', 'tom_m', 'tom_m', 'tom_l', 'tom_l', 'tom_l', 'kick'],
            'snare': ['snare'] * 8, 'osnare': ['osnare'] * 8,
            'taiko': ['taiko', 'taiko', 'odaiko', 'taiko', 'odaiko', 'odaiko', 'odaiko', 'odaiko'],
            'conga': ['conga_h', 'conga_h', 'conga_l', 'conga_h', 'conga_l', 'conga_l', 'tom_h', 'tom_m'],
            'bodhran': ['tom_m', 'tom_l', 'tom_m', 'tom_l', 'tom_m', 'tom_m', 'tom_l', 'tom_l'],
            'mystic': ['kotsu', None, 'kotsu', 'ohtsu', None, 'kotsu', 'ohtsu', 'ohtsu'],
            'jazz': ['ssnare', None, 'ssnare', 'tom_m', None, 'tom_l', 'ssnare', 'kick'],
            'kids': ['tom_h', 'tom_h', 'tom_m', 'tom_h', 'clap', 'clap', 'clap', 'clap']}
    for i, nm in enumerate(seqs[kind]):
        if nm:
            drum(part, bar, 8 + i, nm, vel - (6 if i % 2 else 0), S)


def timp_solo(part, src, mapping, vel=115, lo=0):
    """De paukensolo van het origineel (spoor 1 en 8, maat 44-53) met andere trommels: mapping(noot) -> drum."""
    for s, e, n, v, p in src.timp:
        if 44 * BAR <= s < 54 * BAR:
            nm = mapping(n)
            if nm:
                part.add(s, s + 2 * S, DK[nm], vel if n < 52 else vel - 8, 'kit')


def bass_rhythm(part, src, inst, pos, bars=range(2, NBARS), vel=118, oct_=0):
    """pos: [(16e-positie, lengte in 16en, keuze)]: 'o' = originele basnoot op dat moment, 'r' = grondtoon van de
    halve maat, 'R' = grondtoon +12, 'f' = de hoge toon (kwint) van de halve maat."""
    for b in bars:
        for p, ln, w in pos:
            t = b * BAR + p * S
            n = {'o': src.bass_at(t), 'r': src.half_root(t), 'R': src.half_root(t) + 12, 'f': src.half_top(t)}[w]
            part.add(t, t + ln * S, n + oct_, vel - (0 if p % 4 == 0 else 8), inst)


def orig_bass(part, src, inst, bars=range(0, NBARS), shift=0, vel=116, stacc=None):
    for s, e, n, v, p in src.bass:
        if s // BAR in bars:
            part.add(s, s + stacc if stacc else e, n + shift, vel, inst)


def comp(part, src, inst, bars, pos, lo, n=3, add7=False, vel=96, power=False, strict=False):
    """Akkoorden per halve maat; pos: [(16e-positie, lengte in 16en, velocity-verschil)]."""
    for b in bars:
        for p, ln, dv in pos:
            t = b * BAR + p * S
            root, pcs = src.chord(t, n, add7, strict)
            if power:
                pcs = [root, (root + 7) % 12]
            for pc in pcs:
                part.add(t, t + ln * S, place(pc, lo), vel + dv, inst)


def arp(part, src, inst, bars, step, lo, seq=(0, 1, 2, 1), vel=90, ln=None, oct_span=2):
    """Gebroken akkoorden: akkoordtonen oplopend over oct_span octaven, volgorde seq (index in de opgebouwde ladder)."""
    for b in bars:
        for k in range(BAR // step):
            t = b * BAR + k * step
            root, pcs = src.chord(t, 3)
            ladder = sorted(place(pc, lo) + 12 * o for o in range(oct_span) for pc in pcs)
            n = ladder[seq[k % len(seq)] % len(ladder)]
            part.add(t, t + (ln or step), n, vel - (0 if k % 4 == 0 else 10), inst)


def hats(part, bars, step, vel=(100, 70), key=None, accent=None):
    """PSG-ruis (hihat/shaker): kost geen DirectSound-kanaal."""
    key = key or 84
    for b in bars:
        for k in range(BAR // step):
            t = b * BAR + k * step
            v = vel[0] if (accent and (k * step // S) in accent) or (not accent and k % 2 == 0) else vel[1]
            part.add(t, t + max(2, step // 2), key, v, 'noise')


def psg_copy(name, src, i, bars, vol):
    """PSG-spoor i van het origineel 1-op-1 in de gegeven maten (noten + programmawissels/XCMD's)."""
    part = Part(name, ds=False, vol=vol)
    part.notes = [list(x) for x in src.notes[i] if x[0] // BAR in bars]
    part.raw_prog = True
    return part


def lilt(part, amount=1):
    """Lichte calypso-swing: aanslagen op de oneven zestienden `amount` ticks later."""
    for x in part.notes:
        if (x[0] // S) % 2 == 1 and x[0] % S == 0:
            x[0] += amount
            x[1] = max(x[1], x[0] + 2)


def swing(part, a=2 * BAR):
    """Swing 2:1 vanaf tick a: de tweede achtste van elke tel schuift naar 2/3 (16 van 24 ticks)."""
    def f(t):
        if t < a:
            return t
        b, p = divmod(t, 24)
        q = p * 16 / 12 if p <= 12 else 16 + (p - 12) * 8 / 12
        return b * 24 + int(round(q))
    for x in part.notes:
        x[0], x[1] = f(x[0]), max(f(x[0]) + 2, f(x[1]))
    part.ccs = [(f(t), c, v) for t, c, v in part.ccs]


# ---- de acht remixes ------------------------------------------------------------------------------------------------
ALL = range(0, NBARS)
LOOPB = range(2, NBARS)


def bars_of(*secs):
    return [b for k, a, z in SECS if k in secs for b in range(a, z)]


def sea(src):
    """Calypso: steel drum met rolls, xylofoon als marimba, nylon-strums, conga's, cowbell, golvende PSG."""
    lead = Part('lead', vol=118, pan=60)
    route(lead, src.lead, by_sec({'intro': ('steel', -12), 'riff': ('steel', 0), 'A': ('steel', 0),
                                  'B': ('steel', 12), 'C': ('steel', 0), 'C2': ('steel', -12), 'D': ('steel', -12),
                                  'E': ('steel', 12), 'F': ('steel', 0), 'G': ('steel', 0), 'riff2': ('steel', 0)}))
    roll(lead, minlen=6 * S, step=S, accent=(112, 90))     # v2: rolls alleen op lange noten, 144 bpm = ±10 slagen/s
    harm = Part('harm', vol=96, pan=80)
    route(harm, src.harm, by_sec({'intro': ('xylo', -12), 'riff': ('xylo', 0), 'A': ('xylo', 0), 'B': ('xylo', 12),
                                  'C': ('xylo', 0), 'C2': ('xylo', 0), 'D': ('xylo', 0), 'F': ('xylo', 0),
                                  'G': ('xylo', 12), 'riff2': ('xylo', 0)}))
    roll(harm, minlen=6 * S, step=2 * S, accent=(104, 92))
    bass = Part('bass', vol=112)
    orig_bass(bass, src, 'fbass', bars=range(0, 2))
    bass_rhythm(bass, src, 'fbass', [(0, 3, 'r'), (3, 1, 'f'), (6, 2, 'f'), (8, 3, 'r'), (11, 1, 'f'), (14, 2, 'f')],
                bars=LOOPB)
    cmp_ = Part('comp', vol=78, pan=40)
    comp(cmp_, src, 'nylon', bars_of('A', 'B', 'C', 'C2', 'F', 'G'), [(0, 2, 6), (3, 1, -6), (6, 2, 0), (12, 2, 0)],
         55, n=3)
    dr = Part('drums', vol=100)
    for b in ALL:
        k = sec(b)
        if k == 'E':
            continue
        e = ENERGY[k]
        pat = {'kick': [0, 8], 'conga_h': [(2, 92), (10, 92)],
               'conga_l': [(6, 104), (7, 88), (14, 104), (15, 88)]}
        if e >= 3:
            pat['wood'] = [(4, 84), (12, 84)]
        if k in ('C2', 'G', 'D', 'intro'):
            pat['cowbell'] = [(0, 96), (3, 88), (6, 96), (10, 88), (12, 96)]
        if b in SEC_END and k not in ('intro',):
            pattern(dr, b, {'kick': [0], 'conga_l': [(6, 100)]})
            fill(dr, b, 'conga')
        else:
            pattern(dr, b, pat)
        if b in SEC_START:
            drum(dr, b, 0, 'crash', 108)
    timp_solo(dr, src, lambda n: 'conga_l' if n < 50 else ('conga_h' if n < 54 else 'tom_h'))
    for b in bars_of('E'):
        drum(dr, b, 0, 'kick', 104)
    psg = Part('shaker', ds=False, vol=60)
    hats(psg, [b for b in ALL if sec(b) != 'E'], S, vel=(84, 52), accent={2, 6, 10, 14})
    wave = Part('waves', ds=False, vol=52)
    arp(wave, src, 'wave', bars_of('A', 'C', 'G', 'F'), S, 60, seq=(0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 1, 2, 3, 2, 1),
        vel=100, oct_span=2)
    for p in (dr, cmp_, psg, wave):                        # v2: laid-back, de oneven zestienden iets later
        lilt(p)
    return dict(bpm=144, V=96, parts=[lead, bass, dr, harm, cmp_], psg=[psg, wave],
                order=['lead', 'bass', 'drums', 'harm', 'comp'])


def mountain(src):
    """Zwaar: half-time, odaiko/taiko, gongs, hoorns, strijkers, de paukensolo op taiko's."""
    lead = Part('lead', vol=118, pan=60)
    route(lead, src.lead, by_sec({'intro': ('horn', -12), 'riff': ('horn', 0), 'A': ('horn', 0), 'B': ('horn', 12),
                                  'C': ('shaku', 0), 'C2': ('trumpet', -12), 'D': ('horn', -12), 'E': ('horn', 12),
                                  'F': ('horn', 0), 'G': ('horn', 12), 'riff2': ('horn', 0)}))
    for x in lead.notes:
        if x[4] in ('horn', 'trumpet') and x[2] < 48:
            x[2] += 12
    vibrato(lead, 6, delay=18, min_len=36)
    harm = Part('harm', vol=92, pan=84)
    route(harm, src.harm, by_sec({'intro': ('strings', -12), 'riff': ('strings', -12), 'A': ('strings', 0),
                                  'B': ('strings', 0), 'C': ('strings', 0), 'C2': ('strings', -12),
                                  'D': ('strings', -12), 'F': ('strings', 0), 'G': ('koto', 12),
                                  'riff2': ('strings', -12)}))
    bass = Part('bass', vol=118)
    orig_bass(bass, src, 'fbass', bars=range(0, 2))
    bass_rhythm(bass, src, 'fbass', [(0, 6, 'r'), (6, 2, 'r'), (8, 5, 'r'), (14, 2, 'f')], bars=LOOPB)
    low = Part('lowbrass', vol=88, pan=44)
    for b in bars_of('A', 'C2', 'D', 'G'):
        for p, dv in ((0, 0), (8, -8)):
            t = b * BAR + p * S
            low.add(t, t + 6 * S, place(src.half_root(t) % 12, 40), 104 + dv, 'tuba')
    dr = Part('drums', vol=106)
    for b in ALL:
        k = sec(b)
        if k == 'E':
            continue
        e = ENERGY[k]
        pat = {'odaiko': [(0, 122), (8, 112)] if e >= 2 else [(0, 118)], 'kotsu': [(4, 100), (12, 100)],
               'taiko': [(6, 96), (7, 84), (14, 100)] if e >= 2 else [(14, 96)]}
        if e >= 3:
            pat['wood'] = [(4, 96), (12, 96)]
            pat['taiko'] = pat['taiko'] + [(10, 92)]
        if b in SEC_END and k != 'intro':
            pattern(dr, b, {'odaiko': [(0, 118)], 'kotsu': [(4, 96)]})
            fill(dr, b, 'taiko', 116)
        else:
            pattern(dr, b, pat)
        if b in SEC_START:
            drum(dr, b, 0, 'gong', 118)
    timp_solo(dr, src, lambda n: 'odaiko' if n < 50 else ('taiko' if n < 54 else 'kotsu'), vel=118)
    drum(dr, 44, 0, 'gong', 118)
    drum(dr, 54, 0, 'gong', 120)
    wave = psg_copy('psgw', src, 6, range(0, 2), 50)
    return dict(bpm=168, V=96, parts=[lead, bass, dr, harm, low], psg=[wave],
                order=['lead', 'bass', 'drums', 'harm', 'lowbrass'])


def nature(src):
    """Folk: fluit en tin whistle, nylon-strums in achtsten, pizzicato, bodhrán-toms, tamboerijn, shaker."""
    lead = Part('lead', vol=116, pan=66)
    route(lead, src.lead, by_sec({'intro': ('flute', -12), 'riff': ('flute', 0), 'A': ('flute', 0), 'B': ('flute', 12),
                                  'C': ('whistle', 0), 'C2': ('whistle', -12), 'D': ('flute', -12), 'E': ('flute', 12),
                                  'F': ('flute', 0), 'G': ('flute', 12), 'riff2': ('flute', 0)}))
    vibrato(lead, 4, delay=14, min_len=30)
    harm = Part('harm', vol=94, pan=84)
    route(harm, src.harm, by_sec({'intro': ('pizz', -12), 'riff': ('pizz', 0), 'A': ('oboe', 0), 'B': ('pizz', 12),
                                  'C': ('oboe', 0), 'C2': ('harp', 0), 'D': ('harp', 0), 'F': ('oboe', 12),
                                  'G': ('pizz', 12), 'riff2': ('pizz', 0)}))
    bass = Part('bass', vol=112)
    orig_bass(bass, src, 'fretless', bars=range(0, 2))
    bass_rhythm(bass, src, 'fretless', [(0, 3, 'r'), (4, 2, 'f'), (6, 2, 'r'), (8, 3, 'r'), (12, 2, 'f'),
                                        (14, 2, 'f')], bars=LOOPB, vel=114)
    cmp_ = Part('comp', vol=80, pan=36)
    comp(cmp_, src, 'nylon', bars_of('A', 'B', 'C', 'C2', 'D', 'F', 'G'),
         [(0, 2, 8), (2, 1, -8), (4, 2, 0), (6, 1, -8), (8, 2, 4), (10, 1, -8), (12, 2, 0), (14, 1, -8)], 55)
    comp(cmp_, src, 'nylon', bars_of('riff', 'riff2'), [(0, 2, 4), (6, 1, -8), (12, 2, 0)], 48, power=True)
    dr = Part('drums', vol=100)
    for b in ALL:
        k = sec(b)
        if k == 'E':
            continue
        e = ENERGY[k]
        pat = {'tom_l': [(0, 116), (3, 92), (8, 110), (11, 92)], 'tom_m': [(6, 96), (14, 96)],
               'tamb': [(4, 100), (12, 100)] if e >= 2 else [(12, 92)]}
        if e >= 3:
            pat['skick'] = [(0, 110), (8, 104)]
        if b in SEC_END and k != 'intro':
            pattern(dr, b, {'tom_l': [(0, 112)], 'tamb': [(4, 96)]})
            fill(dr, b, 'bodhran', 112)
        else:
            pattern(dr, b, pat)
        if b in SEC_START:
            drum(dr, b, 0, 'triangle', 104)
    timp_solo(dr, src, lambda n: 'tom_l' if n < 50 else ('tom_m' if n < 54 else 'tom_h'))
    psg = Part('shaker', ds=False, vol=58)
    hats(psg, [b for b in ALL if sec(b) != 'E'], 2 * S, vel=(86, 60))
    arps = psg_copy('psg4', src, 4, bars_of('G'), 62)
    return dict(bpm=192, V=96, parts=[lead, bass, dr, harm, cmp_], psg=[psg, arps],
                order=['lead', 'bass', 'drums', 'harm', 'comp'])


def mystic(src):
    """Zwevend: fluitje met vibrato, koor, vibrafoon-arpeggio's, fretless, sparse Japanse percussie, half-time."""
    lead = Part('lead', vol=112, pan=64)
    route(lead, src.lead, by_sec({'intro': ('whistle', -12), 'riff': ('shaku', 0), 'A': ('whistle', 0),
                                  'B': ('whistle', 12), 'C': ('shaku', 0), 'C2': ('whistle', -12),
                                  'D': ('whistle', -12), 'E': ('shaku', 12), 'F': ('whistle', 0),
                                  'G': ('whistle', 12), 'riff2': ('shaku', 0)}))
    vibrato(lead, 10, delay=10, min_len=24, speed=18)
    harm = Part('harm', vol=90, pan=76)
    route(harm, src.harm, by_sec({'intro': ('choir', -12), 'riff': ('choir', 0), 'A': ('choir', 0), 'B': ('choir', 12),
                                  'C': ('choir', 0), 'C2': ('choir', -12), 'D': ('choir', -12), 'F': ('choir', 0),
                                  'G': ('choir', 12), 'riff2': ('choir', 0)}))
    bass = Part('bass', vol=114)
    orig_bass(bass, src, 'fretless', bars=range(0, 2))
    bass_rhythm(bass, src, 'fretless', [(0, 7, 'r'), (8, 5, 'r'), (14, 2, 'f')], bars=LOOPB)
    bells = Part('bells', vol=84, pan=40)
    arp(bells, src, 'vibes', bars_of('A', 'B', 'C', 'C2', 'F', 'G'), 3 * S, 67, seq=(0, 2, 4, 1, 3, 5, 2, 4),
        vel=96, ln=3 * S)
    dr = Part('drums', vol=96)
    for b in ALL:
        k = sec(b)
        if k == 'E':
            continue
        e = ENERGY[k]
        pat = {'ohtsu': [(0, 112), (10, 100)], 'kotsu': [(6, 96), (14, 92)]}
        if e >= 2:
            pat['ssnare'] = [(8, 100)]
            pat['skick'] = [(0, 108)]
        if e >= 3:
            pat['wood'] = [(4, 84), (12, 84)]
        if b in SEC_END and k != 'intro':
            pattern(dr, b, {'ohtsu': [(0, 108)]})
            fill(dr, b, 'mystic', 108)
        else:
            pattern(dr, b, pat)
        if b in SEC_START:
            drum(dr, b, 0, 'gong', 100)
            drum(dr, b, 0, 'triangle', 96)
    timp_solo(dr, src, lambda n: 'ohtsu' if n < 50 else ('kotsu' if n < 54 else 'wood'), vel=112)
    psg = Part('hats', ds=False, vol=44)
    hats(psg, [b for b in ALL if ENERGY[sec(b)] >= 2], S, vel=(80, 52))
    wave = psg_copy('psgw', src, 6, ALL, 52)
    p5 = psg_copy('psg5', src, 5, bars_of('B', 'D', 'E', 'F'), 56)
    return dict(bpm=176, V=98, parts=[lead, bass, dr, harm, bells], psg=[psg, wave, p5],
                order=['lead', 'bass', 'drums', 'harm', 'bells'])


def chic(src):
    """Jazz-lounge swing: vibrafoon/trompet, Rhodes, walking bass, Charleston-piano, ride (swing 2:1)."""
    lead = Part('lead', vol=114, pan=60)
    route(lead, src.lead, by_sec({'intro': ('vibes', -12), 'riff': ('vibes', 0), 'A': ('vibes', 0),
                                  'B': ('trumpet', 12), 'C': ('vibes', 0), 'C2': ('trumpet', -12),
                                  'D': ('trumpet', -12), 'E': ('trumpet', 12), 'F': ('vibes', 0),
                                  'G': ('trumpet', 12), 'riff2': ('vibes', 0)}))
    vibrato(lead, 5, delay=16, min_len=36)
    harm = Part('harm', vol=90, pan=82)
    route(harm, src.harm, by_sec({'intro': ('epiano', -12), 'riff': ('epiano', 0), 'A': ('epiano', 0),
                                  'B': ('epiano', 12), 'C': ('epiano', 0), 'C2': ('epiano', -12),
                                  'D': ('epiano', -12), 'F': ('epiano', 0), 'G': ('epiano', 12),
                                  'riff2': ('epiano', 0)}))
    bass = Part('bass', vol=118)
    orig_bass(bass, src, 'fretless', bars=range(0, 2))
    for b in LOOPB:                                   # walking bass: grondtoon, akkoordtoon, kwint, aanloop
        for q in range(4):
            t = b * BAR + q * 24
            root, pcs = src.chord(t, 3)
            r = place(root, 36)
            if q == 0 or (q == 2 and src.half_root(t) % 12 != src.half_root(t - 48) % 12):
                n = r
            elif q == 1:
                n = place(pcs[1] if len(pcs) > 1 else root + 7, r + 1)
            elif q == 2:
                n = place((root + 7) % 12, r)
            else:
                nr = place(src.chord(t + 24, 3)[0], 36)
                n = nr + (1 if (b % 2) else -1)
            while n > 52:
                n -= 12
            bass.add(t, t + 20, n, 116 if q % 2 == 0 else 106, 'fretless')
    pno = Part('comp', vol=76, pan=36)
    comp(pno, src, 'piano', bars_of('A', 'B', 'C', 'C2', 'D', 'F', 'G'), [(0, 2, 6), (6, 1, 0), (10, 1, -6)],
         57, n=2, add7=True, strict=True)
    dr = Part('drums', vol=96)
    for b in ALL:
        k = sec(b)
        if k == 'E':
            continue
        e = ENERGY[k]
        pat = {}                                          # v2: geen ride-bell meer (de 'hoge tik', 2,8/3,6 kHz)
        if e >= 2:
            pat['skick'] = [(0, 96)]
            pat['ssnare'] = [(14, 78)] if b % 2 else [(10, 78)]
        if b in SEC_END and k != 'intro':
            fill(dr, b, 'jazz', 104)
        else:
            pattern(dr, b, pat)
        if b in SEC_START:
            drum(dr, b, 0, 'crash', 100)
    timp_solo(dr, src, lambda n: 'tom_l' if n < 50 else ('ssnare' if n < 54 else 'tom_h'), vel=108)
    hh = Part('hihat', ds=False, vol=40)                  # v2: zachte brush-ride + hihat-voet op 2 en 4 (PSG-ruis)
    for b in [b for b in ALL if sec(b) != 'E']:
        for p in ((0, 4, 6, 8, 12, 14) if b not in SEC_END else (0, 4)):
            t = b * BAR + p * S
            if p in (4, 12):
                hh.add(t, t + 3, 72, 80, 'noise')
            else:
                hh.add(t, t + 8, 58, 66 if p % 8 == 0 else 58, 'brush')
    for p in (lead, harm, bass, pno, dr, hh):
        swing(p)
    return dict(bpm=200, V=94, parts=[lead, bass, dr, harm, pno], psg=[hh],
                order=['lead', 'bass', 'drums', 'harm', 'comp'])


def rock(src):
    """Rock: distortion-lead, overdrive-tweede stem, powerchords in achtsten, rockkit, tomsolo."""
    lead = Part('lead', vol=112, pan=58)
    route(lead, src.lead, by_sec({'intro': ('dist', -12), 'riff': ('dist', 0), 'A': ('dist', 0), 'B': ('dist', 12),
                                  'C': ('dist', 0), 'C2': ('dist', -12), 'D': ('dist', -12), 'E': ('dist', 12),
                                  'F': ('dist', 0), 'G': ('dist', 12), 'riff2': ('dist', 0)}))
    vibrato(lead, 7, delay=12, min_len=30)
    harm = Part('harm', vol=86, pan=86)
    route(harm, src.harm, by_sec({'intro': ('odrive', -12), 'riff': ('odrive', 0), 'A': ('odrive', 0),
                                  'B': ('odrive', 12), 'C': ('odrive', 0), 'C2': ('odrive', -12),
                                  'D': ('odrive', -12), 'F': ('odrive', 0), 'G': ('odrive', 0),
                                  'riff2': ('odrive', 0)}))
    bass = Part('bass', vol=116)
    orig_bass(bass, src, 'fbass', bars=range(0, 2))
    bass_rhythm(bass, src, 'fbass', [(p, 2, 'r') for p in range(0, 16, 2)], bars=LOOPB, vel=118)
    # v2 (Jordi: 'klinkt als half afgemaakte gitaarakkoorden'): de oude 'unused_guitar_separates_power_chord' is een
    # akkoord met een harmonische reeks op C2 incl. de 7e boventoon, duurt maar 0,36 s en speelde een octaaf te hoog in
    # 16e-stootjes. Nu: grondtoon + kwint als twee low-distortion-noten (sample klinkt C3 op toets 60, met loop),
    # uitklinkend per halve maat; alleen in B/C/F bewust kortere aanslagen.
    pw = Part('power', vol=84, pan=30)

    def chord(t, ln, v):
        r = place(src.half_root(t) % 12, 40)
        pw.add(t, t + ln, r, v, 'dist_low')
        pw.add(t, t + ln, r + 7, v - 8, 'dist_low')
    for b in bars_of('A', 'C2', 'D', 'G'):
        for p in (0, 8):
            chord(b * BAR + p * S, 8 * S, 112)
    for b in bars_of('riff', 'riff2'):
        for p, ln in ((0, 6), (6, 6), (12, 4)):
            chord(b * BAR + p * S, ln * S, 110 if p == 0 else 102)
    for b in bars_of('B', 'C', 'F'):
        for p, ln in ((0, 6), (6, 2), (8, 6), (14, 2)):
            chord(b * BAR + p * S, ln * S, 106 if ln > 2 else 96)
    dr = Part('drums', vol=106)
    for b in ALL:
        k = sec(b)
        if k == 'E':
            continue
        e = ENERGY[k]
        pat = {'kick': [0, 6, 8, 10] if e >= 3 else [0, 8, 10], 'snare': [4, 12]}
        if b in SEC_END and k != 'intro':
            pattern(dr, b, {'kick': [0], 'snare': [4]})
            fill(dr, b, 'toms', 116)
        else:
            pattern(dr, b, pat)
        if b in SEC_START or (e >= 3 and b % 4 == 2):
            drum(dr, b, 0, 'crash', 110)
    timp_solo(dr, src, lambda n: 'tom_l' if n < 50 else ('tom_m' if n < 54 else 'tom_h'), vel=116)
    for b in bars_of('E'):
        drum(dr, b, 0, 'kick', 112)
    psg = Part('hats', ds=False, vol=56)
    hats(psg, [b for b in ALL if sec(b) != 'E'], 2 * S, vel=(96, 70))
    p4 = psg_copy('psg4', src, 4, bars_of('riff', 'riff2', 'G'), 58)
    p5 = psg_copy('psg5', src, 5, bars_of('riff', 'riff2', 'G'), 52)
    return dict(bpm=216, V=90, parts=[lead, bass, dr, harm, pw], psg=[psg, p4, p5],
                order=['lead', 'bass', 'drums', 'power', 'harm'])


def elite(src):
    """Episch: trompetten/hoorns, strijkersostinato, koor, de pauken van het origineel, orkestsnare en bekkens."""
    lead = Part('lead', vol=118, pan=58)
    route(lead, src.lead, by_sec({'intro': ('strings', -12), 'riff': ('trumpet', 0), 'A': ('trumpet', 0),
                                  'B': ('horn', 12), 'C': ('trumpet', 0), 'C2': ('trumpet', -12),
                                  'D': ('trumpet', -12), 'E': ('horn', 12), 'F': ('trumpet', 0),
                                  'G': ('trumpet', 12), 'riff2': ('trumpet', 0)}))
    for x in lead.notes:
        if x[4] in ('horn', 'trumpet') and x[2] < 48:
            x[2] += 12
    vibrato(lead, 6, delay=16, min_len=36)
    harm = Part('harm', vol=94, pan=84)
    route(harm, src.harm, by_sec({'intro': ('strings', -12), 'riff': ('horn', 0), 'A': ('horn', 0), 'B': ('strings', 12),
                                  'C': ('horn', 0), 'C2': ('horn', -12), 'D': ('horn', -12), 'F': ('strings', 0),
                                  'G': ('horn', 0), 'riff2': ('horn', 0)}))
    for x in harm.notes:
        if x[4] == 'horn' and x[2] < 48:
            x[2] += 12
    bass = Part('bass', vol=112)
    orig_bass(bass, src, 'fbass', bars=ALL)
    ost = Part('ostinato', vol=80, pan=40)
    for b in bars_of('A', 'C', 'C2', 'D', 'G'):
        for p in range(0, 16, 2):
            t = b * BAR + p * S
            root, pcs = src.chord(t, 3)
            n = place(root, 55) if p % 4 == 0 else place((root + 7) % 12, 55)
            ost.add(t, t + S + 2, n, 104 if p % 8 == 0 else 94, 'stac')
    choir = Part('choir', vol=78, pan=70)
    comp(choir, src, 'choir', bars_of('F', 'G'), [(0, 7, 0), (8, 7, -4)], 60, n=2, vel=100, strict=True)
    timp = Part('timpani', vol=100, pan=64)
    for s, e, n, v, p in src.timp:
        timp.add(s, s + 2 * S, n, 118, 'timpani')
    dr = Part('drums', vol=100)
    for b in ALL:
        k = sec(b)
        if k == 'E':
            continue
        e = ENERGY[k]
        pat = {'osnare': [(4, 110), (12, 110)] + ([(14, 86), (15, 92)] if e >= 3 else []), 'kick': [(0, 108)]}
        if b in SEC_END and k != 'intro':
            pattern(dr, b, {'kick': [(0, 108)], 'osnare': [(4, 104)]})
            fill(dr, b, 'osnare', 112)
        else:
            pattern(dr, b, pat)
        if b in SEC_START:
            drum(dr, b, 0, 'ocrash', 116)
    drum(dr, 44, 0, 'ocrash', 116)
    psg = Part('hats', ds=False, vol=46)
    hats(psg, [b for b in ALL if ENERGY[sec(b)] >= 3], 2 * S, vel=(88, 64))
    p4 = psg_copy('psg4', src, 4, bars_of('riff', 'riff2', 'C', 'G'), 54)
    p5 = psg_copy('psg5', src, 5, bars_of('intro', 'riff', 'riff2', 'C', 'G', 'B', 'D'), 50)
    return dict(bpm=204, V=94, parts=[lead, bass, timp, dr, harm, ost, choir], psg=[psg, p4, p5],
                order=['lead', 'bass', 'timpani', 'drums', 'harm', 'ostinato', 'choir'])


def kids(src):
    """Speels: xylofoon, glockenspiel, pizzicato, PSG-blokgolf, stuiterbas, claps, fietsbel."""
    lead = Part('lead', vol=116, pan=60)
    route(lead, src.lead, by_sec({'intro': ('xylo', -12), 'riff': ('xylo', 0), 'A': ('xylo', 0), 'B': ('xylo', 12),
                                  'C': ('glock', -12), 'C2': ('glock', -12), 'D': ('xylo', -12), 'E': ('xylo', 12),
                                  'F': ('xylo', 0), 'G': ('xylo', 12), 'riff2': ('xylo', 0)}))
    roll(lead, insts={'xylo'}, minlen=6 * S, step=2 * S, accent=(116, 100))
    sq = Part('square', ds=False, vol=50)
    route(sq, src.lead, by_sec({'A': ('sq_lead', 0), 'C': ('sq_lead', 0), 'G': ('sq_lead', 12)}), vel=100)
    harm = Part('harm', vol=92, pan=84)
    route(harm, src.harm, by_sec({'intro': ('pizz', -12), 'riff': ('pizz', 0), 'A': ('pizz', 0), 'B': ('pizz', 12),
                                  'C': ('pizz', 0), 'C2': ('pizz', -12), 'D': ('pizz', -12), 'F': ('pizz', 0),
                                  'G': ('pizz', 12), 'riff2': ('pizz', 0)}))
    roll(harm, minlen=6 * S, step=3 * S, accent=(104, 94))
    bass = Part('bass', vol=112)
    orig_bass(bass, src, 'synbass', bars=range(0, 2))
    bass_rhythm(bass, src, 'synbass', [(0, 1, 'r'), (2, 1, 'R'), (4, 1, 'r'), (6, 1, 'R'), (8, 1, 'r'),
                                       (10, 1, 'R'), (12, 1, 'f'), (14, 1, 'R')], bars=LOOPB, vel=116)
    cmp_ = Part('comp', vol=74, pan=36)
    comp(cmp_, src, 'glock', bars_of('A', 'C2', 'G'), [(0, 1, 0), (8, 1, -6)], 72, n=3, vel=92)
    dr = Part('drums', vol=100)
    for b in ALL:
        k = sec(b)
        if k == 'E':
            continue
        e = ENERGY[k]
        pat = {'kick': [0, 8] + ([10] if e >= 2 else []), 'clap': [4, 12]}
        if e >= 3:
            pat['tamb'] = [(2, 86), (6, 86), (10, 86), (14, 86)]
        if b in SEC_END and k != 'intro':
            pattern(dr, b, {'kick': [0], 'clap': [4]})
            fill(dr, b, 'kids', 112)
        else:
            pattern(dr, b, pat)
        if b in SEC_START:
            drum(dr, b, 0, 'crash', 104)
            if k in ('A', 'G', 'C2'):
                drum(dr, b, 8, 'bike', 96)
    timp_solo(dr, src, lambda n: 'tom_m' if n < 50 else ('tom_h' if n < 54 else 'cowbell'), vel=112)
    psg = Part('hats', ds=False, vol=52)
    hats(psg, [b for b in ALL if sec(b) != 'E'], 2 * S, vel=(90, 66))
    p4 = psg_copy('psg4', src, 4, bars_of('riff', 'riff2'), 54)
    p5 = psg_copy('psg5', src, 5, bars_of('intro', 'riff', 'riff2', 'D', 'F'), 50)
    return dict(bpm=208, V=96, parts=[lead, bass, dr, harm, cmp_], psg=[sq, psg, p4, p5],
                order=['lead', 'bass', 'drums', 'harm', 'comp'])


REMIXES = [(696, 'SEA', sea), (697, 'MOUNTAIN', mountain), (698, 'NATURE', nature), (699, 'MYSTIC', mystic),
           (700, 'CHIC', chic), (701, 'ROCK', rock), (702, 'ELITE', elite), (703, 'KIDS', kids)]
DESC = {'SEA': 'calypso (zee: Swimmer, Triathlete zwemmend, Sailor, Fisherman, Tuber)',
        'MOUNTAIN': 'taiko en gongs (berg: Hiker, Black Belt, Battle Girl, Expert)',
        'NATURE': 'folk met fluiten (natuur: Bug Catcher, Bug Maniac, Camper, Picnicker, Ranger, Breeder)',
        'MYSTIC': 'zwevend en spookachtig (Psychic, Hex Maniac, Ruin Maniac)',
        'CHIC': 'jazz-lounge swing (Beauty, Lady, Rich Boy, Gentleman, Pokefan)',
        'ROCK': 'snelle e-gitaarrock (Guitarist, Kindler, Ninja Boy)',
        'ELITE': 'episch koper (Cooltrainer, Dragon Tamer, Bird Keeper)',
        'KIDS': 'speels en stuiterend (Youngster, Lass, School Kid, Twins)'}


# ---- stemverdeler en wegschrijven -----------------------------------------------------------------------------------
def no_overlap(notes):
    notes = sorted(notes)
    last = {}
    for x in notes:
        k = (x[2], x[4] if x[4] == 'kit' else 'm')
        if k in last and last[k][1] > x[0]:
            last[k][1] = x[0]
        last[k] = x
    return [x for x in notes if x[1] > x[0]]


def tail_of(vg, x, bpm):
    if x[4] == 'kit':
        return release_ticks(DREL[x[2]], TPB, bpm) + 1
    p, _ = vg.pick(x[4], x[2])
    return release_ticks(vg.rel[p], TPB, bpm) + 1


def fit(part, vg, bpm, minlen=3):
    """Melodische partij: noot + uitklinktijd eindigt vóór de volgende aanslag in dezelfde partij (1 kanaal)."""
    notes = sorted(part.notes)
    starts = sorted(set(x[0] for x in notes))
    for x in notes:
        if x[4] == 'kit':
            continue
        nxt = next((t for t in starts if t > x[0]), None)
        if nxt is None:
            continue
        tl = tail_of(vg, x, bpm)
        same_chord = [y for y in notes if y[0] == x[0]]
        if len(same_chord) > 1:              # akkoord: alle tonen samen los
            pass
        x[1] = max(x[0] + minlen, min(x[1], nxt - tl))
    part.notes = notes


def allocate(parts, order, vg, bpm):
    busy, report = [], []
    by = {p.name: p for p in parts}
    for name in order:
        part = by[name]
        kept = []
        for x in sorted(part.notes):
            s, e = x[0], x[1]
            en = (s + min(e - s, 2 * TPB) if x[4] == 'kit' else e) + tail_of(vg, x, bpm)
            pts = [s] + [b[0] for b in busy if s < b[0] < en]
            if all(sum(1 for b in busy if b[0] <= q < b[1]) < MAX_VOICES for q in pts):
                kept.append(x)
                busy.append((s, en))
        report.append((name, len(part.notes), len(part.notes) - len(kept)))
        part.notes = kept
    return report


def write(path, res, vg):
    bpm = res['bpm']
    song = Song(TPB, int(round(60e6 / bpm)))
    song.tempo(0, 1.0)
    song.loop = LOOP
    tracks = res['parts'] + res['psg']
    assert len(tracks) <= 16
    for ch, part in enumerate(tracks):
        notes = no_overlap(part.notes)
        if part.raw_prog:                         # PSG-kopie: programma's van het origineel
            out, ccs, cur = [], [], None
            for s, e, n, v, p in notes:
                if p != cur:
                    ccs.append((s, 'prog', p))
                    cur = p
                out.append([s, e, n, v])
            first = notes[0][4] if notes else 4
            ccs = ccs[1:] if ccs else ccs
            song.add(out, first, part.vol, ch, part.pan, ccs=ccs)
            continue
        out, ccs, cur = [], [], None
        for s, e, n, v, inst in notes:
            p, key = vg.pick(inst, n)
            if p != cur:
                ccs.append((s, 'prog', p))
                cur = p
            out.append([s, e, key, v])
        first = ccs[0][2] if ccs else 127
        ccs = ccs[1:] + list(part.ccs)
        song.add(out, first, part.vol, ch, part.pan, ccs=ccs)
    song.save(path, NBARS * BAR)


def melody_check(name, src, lead, swung):
    """Elke noot van de melodie (spoor 2) moet in de leadpartij staan: zelfde aanslag (of het begin van de roll) en
    dezelfde toonklasse."""
    def f(t):
        if not swung or t < 2 * BAR:
            return t
        b, p = divmod(t, 24)
        q = p * 16 / 12 if p <= 12 else 16 + (p - 12) * 8 / 12
        return b * 24 + int(round(q))
    have = {(x[0], x[2] % 12) for x in lead.notes}
    miss = [x for x in src.lead if (f(x[0]), x[2] % 12) not in have]
    return miss


def low_checks(name, parts, vg):
    for part in parts:
        for s, e, n, v, inst in part.notes:
            if inst == 'kit' or inst in PSG_INST:
                continue
            p, key = vg.pick(inst, n)
            assert n >= 28, '%s/%s: noot onder E1 (%d) op %s' % (name, part.name, n, inst)
            if inst in ('trumpet', 'horn'):
                assert n >= 48, '%s/%s: koper onder C3 (%d)' % (name, part.name, n)


def register(num, key, V):
    """songs.h, song_table.inc, midi.cfg en voice_groups.inc (idempotent; nieuwe nummers achteraan, na 695)."""
    const, low = 'MUS_GROUNDED_VS_TRAINER_' + key, 'mus_grounded_vs_trainer_' + key.lower()
    h = open('include/constants/songs.h').read()
    if const + ' ' not in h:
        prev = 'MUS_GROUNDED_WL4_FIERY_CAVERN' if num == 696 else 'MUS_GROUNDED_VS_TRAINER_' + REMIXES[num - 697][1]
        i = h.index('\n', h.index('#define %s ' % prev)) + 1
        h = h[:i] + '#define %-27s %d // Project Grounded: trainerklasse-remix van MUS_VS_TRAINER: %s (tools/grounded/trclass_theme.py)\n' % (
            const, num, DESC[key]) + h[i:]
        open('include/constants/songs.h', 'w').write(h)
    t = open('sound/song_table.inc').read()
    if '\tsong %s,' % low not in t:
        prev = 'mus_grounded_wl4_fiery_cavern' if num == 696 else 'mus_grounded_vs_trainer_' + REMIXES[num - 697][1].lower()
        i = t.index('\n', t.index('\tsong %s,' % prev)) + 1
        t = t[:i] + '\n\tsong %s, MUSIC_PLAYER_BGM, 0\n' % low + t[i:]
        open('sound/song_table.inc', 'w').write(t)
    c = open('sound/songs/midi/midi.cfg').read()
    line = '%s.mid: -E -R50 -G_%s -V%03d' % (low, VG, V)
    lines = c.rstrip('\n').split('\n')
    hit = [i for i, l in enumerate(lines) if l.startswith(low + '.mid:')]
    if hit:
        lines[hit[0]] = line                      # op zijn plek laten staan (geen verschuiving bij elke run)
    else:
        lines.append(line)
    open('sound/songs/midi/midi.cfg', 'w').write('\n'.join(lines) + '\n')
    v = open('sound/voice_groups.inc').read()
    for inc in ('drumsets/%s.inc' % KIT, '%s.inc' % VG):
        if inc not in v:
            v = v.rstrip('\n') + '\n.include "sound/voicegroups/%s"\n' % inc
    open('sound/voice_groups.inc', 'w').write(v)


def main():
    src = Src()
    vg = VGroup()
    vg.write()
    for num, key, fn in REMIXES:
        res = fn(src)
        bpm = res['bpm']
        for part in res['parts']:
            fit(part, vg, bpm)
        low_checks(key, res['parts'], vg)
        rep = allocate(res['parts'], res['order'], vg, bpm)
        lead = next(p for p in res['parts'] if p.name == 'lead')
        miss = melody_check(key, src, lead, key == 'CHIC')
        path = 'sound/songs/midi/mus_grounded_vs_trainer_%s.mid' % key.lower()
        write(path, res, vg)
        register(num, key, res['V'])
        lost = ', '.join('%s %d/%d' % (n, l, t) for n, t, l in rep if l)
        print('%d %-9s %3d bpm  weggevallen: %s | melodie mist %d noten' % (
            num, key, bpm, lost or 'niets', len(miss)))
        assert not miss, miss[:5]


if __name__ == '__main__':
    main()
