#!/usr/bin/env python3
"""Project Grounded: drie grot-remixes van het Hoenn-wildthema (MUS_VS_WILD, sound/songs/midi/mus_vs_wild.mid).

Jordi (11 okt): "Grot theme ook prima, maar Meteor Falls mag dan avontuurlijker klinken en Fiery Path vurig. Maar het
hoeven allemaal echt maar lichte variaties te zijn van het theme."
  708 MUS_GROUNDED_VS_WILD_CAVE    grot: 188 bpm, fluit-lead met galm (echo-spoor, 3 16en later), strijkers op de tweede
                                   stem, holle bas (fretless een octaaf lager + PSG-golf), gedempte drums (doffe
                                   kick/snare, ambient toms, zachte PSG-hihat)
  709 MUS_GROUNDED_VS_WILD_METEOR  Meteor Falls: 196 bpm (tempo van het origineel), de grot als basis maar met heroisch
                                   koper (trompet-lead, trompetstoten in de riffs), een hoorn op de melodie (in B de
                                   melodie zelf, in A/C een octaaf onder de trompet), snellere toms (16en-galop), pauken
                                   en een stijgend glockenspiel-loopje bij elke nieuwe frase (ontdekking)
  710 MUS_GROUNDED_VS_WILD_FIERY   Fiery Path: 196 bpm, de grot met hitte: rock-orgel als lead met galm, gloeiende
                                   distortion-pads (grondtoon per halve maat, aanzwellend, trillende bend), diepe taiko; geen gitaar-lead/chugs/koper zoals de vulkaan-remix (673)

Vorm, melodie, harmonie en lengte zijn die van het origineel (zie regio_theme.py: tick x 4, intro maat 0-10, loop maat
11-42). Van het origineel blijven de melodie (spoor 2), de tweede stem (spoor 1) en de bas (spoor 3, noot voor noot);
in B wisselen spoor 1 en 2 van rol (roles()). Alleen stock-samples. Stemverdeler max. 10 DirectSound-noten.
Hergebruikt de helpers van regio_theme.py (orig, roles, section, CH, drum); regio_theme.py zelf blijft ongemoeid.
v2 (Jordi: 'een soort percussie op de achtergrond die niet past en heel irritant wordt', in alle drie): dat was de
hyoushigi (houten klepper, in de kit op toets 56/58: een ringende 'tok' op 2,1-2,4 kHz, 2-3x per maat het hele
nummer door). Eruit, net als de andere effectpercussie: de PSG-druppels (klonken in de game niet eens: PSG-volume 0)
en het PSG-knetteren van Fiery Path. De normale kit (kick, snare, toms, pauken, bekkens, zachte PSG-hihat) blijft.
  python3 tools/grounded/regio_theme2.py"""
import math, os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song
from regio_theme import orig, roles, section, bar_of, drum, Parts, CH, PHRASE_END, TPB, S, BAR, LOOP0, END_BAR

MAXV = 10
SECTION_START = (2, 10, 18, 26, 34, 42)


# ---------------------------------------------------------------- voicegroups
def voicegroup(vg, title, over, kitname, kit):
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor %s (grot-remix van het Hoenn-wildthema).' % title
    lines[1] = '@ Gegenereerd door tools/grounded/regio_theme2.py.'
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
        '@ Project Grounded: drumkit voor regio_theme2.py (%s). Alleen stock-samples, geen PSG.\n' % title
        + '@ ' + ', '.join(n for n, _ in kit) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group %s_drumset, 36\n' % kitname + ''.join('\t%s\n' % v for _, v in kit))


# ---------------------------------------------------------------- gedeelde grotlagen
def hollow_bass(P, O, vel=112):
    """Bas noot voor noot het origineel, vanaf E2 een octaaf lager; dezelfde noten op de PSG-golf (hol, geen kanaal)."""
    for s, e, n, v in O[3]:
        n2 = n - 12 if n >= 40 else n
        P['bass'].append([s, e, n2, vel])
        P['sub'].append([s, max(s + S, e - 6), n2 + 12, 100])


def echo_of(P, src, dst, delay=3 * S, vel=90, maxlen=4 * S):
    for s, e, n, v in P[src]:
        P[dst].append([s + delay, s + delay + min(e - s, maxlen), n, vel])


def cave_drums(P, D, K, t0, b, fast_toms=False):
    """Gedempte grotdrums. K = dict met sleutels kick, sn, stick, toms (laag, midden, hoog), crash, taiko."""
    sec = section(b)
    kick, sn, stick, crash, taiko = K['kick'], K['sn'], K['stick'], K['crash'], K['taiko']
    tl, tm, th = K['toms']
    if b == 0:
        drum(P, t0, (0, 6, 12), taiko, 112, D)
        return range(0)
    if b == 1:
        drum(P, t0, (0, 6), taiko, 112, D)
        for k, key in zip(range(8, 16), (th, th, tm, tm, tl, tl, sn, sn)):
            P['drums'].append([t0 + k * S, t0 + (k + 1) * S, key, 96 + 3 * (k - 8)])
        return range(0)
    hats = range(0, 16, 2)
    if sec == 'R1' and b < 6:
        drum(P, t0, (0, 8, 10), kick, 112, D)
        drum(P, t0, (4, 12), sn, 104, D)
        drum(P, t0, (0,), taiko, 104, D)
    elif sec in ('R1', 'R2'):
        drum(P, t0, (0, 8, 10), kick, 116, D)
        drum(P, t0, (4, 12), sn, 110, D)
        drum(P, t0, (0, 6), taiko, 104, D)
    elif sec == 'B':
        drum(P, t0, (0, 6, 8), kick, 114, D)
        drum(P, t0, (4, 12), sn, 108, D)
    else:   # A, C
        drum(P, t0, (0, 6, 8, 10), kick, 114, D)
        drum(P, t0, (4, 12), sn, 108, D)
        if sec == 'C':
            drum(P, t0, (0,), taiko, 104, D)
    if fast_toms and sec in ('A', 'C', 'R2'):            # Meteor: 16en-galop op de toms (hoog-midden) tussen de tellen
        drum(P, t0, (2, 3, 14), th, 94, D)
        drum(P, t0, (10, 11), tm, 94, D)
    if b in SECTION_START:
        drum(P, t0, (0,), crash, 108, D)
    if b in PHRASE_END + (29,):                          # tomroffel (ambient toms: dalend, de grot in)
        P['drums'] = [x for x in P['drums'] if not (t0 + 8 * S <= x[0] < t0 + BAR)]
        seq = (th, th, tm, tm, tl, tl, tl, sn) if not fast_toms else (th, th, th, tm, tm, tm, tl, tl)
        for k, key in zip(range(8, 16), seq):
            P['drums'].append([t0 + k * S, t0 + (k + 1) * S, key, 98 + 3 * (k - 8)])
        hats = range(0, 8, 2)
    return hats


def soft_hats(P, t0, hats, crash_ticks):
    for k in hats:
        t = t0 + k * S
        if t not in crash_ticks:
            P['hat'].append([t, t + 6, 84, 52 if k % 4 == 0 else 36])


# ---------------------------------------------------------------- grot
def cave(O):
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, SN, STICK, TOM_L, TOM_M, TOM_H, CRASH, TAIKO = range(36, 44)
    D = {KICK: 3 * S, SN: 2 * S, STICK: S, TOM_L: 3 * S, TOM_M: 3 * S, TOM_H: 3 * S, CRASH: 6 * S, TAIKO: 4 * S}
    K = dict(kick=KICK, sn=SN, stick=STICK, toms=(TOM_L, TOM_M, TOM_H), crash=CRASH, taiko=TAIKO)
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        if sec in ('R1', 'R2'):
            P['flute'].append([s, min(e, s + 2 * S), n, 116])
        else:
            P['flute'].append([s, e, n, 114 if e - s > 2 * S else 106])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':                                   # chromatische val op de strijkers
            P['str'].append([s, e, n, 100 + (s % BAR) // 24])
        elif sec in ('R1', 'R2'):
            P['str'].append([s, min(e, s + 2 * S), n, 108])
        else:
            P['str'].append([s, e, n - 12 if n >= 72 else n, 100])
    echo_of(P, 'flute', 'echo', vel=92)
    hollow_bass(P, O)
    for b in range(END_BAR):
        t0 = b * BAR
        hats = cave_drums(P, D, K, t0, b)
        cr = {x[0] for x in P['drums'] if x[2] == CRASH}
        soft_hats(P, t0, hats, cr)
    CC['flute'] = [(0, 1, 6), (0, 21, 5)]                 # lichte vibrato
    over = {
        35: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 240, 0, 140',
        73: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 150',
        74: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 140',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_3, 0, 7, 15, 2',
        121: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    }
    kit = [
        ('36 doffe kick', 'voice_directsound 58, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 doffe snare', 'voice_directsound 52, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170'),
        ('38 hyoushigi', 'voice_directsound 56, 72, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 120'),
        ('39 ambient tom laag', 'voice_directsound 48, 52, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180'),
        ('40 ambient tom midden', 'voice_directsound 53, 64, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180'),
        ('41 ambient tom hoog', 'voice_directsound 58, 76, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180'),
        ('42 donker bekken', 'voice_directsound 52, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 160'),
        ('43 taiko diep', 'voice_directsound 46, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
    ]
    layout = [  # (partij, programma, volume, kanaal, pan)
        ('flute', 73, 112, 0, 64),
        ('echo', 74, 64, 1, 88),
        ('str', 48, 84, 2, 44),
        ('bass', 35, 100, 3, 64),
        ('sub', 84, 56, 6, 64),
        ('hat', 121, 32, 10, 64),
    ]
    order = ['flute', 'drums', 'bass', 'str', 'echo']
    return dict(name='cave', title='grot', bpm=188, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=180, brass=())


# ---------------------------------------------------------------- Meteor Falls
def meteor(O):
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, SN, STICK, TOM_L, TOM_M, TOM_H, CRASH, TAIKO, TIMP = range(36, 45)
    D = {KICK: 2 * S, SN: 2 * S, STICK: S, TOM_L: 2 * S, TOM_M: 2 * S, TOM_H: 2 * S, CRASH: 6 * S, TAIKO: 4 * S,
         TIMP: 3 * S}
    K = dict(kick=KICK, sn=SN, stick=STICK, toms=(TOM_L, TOM_M, TOM_H), crash=CRASH, taiko=TAIKO)
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        if sec in ('R1', 'R2'):                          # riff: trompetstoten
            P['tpt'].append([s, min(e, s + 2 * S), n, 120])
        elif sec == 'B':                                 # B: de hoorn draagt de melodie (3+3+2), zoals in het origineel
            P['horn'].append([s, e, n, 118])
        else:                                            # A/C: trompet, hoorn een octaaf eronder
            P['tpt'].append([s, e, n, 116 if e - s > 2 * S else 106])
            P['horn2'].append([s, e, n - 12, 100])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':
            P['tpt'].append([s, e, n, 104 + (s % BAR) // 24])
        elif sec in ('R1', 'R2'):
            P['horn'].append([s, min(e, s + 2 * S), n, 116])
        elif sec == 'B':                                 # lange bovenstem op trompet
            P['tpt'].append([s, e, n, 108])
        else:
            P['str'].append([s, e, n - 12 if n >= 72 else n, 100])
    echo_of(P, 'tpt', 'echo', vel=88, maxlen=2 * S)
    hollow_bass(P, O, vel=116)
    # ontdekking: stijgend glockenspiel-loopje (akkoordtonen in 16en) aan het begin van elke frase
    for b in SECTION_START[:-1]:
        r, _ = CH[b]
        t0 = b * BAR + 8 * S
        for i, iv in enumerate((0, 4, 7, 12, 16, 19)):
            P['glock'].append([t0 + i * S, t0 + (i + 1) * S, 72 + r % 12 + iv - (12 if r >= 7 else 0), 92 + 3 * i])
    for b in range(END_BAR):
        t0 = b * BAR
        hats = cave_drums(P, D, K, t0, b, fast_toms=True)
        if b in SECTION_START or b == 1:
            drum(P, t0, (0,) if b != 1 else (12,), TIMP, 114, D)
        if b in PHRASE_END:
            drum(P, t0, (8,), TIMP, 112, D)
        cr = {x[0] for x in P['drums'] if x[2] == CRASH}
        soft_hats(P, t0, hats, cr)
    over = {
        9: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 180',
        35: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 240, 0, 140',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_3, 0, 7, 15, 2',
        121: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    }
    kit = [
        ('36 kick', 'voice_directsound 62, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 snare', 'voice_directsound 56, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170'),
        ('38 hyoushigi', 'voice_directsound 58, 72, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 120'),
        ('39 tom laag', 'voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('40 tom midden', 'voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('41 tom hoog', 'voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('42 crash', 'voice_directsound 56, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 165'),
        ('43 taiko diep', 'voice_directsound 48, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
        ('44 pauk', 'voice_directsound 43, 64, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200'),
    ]
    layout = [
        ('tpt', 56, 104, 0, 64),
        ('horn', 60, 104, 1, 70),
        ('horn2', 60, 80, 2, 58),
        ('str', 48, 80, 3, 44),
        ('echo', 56, 52, 4, 90),
        ('glock', 9, 76, 5, 84),
        ('bass', 35, 100, 8, 64),
        ('sub', 84, 56, 6, 64),
        ('hat', 121, 34, 10, 64),
    ]
    order = ['tpt', 'horn', 'drums', 'bass', 'horn2', 'str', 'glock', 'echo']
    return dict(name='meteor', title='Meteor Falls', bpm=196, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=180, brass=('tpt', 'horn', 'horn2', 'echo'))


# ---------------------------------------------------------------- Fiery Path
def fiery(O):
    P, CC, EX = Parts(), Parts(), Parts()
    KICK, SN, STICK, TOM_L, TOM_M, TOM_H, CRASH, TAIKO = range(36, 44)
    D = {KICK: 3 * S, SN: 2 * S, STICK: S, TOM_L: 3 * S, TOM_M: 3 * S, TOM_H: 3 * S, CRASH: 6 * S, TAIKO: 4 * S}
    K = dict(kick=KICK, sn=SN, stick=STICK, toms=(TOM_L, TOM_M, TOM_H), crash=CRASH, taiko=TAIKO)
    lead, second = roles(O)
    for s, e, n, v in lead:
        sec = section(bar_of(s))
        if sec == 'I':
            continue
        if sec in ('R1', 'R2'):
            P['organ'].append([s, min(e, s + 2 * S), n, 116])
        else:
            P['organ'].append([s, e, n, 112 if e - s > 2 * S else 104])
    for s, e, n, v in second:
        sec = section(bar_of(s))
        if sec == 'I':
            P['organ'].append([s, e, n, 98 + (s % BAR) // 24])
        elif sec in ('R1', 'R2'):
            P['str'].append([s, min(e, s + 2 * S), n, 108])
        else:
            P['str'].append([s, e, n - 12 if n >= 72 else n, 100])
    echo_of(P, 'organ', 'echo', vel=90, maxlen=2 * S)
    hollow_bass(P, O, vel=114)
    # gloeiende pads: lage distortion (klinkt een octaaf lager: toets 60 = C3), grondtoon per halve maat, zwelt aan
    for b in range(2, END_BAR):
        r, _ = CH[b]
        for h in (0, 1):
            t = b * BAR + h * 8 * S
            P['pad'].append([t, t + 8 * S - 6, 60 + r if r < 7 else 48 + r, 100])
            for i in range(8):
                CC['pad'].append((t + i * S, 7, 44 + 6 * i))
    EX['pad'].append((0, mido.Message('control_change', control=20, value=2)))
    for t in range(0, END_BAR * BAR, 12):                 # hitte-trilling: trage golvende bend
        EX['pad'].append((t, mido.Message('pitchwheel', pitch=int(1600 * math.sin(2 * math.pi * t / BAR)))))
    for b in range(END_BAR):
        t0 = b * BAR
        hats = cave_drums(P, D, K, t0, b)
        if section(b) == 'C' or b in (30, 31):
            drum(P, t0, (8,), TAIKO, 108, D)
        cr = {x[0] for x in P['drums'] if x[2] == CRASH}
        soft_hats(P, t0, hats, cr)
    over = {
        17: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 150',
        18: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 140',
        31: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_low, 40, 0, 255, 150',
        35: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 240, 0, 140',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_3, 0, 7, 15, 2',
        122: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    }
    kit = [
        ('36 doffe kick', 'voice_directsound 60, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 doffe snare', 'voice_directsound 54, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170'),
        ('38 hyoushigi', 'voice_directsound 56, 72, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 120'),
        ('39 ambient tom laag', 'voice_directsound 48, 52, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180'),
        ('40 ambient tom midden', 'voice_directsound 53, 64, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180'),
        ('41 ambient tom hoog', 'voice_directsound 58, 76, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 180'),
        ('42 donker bekken', 'voice_directsound 52, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, 160'),
        ('43 taiko diep', 'voice_directsound 46, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
    ]
    layout = [
        ('organ', 17, 104, 0, 64),
        ('echo', 18, 60, 1, 88),
        ('str', 48, 80, 2, 44),
        ('pad', 31, 76, 3, 56),
        ('bass', 35, 100, 4, 64),
        ('sub', 84, 56, 6, 64),
        ('hat', 122, 32, 10, 64),
    ]
    order = ['organ', 'drums', 'bass', 'pad', 'str', 'echo']
    return dict(name='fiery', title='Fiery Path', bpm=196, P=P, CC=CC, EX=EX, over=over, kit=kit, layout=layout,
                order=order, kit_rel=180, brass=())


# ---------------------------------------------------------------- wegschrijven (zoals regio_theme.build)
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
        last = {}
        for e in sorted(P[k]):
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
        song.add([[a, min(e, end), n, v] for a, e, n, v in P[k] if a < end], pr, vol, ch, pan, extra=EX.get(k, []), ccs=CC.get(k, []))
    song.add(sorted(P['drums']), 127, 112, 9)
    written = {k for k, *_ in spec['layout']} | {'drums'}
    assert not [k for k in P if P[k] and k not in written], [k for k in P if P[k] and k not in written]
    out = 'sound/songs/midi/mus_grounded_vs_wild_%s.mid' % name
    song.save(out, end)
    print('  %s | intro %.1f s | loop %.1f s | totaal %.1f s' % (
        out, LOOP0 * BAR / TPB * 60 / bpm, (end - LOOP0 * BAR) / TPB * 60 / bpm, end / TPB * 60 / bpm))


if __name__ == '__main__':
    O = orig()
    for f in (cave, meteor, fiery):
        build(f(O))
