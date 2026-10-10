#!/usr/bin/env python3
"""Project Grounded: Battle! Arceus (Pokémon Diamond/Pearl/Platinum, SEQ_BA_SECRET1) op de GBA.

Bron: Jordi's MIDI `Battle_Arceus.mid` op origin/master (Domino-bewerking van een rip, sporen heten naar de
SSEQ-offsets; niet in de werkbranch). De noten komen 1-op-1 uit die MIDI; dit script kiest alleen de GBA-instrumenten,
dunt uit binnen de kanaalgrens en zet de loop.
  python3 tools/grounded/arceus_theme.py [pad/naar/Battle_Arceus.mid]   (zonder pad: git show origin/master:...)

Vorm (150 bpm, 4/4, tpb 48; maat = 192 ticks):
  maat 0-3    clusterstoten (A#-B-C boven C#/E) met uitgeschreven echo, laag -> midden -> hoog (koper)
  maat 4-9    pauken-dreunen (G1+C2+E2), elke maat
  maat 10-37  pauken-ostinato G-E-E (3+3+2), pauken G1/E2 + C2 op elke tel 1; toms + bekkens in maat 14-17,
              22-25, 30-33; strijkersclusters in maat 21.3-26 (laag) en 29.3-34 (hoog)
  maat 38-41  lage strijkerscluster C2+C#2 met crescendo (CC7 72 -> 127), pauken G1/E2/C2
  maat 41.3-44 clusterstoten (midden, laag) zoals de intro
  maat 44-49  pauken-dreunen (C+G), dan terug naar maat 10 (loop 10-50)
Opgeruimd t.o.v. de bron:
  - spoor 5 (kopie van het ostinato, 2 ticks later, -0,56 halve toon, hard rechts = stereo-chorus) valt weg;
    detune van spoor 5/7 (pitchwheel -384/+320 bij bend-range 12) niet overgenomen.
  - pauken C1 (maat 44/48) -> C2 (geen DirectSound onder E1; C2 klinkt daar al mee).
  - echonoten zachter dan v20 vallen weg (8-bit-ruis).
  - 'Track 10' (kanaal 8, programma 117) is een drumspoor met GM-drumnummers (41/45 toms, 52/53/57 bekkens);
    gespeeld op een eigen kit (drumsets/arceus.inc), niet als melodische taiko.
Instrumenten (alleen stock-samples, geen ROM-kosten voor samples): koper = tuba-keysplit (< C4) en trompet-keysplit
(>= C4), strijkers = string-ensemble-keysplit, pauken = sc88pro_timpani; kit: sc55-tom, sd90-ambient-tom,
orkest-crash, trinity-crash, ride bell. Stemverdeler max. 11 DirectSound-noten (legendary).
Zie tools/grounded/MUZIEK.md."""
import os, subprocess, sys, io
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, detach, allocate, releases, release_ticks, Song

VG = 'grounded_arceus'
OUT = 'sound/songs/midi/mus_grounded_vs_arceus.mid'
MAXV = 11
TPB = 48
BAR = TPB * 4
BPM = 150
LOOP0, LOOP1 = 10 * BAR, 50 * BAR

# programma's in voicegroup_grounded_arceus
STR, TPT, TUBA, TIMP, KIT = 48, 56, 57, 47, 127
# drumkit drumsets/arceus.inc: de GM-nummers van de bron
FTOM, LTOM, CHINA, RBELL, CRASH = 41, 45, 52, 53, 57
DLEN = {FTOM: 12, LTOM: 12, CHINA: 48, RBELL: 48, CRASH: 48}   # toms = bronlengte; bekkens 1 tel + uitklink
BOOM = 2 * TPB   # pauken-dreunen na 2 tellen los (de sample is dan al -16 dB uitgeklonken)
ECHO_MIN = 20


def source(path=None):
    if path:
        return mido.MidiFile(path)
    data = subprocess.run(['git', 'show', 'origin/master:Battle_Arceus.mid'], check=True,
                          capture_output=True).stdout
    return mido.MidiFile(file=io.BytesIO(data))


def ccs_of(track, controllers=(7, 10)):
    tick, out = 0, []
    for x in track:
        tick += x.time
        if x.type == 'control_change' and x.control in controllers:
            out.append((tick, x.control, x.value))
    return out


def brass(n):
    return TUBA if n < 60 else TPT


def build():
    m = source(sys.argv[1] if len(sys.argv) > 1 else None)
    assert m.ticks_per_beat == TPB
    T = {i: notes_of(t) for i, t in enumerate(m.tracks)}
    P, CC, PROG = {}, {}, {}

    # ---- clusters/strijkers (bronsporen 1-4): koper tot maat 21.3, daarna strijkers (spoor 4 blijft koper) ----
    STR_FROM = 21 * BAR + 3 * TPB
    for src, name in ((1, 'v1'), (2, 'v2'), (3, 'v3'), (4, 'v4')):
        main, echo, progs = [], [], []
        for s, e, n, v in T[src]:
            if v < ECHO_MIN:
                continue
            (main if v >= 100 else echo).append([s, e, n, v])
        cur = None
        for s, e, n, v in sorted(main + echo):
            pr = STR if (src != 4 and s >= STR_FROM) else brass(n)
            if pr != cur:
                progs.append((s, 'prog', pr))
                cur = pr
        P[name], P[name + '_echo'] = main, echo
        PROG[name] = progs
        cc = [c for c in ccs_of(m.tracks[src])]
        # CC7-crescendo (maat 38-41) uitdunnen tot elke 2e stap; bij het loopbegin het beginvolume terugzetten
        vol0 = next(v for t, c, v in cc if c == 7)
        cc = [c for i, c in enumerate(cc) if c[1] != 7 or c[0] == 0 or i % 2 == 0 or c[2] == 127]
        cc.append((LOOP0, 7, vol0))
        CC[name] = [c for c in cc if c[0] > 0]
        CC[name].insert(0, (0, 'prog', progs[0][2]))
        CC[name] += progs[1:]
        CC[name].sort(key=lambda c: (c[0], str(c[1])))

    # ---- pauken: 6 = ostinato + dreunen (5 = kopie, weg), 7 en 8 = dreunen ----
    def timp(src):
        out = []
        for s, e, n, v in T[src]:
            while n < 31:
                n += 12             # C1 -> C2 (E1-grens)
            out.append([s, min(e, s + BOOM), n, v])
        return dedupe(out)
    P['timp_ost'] = timp(6)
    P['timp_b1'] = timp(7)
    P['timp_b2'] = timp(8)
    # dezelfde toonhoogte tegelijk in twee paukensporen (C2 in maat 44/48) maar één keer
    taken = {(s, n) for s, e, n, v in P['timp_ost'] + P['timp_b2']}
    P['timp_b1'] = [e for e in P['timp_b1'] if (e[0] - 2, e[2]) not in taken and (e[0], e[2]) not in taken]

    # ---- drums (bronspoor 9) ----
    P['drums'] = [[s, s + DLEN[n], n, v] for s, e, n, v in T[9]]
    # een bekken dat een tel later opnieuw klinkt (tel 3 en 3-en) eerder los, dan bezet het geen 2 kanalen
    for d in P['drums']:
        nxt = [x[0] for x in P['drums'] if x[2] == d[2] and x[0] > d[0]]
        if nxt and d[1] > min(nxt) - 18:
            d[1] = max(d[0] + 6, min(nxt) - 18)
    assert {n for s, e, n, v in T[9]} <= set(DLEN), {n for s, e, n, v in T[9]}
    return P, CC


LAYOUT = [  # (partij, programma, volume, kanaal, pan)  volume = bron-CC7
    ('v1', TUBA, 127, 0, 64),
    ('v2', TPT, 110, 1, 96),
    ('v3', TPT, 110, 2, 64),
    ('v4', TUBA, 110, 3, 32),
    ('timp_ost', TIMP, 104, 4, 64),
    ('timp_b1', TIMP, 110, 6, 82),
    ('timp_b2', TIMP, 120, 8, 47),
]
ORDER = ['v2', 'v3', 'v4', 'v1', 'timp_b2', 'timp_ost', 'timp_b1', 'drums',
         'v2_echo', 'v3_echo', 'v4_echo', 'v1_echo']


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor Battle! Arceus (DPPt).'
    lines[1] = '@ Gegenereerd door tools/grounded/arceus_theme.py. Alleen stock-samples.'
    lines[2] = 'voice_group %s' % VG
    over = {
        47: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200',
        127: 'voice_keysplit_all voicegroup_arceus_drumset',
    }
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    blank = 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216'
    kit = {
        FTOM: ('floor tom', 'voice_directsound 52, 60, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 200'),
        LTOM: ('low tom', 'voice_directsound 47, 68, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        CHINA: ('china', 'voice_directsound 64, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
        RBELL: ('ride bell', 'voice_directsound 60, 64, DirectSoundWaveData_dance_drums_ride_bell, 255, 0, 255, 180'),
        CRASH: ('crash', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216'),
    }
    body = ''.join('\t%s  @ %d %s\n' % (kit[k][1] if k in kit else blank, k, kit[k][0] if k in kit else '(vrij)')
                   for k in range(FTOM, CRASH + 1))
    open('sound/voicegroups/drumsets/arceus.inc', 'w').write(
        '@ Project Grounded: drumkit voor arceus_theme.py (Battle! Arceus). GM-nummers van de bron (41/45 toms,\n'
        '@ 52 china, 53 ride bell, 57 crash); alleen stock-samples, geen PSG. Vrije plekken = crash (nooit gespeeld).\n'
        'voice_group arceus_drumset, %d\n' % FTOM + body)


def main():
    voicegroup()
    P, CC = build()
    rel = releases(VG)
    progs = {k: pr for k, pr, *_ in LAYOUT}
    tail = {}
    for k in P:
        base = k.replace('_echo', '')
        if base in progs:
            # koper/strijkers: de langste uitklinktijd van de instrumenten die dit spoor speelt
            prs = {v for t, c, v in CC.get(base, []) if c == 'prog'} or {progs[base]}
            tail[k] = max(release_ticks(rel.get(pr) or 200, TPB, BPM) for pr in prs) + 2
    tail['drums'] = release_ticks(200, TPB, BPM) + 2
    # clusterstoten + echo per spoor legato los (de uitklink van een stoot bezet geen tweede kanaal)
    for k in ('v1', 'v2', 'v3', 'v4'):
        loud = {(e[0], e[2]) for e in P[k]}
        both = detach(P[k] + P[k + '_echo'], tail[k])
        P[k] = [e for e in both if (e[0], e[2]) in loud]
        P[k + '_echo'] = [e for e in both if (e[0], e[2]) not in loud]
    for k, ev in P.items():
        if k == 'drums':
            continue
        low = [n for _, _, n, _ in ev if n < 28]
        assert not low, '%s: DirectSound-noten onder E1 %s' % (k, low[:5])
    for k in ('v1', 'v2', 'v3', 'v4'):
        prs = sorted(CC[k], key=lambda c: c[0])
        for s, e, n, v in P[k] + P[k + '_echo']:
            pr = [c[2] for c in prs if c[1] == 'prog' and c[0] <= s][-1]
            assert not (pr == TPT and n < 48), '%s: trompet onder C3 (%d)' % (k, n)
    kept = allocate(P, ORDER, tail, max_voices=MAXV)
    for k in ORDER:
        n = len(P[k])
        if n and len(kept[k]) < n:
            lost = [e for e in P[k] if e not in kept[k]]
            print('  %s: %d van %d noten vallen weg (%.1f%%), maten %s' % (
                k, len(lost), n, 100 * len(lost) / n, sorted({e[0] // BAR for e in lost})[:12]))
            if os.environ.get('ARC_LOST'):
                print('    ', [(e[0] // BAR, e[0] % BAR, e[2]) for e in lost])
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (LOOP0, LOOP1)
    for k, pr, vol, ch, pan in LAYOUT:
        notes = sorted(kept[k] + kept.get(k + '_echo', []))
        song.add(notes, pr, vol, ch, pan, ccs=CC.get(k, []))
    song.add(sorted(kept['drums']), KIT, 100, 9)
    song.save(OUT, LOOP1)
    print(OUT, '| intro %.1f s | loop %.1f s' % (LOOP0 / TPB * 60 / BPM, (LOOP1 - LOOP0) / TPB * 60 / BPM))


if __name__ == '__main__':
    main()
