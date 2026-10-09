#!/usr/bin/env python3
"""Project Grounded: Battle! Mitch v3, een eigen compositie: duistere, epische Pokémon-baasgevecht x Chase & Status-DnB.

Jordi over v2: 'het stuk vanaf 1:00 (wobble + two-step + thema) heeft de juiste sfeer, maar het geheel klinkt als
drukke, snelle chiptune / happy hardcore. Neem die groove als basis, schrap de hoge loopjes (less is more), leads 1-2
octaven lager, korte staccato brass stabs / dreigende arpeggio's, strakke 172 bpm two-step met een meedogenloze droge
snare + ducking, lage rauwe reese met portamento (stoten op de off-beat of lange dreigende noten), intro -> build-up
(roffel 8sten -> 16den + riser) -> 1 tel stilte -> drop.'

v3: 172 bpm (TEMPO 86), F-klein. 1 tel = 20,8 frames, 1 maat = 1,40 s. Alles wat piepte is weg: geen PSG-lead, geen
16den-loopjes, geen chromatische stinger, geen luchthoorn/rewind. PSG alleen voor de sub (golf) en de riser (ruis).
  Drums (eigen kit, alles DirectSound): K . . . S . . g . . K . S . . g  (kick 1 en 3-en, snare 2 en 4, ghosts op
    2.75 en 4.75), hihats in 16den met accent op de 'en'. Kick = korte felle punch (mitch3_kick), snare = droge klap
    (mitch3_snare) op een eigen spoor op vol volume.
  Ducking: op elke snare zakt het spoorvolume (CC7) van reese, sub, koper, arpeggio en pad naar 30% en komt in een
    16de terug (30 -> 55 -> 80 -> 100%): de klap snijdt door de mix.
  Bas: rauwe reese (mitch_reese_raw/_raw_dark) F1-F2 met portamento (pitch bend vanaf de vorige noot), om en om een
    lange dreigende noot en een maat off-beat-stoten; in drop B de wobble (mitch3_wob_*, v4: mitch4_wob_*, op 172 bpm) = de groove van
    v2 rond 1:00. PSG-sub eronder.
  Lead: koperstoten in octaven (mitch3_brass_lo/hi, F3-C5 = 1-2 octaven lager dan v2), staccato, 3-3-2-ritmes.
  Arpeggio: donkere pluk (mitch3_pluck) in achtsten, C3-Ab4.

Intro (8 maten, 11,2 s)
  0-3   laag motief: koper (thema maat 1-4), lange reese + sub, alleen kicks (1 en 3-en), hihats in achtsten
  4-7   build-up: snareroffel 8sten (4-5) -> 16den (6-7), ruisriser, reese glijdt een octaaf omhoog, kicks verdichten;
        de laatste tel van maat 7 is stil
Loop (48 maten, 67,0 s)
  8-23  DROP A: two-step, reese (lang / off-beat-stoten), koperthema (2x 8 maten; de tweede keer met arpeggio)
  24-27 break: motief, pad, reese, sub (kick-skelet)
  28-31 build-up (= 4-7)
  32-47 DROP B: wobble-bas, arpeggio; 32-39 koperroepen (oneven maten), 40-47 het hele thema + ride
  48-51 break (= 0-3, met pad)
  52-55 build-up (= 4-7), terug naar maat 8
Max. 10 DirectSound-noten (gewone trainer): snare > kick > koper > reese > hihats > crash > ghost > arpeggio > pad.
Voicegroup grounded_mitch = grounded_gm + eigen samples (mitch_samples.py) + eigen drumkit (drumsets/mitch.inc).
v4 (Jordi over v3: 'ritme en structuur ECHT spot-on Chase & Status, we zijn er bijna; maak er een headbang-banger
van'): noten, ritme en vorm exact v3 (diff per spoor: alleen klank, volume en CC's). (1) De wobble ('wowowow', drop B
vanaf 0:45) op nieuwe samples mitch4_wob_* (ontstemde zaagtanden + distortion vóór een diep, snel resonant filter-LFO
+ pitch-LFO, luid begrensd) en het reese-spoor op CC7 118 i.p.v. 80 zolang een wobble klinkt. (2) Kick en snare
keihard en droog (mitch4_kick: harde klik + tik, mitch4_snare: korte crack, gegate) en de kick op CC7 127;
ducking (sidechain) nu op elke kick én snare, dieper: snare 20 -> 50 -> 80 -> 100%, kick 30 -> 60 -> 85 -> 100%.
De rest (koper, hihats, bekkens, arpeggio, pad) iets zachter, zodat de mixer niet overloopt.
Gemeten in de game (solo via volX): wobble t.o.v. al de rest in drop B -1,3 dB (v3 ±-7 dB: sample +3 dB, CC7 +3,4 dB);
kick+snare in de 30 ms na de slag +10,5 dB boven de (geduckte) rest. midi.cfg -V088 (was -V070; -V100 liep over
op de roffel-einden): recpcm 0 overlopen, piek 92/127.
v5 (Jordi over v4: 'wauw, heel vet, 95%; alleen nog de mix: bas moet baas zijn'): opbouw, tempo, noten, programma's
en drums exact v4 (diff per MIDI-spoor: alleen CC7/ducking; daarnaast nieuwe samples). (1) De hoge koperlead 25%
zachter (CC7 92 -> 69); reese en wobble op nieuwe, vollere samples (mitch5_reese_raw(_dark), mitch5_wob_*: vollere
grondtoon, +laag-midden rond 220 Hz, lagere crest = +3..6 dB bij dezelfde piek), CC7 reese 80 -> 60, wobble 118 -> 110
(netto ±+4 en +2,5 dB), PSG-sub 60 -> 84. (2) Kick en snare op mitch5_kick (dieper, harder) en mitch5_snare (de
ruis-crack ±1,4x, tanh x11, gate na 40 ms; RMS +3 dB); hihats 88 -> 76, bekkens 84 -> 72, arpeggio 52 -> 44, pad
50 -> 44. (3) Ducking korter en dieper: snare 10 -> 50 -> 100% in 10 ticks, kick 15 -> 55 -> 100% (1-2 frames).
Balans afgesteld met solo-opnames in de game (recpcm, volX = 0) en offline gemengd met gains (lineair, gecontroleerd:
som van de solo's = de mix, r = 0,996); zie MUZIEK.md (Log, Mitch v5). midi.cfg -V066 (Jordi hoorde v4 op -V070).
v6 (Mitch zelf: 'die horn sound klinkt heel low quality ... maak hem misschien meer screechy/high pitched zoals de
E4 theme'): noten, ritme, vorm, wobbles en mix exact v5; alleen het koper is nieuw (mitch_samples.py, brass6). Eén
sample per lead-noot (F3-C5, 12 stuks) op de mixfrequentie 21.024 Hz, zodat de game niets transponeert (v5: één
Eb4-sample op 22.050 Hz tot C5 omhoog: alles boven ±6 kHz vouwde terug), vervorming op 8x de samplerate, aanzet uit
FluidR3 + een strikt periodieke loop (geen 8-bit-staart die naar 0 korrelt); de envelope zit in de voicegroup.
Ruis/aliasing in de toon (gesimuleerde GBA-weergave, 8 bit + lineaire interpolatie): v5 -10..-15 dB, v6 -27..-31 dB.
Twee varianten (BRASS_VARIANT): 'a' = dezelfde klank als v5 maar schoon; 'b' (standaard) = à la Elite Four: de
sc88pro-trompet uit vs_elite_four heeft hetzelfde spectrum als FluidR3-trompet 56 (vlak tot de 8e harmonische),
die een octaaf hoger bovenop (E4 speelt zijn hoorns rond D5-Bb5), de geschreven noot als body, feller vervormd
(zwaartepunt ±1,1-1,8 kHz i.p.v. 0,4-1,5 kHz).
Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/mitch_theme.py [a|b]"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_mitch.mid'
VG = 'grounded_mitch'
TPB, BPM = 96, 172
S = TPB // 4                 # zestiende
E = TPB // 2                 # achtste
BAR = TPB * 4
MAX_VOICES = 10              # gewone trainer

# programma's (voicegroup grounded_mitch)
REESE = {'raw': 32, 'dark': 33}
WOB = {29: 34, 36: 35, 37: 36, 39: 37}                    # grondtoon -> wobble-sample (172 bpm)
PLUCK, PAD_MIN, PAD_MAJ = 40, 41, 42
# v6: koper = één sample per noot (mitch6<variant>_brass_<noot>, programma 43-54); 38/39 (v3-v5) zijn weg
BRASS_VARIANT = sys.argv[1] if len(sys.argv) > 1 else 'b'
BRASS_NOTES = (53, 55, 56, 58, 60, 61, 63, 64, 65, 67, 68, 72)          # = BRASS6_NOTES in mitch_samples.py
BRASS_PROG = {nt: 43 + i for i, nt in enumerate(BRASS_NOTES)}
SUB, RISER, DRUMS = 84, 121, 127
# drumkit (drumsets/mitch.inc, vanaf 36): naam, sample, release, lengte (ticks; ±de samplelengte)
KIT = [
    ('KICK', 'mitch5_kick', 150, 44),
    ('SNARE', 'mitch5_snare', 140, 52),
    ('GHOST', 'mitch3_ghost', 120, 20),
    ('HAT', 'mitch_hat', 110, 16),
    ('RIDE', 'mitch_ride', 170, 48),
    ('CRASH', 'trinity_cymbal_crash', None, TPB + E),
    ('REVCYM', 'mitch_revcym', 120, 440),
]
for i, (nm, *_) in enumerate(KIT):
    globals()[nm] = 36 + i
KITLEN = {36 + i: k[3] for i, k in enumerate(KIT)}

INTRO = 8
LOOP_START, LOOP_END = INTRO * BAR, 56 * BAR
NOTE = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def n(name):
    """'F1' -> 29, 'Ab4' -> 68"""
    return NOTE[name[:-1]] + 12 * (int(name[-1]) + 1)


CHORDS = {'Fm': ('F', 'min'), 'Db': ('Db', 'maj'), 'Eb': ('Eb', 'maj'), 'C': ('C', 'maj')}
DROP_CH = ['Fm', 'Fm', 'Db', 'Eb', 'Fm', 'Fm', 'Db', 'C']
BASS_ROOT = {'Fm': 'F1', 'Db': 'Db2', 'Eb': 'Eb2', 'C': 'C2'}
# v5: lead (koper) -25%, reese/wobble/sub luider, arpeggio/pad/hihats/bekkens iets terug (v4: reese 80, wob 118,
# brass 92, arp 52, pad 50, sub 60, hats 88, cym 84)
VOL = {'reese': 60, 'wob': 110, 'brass': 69 if BRASS_VARIANT == 'b' else 86, 'arp': 44, 'pad': 44, 'sub': 84, 'hats': 76, 'cym': 72}
# v5: korter en dieper (1-2 frames; 1 frame = 4,6 ticks op 172 bpm). v4: snare 20->50->80->100% in 32 ticks,
# kick 30->60->85->100% in 26 ticks
DUCK = [(0, 0.10), (5, 0.50), (10, 1.0)]                                 # ducking na elke snare (ticks, factor)
DUCK_K = [(0, 0.15), (5, 0.55), (10, 1.0)]                               # en na elke kick


def t(bar, pos=0):
    return bar * BAR + int(pos * S)


# ---------------- het thema (koper): per maat (16de, lengte, noot); nooit op 4 en 12 (daar klapt de snare)
MEL_A = [
    [(0, 2, 'F3'), (3, 2, 'F3'), (6, 2, 'Ab3'), (8, 2, 'C4'), (11, 2, 'Ab3'), (14, 2, 'G3')],
    [(0, 3, 'F3'), (8, 2, 'Eb4'), (10, 2, 'Db4'), (13, 1, 'C4'), (14, 2, 'Ab3')],
    [(0, 2, 'Db4'), (3, 2, 'Db4'), (6, 2, 'F4'), (8, 2, 'Ab4'), (11, 2, 'F4'), (14, 2, 'Eb4')],
    [(0, 3, 'Eb4'), (6, 2, 'Bb3'), (8, 2, 'G3'), (10, 1, 'Bb3'), (11, 2, 'Eb4'), (14, 2, 'G4')],
    [(0, 2, 'F4'), (3, 2, 'F4'), (6, 2, 'Ab4'), (8, 2, 'C5'), (11, 2, 'Ab4'), (14, 2, 'G4')],
    [(0, 3, 'F4'), (8, 2, 'Eb4'), (10, 2, 'Db4'), (13, 1, 'C4'), (14, 2, 'Ab3')],
    [(0, 2, 'Db4'), (3, 2, 'C4'), (6, 2, 'Ab3'), (8, 2, 'F3'), (10, 2, 'Ab3'), (13, 1, 'C4'), (14, 2, 'Db4')],
    [(0, 3, 'E4'), (3, 2, 'C4'), (6, 2, 'G3'), (8, 2, 'Bb3'), (10, 1, 'C4'), (11, 2, 'Db4'), (14, 2, 'E4')],
]

# ---------------- bas: per maat (16de, lengte, interval, klank, glijtijd in ticks vanaf de vorige noot)
# H = lange dreigende noot onder de beat (geduckt op de snares) + een octaafsprong als opmaat (de volgende maat
# duikt daar met portamento uit omlaag); St = harde stoten op de off-beat ('en' van 2 en 4) en de kick van 3-en.
BASS_H = [(0, 14, 0, 'dark', 20), (14, 2, 12, 'raw', 8)]
BASS_ST = [(0, 3, 0, 'raw', 16), (6, 2, 12, 'raw', 6), (10, 3, 0, 'dark', 6), (14, 2, 7, 'raw', 8)]
BASS_RISE = [(0, 3, 0, 'raw', 16), (6, 2, 12, 'raw', 6), (10, 6, 0, 'raw', 6)]


def build():
    P = {k: [] for k in ('kick', 'snare', 'ghost', 'hat', 'ride', 'crash', 'fx', 'reese', 'brass', 'arp', 'pad',
                         'noise', 'sub')}
    prog = {'reese': [], 'brass': [], 'pad': []}
    bendev = []                    # (tick, pitchwheel) voor de reese
    snares = []                    # ticks van de hoofdsnares (ducking)
    kicks = []                     # v4: ticks van de kicks (ducking)

    # ---------------- drums ----------------
    def K(b, p, v=127):
        P['kick'].append([t(b, p), t(b, p) + KITLEN[KICK], KICK, v])
        kicks.append(t(b, p))

    def SN(b, p, v=127, duck=True):
        P['snare'].append([t(b, p), t(b, p) + KITLEN[SNARE], SNARE, v])
        if duck:
            snares.append(t(b, p))

    def G(b, p, v=44):
        P['ghost'].append([t(b, p), t(b, p) + KITLEN[GHOST], GHOST, v])

    def two_step(b, fill=False):
        K(b, 0); SN(b, 4); K(b, 10); SN(b, 12)
        G(b, 7); G(b, 15)
        if fill:                                   # einde van een frase: twee ghosts vóór de laatste snare
            G(b, 13, 60); G(b, 14, 76)

    def hats(b, vel=1.0, dens=16, upto=16):
        acc = [64, 50, 112, 56]                    # 1 e EN a: accent op de off-beat
        for p in range(0, upto, 16 // dens):
            P['hat'].append([t(b, p), t(b, p) + KITLEN[HAT], HAT, int(acc[p % 4] * vel)])

    def crash(b, v=116):
        P['crash'].append([t(b), t(b) + KITLEN[CRASH], CRASH, v])

    def ride(b):
        P['ride'] += [[t(b, p), t(b, p) + KITLEN[RIDE], RIDE, 84 if p % 8 == 0 else 66] for p in (0, 4, 8, 12)]

    # ---------------- bas ----------------
    def reese(st, en, nt, kind, glide, v=118):
        P['reese'].append([st, en, nt, v])
        prog['reese'].append((st, WOB[nt] if kind == 'wob' else REESE[kind]))
        bendev.append((st, 'glide', glide))

    def sub(st, en, nt, v=112):
        while nt > n('Eb2'):
            nt -= 12
        P['sub'].append([st, en, nt, v])

    def bass_bar(b, ch, pattern):
        root = n(BASS_ROOT[ch])
        maj = CHORDS[ch][1] == 'maj'
        for p, ln, iv, kind, gl in pattern:
            if iv == 3 and maj:
                iv = 4
            nt = root + iv
            st, en = t(b, p), t(b, p + ln)
            reese(st, en, nt, kind, gl, 110 if kind == 'raw' else 116)
            if iv == 0:
                sub(st, en, nt)

    def wobble(b, ch, bars):
        nt = n(BASS_ROOT[ch])
        reese(t(b), t(b + bars) - S, nt, 'wob', 20, 122)
        sub(t(b), t(b + bars) - S, nt)

    # ---------------- melodisch ----------------
    def brass(b, mel, vel=124, oct=0):
        for p, ln, nm in mel:
            nt = n(nm) + oct
            st = t(b, p)
            P['brass'].append([st, st + (S + 8 if ln < 3 else 2 * S), nt, vel if p % 4 != 0 else min(127, vel + 3)])
            prog['brass'].append((st, BRASS_PROG[nt]))

    def arp(b, ch, vel=96):
        r = n(CHORDS[ch][0] + '3')
        while r < n('C3'):
            r += 12
        m3 = 4 if CHORDS[ch][1] == 'maj' else 3
        seq = [0, 12, 7, 12, m3, 12, 7, 12 + m3]
        for i, iv in enumerate(seq):
            st = t(b, 2 * i)
            P['arp'].append([st, st + S, r + iv, vel if i % 2 else vel - 22])

    def pad(b, ch, vel=100):
        r = n(CHORDS[ch][0] + '3')
        while r < n('F3'):
            r += 12
        P['pad'].append([t(b), t(b + 1), r, vel])
        prog['pad'].append((t(b), PAD_MAJ if CHORDS[ch][1] == 'maj' else PAD_MIN))

    # ---------------- secties ----------------
    def motif(b0, with_pad=False):
        """4 maten laag motief: koper (thema 1-4), lange reese + sub, kick-skelet, hihats vanaf maat 2."""
        for i, ch in enumerate(['Fm', 'Fm', 'Db', 'Eb']):
            b = b0 + i
            K(b, 0, 118); K(b, 10, 104)
            if i:
                hats(b, 0.55 + 0.1 * i, dens=8)
            brass(b, MEL_A[i], 112 + 3 * i)
            r = n(BASS_ROOT[ch])
            if i == 1:
                reese(t(b), t(b, 14), r, 'dark', 0, 108)
                reese(t(b, 14), t(b + 1), r + 12, 'raw', 10, 104)
            else:
                reese(t(b), t(b + 1), r, 'dark', 0 if i == 0 else 24, 108)
            sub(t(b), t(b + 1) - 6, r, 104)
            if with_pad:
                pad(b, ch, 92)

    def build_up(b):
        """4 maten (Db Db C C): roffel 8sten -> 16den, kicks verdichten, ruisriser, reese glijdt een octaaf omhoog,
        koper op de grondtoon; de laatste tel (maat b+3, tel 4) is stil."""
        end = t(b + 3, 12)
        for i in range(4):
            bb = b + i
            for p in ((0,), (0,), (0, 8), (0, 4, 8))[i]:
                K(bb, p, 112 + 4 * i)
            hats(bb, 0.6 + 0.12 * i, dens=8 if i < 2 else 16, upto=12 if i == 3 else 16)
        # roffel: maat 1-2 achtsten, maat 3-4 zestienden, aanzwellend; stopt op de stille tel
        roll = [(b + i // 8, 2 * (i % 8)) for i in range(16)] + [(b + 2 + i // 16, i % 16) for i in range(28)]
        for k, (bb, p) in enumerate(roll):
            SN(bb, p, int(48 + 79 * (k / (len(roll) - 1)) ** 1.3), duck=False)
        # ruisriser (PSG): 32 achtsten, toonhoogte en volume omhoog
        P['noise'] += [[t(b) + i * E, min(end, t(b) + i * E + E), 34 + int(i * 1.5), 24 + 3 * i] for i in range(30)]
        # koperstoten 3-3-2 op de grondtoon, in maat 4 in achtsten tot de stilte
        for i, nm in enumerate(['Db4', 'Db4', 'C4', 'C4']):
            for p in ((0, 3, 6), (0, 3, 6), (0, 3, 6, 8, 11, 14), (0, 2, 4, 6, 8, 10))[i]:
                P['brass'].append([t(b + i, p), t(b + i, p) + S + 8, n(nm), 108 + 5 * i])
                prog['brass'].append((t(b + i, p), BRASS_PROG[n(nm)]))
        # reese: Db lang, dan C die over twee maten een octaaf opstijgt (de riser); sub mee tot de stilte
        reese(t(b), t(b + 2) - 8, n('Db2'), 'dark', 16, 110)
        sub(t(b), t(b + 2) - 8, n('Db2'), 104)
        reese(t(b + 2), end, n('C2'), 'raw', 10, 114)
        bendev.append((t(b + 2), 'rise', end))
        sub(t(b + 2), end, n('C2'), 104)
        P['fx'].append([end - 440, end - 2, REVCYM, 96])

    def drop_bar(b, k, mel=None, bass='A', arp_on=False, ride_on=False):
        ch = DROP_CH[k % 8]
        two_step(b, fill=k % 8 == 7)
        hats(b)
        if bass == 'A':
            bass_bar(b, ch, BASS_RISE if k % 16 == 15 else (BASS_H if k % 2 == 0 else BASS_ST))
        if mel is not None:
            brass(b, mel[k % 8])
        if arp_on:
            arp(b, ch)
        if ride_on:
            ride(b)
        if k % 8 == 0:
            crash(b)

    # ================= INTRO =================
    motif(0)
    build_up(4)
    # ================= LOOP =================
    for k in range(16):                                        # DROP A
        drop_bar(8 + k, k, MEL_A, arp_on=k >= 8)
    motif(24, with_pad=True)                                   # break
    build_up(28)
    for k in range(16):                                        # DROP B: wobble
        b = 32 + k
        mel = MEL_A if k >= 8 or k % 2 == 0 else None         # 32-39: alleen de roepen (oneven maten rust)
        drop_bar(b, k, mel, bass=None, arp_on=True, ride_on=k >= 8)
    for b0 in (32, 40):
        wobble(b0, 'Fm', 2); wobble(b0 + 2, 'Db', 1); wobble(b0 + 3, 'Eb', 1)
        wobble(b0 + 4, 'Fm', 2); wobble(b0 + 6, 'Db', 1)
        bass_bar(b0 + 7, 'C', BASS_ST)
    motif(48, with_pad=True)                                   # break (= intro 0-3)
    build_up(52)                                               # = intro 4-7
    return P, prog, bendev, sorted(set(snares)), sorted(set(kicks))


def clip_loop(notes):
    out = []
    for a, b, nt, v in notes:
        for g in (LOOP_START, LOOP_END):
            if a < g < b:
                b = g
        if a < LOOP_END:
            out.append([a, b, nt, v])
    return dedupe(out)


def same_pitch_overlap(notes):
    """Dezelfde toonhoogte mag in één spoor niet overlappen (de note-off van de eerste kapt de tweede af)."""
    notes = sorted(notes)
    for i, e in enumerate(notes):
        for f in notes[i + 1:]:
            if f[0] >= e[1]:
                break
            if f[2] == e[2] and f[0] > e[0]:
                e[1] = f[0]
    return notes


def pw(semis):
    return max(-8192, min(8191, int(round(8192 * semis / 12))))


def reese_bends(notes, bendev):
    """Portamento: elke reese-noot begint op de toonhoogte van de vorige en glijdt in `glide` ticks naar zijn eigen
    toonhoogte (BENDR 12). 'rise' = over de noot een octaaf omhoog (build-up)."""
    ev = [(0, mido.Message('control_change', control=20, value=12))]
    pitch_at = {a: nt for a, b, nt, v in notes}
    starts = sorted(pitch_at)
    info = {}
    for tk, kind, x in bendev:
        info.setdefault(tk, []).append((kind, x))
    prev = None
    for st in starts:
        nt = pitch_at[st]
        glide = next((x for k, x in info.get(st, []) if k == 'glide'), 0)
        rise = next((x for k, x in info.get(st, []) if k == 'rise'), None)
        if prev is not None and glide and prev != nt:
            off = max(-12, min(12, prev - nt))
            ev.append((st, mido.Message('pitchwheel', pitch=pw(off))))
            for i in range(1, 7):
                ev.append((st + glide * i // 6, mido.Message('pitchwheel', pitch=pw(off * (1 - i / 6) ** 1.5))))
        else:
            ev.append((st, mido.Message('pitchwheel', pitch=0)))
        if rise:
            ev += [(st + (rise - st) * i // 24, mido.Message('pitchwheel', pitch=pw(12 * (i / 24) ** 1.6)))
                   for i in range(1, 24)]
        prev = nt + (12 if rise else 0)
    # op het loopbegin zet de glide van de eerste drop-noot de bend zelf (vanaf de rise)
    # na de rise eindigt de reese een octaaf hoger: de drop duikt daar met portamento uit omlaag (zie glide)
    return [(tk, m) for tk, m in ev if tk < LOOP_END]


def duck_ccs(base, snares, kicks=(), base_at=None):
    """CC7-ducking: op elke snare (DUCK) en kick (DUCK_K) kort omlaag; een dip stopt waar de volgende begint (de
    snare wint als ze samenvallen). base_at(tick) = basisvolume op dat moment (v4: luider zolang de wobble klinkt);
    `changes` = ticks waarop het basisvolume wisselt."""
    at = base_at or (lambda tk: base)
    ev = sorted({**{k: DUCK_K for k in kicks}, **{s: DUCK for s in snares}}.items())
    cc = [(0, 7, at(0)), (LOOP_START, 7, at(LOOP_START))]
    for i, (s, curve) in enumerate(ev):
        nxt = ev[i + 1][0] if i + 1 < len(ev) else LOOP_END
        cc += [(s + d, 7, max(1, int(round(at(s + d) * f)))) for d, f in curve if s + d < min(nxt, LOOP_END)]
    return cc


def main():
    P, prog_, bendev, snares, kicks = build()
    for k in P:
        P[k] = same_pitch_overlap(clip_loop(P[k]))
    # golfkanaal: een golf van één periode klinkt een octaaf lager dan genoteerd (zie MUZIEK.md)
    P['sub'] = [[a, b, nt + 12, v] for a, b, nt, v in P['sub']]
    write_voicegroup()
    rel = {'reese': 160, 'brass': 160, 'arp': 150, 'pad': 200}
    tail = {k: release_ticks(r, TPB, BPM) for k, r in rel.items()}
    kitrel = {36 + i: k[2] for i, k in enumerate(KIT)}
    for k in ('kick', 'snare', 'ghost', 'hat', 'ride', 'fx'):
        tail[k] = max(release_ticks(kitrel[nt], TPB, BPM) if kitrel[nt] else 0 for _, _, nt, _ in P[k]) if P[k] else 0
    tail['crash'] = 0
    for k in ('reese', 'pad'):
        P[k] = detach(P[k], tail[k])
    order = ['snare', 'kick', 'brass', 'reese', 'hat', 'crash', 'ghost', 'fx', 'arp', 'ride', 'pad']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAX_VOICES)
    for k in order:
        tot = len(ds[k])
        if tot and len(kept[k]) < tot:
            print('  %-6s %3d van %4d noten vallen weg (%.1f%%)' % (k, tot - len(kept[k]), tot, 100 * (tot - len(kept[k])) / tot))
        P[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (LOOP_START, LOOP_END)

    def progs(lst):
        """programmawissels; op het loopbegin het programma dat daar hoort nog eens zetten (de sprong terug)."""
        lst = sorted(set(lst))
        out = [(tk, 'prog', p) for tk, p in lst if tk < LOOP_END]
        cur = [p for tk, p in lst if tk <= LOOP_START]
        if cur and not any(tk == LOOP_START for tk, _ in lst):
            out.append((LOOP_START, 'prog', cur[-1]))
        return out

    def first(lst, dflt):
        return sorted(lst)[0][1] if lst else dflt

    # v4: het reese-spoor staat luider zolang een wobble-programma klinkt
    rp = sorted(set(prog_['reese']))
    wobs = set(WOB.values())

    def reese_base(tk):
        cur = [p for t_, p in rp if t_ <= tk]
        return VOL['wob'] if cur and cur[-1] in wobs else VOL['reese']
    reese_ccs = duck_ccs(VOL['reese'], snares, kicks, reese_base)
    hits = set(snares) | set(kicks)
    reese_ccs += [(t_, 7, reese_base(t_)) for t_, p in rp
                  if t_ < LOOP_END and t_ not in hits and reese_base(t_) != reese_base(t_ - 1)]
    layout = [  # naam, noten, programma, volume, kanaal, pan, ccs, extra
        ('reese', P['reese'], first(prog_['reese'], REESE['dark']), VOL['reese'], 0, 64,
         progs(prog_['reese']) + reese_ccs, reese_bends(P['reese'], bendev)),
        ('brass', P['brass'], first(prog_['brass'], BRASS_PROG[53]), VOL['brass'], 1, 60,
         progs(prog_['brass']) + duck_ccs(VOL['brass'], snares, kicks), ()),
        ('arp', P['arp'], PLUCK, VOL['arp'], 2, 84, duck_ccs(VOL['arp'], snares, kicks), ()),
        ('pad', P['pad'], PAD_MIN, VOL['pad'], 3, 44, progs(prog_['pad']) + duck_ccs(VOL['pad'], snares, kicks), ()),
        ('kick', sorted(P['kick'] + P['ghost']), DRUMS, 127, 9, 64, (), ()),
        ('snare', P['snare'], DRUMS, 127, 10, 64, (), ()),
        ('hats', P['hat'], DRUMS, VOL['hats'], 8, 76, (), ()),
        ('cym', sorted(P['ride'] + P['crash'] + P['fx']), DRUMS, VOL['cym'], 11, 54, (), ()),
        ('noise', P['noise'], RISER, 64, 12, 70, (), ()),
        ('sub', P['sub'], SUB, VOL['sub'], 13, 64, duck_ccs(VOL['sub'], snares, kicks), ()),
    ]
    for name, notes, prog, vol, ch, pan, ccs, extr in layout:
        song.add(notes, prog, vol, ch, pan, extra=extr, ccs=ccs)
    written = {'kick', 'snare', 'ghost', 'hat', 'ride', 'crash', 'fx'} | {nm for nm, *_ in layout}
    assert not [k for k in P if P[k] and k not in written], 'partij niet weggeschreven'
    assert len(layout) <= 16
    song.save(OUT, LOOP_END)
    sec = lambda tk: tk / TPB * 60 / BPM
    print(OUT, '%d sporen, intro %.1f s, loop %.1f s, totaal %.1f s' % (len(layout), sec(LOOP_START),
                                                                      sec(LOOP_END - LOOP_START), sec(LOOP_END)))
    for nm, b in (('motief', 0), ('build-up', 4), ('drop A', 8), ('break', 24), ('build-up', 28), ('drop B', 32),
                  ('thema', 40), ('break', 48), ('build-up', 52)):
        print('  %-9s maat %2d  %5.1f s' % (nm, b, sec(t(b))))


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + Drum & Bass-samples (mitch_samples.py) en een eigen drumkit voor Battle! Mitch.'
    lines[1] = '@ Gegenereerd door tools/grounded/mitch_theme.py.'
    lines[2] = 'voice_group %s' % VG
    ds = lambda smp, rel, key=60, att=255, dec=0, sus=255: \
        '\tvoice_directsound %d, 0, DirectSoundWaveData_%s, %d, %d, %d, %d' % (key, smp, att, dec, sus, rel)
    rep = {
        32: ds('mitch5_reese_raw', 160), 33: ds('mitch5_reese_raw_dark', 160),
        34: ds('mitch5_wob_f1', 170), 35: ds('mitch5_wob_c2', 170), 36: ds('mitch5_wob_db2', 170),
        37: ds('mitch5_wob_eb2', 170),
        40: ds('mitch3_pluck', 150),
        41: ds('mitch_pad_min', 200, att=40), 42: ds('mitch_pad_maj', 200, att=40),
        **{pr: ds('mitch6%s_brass_%d' % (BRASS_VARIANT, nt), 160, key=nt, dec=248, sus=200)
           for nt, pr in BRASS_PROG.items()},
        84: '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_8, 0, 7, 15, 1',
        121: '\tvoice_noise_alt 60, 0, 0, 3, 0, 15, 2',
        127: '\tvoice_keysplit_all voicegroup_mitch_drumset',
    }
    out = []
    for l in lines:
        tag = l.rstrip().rsplit('@ ', 1)[-1] if '@ ' in l and l.startswith('\t') else None
        if tag is not None and tag.isdigit() and int(tag) in rep:
            out.append('%s  @ %s' % (rep[int(tag)], tag))
        else:
            out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = []
    for nm, smp, r, _ in KIT:
        if smp == 'trinity_cymbal_crash':
            kit.append('voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165')
        else:
            kit.append('voice_directsound_no_resample 60, 64, DirectSoundWaveData_%s, 255, 0, 255, %d' % (smp, r))
    open('sound/voicegroups/drumsets/mitch.inc', 'w').write(
        '@ Project Grounded: Drum & Bass-kit voor Battle! Mitch (mitch_theme.py), alles DirectSound:\n'
        '@ ' + ', '.join('%d %s' % (36 + i, k[0].lower()) for i, k in enumerate(KIT)) + '.\n'
        'voice_group mitch_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    main()
