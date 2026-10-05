#!/usr/bin/env python3
"""Project Grounded: "Battle! Rayquaza" als Balinese gamelan (gong kebyar). Remix van het weather trio-thema
(mus_vs_rayquaza = mus_vs_kyogre_groudon, 196 bpm, C-mineur/chromatisch) op verzoek van Jordi.

Het origineel blijft maat voor maat in dezelfde volgorde staan (40 maten, intro 0-7, loop 8-39); alleen de
instrumenten worden gamelan en er komen gamelanlagen bij:
  - melodie (spoor 1: trompet/strijkers/hoorn)  -> reyong/trompong (ketelgongs), lange noten opnieuw aangeslagen
  - kwint erboven (spoor 2: trompet/strijkers)  -> gangsa (metallofoon, ombak-paar); de fluit (maat 20-23) -> suling
  - lange melodienoten                          -> suling houdt ze aan (gamelan kan niet aanhouden)
  - bas (spoor 3)                               -> jegogan (diepe metallofoon, een octaaf hoger)
  - pauken (spoor 6 + de pauken in 1/2)         -> kendang (handtrommels): laag 'dag', open 'tut', slap 'pek', 'ka'
  - PSG-leads (spoor 4/5)                       -> kotekan: polos (links) + sangsih (rechts), twee in elkaar
                                                  grijpende zestienden in pelog die samen één figuur maken
  - kolotomisch: gong ageng op elke sectiegrens, kempur halverwege, kempli (PSG-golf) op elke tel
  - ceng-ceng (PSG-ruis): 'cek' op de achtsten, roffels en kopyak-klappen op de byar's
Stemming: pelog selisir op de grondtoon R = R, R+1, R+3, R+7, R+8. Op C: C Db Eb G Ab = precies de kerntonen van
het thema (C-C#-G-G#-D#), dus de melodie blijft intact en de kotekan/kempli kleuren alles pelog. Sectie F (maat
16-19): F Gb Ab C Db; sectie Eb (maat 28-31): Eb E Gb Bb B (de E en B van de melodie zitten erin).
Kebyar: byar (unisono-explosie + gong) op maat 0, 8, 20, 28, 32; angsel (plotse stop) vóór 20 en 28; tempo:
intro maat 0-3 statig (0,82), 4-7 versnellend (ngencet) tot 1,12; loop op 1,0; maat 36-39 weer versnellend tot
1,12, zodat de sprong naar het loopbegin precies klinkt als het einde van de intro.

v2 (Jordi: 'pas op 28 s herken ik het nummer, tonen weggevallen; 50-60 s en vanaf 1:10 ook'): in het origineel
dragen in maat 8-19 niet de trompetten maar de pauken (G-C-ostinato, luidste spoor), de G-baspedaal en de twee
PSG-lijnen (melodie een octaaf lager + herhaalde achtsten, kwint erboven, tegenmelodie in 28-31) de herkenning; in
maat 24-31 de octaafachtsten van de bas. v1 had die vervangen door ongestemde conga's, een jegogan op de tellen en de
kotekan in pelog (die bovendien Db/Eb tegen de D/E van het origineel speelde). v2: pauken op gestemde kendangslagen
(G3/C4/Bb3/Eb4), PSG-sporen 1-op-1 terug (kosten geen kanaal), de hele baslijn op een gongbas, kotekan-toonladder
past zich aan de toon van het origineel aan en wijkt in de melodiematen, plus een laag mannenkoor (kwint-tweeklank
in één sample), spookslagen in de kendang en meer gongs.

Samples (eigen, additief met inharmonische partialen, zie gm_samples.py ADDITIVE): rayquaza_gangsa, _reyong,
_jegogan, _gong. Suling = sd90_classical_shakuhachi; kendang = heart_of_asia indian drum + conga's + kotsuzumi.
Voicegroup grounded_rayquaza = grounded_gm met 10-15 gamelan, 75 suling, 112 kempli (golf), 121 ceng-ceng (ruis),
127 = drumsets/rayquaza.inc. Zie tools/grounded/MUZIEK.md. Gebruik: python3 tools/grounded/rayquaza_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, detach, allocate, releases, release_ticks

SRC = 'sound/songs/midi/mus_vs_rayquaza.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_rayquaza.mid'
VG = 'grounded_rayquaza'
TPB, BAR, S16, E8 = 24, 96, 6, 12
BASE_TEMPO = 306122                      # 196 bpm, zoals het origineel
BPM = 196
LOOP_START, END = 8, 40
KOT, GANGSA, REYONG, JEGOG, GONG, KEMPUR, SULING, KEMPLI, CENG, KIT = 10, 11, 12, 13, 14, 15, 75, 112, 121, 127
GBAS, KOOR, PSG_B, PSG_A1, PSG_A2 = 16, 52, 80, 82, 83  # v2: gongbas, laag mannenkoor, de PSG-sporen van het origineel
DAG, TUT, PEK, KA, DAG2 = 36, 37, 38, 39, 40          # drumsets/rayquaza.inc
# v2: gestemde open kendangslagen voor het pauken-ostinato (open conga 222 Hz, gestemd op G3, C4, Bb3, Eb4);
# de 'dag' (indian drum) klinkt zelf al op C3
TG, TC, TBB, TEB = 41, 42, 43, 45
TUNED = {7: TG, 0: TC, 10: TBB, 3: TEB}                 # toonklasse van de pauk -> kendangnoot
KLEN = {DAG: 22, TUT: 10, PEK: 8, KA: 20, DAG2: 26, TG: 10, TC: 10, TBB: 10, TEB: 10}   # lengte van de slag in ticks
# tempo: (maat, factor)
TEMPO = [(0, 0.82), (4, 0.88), (5, 0.96), (6, 1.04), (7, 1.12), (8, 1.0), (36, 1.0), (37, 1.04), (38, 1.08), (39, 1.12)]
GONGS = [0, 3, 8, 12, 16, 20, 24, 28, 32, 36]         # gong ageng (v2: ook halverwege de secties)
KEMPURS = [1, 2, 10, 14, 18, 22, 26, 30, 34, 38]
BYARS = [0, 8, 20, 28, 32]
ANGSEL = [19, 27]                                      # plotse stop op tel 4, dan byar


def root_of(bar):
    if 16 <= bar < 20:
        return 5          # F
    if 28 <= bar < 32:
        return 3          # Eb
    return 0              # C


def pelog(root, lo, hi):
    pcs = {(root + d) % 12 for d in (0, 1, 3, 7, 8)}
    return [n for n in range(lo, hi + 1) if n % 12 in pcs]


def snap(n, scale):
    return min(scale, key=lambda x: (abs(x - n), x))


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().rstrip('\n').split('\n')
    lines[0] = '@ Project Grounded: grounded_gm met gamelan voor Battle! Rayquaza. Gegenereerd door tools/grounded/rayquaza_theme.py.'
    lines[1] = ('@ 10 kotekan-gangsa (gedempt), 11 gangsa, 12 reyong, 13 jegogan, 14 gong ageng, 15 kempur, 16 gongbas, '
                '52 laag koor, 75 suling, 80/82/83 PSG-leads van het origineel, 112 kempli, 121 ceng-ceng, 127 kendang.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        10: 'voice_directsound 60, 0, DirectSoundWaveData_rayquaza_gangsa, 255, 0, 255, 140',   # v2: droger (175 -> 140)
        11: 'voice_directsound 60, 0, DirectSoundWaveData_rayquaza_gangsa, 255, 0, 255, 226',
        12: 'voice_directsound 60, 0, DirectSoundWaveData_rayquaza_reyong, 255, 0, 255, 228',
        13: 'voice_directsound 60, 0, DirectSoundWaveData_rayquaza_jegogan, 255, 0, 255, 232',
        14: 'voice_directsound 60, 0, DirectSoundWaveData_rayquaza_gong, 255, 0, 255, 220',
        15: 'voice_directsound 60, 0, DirectSoundWaveData_rayquaza_gong, 255, 0, 255, 220',
        75: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_shakuhachi, 255, 0, 255, 200',
        112: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 1, 0, 0',
        121: 'voice_noise_alt 60, 0, 0, 0, 1, 5, 2',
        GBAS: 'voice_directsound 60, 0, DirectSoundWaveData_rayquaza_gongbass, 255, 0, 255, 180',
        KOOR: 'voice_directsound 60, 0, DirectSoundWaveData_rayquaza_choir, 40, 0, 255, 215',
        # de PSG-leads van het origineel (vs_kyogre_groudon.inc), ongewijzigd: kosten geen DirectSound-kanaal
        PSG_B: 'voice_square_2 60, 0, 3, 0, 1, 7, 1',
        PSG_A1: 'voice_square_1 60, 0, 0, 3, 0, 1, 7, 1',
        PSG_A2: 'voice_square_1 60, 0, 0, 3, 0, 0, 7, 1',
        127: 'voice_keysplit_all voicegroup_rayquaza_drumset',
    }
    out = []
    for l in lines:
        if l.startswith('\t') and '@' in l:
            prog = int(l.rsplit('@', 1)[1])
            if prog in repl:
                l = '\t%s  @ %d' % (repl[prog], prog)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out) + '\n')
    kit = [   # vanaf noot 36; alles DirectSound
        'voice_directsound_no_resample 60, 54, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 0',  # 36 dag
        'voice_directsound 56, 74, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                      # 37 tut
        'voice_directsound_no_resample 60, 76, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 40',         # 38 pek
        'voice_directsound 55, 60, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 60',                   # 39 ka
        'voice_directsound 55, 50, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 0',              # 40 dag laag
        'voice_directsound 58, 52, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                      # 41 G3
        'voice_directsound 63, 76, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                      # 42 C4
        'voice_directsound 61, 52, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                      # 43 Bb3
        'voice_directsound 55, 60, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 0',              # 44 (ongebruikt)
        'voice_directsound 66, 76, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                      # 45 Eb4
    ]
    open('sound/voicegroups/drumsets/rayquaza.inc', 'w').write(
        '@ Project Grounded: kendang-drumkit voor Battle! Rayquaza (rayquaza_theme.py): 36 dag (wadon, laag open),\n'
        '@ 37 tut (open), 38 pek (slap), 39 ka (hoog), 40 dag laag, 41-45 gestemde open slagen G3/C4/Bb3/-/Eb4 (het pauken-ostinato).\n'
        'voice_group rayquaza_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


def active(ev, t):
    return [e for e in ev if e[0] <= t < e[1]]


def build():
    voicegroup()
    src = mido.MidiFile(SRC)
    assert src.ticks_per_beat == TPB
    T = {i: notes_of(src.tracks[i]) for i in range(1, 7)}
    bar = lambda t: t // BAR
    P = {k: [] for k in ('reyong', 'gangsa', 'suling', 'jegog', 'gong', 'kempur', 'kendang', 'polos', 'sangsih',
                         'kempli', 'ceng', 'byar', 'bas', 'koor', 'psg_a', 'psg_b', 'ghost')}

    # ---- melodie en harmonie (bron 1-op-1, andere instrumenten) ------------------------------------------------
    for s, e, n, v in T[1]:
        b = bar(s)
        if b < 8 and b >= 4 or b >= 32:       # pauken (G2) in spoor 1 -> gestemde kendang op G
            P['kendang'].append([s, s + KLEN[TG], TG, 108 + (10 if s % 48 == 0 else 0)])
            continue
        if b < 4:                              # buisklok C3 -> byar (hieronder)
            continue
        vel = 118
        P['reyong'].append([s, s + min(e - s, 20), n, vel])
        if e - s >= 72:                        # lange noot: om de halve noot opnieuw aanslaan (gamelan houdt niet aan)
            for t in range(s + 48, e - 12, 48):
                P['reyong'].append([t, t + 16, n, 84])
            if not 20 <= b < 28:               # (maat 20-27: suling speelt de fluitmelodie uit spoor 2)
                P['suling'].append([s, e, n + 12 if n + 12 <= 84 else n, 100])
    for s, e, n, v in T[2]:
        b = bar(s)
        if b < 4:
            continue
        prog_flute = 20 <= b < 24
        if b >= 32:
            if s % BAR == 0 and n >= 60:       # buisklok C5 op de maatslag -> byar
                continue
            P['kendang'].append([s, s + KLEN[DAG2 if n < 45 else KA], DAG2 if n < 45 else KA, 100])
            continue
        if prog_flute:
            P['suling'].append([s, e, n, 112])
        else:
            P['gangsa'].append([s, s + min(e - s, 24), n, 112])
            if 24 <= b < 28 and e - s >= 72:
                P['suling'].append([s, e, n, 104])
    # bas -> jegogan (een octaaf hoger)
    # jegogan speelt traag (pokok): alleen de basnoten op de tel; de achtste-ostinato's (maat 24-31) op de tellen
    beats = [x for x in T[3] if x[0] % 48 == 0]     # v2: alleen op tel 1 en 3 (de gongbas speelt de hele lijn)
    for s, e, n, v in beats:
        if 24 <= bar(s) < 32:
            continue                           # v2: daar speelt de gongbas de octaafachtsten
        nxt = min([x[0] for x in beats if x[0] > s] + [s + 48])
        P['jegog'].append([s, s + min(40, nxt - s), n + 12, 104])
    # v2: de originele baslijn volledig (ook de octaafachtsten van maat 24-31) op de gongbas, in de originele ligging
    for s, e, n, v in T[3]:
        nxt = min([x[0] for x in T[3] if x[0] > s] + [s + 96])
        ln = min(e - s, nxt - s, 10 if 24 <= bar(s) < 32 else 96)    # octaafachtsten: kort (1 kanaal + uitklinken)
        P['bas'].append([s, s + ln, n, 127 if s % BAR == 0 and bar(s) in BYARS else 112])
    # v2: de PSG-sporen van het origineel 1-op-1 terug (spoor 5: melodie een octaaf lager + de herhaalde achtsten onder
    # de lange noten; spoor 4: kwint-verdubbeling, de Db5 in maat 23/27 en de tegenmelodie van maat 28-31). In v1 waren
    # die vervangen door de kotekan; daardoor vielen de herkenbare begeleidingsfiguren weg.
    for s, e, n, v in T[5]:
        P['psg_a'].append([s, e, n, v])
    for s, e, n, v in T[4]:
        if bar(s) >= 8:
            P['psg_b'].append([s, e, n, v])
    # v2: laag mannenkoor (kwint-tweeklank in één sample), parallel aan de melodie/harmonie van het origineel
    def koor(b, t0, t1, root, vel):
        P['koor'].append([b * BAR + t0, b * BAR + t1, root, vel])
    for b in range(0, 4):                          # intro: elke klokslag een 'aah' die aanzwelt
        koor(b, 0, 84, 48, 92 + 8 * b)
    for b in range(4, 8):                          # pauken-ostinato: C-pedaal, crescendo naar de byar
        koor(b, 0, 48, 48, 88 + 6 * (b - 4)); koor(b, 48, 96 if b < 7 else 72, 48, 92 + 6 * (b - 4))
    long8 = {9: 43, 11: 51, 13: 43, 15: 52, 17: 48, 19: 44}   # lange melodienoot (G, Eb, G, E | C, Ab), kwint erboven = spoor 2
    for b in range(8, 20):
        r = 48 if b < 16 else 53                   # C / F
        if b % 2 == 0:
            koor(b, 0, 72, r, 100); koor(b, 72, 96, r + 1, 104)
        else:
            koor(b, 0, 24, r + 1, 104); koor(b, 24, 96 if b != 19 else 72, long8[b], 108)
    for b in range(20, 28):                        # C (G-C / C-G) en Db (Ab / Db)
        koor(b, 0, 96 if b != 27 else 72, 48 if b % 2 == 0 else 49, 104)
    for b in range(28, 32):                        # Eb / E
        koor(b, 0, 96, 51 if b % 2 == 0 else 52, 108)
    for b in range(32, 40):                        # break: C-pedaal, versnelling: aanzwellen
        v = 96 if b < 36 else 100 + 6 * (b - 36)
        koor(b, 0, 48, 48, v); koor(b, 48, 96 if b != 39 else 72, 48, v)
    # pauken (spoor 6) -> kendang; intro maat 0-3: gong/kempur (hieronder)
    for s, e, n, v in T[6]:
        if bar(s) < 4:
            continue
        # v2: het G-C-ostinato van de pauken klinkt weer op toonhoogte (in v1: ongestemde conga's -> onherkenbaar);
        # intro/break: de C3-slagen op de 'dag' (C3), met een slap op tel 1 en 3
        k = TUNED[n % 12]
        if bar(s) < 8 or bar(s) >= 32:
            k = DAG if s % 48 else PEK
        P['kendang'].append([s, s + KLEN[k], k, 104 + (12 if s % 24 == 0 else 0)])
    # crash-zwelling (spoor 4, maat 0-3) -> ceng-ceng-roffel die aanzwelt naar de volgende byar
    for b in range(4):
        for i in range(4, 16):
            t = b * BAR + i * S16
            P['ceng'].append([t, t + 4, 84, 30 + i * 5])

    # ---- byar's: unisono-explosie van alles + kopyak + gong --------------------------------------------------
    def byar(t, top, vel=124):
        P['byar'] += [[t, t + 14, top, vel], [t, t + 14, top - 12, vel]]
        P['ceng'].append([t, t + 24, 78, 127])
    for b in BYARS + [1, 2, 3]:
        byar(b * BAR, 72 if root_of(b) == 0 else 72 + root_of(b) - 12 * (root_of(b) > 6), 124 if b in BYARS else 112)
    # intro: gangsa-loopjes in pelog na elke slag (maat 0-2), steeds langer en hoger
    sc = pelog(0, 60, 88)
    for b, (start16, top) in enumerate([(12, 79), (8, 80), (8, 84)]):
        idx = sc.index(snap(top, sc))
        for k, i in enumerate(range(start16, 16)):
            t = b * BAR + i * S16
            n = sc[idx - (k % 4) - (k // 4)]
            P['byar'].append([t, t + 5, n, 92 + k * 3])
    # maat 3: tremolo op C (ngerincik), aanzwellend
    for i in range(8, 16):
        t = 3 * BAR + i * S16
        P['byar'].append([t, t + 5, 72 + (7 if i % 2 else 0), 70 + i * 3])

    # angsel: alles stopt op tel 4 na een unisono-klap
    for b in ANGSEL + [7, 39]:
        t = b * BAR + 72
        P['byar'] += [[t, t + 8, 79, 120], [t + 12, t + 20, 79, 124], [t + 12, t + 20, 67, 124]]
        P['ceng'] += [[t, t + 6, 80, 110], [t + 12, t + 24, 78, 124]]

    # ---- kolotomisch: gong ageng, kempur, kempli ---------------------------------------------------------
    for i, b in enumerate(GONGS):
        nxt = GONGS[i + 1] if i + 1 < len(GONGS) else END
        P['gong'].append([b * BAR, b * BAR + min(2 * BAR, (nxt - b) * BAR - 4), 36 + root_of(b), 127])
    for b in KEMPURS:
        r = root_of(b)
        n = 36 + (r + 7) % 12                  # kwint van de grondtoon, G2-F#3
        P['kempur'].append([b * BAR, b * BAR + BAR, n + 12 if n < 42 else n, 110])
    for b in range(4, END):
        for beat in range(4):
            t = b * BAR + beat * TPB
            P['kempli'].append([t, t + 4, 72, 90 if beat in (0, 2) else 70])

    # ---- kotekan: polos + sangsih in pelog (maat 6-31 en 36-39) -----------------------------------------------
    def scale_at(t):
        # v2: pelog, maar een toon van het origineel die er niet in zit (D, E, B, Bb ...) vervangt de pelogtonen een
        # halve toon ernaast; anders botst de kotekan (Db/Eb tegen de D van spoor 2) en klinkt de melodie 'vals'
        b = bar(t)
        pcs = {(root_of(b) + d) % 12 for d in (0, 1, 3, 7, 8)}
        srcs = [T[2], T[5], T[4]] + ([T[1], T[3]] if 8 <= b < 32 else [])
        for e in [x for tr in srcs for x in active(tr, t)]:
            pc = e[2] % 12
            if pc not in pcs:
                pcs -= {(pc + 1) % 12, (pc - 1) % 12}
                pcs.add(pc)
        return [n for n in range(67, 87) if n % 12 in pcs]

    def pokok(t):
        b = bar(t)
        sc = scale_at(t)
        on = active(T[2], t) or active(T[1], t)
        n = max(x[2] for x in on) if on and b >= 8 else 72 + root_of(b)
        while n < 70:
            n += 12
        while n > 84:
            n -= 12
        return sc, sc.index(snap(n, sc))
    kot_bars = list(range(6, 32)) + list(range(36, 40))
    for b in kot_bars:
        for beat in range(4):
            t0 = b * BAR + beat * TPB
            if b in ANGSEL + [7, 39] and beat == 3:
                continue                                   # angsel: stilte
            if b in BYARS and beat == 0:
                continue                                   # byar: eerst de klap laten uitgalmen
            sc, k = pokok(t0)
            _, q = pokok(t0 + TPB)
            last = q - 1 if q > k else q + 1 if q < k else k + (1 if beat % 2 == 0 else -1)
            fig = [k, k + 1, k - 1, last] if beat % 2 == 0 else [k, k - 1, k + 1, last]
            fig = [max(0, min(len(sc) - 1, x)) for x in fig]
            if b < 8:
                base = 54 + (b - 6) * 26 + beat * 6        # binnenkomen: aanzwellen
            elif b >= 36:
                base = 84 + (b - 36) * 9
            elif 8 <= b < 20 and b % 2 == 0:
                base = 70                                  # v2: maat met de melodie-aanslagen: kotekan op de achtergrond
            elif 28 <= b < 32:
                base = 80                                  # v2: ruimte voor de tegenmelodie (spoor 4)
            else:
                base = 96 if b >= 20 else 88
            for i, x in enumerate(fig):
                t = t0 + i * S16
                part = 'polos' if i % 2 == 0 else 'sangsih'
                P[part].append([t, t + 5, sc[x], min(127, base + (14 if i == 0 else 0))])

    # ---- ceng-ceng: 'cek' op de achtsten in de loop, zestienden in de break en de versnelling ------------------
    for b in range(8, END):
        for i in range(16):
            t = b * BAR + i * S16
            if b in ANGSEL + [39] and i >= 12:
                continue
            if 32 <= b < 36 and i % 2 == 0 or b >= 36 or i % 4 == 2:
                P['ceng'].append([t, t + 3, 84, 64 + (20 if i % 4 == 2 else 0)])
    for b in range(4, 8):
        for i in range(16):
            if (b >= 6 or i % 4 == 2) and not (b == 7 and i >= 12):
                t = b * BAR + i * S16
                P['ceng'].append([t, t + 3, 84, 44 + (b - 4) * 12 + (16 if i % 4 == 2 else 0)])
    # kendang-roffel naar de byar's (maat 7, 19, 27, 39 tel 3)
    for b in (7, 19, 27, 39):
        for i in range(8, 12):
            t = b * BAR + i * S16
            P['kendang'].append([t, t + KLEN[KA], KA if i % 2 else PEK, 96 + i * 2])

    # v2: meer drive: spookslagen op de laatste zestiende van elke tel (en in maat 24-31 ook op de tweede)
    for b in range(8, 32):
        for i in range(16):
            if b in ANGSEL and i >= 8:
                continue
            if i % 4 == 3 or (b >= 24 and i % 4 == 1):
                t = b * BAR + i * S16
                P['ghost'].append([t, t + KLEN[PEK], PEK, 72 if i % 4 == 3 else 62])
    # kendang zwijgt op de eerste tel van een byar; de roffels gaan voor op wat er op dezelfde tick valt
    P['kendang'] = [e for e in P['kendang'] if not (bar(e[0]) in BYARS and e[0] % BAR < TPB)]
    rolls = {e[0] for e in P['kendang'] if e[2] == KA and e[0] % BAR >= 48 and bar(e[0]) in (7, 19, 27, 39)}
    P['kendang'] = [e for e in P['kendang'] if e[0] not in rolls or e[2] in (KA, PEK) and e[3] >= 96 + 16]
    for k in P:
        P[k] = dedupe(P[k])
    P['ceng'] = mono(P['ceng'])       # één ruiskanaal: geen overlap
    P['kempli'] = mono(P['kempli'])

    # ---- stemverdeler (11 DirectSound-noten: legendary) -------------------------------------------------------
    rel = releases(VG)
    progs = {'reyong': REYONG, 'gangsa': GANGSA, 'byar': GANGSA, 'suling': SULING, 'jegog': JEGOG, 'gong': GONG,
             'kempur': KEMPUR, 'polos': KOT, 'sangsih': KOT, 'bas': GBAS, 'koor': KOOR}
    tail = {k: release_ticks(rel.get(p, 200), TPB, BPM * 1.12) for k, p in progs.items()}
    tail['kendang'] = tail['ghost'] = 1
    for k in ('suling', 'jegog', 'reyong', 'gangsa', 'bas', 'koor'):   # eenstemmige lijnen: de vorige noot laat op tijd los
        P[k] = detach(P[k], tail[k])
    order = ['reyong', 'gong', 'byar', 'suling', 'gangsa', 'bas', 'koor', 'kendang', 'jegog', 'kempur', 'polos', 'sangsih', 'ghost']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=11)
    print('tail (ticks):', tail)
    for k in order:
        n = len(ds[k])
        print('  %-8s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        P[k] = kept[k]

    # ---- wegschrijven ------------------------------------------------------------------------------------------
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    ev = [(0, 0, mido.MetaMessage('time_signature', numerator=4, denominator=4))]
    ev += [(b * BAR, 1, mido.MetaMessage('set_tempo', tempo=int(BASE_TEMPO / f))) for b, f in TEMPO]
    ev += [(LOOP_START * BAR, 2, mido.MetaMessage('marker', text='[')), (END * BAR, 3, mido.MetaMessage('marker', text=']'))]
    last = 0
    for t, _, m in sorted(ev, key=lambda x: (x[0], x[1])):
        cond.append(m.copy(time=t - last))
        last = t
    out.tracks.append(cond)
    layout = [  # partij, programma, volume, kanaal, pan, extra CC's
        ('reyong', REYONG, 110, 0, 54, []), ('gangsa', GANGSA, 100, 1, 76, []), ('byar', GANGSA, 104, 2, 64, []),
        ('suling', SULING, 92, 3, 70, [(21, 18), (1, 3)]), ('jegog', JEGOG, 112, 4, 64, []),
        ('gong', GONG, 127, 5, 64, []), ('kempur', KEMPUR, 100, 6, 58, []),
        ('polos', KOT, 82, 7, 36, []), ('sangsih', KOT, 82, 8, 92, []),
        ('kendang', KIT, 100, 9, 64, []), ('kempli', KEMPLI, 52, 10, 64, []), ('ceng', CENG, 46, 11, 70, []),
        ('bas', GBAS, 127, 12, 64, []), ('koor', KOOR, 124, 13, 64, []),
        ('psg_a', PSG_A1, 120, 14, 112, []), ('psg_b', PSG_B, 120, 15, 16, []),
    ]
    extra = {'psg_a': src_events(src.tracks[5]), 'psg_b': src_events(src.tracks[4], LOOP_START * BAR)}
    P['kendang'] = sorted(P['kendang'] + P.pop('ghost'))   # spookslagen (laagste prioriteit) op het kendangspoor
    for k in P:                                   # naadloze loop: geen noot over de loopgrens
        P[k] = [[a, min(b, END * BAR), n, v] for a, b, n, v in P[k] if a < END * BAR]
    for k, prog, vol, ch, pan, ccs in layout:
        out.tracks.append(note_track(P[k], prog, vol, ch, pan, ccs, extra.get(k, ())))
    written = {x[0] for x in layout}
    assert not [k for k in P if P[k] and k not in written], 'partij berekend maar niet weggeschreven'
    out.save(OUT)
    secs = lambda b0, b1: sum(60 / (BPM * f_at(b)) * 4 for b in range(b0, b1))
    print(OUT, '%.1f s intro, %.1f s loop, %d sporen' % (secs(0, LOOP_START), secs(LOOP_START, END), len(out.tracks) - 1))


def f_at(b):
    return [f for bb, f in TEMPO if bb <= b][-1]


def mono(ev):
    ev = sorted(ev)
    for a, b in zip(ev, ev[1:]):
        a[1] = min(a[1], b[0])
    return [e for e in ev if e[1] > e[0]]


def note_track(notes, prog, vol, ch, pan, ccs, extra=()):
    """extra: [(tick, mido.Message)] (programma- en CC-wissels uit de bron), na de note-offs en vóór de note-ons."""
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    for c, v in ccs:
        t.append(mido.Message('control_change', channel=ch, control=c, value=v, time=0))
    msgs = sorted([(s, 2, i, n, v) for i, (s, e, n, v) in enumerate(notes)] + [(e, 0, i, n, 0) for i, (s, e, n, v) in enumerate(notes)]
                  + [(tk, 1, i, m, 0) for i, (tk, m) in enumerate(extra)], key=lambda x: x[:3])
    last = 0
    for tk, kind, _, n, v in msgs:
        if kind == 1:
            t.append(n.copy(channel=ch, time=tk - last))
        else:
            t.append(mido.Message('note_on' if kind else 'note_off', channel=ch, note=n,
                                  velocity=max(1, min(127, int(v))) if kind else 0, time=tk - last))
        last = tk
    return t


def src_events(track, t0=0):
    """Programma- en CC-wissels (behalve volume) uit een bronspoor vanaf tick t0, in de originele volgorde."""
    out, t = [], 0
    for m in track:
        t += m.time
        if t >= t0 and (m.type == 'program_change' or m.type == 'control_change' and m.control != 7):
            out.append((t, m))
    return out


if __name__ == '__main__':
    build()
