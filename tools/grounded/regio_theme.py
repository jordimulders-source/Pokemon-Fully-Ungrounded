#!/usr/bin/env python3
"""Project Grounded: drie regionale remixes van het Hoenn-wildthema (MUS_VS_WILD, sound/songs/midi/mus_vs_wild.mid).

Jordi: "remix de hoenn battle theme naar bepaalde regio's. dus maak het meer fiery, meer sandstormy, maak een
specifiek op water theme".
  673 MUS_GROUNDED_VS_WILD_VOLCANO  vulkaan: 204 bpm, distortion-gitaar-lead, koperstoten, chugs op de bas, taiko,
                                    lagere bas, stijgende chromatische 'lava'-loopjes aan het eind van elke frase
  674 MUS_GROUNDED_VS_WILD_DESERT   woestijn: 188 bpm, C-frygisch-dominant (D->Db, A->Ab, Eb->E), hobo met mordenten,
                                    nylon als oud, koor-'waas', darbuka (maqsum/saidi), riq, PSG-ruis als zandwind
  675 MUS_GROUNDED_VS_WILD_WATER    water (surfen/vissen): 188 bpm, steel drum met roffels (eigen sample), xylofoon,
                                    harp-golven, calypso-bas en conga's, PSG-shaker, splash-bekkens, strijkers-swells
  680 MUS_GROUNDED_VS_WILD_UNDERWATER onderwater (duiken): 168 bpm half-time, zachte EP-mallet met trage vibrato,
                                    donkere pad met golvende bend, PSG-sub-bas, PSG-'bloop'-belletjes (sweep omhoog),
                                    melodie-echo en snare-echo's
v1.0.x, lichte variaties (Jordi 11 okt: "het hoeven allemaal echt maar lichte variaties te zijn van het theme"):
  704 MUS_GROUNDED_VS_WILD_SEA      zee (surfen/vissen op zeeroutes en bij kustplaatsen): 180 bpm, accordeon, hoorns,
                                    brede strijkers, shanty-stamp met tamboerijn, bekkenzwellen, PSG-branding
  705 MUS_GROUNDED_VS_WILD_SNOW     sneeuw/ijs: fluit, glockenspiel-glinsteringen en ijsloopjes, pizzicato,
                                    PSG-wind, kaler (geen pad); v2: sleebelletjes alleen nog als accent
  706 MUS_GROUNDED_VS_WILD_SPOOKY   spookachtig: 180 bpm, kerkorgel, PSG-klavecimbel, gebroken akkoord met tritonus,
                                    koorwaas met kleine terts (v2: alleen B/C, lager en zachter), doodsklok, pauken
  707 MUS_GROUNDED_VS_WILD_NIGHT    nacht: 176 bpm, zachte EP, fluit, pizzicato, licht drumpatroon, PSG-krekels;
                                    v2: voller intro (triller op fluit, strijkers onder val en riff)

Vorm, melodie en harmonie blijven die van het origineel (tick x 4: tpb 24 -> 96): intro maat 0-10 (chromatische val,
de C-Db-riff in 3+3+2, maat 10), loop maat 11-42 (A 10-17, B 18-25, C 26-33, riff 34-41, maat 42 = maat 10). Van het
origineel blijven alleen de melodie (spoor 2, bovenstem), de tweede stem (spoor 1) en de bas (spoor 3, noot voor
noot; in de calypso-delen het ritme nieuw op dezelfde grondtonen); alle begeleiding is nieuw (MUZIEK.md: anti-kermis,
geen tegenlijnen boven de melodie). In B (maat 18-25) draagt spoor 1 de beweeglijke melodie (de hoorn in 3+3+2) en
spoor 2 de lange bovenstem: daar wisselen de rollen.
Alleen stock-samples + één eigen sample (regio_steeldrum, regio_samples.py). Stemverdeler max. 10 DirectSound-noten.
  python3 tools/grounded/regio_theme.py"""
import math, os, random, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, detach, allocate, releases, release_ticks, Song

SRC = 'sound/songs/midi/mus_vs_wild.mid'
MAXV = 10
TPB = 96
S = TPB // 4
BAR = TPB * 4
SCALE = 4
LOOP0, END_BAR = 11, 43            # loopmarkers van het origineel: tick 1056 en 4128 (tpb 24)

# akkoord per maat (grondtoon, kwaliteit) uit bas + stemmen van het origineel
CH = {}
for b in range(2, 10):
    CH[b] = (0, 'M') if b % 2 == 0 else (1, 'M')
for b in range(34, 42):
    CH[b] = CH[b - 32]
for b in (10, 11, 14, 15, 18, 19, 22, 23, 24, 25, 28, 29, 32, 33, 42):
    CH[b] = (0, 'M')
for b in (12, 13, 16, 17, 20, 21, 26, 27):
    CH[b] = (10, 'M')
for b in (30, 31):
    CH[b] = (1, 'M')


def section(b):
    if b < 2:
        return 'I'
    if b < 10:
        return 'R1'
    if b < 18 or b == 42:
        return 'A'
    if b < 26:
        return 'B'
    if b < 34:
        return 'C'
    return 'R2'


PHRASE_END = (9, 17, 25, 33, 41)


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def orig():
    m = mido.MidiFile(SRC)
    assert m.ticks_per_beat * SCALE == TPB
    return {i: [[s * SCALE, e * SCALE, n, v] for s, e, n, v in notes_of(t)] for i, t in enumerate(m.tracks)}


def bar_of(t):
    return t // BAR


def roles(O, pmap=lambda n: n):
    """(lead, second): de beweeglijke melodie en de tweede stem; in B wisselen spoor 1 en 2."""
    lead, second = [], []
    for src, e_lead in ((O[2], True), (O[1], False)):
        for s, e, n, v in src:
            b = bar_of(s)
            n2 = pmap(n) if b >= 2 else n
            is_lead = e_lead != (section(b) == 'B')
            (lead if is_lead else second).append([s, e, n2, v])
    return sorted(lead), sorted(second)


def drum(P, t0, steps, key, vel, dlen, part='drums'):
    for k in steps:
        P[part].append([t0 + k * S, t0 + k * S + dlen[key], key, vel])


def chord_tones(b, minor_third=False):
    r, _ = CH.get(b, (0, 'M'))
    third = 3 if minor_third else 4
    return r, (r + third) % 12, (r + 7) % 12


def lowest_lead(lead, t0, t1):
    ns = [n for s, e, n, v in lead if s < t1 and e > t0]
    return min(ns) if ns else 127


# ---------------------------------------------------------------- voicegroups
def voicegroup(vg, title, over, kitname, kit):
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor %s (regionale remix van het Hoenn-wildthema).' % title
    lines[1] = '@ Gegenereerd door tools/grounded/regio_theme.py.'
    lines[2] = 'voice_group %s' % vg
    over = dict(over)
    over[127] = 'voice_keysplit_all voicegroup_%s_drumset' % kitname
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % vg, 'w').write('\n'.join(out))
    open('sound/voicegroups/drumsets/%s.inc' % kitname, 'w').write(
        '@ Project Grounded: drumkit voor regio_theme.py (%s). Alleen stock-samples, geen PSG.\n' % title
        + '@ ' + ', '.join(n for n, _ in kit) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group %s_drumset, 36\n' % kitname + ''.join('\t%s\n' % v for _, v in kit))


# ---------------------------------------------------------------- vulkaan
def volcano(O):
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, SN, CRASH, TOM_L, TOM_M, TOM_H, TAIKO, TAIKO_LO, TIMP = range(36, 45)
    D = {KICK: 2 * S, SN: 2 * S, CRASH: 6 * S, TOM_L: 2 * S, TOM_M: 2 * S, TOM_H: 2 * S, TAIKO: 3 * S,
         TAIKO_LO: 4 * S, TIMP: 2 * S}
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        if sec in ('R1', 'R2'):                       # riff: koperstoten
            P['tpt'].append([s, min(e, s + 2 * S), n, 120])
        else:
            P['gtr'].append([s, e, n, 116 if e - s > 2 * S else 104])
    for s, e, n, v in second:
        b = bar_of(s)
        sec = section(b)
        if sec == 'I':                                # chromatische val (spoor 1) op trompet
            P['tpt'].append([s, e, n, 104 + (s % BAR) // 24])
        elif sec in ('R1', 'R2'):
            P['horn'].append([s, min(e, s + 2 * S), n, 120])
        elif sec == 'B':
            P['horn'].append([s, e, n, 104])
        else:
            P['tpt2'].append([s, e, n, 100])
    # bas: noot voor noot het origineel, alles vanaf E2 een octaaf lager (zwaarder); chugs = de originele basnoten op
    # de lage distortion (klinkt een octaaf lager dan genoteerd: +12)
    for s, e, n, v in O[3]:
        b = bar_of(s)
        P['bass'].append([s, e, n - 12 if n >= 40 else n, 116])
        if b < 2 or (b in PHRASE_END + (29,) and s % BAR >= 8 * S):
            continue
        if section(b) == 'C' and e - s <= 2 * S:      # C: galop (twee 16en per achtste)
            P['chug'].append([s, s + S, n + 12, 120])
            P['chug'].append([s + S, s + 2 * S, n + 12, 100])
        else:
            P['chug'].append([s, s + S + 6, n + 12, 120 if (s % BAR) % (4 * S) == 0 else 104])
    # lava: stijgend chromatisch loopje (16en) naar de volgende maat
    for b in PHRASE_END + (29,):
        t0 = b * BAR
        tgt = 61 if b == 29 else 60                   # naar Db (maat 30) of C
        for k in range(8):
            P['lava'].append([t0 + (8 + k) * S, t0 + (9 + k) * S, tgt - 8 + k, 100 + 3 * k])
    # drums
    for b in range(END_BAR):
        t0 = b * BAR
        sec = section(b)
        if b == 0:
            drum(P, t0, (0, 6, 12), TAIKO_LO, 116, D)
            drum(P, t0, (0,), TIMP, 112, D)
            continue
        if b == 1:
            drum(P, t0, (0, 6), TAIKO_LO, 116, D)
            for k in range(8, 16):
                P['drums'].append([t0 + k * S, t0 + (k + 1) * S, TAIKO if k < 12 else SN, 96 + 4 * (k - 8)])
            continue
        hats = range(0, 16, 2)
        if sec == 'R1' and b < 6:
            drum(P, t0, (0, 8, 10), KICK, 116, D)
            drum(P, t0, (4, 12), SN, 116, D)
            drum(P, t0, (0,), TAIKO, 112, D)
        elif sec in ('R1', 'R2'):
            drum(P, t0, (0, 8, 10), KICK, 118, D)
            drum(P, t0, (4, 12), SN, 120, D)
            drum(P, t0, (0, 3, 6, 8, 11, 14), TAIKO, 108, D)
            hats = range(16)
        elif sec == 'A':
            drum(P, t0, (0, 6, 8, 10), KICK, 116, D)
            drum(P, t0, (4, 12), SN, 118, D)
            drum(P, t0, (0, 8), TAIKO, 108, D)
        elif sec == 'B':
            drum(P, t0, (0, 3, 6, 8, 11, 14), KICK, 116, D)
            drum(P, t0, (4, 12), SN, 120, D)
            drum(P, t0, (0, 8), TAIKO_LO, 110, D)
        else:   # C: taiko in 3+3+2, in de Db-maten dubbele kick op alle achtsten
            drum(P, t0, range(0, 16, 2) if b in (30, 31) else (0, 8, 10), KICK, 118, D)
            drum(P, t0, (4, 12), SN, 120, D)
            drum(P, t0, (0, 3, 6, 8, 11, 14), TAIKO, 108, D)
            hats = range(16)
        if b in (2, 10, 18, 22, 26, 30, 34, 38, 42):
            drum(P, t0, (0,), CRASH, 120, D)
        if b in PHRASE_END + (29,):                     # tomroffel stijgt mee met het lavaloopje
            P['drums'] = [x for x in P['drums'] if not (x[0] >= t0 + 8 * S and x[0] < t0 + BAR)]
            for k, key in zip(range(8, 16), (TOM_L, TOM_L, TOM_M, TOM_M, TOM_H, TOM_H, SN, SN)):
                P['drums'].append([t0 + k * S, t0 + (k + 1) * S, key, 104 + 3 * (k - 8)])
            drum(P, t0, (8,), TIMP, 116, D)
            hats = range(0, 8, 2)
        cr = {x[0] for x in P['drums'] if x[2] == CRASH}
        for k in hats:
            t = t0 + k * S
            if t not in cr:
                P['hat'].append([t, t + 6, 84, 64 if k % 4 == 0 else (48 if k % 2 == 0 else 36)])
    over = {
        30: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_high, 255, 0, 255, 165',
        31: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_low, 255, 0, 255, 110',
        33: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
        121: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    }
    kit = [
        ('36 kick', 'voice_directsound 67, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 snare', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180'),
        ('38 crash', 'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
        ('39 tom laag', 'voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('40 tom midden', 'voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('41 tom hoog', 'voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('42 taiko', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
        ('43 taiko laag', 'voice_directsound 53, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
        ('44 pauk', 'voice_directsound 43, 64, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200'),
    ]
    layout = [  # (partij, programma, volume, kanaal, pan)
        ('gtr', 30, 100, 0, 64),
        ('tpt', 56, 104, 1, 60),
        ('horn', 60, 100, 2, 70),
        ('tpt2', 56, 84, 3, 76),
        ('lava', 30, 84, 4, 54),
        ('bass', 33, 104, 5, 64),
        ('chug', 31, 76, 6, 64),
        ('hat', 121, 40, 10, 64),
    ]
    order = ['gtr', 'tpt', 'horn', 'drums', 'bass', 'lava', 'tpt2', 'chug']
    return dict(name='volcano', title='vulkaan', bpm=204, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=180, brass=('tpt', 'horn', 'tpt2'))


# ---------------------------------------------------------------- woestijn
SCALE_PD = (0, 1, 4, 5, 7, 8, 10)          # C-frygisch-dominant


def phryg(n):
    return n + {2: -1, 9: -1, 3: 1}.get(n % 12, 0)


def upper_neighbour(n):
    for d in (1, 2, 3):
        if (n + d) % 12 in SCALE_PD:
            return n + d
    return n + 1


def desert(O):
    P, CC, EX = Parts(), Parts(), Parts()
    DUM, TEK, KA, RIQ, FRAME, ZILL, TAIKO, CRASH = range(36, 44)
    D = {DUM: 2 * S, TEK: S, KA: S, RIQ: 2 * S, FRAME: 3 * S, ZILL: 4 * S, TAIKO: 4 * S, CRASH: 6 * S}
    lead, second = roles(O, phryg)
    orn = 0
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        ln = e - s
        if sec in ('R1', 'R2'):
            P['oboe'].append([s, min(e, s + 2 * S), n, 120])
        elif ln >= 6 * S and orn % 2 == 0:            # mordent (noot - bovenbuur in de toonladder - noot) in 32en
            P['oboe'] += [[s, s + 12, n, 116], [s + 12, s + 24, upper_neighbour(n), 104], [s + 24, e, n, 112]]
            orn += 1
        else:
            if ln >= 6 * S:
                orn += 1
            P['oboe'].append([s, e, n, 116 if ln > 2 * S else 106])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':
            P['oboe'].append([s, e, n, 100 + (s % BAR) // 24])
        else:                                          # nylon als oud (klinkt een octaaf lager: +12)
            P['oud'].append([s, min(e, s + 6 * S), n + 12, 116 if sec in ('R1', 'R2') else 108])
    for s, e, n, v in O[3]:
        b = bar_of(s)
        P['bass'].append([s, e, phryg(n) if b >= 2 else n, 116])
    # koor-waas: per halve maat één akkoordtoon (grondtoon / terts, de grote terts = frygisch-dominant), 2 tellen
    for b in range(2, END_BAR):
        r, _ = CH[b]
        minor = r == 10                                # Bb -> Bbm (Db)
        for h, iv in ((0, 0), (1, 3 if minor else 4)):
            n = 60 + (r + iv) % 12
            if n > 66:
                n -= 12
            t = b * BAR + h * 8 * S
            P['pad'].append([t, t + 8 * S - 6, n, 96])
    # zandwind: PSG-ruis met bend-curve, één vlaag per 4 maten (+ één lange in de intro)
    EX['wind'].append((0, mido.Message('control_change', control=20, value=24)))
    gusts = [(0, 2)] + [(b, 4) for b in range(2, 42, 4)]
    for b0, nb in gusts:
        t0, t1 = b0 * BAR, (b0 + nb) * BAR - S
        P['wind'].append([t0, t1, 60, 100])
        for t in range(t0, t1, 12):
            x = (t - t0) / (t1 - t0)
            curve = (x / 0.6) if x < 0.6 else (1 - (x - 0.6) / 0.4)
            EX['wind'].append((t, mido.Message('pitchwheel', pitch=int(-6000 + 12000 * curve))))
    # percussie
    for b in range(END_BAR):
        t0 = b * BAR
        sec = section(b)
        if b < 2:
            drum(P, t0, (0,), FRAME, 116, D)
            if b == 1:
                for k in range(16):
                    P['drums'].append([t0 + k * S, t0 + (k + 1) * S, TEK if k % 2 else DUM if k % 4 == 0 else KA,
                                       90 + 2 * k])
            else:
                drum(P, t0, (0, 6, 12), DUM, 112, D)
                drum(P, t0, (3, 9, 14), TEK, 100, D)
            continue
        if sec == 'B':                                 # saidi: D T . D D . T .
            drum(P, t0, (0, 6, 8), DUM, 118, D)
            drum(P, t0, (2, 12), TEK, 112, D)
            drum(P, t0, (2, 6, 10, 14), ZILL, 92, D)
        else:                                          # maqsum: D T . T D . T .
            drum(P, t0, (0, 8), DUM, 118, D)
            drum(P, t0, (2, 6, 12), TEK, 112, D)
        drum(P, t0, (4, 12), RIQ, 108, D)              # de backbeat van het origineel (snare op 2 en 4)
        if sec in ('A', 'C') or (sec in ('R1', 'R2') and b % 8 >= 6):
            drum(P, t0, (10, 14, 15), KA, 96, D)
        if sec == 'R2' or (sec == 'R1' and b >= 6):
            drum(P, t0, (1, 3, 5, 7, 9, 11, 13), KA, 90, D)
        if b % 2 == 0:
            drum(P, t0, (0,), FRAME, 114, D)
        if b in (30, 31):
            drum(P, t0, (0, 6), TAIKO, 116, D)
        if b in (2, 10, 18, 26, 34, 42):
            drum(P, t0, (0,), CRASH, 112, D)
            drum(P, t0, (0,), TAIKO, 118, D)
        if b in PHRASE_END:                            # tek-roffel naar de volgende frase
            P['drums'] = [x for x in P['drums'] if not (t0 + 8 * S <= x[0] < t0 + BAR)]
            for k in range(8, 16):
                P['drums'].append([t0 + k * S, t0 + (k + 1) * S, TEK if k % 2 else DUM, 100 + 3 * (k - 8)])
    over = {
        25: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_nylon_str_guitar, 255, 249, 0, 165',
        33: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
        52: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 90, 0, 255, 165',
        68: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127',
        122: 'voice_noise_alt 60, 0, 0, 5, 0, 15, 4',
    }
    kit = [
        ('36 dum', 'voice_directsound 52, 64, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 160'),
        ('37 tek', 'voice_directsound 64, 64, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 140'),
        ('38 ka', 'voice_directsound 69, 60, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 140'),
        ('39 riq', 'voice_directsound 60, 72, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 160'),
        ('40 lijsttrom', 'voice_directsound 56, 64, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 170'),
        ('41 zill', 'voice_directsound 72, 80, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 160'),
        ('42 taiko', 'voice_directsound 52, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
        ('43 crash', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 165'),
    ]
    layout = [
        ('oboe', 68, 112, 0, 64),
        ('oud', 25, 100, 1, 76),
        ('pad', 52, 64, 2, 52),
        ('bass', 33, 104, 3, 64),
        ('wind', 122, 30, 10, 64),
    ]
    order = ['oboe', 'oud', 'drums', 'bass', 'pad']
    return dict(name='desert', title='woestijn', bpm=188, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=170, brass=())


# ---------------------------------------------------------------- water
def water(O):
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, SN, SPLASH, CLO, CHI, COPEN, BUBBLE, TRI, CRASH = range(36, 45)
    D = {KICK: 2 * S, SN: 2 * S, SPLASH: 4 * S, CLO: 2 * S, CHI: S, COPEN: 2 * S, BUBBLE: 6 * S, TRI: 3 * S,
         CRASH: 6 * S}
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        if e - s >= 3 * S and sec not in ('R1', 'R2'):     # steel-drum-roffel op lange noten
            for i, t in enumerate(range(s, e - S // 2, S)):
                P['steel'].append([t, min(e, t + S), n, 114 if i == 0 else (96 if i % 2 else 102)])
        else:
            P['steel'].append([s, min(e, s + 2 * S), n, 116])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':                                   # chromatische val op de steel drum
            P['steel'].append([s, e, n, 100 + (s % BAR) // 24])
        elif e - s > 2 * S and sec != 'R1' and sec != 'R2':
            P['str'].append([s, e, n, 100])              # lange tweede-stemnoten als strijkers-swell
            k0 = 52
            steps = max(1, (e - s) // 12)
            for i in range(steps):
                CC['str'].append((s + i * 12, 7, k0 + (110 - k0) * i // steps))
        else:
            P['xylo'].append([s, min(e, s + 2 * S), n, 108])
    # bas: in de riffs het origineel, verder calypso op de grondtonen (1 . . a 2 . . . 3 . . a 4 . o .)
    for s, e, n, v in O[3]:
        if section(bar_of(s)) in ('I', 'R1', 'R2'):
            P['bass'].append([s, e, n, 112])
    for b in range(10, END_BAR):
        if section(b) in ('R1', 'R2'):
            continue
        r, _ = CH[b]
        root = 36 + r if 36 + r <= 43 else 24 + r
        fifth = root + 7
        nxt = CH.get(b + 1, (0, 'M'))[0]
        app = (36 + nxt if 36 + nxt <= 43 else 24 + nxt) + 1
        t0 = b * BAR
        for k, ln, n, vel in ((0, 3, root, 118), (3, 1, root, 96), (4, 3, fifth, 108), (8, 3, root, 116),
                              (11, 1, root, 96), (12, 2, fifth, 106), (14, 2, app if nxt != r else root + 12, 100)):
            P['bass'].append([t0 + k * S, t0 + (k + ln) * S, n, vel])
    # harp-golven: arpeggio in achtsten (grondtoon-kwint-octaaf-terts-kwint en terug), altijd onder de melodie
    for b in list(range(10, 18)) + list(range(26, 34)) + list(range(38, 42)) + [42]:
        r, _ = CH[b]
        base = 48 + r if r < 5 else 36 + r
        shape = [0, 7, 12, 16, 19, 16, 12, 7]
        t0 = b * BAR
        for i, iv in enumerate(shape):
            t = t0 + i * 2 * S
            n = base + iv
            lo = lowest_lead(lead, t, t + 2 * S)
            while n >= lo - 2:
                n -= 12
            if n < 43:
                continue
            P['harp'].append([t, t + S, n, 100 if i % 4 == 0 else 90])
    # drums
    for b in range(END_BAR):
        t0 = b * BAR
        sec = section(b)
        if b < 2:
            if b == 0:
                drum(P, t0, (0,), BUBBLE, 112, D)
                drum(P, t0, (0,), SPLASH, 100, D)
            else:
                for k in range(8, 16):
                    P['drums'].append([t0 + k * S, t0 + (k + 1) * S, CHI if k % 2 else CLO, 94 + 3 * (k - 8)])
            continue
        shaker = range(16)
        if sec == 'R1' and b < 6:
            drum(P, t0, (0, 8, 10), KICK, 116, D)
            drum(P, t0, (4, 12), SN, 100, D)
            drum(P, t0, (6, 14), COPEN, 104, D)
            shaker = range(0, 16, 2)
        else:
            drum(P, t0, (0, 6, 8, 14) if sec != 'B' else (0, 8), KICK, 116, D)
            drum(P, t0, (4, 12), SN, 104, D)
            drum(P, t0, (2, 10), CHI, 104, D)
            drum(P, t0, (6, 14, 15), COPEN, 108, D)
            drum(P, t0, (11,), CLO, 104, D)
            if sec == 'B':
                drum(P, t0, (3, 7, 11, 15), TRI, 92, D)
        if b % 2 == 1 and sec in ('A', 'C', 'R2'):         # splash op de golftop van elke 2-maatsfrase
            drum(P, t0, (6,), SPLASH, 104, D)
        if b in (2, 10, 18, 26, 34, 42):
            drum(P, t0, (0,), CRASH, 116, D)
        if b in (17, 25, 33):
            drum(P, t0, (12,), BUBBLE, 108, D)
        if b in PHRASE_END:                               # conga-roffel
            P['drums'] = [x for x in P['drums'] if not (t0 + 8 * S <= x[0] < t0 + BAR) or x[2] == BUBBLE]
            for k in range(8, 16):
                P['drums'].append([t0 + k * S, t0 + (k + 1) * S, CHI if k % 2 else (CLO if k < 12 else COPEN),
                                   98 + 3 * (k - 8)])
            shaker = range(0, 8)
        cr = {x[0] for x in P['drums'] if x[2] in (CRASH, SPLASH)}
        for k in shaker:
            t = t0 + k * S
            if t not in cr:
                P['shaker'].append([t, t + 6, 88, 60 if k % 4 == 2 else (44 if k % 2 == 0 else 34)])
    over = {
        13: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_xylophone, 255, 235, 0, 180',
        35: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 253, 0, 149',
        46: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 165',
        114: 'voice_directsound 60, 0, DirectSoundWaveData_regio_steeldrum, 255, 0, 255, 160',
        121: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    }
    kit = [
        ('36 kick', 'voice_directsound 67, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 rimsnare', 'voice_directsound 66, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 150'),
        ('38 splash', 'voice_directsound 70, 70, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 225, 0, 150'),
        ('39 conga laag', 'voice_directsound 57, 52, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 160'),
        ('40 conga hoog', 'voice_directsound 62, 76, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 140'),
        ('41 conga open', 'voice_directsound 65, 76, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 160'),
        ('42 belletjes', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_bubbles, 255, 0, 255, 170'),
        ('43 triangel', 'voice_directsound 74, 84, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 150'),
        ('44 crash', 'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
    ]
    layout = [
        ('steel', 114, 108, 0, 64),
        ('xylo', 13, 92, 1, 76),
        ('str', 48, 80, 2, 52),
        ('harp', 46, 84, 3, 84),
        ('bass', 35, 108, 4, 64),
        ('shaker', 121, 38, 10, 64),
    ]
    order = ['steel', 'drums', 'bass', 'xylo', 'str', 'harp']
    return dict(name='water', title='water', bpm=188, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=170, brass=())


# ---------------------------------------------------------------- onderwater
def underwater(O):
    """Jordi: 'doe ook een specifiek onderwater theme wat heel onderwater klinkt'. Half-time (gevoelde tel = halve
    maat), dof: zachte EP-mallet als melodie met trage vibrato, donkere koor/strijkers-pad met een golvende bend,
    sub-bas op de PSG-golf, stijgende 'bloop'-belletjes op PSG-vierkant 1 (sweep omhoog), echo's (melodie 3 16en
    later op een zacht spoor, snare-echo's)."""
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, SN, BUBBLE, TAIKO, SWELL, TRI = range(36, 42)
    D = {KICK: 3 * S, SN: 2 * S, BUBBLE: 6 * S, TAIKO: 4 * S, SWELL: 8 * S, TRI: 3 * S}
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        e2 = min(e, s + 3 * S) if sec in ('R1', 'R2') else e
        P['ep'].append([s, e2, n, 112])
        P['echo'].append([s + 3 * S, e2 + 3 * S, n, 96])          # delay: zelfde noot, 3 16en later, zachter spoor
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':                                             # chromatische val als zachte mallets
            P['ep'].append([s, e, n, 100 + (s % BAR) // 24])
        else:
            P['str'].append([s, max(e, s + 2 * S), n - 12 if n >= 72 else n, 100])
    # donkere pad: per halve maat grondtoon + kwint (één noot: kwint in octaaf 3), trage golvende bend
    for b in range(2, END_BAR):
        r, _ = CH[b]
        for h in (0, 1):
            t = b * BAR + h * 8 * S
            P['pad'].append([t, t + 8 * S - 6, 48 + r if h == 0 else 48 + (r + 7) % 12, 96])
    EX['pad'].append((0, mido.Message('control_change', control=20, value=2)))
    for t in range(0, END_BAR * BAR, 12):
        EX['pad'].append((t, mido.Message('pitchwheel', pitch=int(2400 * math.sin(2 * math.pi * t / (2 * BAR))))))
    CC['ep'] = [(0, 1, 10), (0, 21, 6)]                            # MOD + LFOS: trage vibrato op de melodie
    CC['str'] = [(0, 1, 18), (0, 21, 4)]
    # sub-bas (PSG-golf): grondtoon per halve maat; fretless-pluk op tel 1 voor de aanzet
    for b in range(END_BAR):
        t0 = b * BAR
        if b < 2:
            r = 7 if b == 0 else 10
            P['sub'].append([t0, t0 + BAR - 6, 36 + r, 110])
            continue
        r, _ = CH[b]
        for h in (0, 1):
            P['sub'].append([t0 + h * 8 * S, t0 + (h + 1) * 8 * S - 6, 36 + r, 110])
        P['bass'].append([t0, t0 + 4 * S, 36 + r if r < 8 else 24 + r, 104])
    # belletjes: korte stijgende groepjes van 3-4 hoge akkoordtonen (PSG, kost geen kanalen)
    rnd = random.Random(673)
    for b in range(2, END_BAR):
        r, _ = CH[b]
        tones = sorted({84 + (r + iv) % 12 for iv in (0, 4, 7)} | {96 + r % 12})
        for h in (0, 1):
            if rnd.random() < 0.35 and section(b) in ('R1',):
                continue
            k0 = h * 8 + rnd.choice((2, 3, 4))
            for i, n in enumerate(tones[:rnd.choice((3, 4))]):
                t = b * BAR + k0 * S + i * 12                       # 32en
                P['bub'].append([t, t + 10, n, 100 - 8 * i])
    # drums: half-time (kick op 1, snare op 3), snare-echo's, belletjes en zwellende bekkens
    for b in range(END_BAR):
        t0 = b * BAR
        sec = section(b)
        if b < 2:
            drum(P, t0, (0,), BUBBLE, 112, D)
            drum(P, t0, (0,), TAIKO, 110, D)
            if b == 1:
                drum(P, t0, (8,), SWELL, 108, D)
            continue
        drum(P, t0, (0,), KICK, 118, D)
        if sec in ('B', 'C', 'R2'):
            drum(P, t0, (10,), KICK, 104, D)
        drum(P, t0, (8,), SN, 116, D)
        drum(P, t0, (11,), SN, 92, D)                              # echo
        drum(P, t0, (14,), SN, 80, D)                              # echo van de echo
        if sec in ('A', 'C') and b % 2 == 0:
            drum(P, t0, (4, 12), TRI, 84, D)
        if b % 4 == 0:
            drum(P, t0, (0,), TAIKO, 108, D)
        if b in (2, 10, 18, 26, 34, 42):
            drum(P, t0, (0,), BUBBLE, 108, D)
        if b in PHRASE_END:
            drum(P, t0, (8,), SWELL, 104, D)
            drum(P, t0, (12,), BUBBLE, 100, D)
    over = {
        4: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_detuned_ep1_low, 255, 200, 110, 170',
        5: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_detuned_ep1_low, 255, 200, 110, 150',
        35: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 240, 0, 140',
        49: 'voice_keysplit voicegroup_strings_keysplit, keysplit_strings',
        53: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 60, 0, 255, 170',
        80: 'voice_square_1 60, 0, 21, 2, 0, 2, 0, 0',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_3, 0, 7, 15, 2',
    }
    kit = [
        ('36 kick', 'voice_directsound 58, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 doffe snare', 'voice_directsound 50, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170'),
        ('38 belletjes', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_bubbles, 255, 0, 255, 170'),
        ('39 taiko diep', 'voice_directsound 46, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
        ('40 bekkenzwel', 'voice_directsound 48, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 40, 0, 255, 140'),
        ('41 triangel dof', 'voice_directsound 62, 70, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 150'),
    ]
    layout = [
        ('ep', 4, 112, 0, 64),
        ('echo', 5, 60, 1, 88),
        ('str', 49, 72, 2, 44),
        ('pad', 53, 70, 3, 64),
        ('bass', 35, 88, 4, 64),
        ('sub', 84, 60, 6, 64),
        ('bub', 80, 40, 7, 80),
    ]
    order = ['ep', 'drums', 'str', 'bass', 'pad', 'echo']
    return dict(name='underwater', title='onderwater', bpm=168, P=P, CC=CC, EX=EX, over=over, kit=kit,
                layout=layout, order=order, kit_rel=170, brass=())


# ---------------------------------------------------------------- v1.0.x: lichte variaties (zee, sneeuw, spook, nacht)
# Jordi (11 okt): "het hoeven allemaal echt maar lichte variaties te zijn van het theme". Melodie, tweede stem en bas
# blijven die van het origineel (roles() + O[3] noot voor noot), alleen instrumenten, begeleiding en percussie
# veranderen; alleen stock-samples en PSG.
def gusts(EX, P, part, bars, cc_bendr=24, lo=-6000, span=12000, peak=0.6):
    """PSG-ruis met een bend-curve (zoals de zandwind van de woestijn): één vlaag per (startmaat, maten)."""
    EX[part].append((0, mido.Message('control_change', control=20, value=cc_bendr)))
    for b0, nb in bars:
        t0, t1 = b0 * BAR, (b0 + nb) * BAR - S
        P[part].append([t0, t1, 60, 100])
        for t in range(t0, t1, 12):
            x = (t - t0) / (t1 - t0)
            curve = (x / peak) if x < peak else (1 - (x - peak) / (1 - peak))
            EX[part].append((t, mido.Message('pitchwheel', pitch=int(lo + span * curve))))


def sea(O):
    """704 zee (open water: zeeroutes en kustplaatsen). 180 bpm (iets deinender), accordeon als melodie, hoorns op
    de riff en de tweede stem in de riffs, brede strijkers op de lange tweede stem, shanty-stamp (kick 1/3, snare +
    tamboerijn 2/4), bekkenzwellen als golven, paukenroffels aan het eind van elke frase, PSG-ruis als branding."""
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, SN, TAMB, CRASH, SWELL, TIMP = range(36, 42)
    D = {KICK: 2 * S, SN: 2 * S, TAMB: 2 * S, CRASH: 6 * S, SWELL: 8 * S, TIMP: 2 * S}
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        if sec in ('R1', 'R2'):
            P['acc'].append([s, min(e, s + 2 * S), n, 120])
        else:
            P['acc'].append([s, e, n, 116 if e - s > 2 * S else 106])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec in ('I', 'R1', 'R2'):                     # chromatische val en riff: hoornstoten
            P['horn'].append([s, min(e, s + 2 * S) if sec != 'I' else e, n, 116 if sec != 'I' else 100 + (s % BAR) // 24])
        else:                                            # brede strijkers, minstens een halve tel
            P['str'].append([s, max(e, s + 2 * S), n, 104])
    for s, e, n, v in O[3]:
        P['bass'].append([s, e, n, 116])
    gusts(EX, P, 'surf', [(0, 2)] + [(b, 2) for b in range(2, 42, 2)], peak=0.4)
    for b in range(END_BAR):
        t0 = b * BAR
        sec = section(b)
        if b < 2:
            drum(P, t0, (0,), SWELL, 104, D)
            if b == 1:
                for k in range(8, 16):
                    P['drums'].append([t0 + k * S, t0 + (k + 1) * S, TIMP, 96 + 3 * (k - 8)])
            else:
                drum(P, t0, (0, 8), TIMP, 108, D)
            continue
        drum(P, t0, (0, 8), KICK, 116, D)
        if sec in ('A', 'C'):
            drum(P, t0, (14,), KICK, 100, D)
        drum(P, t0, (4, 12), SN, 108, D)
        drum(P, t0, (4, 12), TAMB, 112, D)
        drum(P, t0, (2, 6, 10, 14), TAMB, 88, D)
        if b % 2 == 1 and sec in ('A', 'B', 'C'):        # golf: bekkenzwel naar de volgende 2-maatsfrase
            drum(P, t0, (8,), SWELL, 100, D)
        if b in (2, 10, 18, 26, 34, 42):
            drum(P, t0, (0,), CRASH, 112, D)
        if b in PHRASE_END:                              # paukenroffel naar de volgende frase
            P['drums'] = [x for x in P['drums'] if not (t0 + 8 * S <= x[0] < t0 + BAR)]
            for k in range(8, 16):
                P['drums'].append([t0 + k * S, t0 + (k + 1) * S, TIMP, 98 + 3 * (k - 8)])
    over = {
        21: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_accordion, 255, 0, 255, 165',
        33: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
        122: 'voice_noise_alt 60, 0, 0, 5, 0, 15, 4',
    }
    kit = [
        ('36 kick', 'voice_directsound 62, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 snare', 'voice_directsound 58, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 160'),
        ('38 tamboerijn', 'voice_directsound 60, 76, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 150'),
        ('39 crash', 'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
        ('40 bekkenzwel', 'voice_directsound 54, 52, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 30, 0, 255, 150'),
        ('41 pauk', 'voice_directsound 43, 64, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 180'),
    ]
    layout = [
        ('acc', 21, 108, 0, 64),
        ('horn', 60, 100, 1, 72),
        ('str', 48, 84, 2, 52),
        ('bass', 33, 104, 3, 64),
        ('surf', 122, 26, 10, 64),
    ]
    order = ['acc', 'horn', 'drums', 'bass', 'str']
    return dict(name='sea', title='zee', bpm=180, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=180, brass=('horn',))


def snow(O):
    """705 sneeuw/ijs. 188 bpm, kaler: fluit als melodie, glockenspiel-glinsteringen (een octaaf hoger op de
    aanzet van lange noten, dalend ijsloopje aan het eind van elke frase), pizzicato op de riff en de chromatische
    val, dunne strijkers op de tweede stem, fretless-bas; percussie met sleebelletjes op de achtsten, lichte kick
    en rimsnare, triangel (ook op de sectiestarts, geen bekkens); PSG-ruis als koude wind (één vlaag per 4 maten).
    Geen pad."""
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, RIM, SLEIGH, TRI = range(36, 40)
    D = {KICK: 2 * S, RIM: 2 * S, SLEIGH: 2 * S, TRI: 3 * S}
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        if sec in ('R1', 'R2'):
            P['flute'].append([s, min(e, s + 2 * S), n, 118])
        else:
            P['flute'].append([s, e, n, 116 if e - s > 2 * S else 106])
            if e - s >= 4 * S:                          # glinstering op de aanzet van lange noten
                P['glock'].append([s, s + 2 * S, n + 12 if n + 12 <= 96 else n, 104])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':
            P['pizz'].append([s, e, n, 100 + (s % BAR) // 24])
        elif sec in ('R1', 'R2'):
            P['pizz'].append([s, min(e, s + 2 * S), n, 112])
        else:
            P['str'].append([s, max(e, s + 2 * S), n, 96])
    for s, e, n, v in O[3]:
        P['bass'].append([s, e, n, 112])
    for b in PHRASE_END:                                # ijsloopje: dalende akkoordtonen in 16en (tel 3-4)
        r, _ = CH[b]
        tones = sorted({84 + (r + iv) % 12 for iv in (0, 4, 7)} | {72 + (r + 7) % 12, 72 + (r + 4) % 12}, reverse=True)
        for i, n in enumerate(tones[:5]):
            t = b * BAR + (10 + i) * S
            P['glock'].append([t, t + S, n, 108 - 4 * i])
    gusts(EX, P, 'wind', [(0, 2)] + [(b, 4) for b in range(2, 42, 4)])
    for b in range(END_BAR):
        t0 = b * BAR
        sec = section(b)
        if b < 2:
            for k in range(0, 16, 4 if b == 0 else 2):
                P['drums'].append([t0 + k * S, t0 + k * S + D[SLEIGH], SLEIGH, 80 + k if b else 84])
            if b == 0:
                drum(P, t0, (0,), TRI, 104, D)
            continue
        drum(P, t0, (0, 8) if sec != 'C' else (0, 8, 10), KICK, 112, D)
        drum(P, t0, (4, 12), RIM, 104, D)
        # v2 (Jordi: 'een instrument dat vanaf 7 sec erin komt en daarna dominant wordt, heel irritant'): de
        # sleebelletjes op de achtsten (vanaf maat 6 = 7,7 s) waren solo gemeten bijna alle energie boven 2 kHz van
        # de mix. Nu alleen een zachte schud op de sectiestarts en een korte roffel aan het eind van elke frase.
        if b in (2, 10, 18, 26, 34, 42):               # kaal: triangel i.p.v. een crash op de sectiestarts
            drum(P, t0, (0,), TRI, 108, D)
            drum(P, t0, (0,), SLEIGH, 84, D)
        elif b % 4 == 2 and sec in ('A', 'B', 'C'):
            drum(P, t0, (0,), TRI, 96, D)
        if b in PHRASE_END:                            # korte sleebelletjes-roffel onder het ijsloopje
            P['drums'] = [x for x in P['drums'] if not (t0 + 8 * S <= x[0] < t0 + BAR)]
            for k in range(12, 16):
                P['drums'].append([t0 + k * S, t0 + k * S + D[SLEIGH], SLEIGH, 78 + 3 * (k - 12)])
            drum(P, t0, (8,), KICK, 108, D)
    over = {
        35: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 253, 0, 149',
        9: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 160',
        45: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_pizzicato_strings, 255, 216, 0, 165',
        122: 'voice_noise_alt 60, 0, 0, 5, 0, 15, 4',
    }
    kit = [
        ('36 kick', 'voice_directsound 60, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 170'),
        ('37 rimsnare', 'voice_directsound 68, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 140'),
        ('38 sleebelletjes', 'voice_directsound 60, 80, DirectSoundWaveData_sc88pro_jingle_bell, 255, 0, 255, 150'),
        ('39 triangel', 'voice_directsound 74, 44, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 160'),
    ]
    layout = [
        ('flute', 73, 112, 0, 64),
        ('glock', 9, 84, 1, 84),
        ('pizz', 45, 96, 2, 76),
        ('str', 48, 76, 3, 48),
        ('bass', 35, 104, 4, 64),
        ('wind', 122, 24, 10, 64),
    ]
    order = ['flute', 'drums', 'bass', 'pizz', 'str', 'glock']
    return dict(name='snow', title='sneeuw', bpm=188, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=170, brass=())


def spooky(O):
    """706 spookachtig (Mt. Pyre, Abandoned Ship, Sky Pillar). 180 bpm, kerkorgel als melodie, PSG-'klavecimbel'
    (blokgolf 25%, korte decay) op de tweede stem en een gebroken akkoord in achtsten met een tritonus als
    doorgangsnoot (0-7-12-#4), koorwaas met de kleine terts (grondtoon / mineur-terts per halve maat), doodsklok
    (buisklok laag) elke 4 maten, pauken; kick en orkestsnare blijven, dus het blijft een gevechtsthema."""
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, SN, BELL, TIMP, CRASH = range(36, 41)
    D = {KICK: 2 * S, SN: 2 * S, BELL: 8 * S, TIMP: 2 * S, CRASH: 6 * S}
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        if sec in ('R1', 'R2'):
            P['organ'].append([s, min(e, s + 2 * S), n, 120])
        else:
            P['organ'].append([s, e, n, 116 if e - s > 2 * S else 106])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':                                  # chromatische val op het orgel
            P['organ'].append([s, e, n, 100 + (s % BAR) // 24])
        else:
            P['hpsi'].append([s, min(e, s + 4 * S), n, 110])
    for s, e, n, v in O[3]:
        P['bass'].append([s, e, n, 112])
    # gebroken akkoord (PSG): grondtoon-kwint-octaaf-overmatige kwart, onder de melodie
    for b in list(range(10, 34)) + [42]:
        r, _ = CH[b]
        base = 48 + r if r < 5 else 36 + r
        t0 = b * BAR
        for i, iv in enumerate((0, 7, 12, 6, 0, 7, 12, 6)):
            t = t0 + i * 2 * S
            n = base + iv
            lo = lowest_lead(lead, t, t + 2 * S)
            while n >= lo - 2:
                n -= 12
            if n < 40:
                continue
            P['arp'].append([t, t + S + 6, n, 100 if i % 4 == 0 else 88])
    # koorwaas: per halve maat grondtoon, dan de kleine terts (mineur-kleuring tegen de grote terts van de melodie)
    # v2 (Jordi: 'de vocalen zijn te dominant'; solo gemeten luider dan het orgel): alleen nog in B en C
    # (maat 18-33), een octaaf lager (onder de melodie, donkerder) en spoorvolume 76 -> 36.
    for b in range(18, 34):
        r, _ = CH[b]
        for h, iv in ((0, 0), (1, 3)):
            n = 48 + (r + iv) % 12
            if n > 54:
                n -= 12
            t = b * BAR + h * 8 * S
            P['choir'].append([t, t + 8 * S - 6, n, 96])
    for b in range(END_BAR):
        t0 = b * BAR
        sec = section(b)
        if b < 2:
            drum(P, t0, (0,), BELL, 112, D)
            if b == 1:
                for k in range(8, 16):
                    P['drums'].append([t0 + k * S, t0 + (k + 1) * S, TIMP, 96 + 3 * (k - 8)])
            continue
        drum(P, t0, (0, 8) if sec != 'B' else (0, 6, 8), KICK, 114, D)
        drum(P, t0, (4, 12), SN, 110, D)
        if b % 4 == 2:
            drum(P, t0, (0,), BELL, 108, D)
        if b in (2, 18, 34):
            drum(P, t0, (0,), CRASH, 104, D)
        if b in PHRASE_END:
            P['drums'] = [x for x in P['drums'] if not (t0 + 8 * S <= x[0] < t0 + BAR)]
            for k in range(8, 16):
                P['drums'].append([t0 + k * S, t0 + (k + 1) * S, TIMP, 98 + 3 * (k - 8)])
    over = {
        19: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_church_organ3_high, 255, 76, 154, 165',
        33: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
        52: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 70, 0, 255, 165',
        80: 'voice_square_1 60, 0, 0, 1, 0, 2, 3, 1',
        81: 'voice_square_2 60, 0, 0, 0, 1, 0, 1',
    }
    kit = [
        ('36 kick', 'voice_directsound 60, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 snare', 'voice_directsound 56, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 160'),
        ('38 doodsklok', 'voice_directsound 50, 64, DirectSoundWaveData_sc88pro_tubular_bell, 255, 165, 90, 200'),
        ('39 pauk', 'voice_directsound 43, 64, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 180'),
        ('40 crash', 'voice_directsound 56, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 165'),
    ]
    layout = [
        ('organ', 19, 104, 0, 64),
        ('hpsi', 80, 52, 1, 80),
        ('arp', 81, 40, 2, 44),
        ('choir', 52, 36, 3, 56),
        ('bass', 33, 104, 4, 64),
    ]
    order = ['organ', 'drums', 'bass', 'choir']
    return dict(name='spooky', title='spookachtig', bpm=180, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=200, brass=())


def night(O):
    """707 nacht (buitenkaarten als GetTimeOfDay() == TIME_NIGHT). 176 bpm, zachte EP als melodie (zonder vibrato
    of echo, dus niet de onderwater-klank), fluit op de tweede stem, pizzicato op de riff, fretless-bas; lichter
    drumpatroon (kick 1/3, rimsnare 2/4, zachte PSG-hihat op de achtsten, triangel), krekels op PSG-blokgolf."""
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, RIM, TRI, CYM = range(36, 40)
    D = {KICK: 2 * S, RIM: 2 * S, TRI: 3 * S, CYM: 6 * S}
    lead, second = roles(O)
    # v2 (Jordi: 'bij night valt de intro een klein beetje weg'): de intro had alleen de chromatische val op de EP
    # en daarna de riff in korte EP-stoten + pizzicato. Nu: de hoge triller van het origineel (maat 0-1) op de
    # fluit, de val luider en een octaaf lager gedubbeld op zachte strijkers, de riff (R1/R2) luider op de EP en
    # liggende strijkers (grondtoon + kwint per halve maat) eronder als body; de rest blijft gelijk.
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            P['flute'].append([s, e, n, 100 + (s % BAR) // 32])
            continue
        if sec in ('R1', 'R2'):
            P['ep'].append([s, min(e, s + 2 * S), n, 122 if e - s > S else 116])
        else:
            P['ep'].append([s, e, n, 116 if e - s > 2 * S else 108])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':
            P['ep'].append([s, e, n, 112 + (s % BAR) // 32])
            P['str'].append([s, e, n - 12, 100 + (s % BAR) // 32])
        elif sec in ('R1', 'R2'):
            P['pizz'].append([s, min(e, s + 2 * S), n, 116])
        else:
            P['flute'].append([s, max(e, s + 2 * S), n, 100])
    for b in list(range(2, 10)) + list(range(34, 42)):
        r, _ = CH[b]
        for h in (0, 1):
            t = b * BAR + h * 8 * S
            for iv in (0, 7):
                n = 48 + (r + iv) % 12
                P['str'].append([t, t + 8 * S - 6, n, 96])
    for s, e, n, v in O[3]:
        P['bass'].append([s, e, n, 112])
    rnd = random.Random(707)                            # krekels: korte trillers van 4 32en, hoog en zacht
    for b in range(2, END_BAR):
        if rnd.random() < 0.5:
            continue
        k0 = rnd.choice((2, 6, 10, 14))
        n = rnd.choice((98, 100))
        for i in range(4):
            t = b * BAR + k0 * S + i * 12
            P['crick'].append([t, t + 8, n, 100])
    for b in range(END_BAR):
        t0 = b * BAR
        sec = section(b)
        if b < 2:
            drum(P, t0, (0,), TRI if b == 0 else KICK, 100, D)
            if b == 1:
                drum(P, t0, (8, 10, 12, 13, 14, 15), RIM, 96, D)
            continue
        hats = range(0, 16, 2)
        drum(P, t0, (0, 8) if sec not in ('C', 'R2') else (0, 8, 10), KICK, 110, D)
        drum(P, t0, (4, 12), RIM, 100, D)
        if b % 2 == 0 and sec in ('A', 'B', 'C'):
            drum(P, t0, (0,), TRI, 92, D)
        if b in (2, 10, 18, 26, 34, 42):
            drum(P, t0, (0,), CYM, 96, D)
        if b in PHRASE_END:
            P['drums'] = [x for x in P['drums'] if not (t0 + 12 * S <= x[0] < t0 + BAR)]
            drum(P, t0, (12, 13, 14, 15), RIM, 92, D)
            hats = range(0, 12, 2)
        for k in hats:
            t = t0 + k * S
            P['hat'].append([t, t + 6, 84, 56 if k % 4 == 0 else 40])
    over = {
        4: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_detuned_ep1_low, 255, 200, 110, 160',
        35: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 253, 0, 149',
        45: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_pizzicato_strings, 255, 216, 0, 165',
        81: 'voice_square_2 60, 0, 2, 0, 1, 0, 0',
        121: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    }
    kit = [
        ('36 kick', 'voice_directsound 58, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 170'),
        ('37 rimsnare', 'voice_directsound 66, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 140'),
        ('38 triangel', 'voice_directsound 72, 84, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 150'),
        ('39 bekken', 'voice_directsound 54, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 120, 235, 0, 150'),
    ]
    layout = [
        ('ep', 4, 112, 0, 64),
        ('flute', 73, 84, 1, 80),
        ('pizz', 45, 92, 2, 76),
        ('bass', 35, 104, 3, 64),
        ('hat', 121, 32, 10, 64),
        ('crick', 81, 20, 6, 96),
        ('str', 48, 62, 4, 44),
    ]
    order = ['ep', 'drums', 'bass', 'flute', 'pizz', 'str']
    return dict(name='night', title='nacht', bpm=176, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=170, brass=())


# ---------------------------------------------------------------- wegschrijven
def build(spec):
    name, bpm = spec['name'], spec['bpm']
    vg, kitname = 'grounded_regio_' + name, 'regio_' + name
    voicegroup(vg, spec['title'], spec['over'], kitname, spec['kit'])
    P, CC, EX = spec['P'], spec['CC'], spec['EX']
    for k in list(P):
        P[k] = dedupe(P[k])
    progs = {k: pr for k, pr, *_ in spec['layout']}
    rel = releases(vg)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, bpm) + 2 for k, pr in progs.items()}
    tail['drums'] = release_ticks(spec['kit_rel'], TPB, bpm) + 2
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            P[k] = detach(P[k], tail[k])
            low = [n for _, _, n, _ in P[k] if n < 28]
            assert not low, '%s/%s: DirectSound-noten onder E1 %s' % (name, k, low[:5])
            if k in spec['brass']:
                bad = [n for _, _, n, _ in P[k] if n < 48]
                assert not bad, '%s/%s: koper onder C3 %s' % (name, k, bad[:5])
            soft = [v for _, _, _, v in P[k] if v < 76]
            assert not soft, '%s/%s: zachte DS-noten (8-bit-fuzz) %s' % (name, k, soft[:5])
    for k, pr in progs.items():                        # zelfde toonhoogte mag in één spoor niet overlappen
        ev = sorted(P[k])
        last = {}
        for e in ev:
            if e[2] in last and last[e[2]][1] > e[0]:
                last[e[2]][1] = e[0]
            last[e[2]] = e
    order = spec['order']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAXV)
    print('== %s (%d bpm)' % (name, bpm))
    for k in order:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            lost = [e for e in ds[k] if e not in kept[k]]
            print('  %s: %d van %d noten vallen weg (%.1f%%), maten %s' % (
                k, len(lost), n, 100 * len(lost) / n, sorted({bar_of(e[0]) for e in lost})[:12]))
        P[k] = kept[k]
    song = Song(TPB, 500000)
    song.tempo(0, bpm / 120)
    end = END_BAR * BAR
    song.loop = (LOOP0 * BAR, end)
    for k, pr, vol, ch, pan in spec['layout']:
        song.add(P[k], pr, vol, ch, pan, extra=EX.get(k, []), ccs=CC.get(k, []))
    song.add(sorted(P['drums']), 127, 112, 9)
    written = {k for k, *_ in spec['layout']} | {'drums'}
    assert not [k for k in P if P[k] and k not in written], [k for k in P if P[k] and k not in written]
    out = 'sound/songs/midi/mus_grounded_vs_wild_%s.mid' % name
    song.save(out, end)
    print('  %s | intro %.1f s | loop %.1f s | totaal %.1f s' % (
        out, LOOP0 * BAR / TPB * 60 / bpm, (end - LOOP0 * BAR) / TPB * 60 / bpm, end / TPB * 60 / bpm))


if __name__ == '__main__':
    O = orig()
    for f in (volcano, desert, water, underwater, sea, snow, spooky, night):
        build(f(O))
