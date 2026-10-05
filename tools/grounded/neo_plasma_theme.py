#!/usr/bin/env python3
"""Project Grounded: gevechtsmuziek van Neo Team Plasma (Battle Stadium): "Battle! Neo Team Plasma"
(Pokémon Black 2/White 2). Noten: MIDI van Byabbington (onlinesequencer, sound/songs/grounded_src/b2w2_neo_plasma.mid,
176 bpm, overal velocity 50). Klank en balans: gemeten aan het origineel (BW2-mp3 van Jordi).

v4 (Jordi over v2/v3: 'een rotzooi, klinkt totaal niet zoals de bron, veel eentoniger'). Het origineel is gemeten:
- Uitlijning: de MIDI loopt precies gelijk met de mp3 (maat k = 0,75 s + k x 1,364 s). Structuur van het origineel:
  intro maat 0-9, loop maat 10-73 (64 maten); de MIDI speelt die loop twee keer (74-137 = 10-73). v4 loopt dus net
  als de game: intro 0-9, dan 10-73 en terug naar 10 (v3 liep het hele 138-maten-bestand door).
- Bronscheiding (Spleeter 4 stems) + per spoor kandidaat-instrumenten (FluidR3) die het mel-spectrogram van het
  origineel het best verklaren (NNLS, zie tools/grounded/balance_orig.py en het rapport van v4):
    bronspoor 'Electric Guitar' (27) -> in het origineel een AANHOUDENDE synth brass/pad (B-sectie duidelijk 62/63;
        schone gitaar scoorde overal slecht). v3 speelde dit als droge, korte schone gitaar.
    'Slap Bass' (36) -> Slap Bass 2, en een octaaf lager dan de MIDI (bas-stem: G2 waar de MIDI G3 schrijft).
    'Church Organ' (19) -> percussief/rockorgel (17/18) past beter.
    drums -> grote elektronische kick op elke tel (lange pitch-sweep), hihats op de achtste off-beats; de MIDI-snares
        (37/38 op de off-beats) klinken in het origineel als hihats, niet als snare.
    'Sawtooth' (81) blijft saw; steel drums (114): geen duidelijke winnaar, blijft.
- Spectrum totale mix v3 t.o.v. origineel: 31-125 Hz 4-9 dB te zacht, 500 Hz-8 kHz 4-5 dB te luid (dun en schel).
- Het origineel laat noten doorklinken (arpeggio's en akkoorden als lange lijnen in het spectrogram): lead en akkoorden
  hier legato tot de volgende noot (max. 2 tellen / 1 maat) i.p.v. de korte MIDI-lengtes.

Gebruik: python3 tools/grounded/neo_plasma_theme.py (samples: tools/grounded/neo_plasma_samples.py)"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, thin, detach, allocate, releases, release_ticks, Song

SRC = 'sound/songs/grounded_src/b2w2_neo_plasma.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_neo_plasma.mid'
VG = 'sound/voicegroups/grounded_neo_plasma.inc'
TPB, BAR, BEAT = 384, 1536, 384
BPM = 176
LOOP0, END = 10 * BAR, 74 * BAR

# programma's in voicegroup_grounded_neo_plasma
SLAP, BRASS, BRASS_LO, ORGAN, LEAD_PSG, SAW, SINE, TRI, SAW_LO, STEEL, DRUMS = 37, 62, 63, 17, 80, 81, 82, 83, 84, 114, 127
VOICES = {
    ORGAN:      'voice_directsound 60, 0, DirectSoundWaveData_np_organ, 255, 0, 255, 120',
    SLAP:       'voice_directsound 60, 0, DirectSoundWaveData_np_slap_bass, 255, 0, 255, 160',
    BRASS:      'voice_directsound 60, 0, DirectSoundWaveData_np_synth_brass, 255, 0, 255, 185',
    BRASS_LO:   'voice_directsound 60, 0, DirectSoundWaveData_np_synth_brass_lo, 255, 0, 255, 170',
    SAW:        'voice_directsound 60, 0, DirectSoundWaveData_gm_saw_lead, 255, 0, 255, 175',
    SAW_LO:     'voice_directsound 60, 0, DirectSoundWaveData_gm_saw_lead, 255, 0, 255, 150',
    LEAD_PSG:   'voice_square_1 60, 0, 0, 2, 0, 2, 9, 1',
    SINE:       'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 1',
    TRI:        'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_2, 0, 7, 15, 1',
    STEEL:      'voice_directsound 60, 0, DirectSoundWaveData_gm_steel_drums, 255, 0, 255, 150',
    DRUMS:      'voice_keysplit_all voicegroup_neo_plasma_drumset',
}
# bron-drumnoot -> (noot in neo_plasma_drumset, lengte in ticks, velocity-factor)
# 36 kick; 37/38 (Electric-kit snares op de off-beats) -> hihat dicht, 38 in fills (2+ op een rij) -> snare;
# 42/44 hihat, 46 open; 49/57 crash, 55 splash; 78 (cuíca, 2 noten) weg.
KICK, SNARE, HAT, OHAT, CRASH, SPLASH = 36, 37, 38, 39, 40, 41
DRUM_MAP = {36: (KICK, 240, 1.0), 37: (HAT, 96, 0.55), 38: (HAT, 96, 0.6), 42: (HAT, 96, 0.5), 44: (HAT, 96, 0.5),
            46: (OHAT, 192, 0.55), 49: (CRASH, 768, 0.75), 55: (SPLASH, 384, 0.7), 57: (CRASH, 768, 0.75)}

# spoorvolumes (CC7), afgesteld met balance_orig.py tegen de mp3
VOL = dict(lead=27, lead_psg=7, saw_lo=16, brass=30, brass_lo=45, organ=66, bass=90, steel=20, sine=16, tri=16,
           drums=62)
GAIN = 1.25          # alles samen luider (piek 69/127 bij -V127 zonder GAIN); de verhoudingen blijven
VOL = {k: min(127, round(v * GAIN)) for k, v in VOL.items()}


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Neo Team Plasma (BW2) v4. Gegenereerd door tools/grounded/neo_plasma_theme.py.'
    lines[1] = '@ 17 perc. orgel, 37 slap bass 2, 62/63 synth brass, 81/84 saw, 114 steel drums, 127 neo_plasma_drumset (np_*).'
    lines[2] = 'voice_group grounded_neo_plasma'
    out = []
    for l in lines:
        k = l.rsplit('@', 1)[1].strip() if '@' in l and l.startswith('\tvoice') else None
        if k and k.isdigit() and int(k) in VOICES:
            l = '\t%s  @ %s' % (VOICES[int(k)], k)
        out.append(l)
    open(VG, 'w').write('\n'.join(out))


def groups(ev):
    g = {}
    for e in ev:
        g.setdefault(e[0], []).append(list(e))
    return [sorted(g[s], key=lambda e: e[2]) for s in sorted(g)]


def legato(ev, cap):
    """Elke noot klinkt door tot de volgende aanslag in de partij (max. `cap` ticks): het origineel laat doorklinken."""
    ev = sorted(ev)
    starts = sorted(set(e[0] for e in ev))
    out = []
    for e in ev:
        nxt = next((t for t in starts if t > e[0]), e[0] + cap)
        out.append([e[0], max(e[1], min(nxt, e[0] + cap)), e[2], e[3]])
    return out


def merge_repeats(ev, gap=0):
    """Herhaalde 16e op dezelfde toonhoogte (aansluitend) samenvoegen tot één aanhoudende noot."""
    by, out = {}, []
    for e in sorted(ev):
        by.setdefault(e[2], []).append(list(e))
    for n, lst in by.items():
        cur = lst[0]
        for e in lst[1:]:
            if e[0] - cur[1] <= gap and e[0] - cur[0] <= 96:
                cur[1] = max(cur[1], e[1])
            else:
                out.append(cur); cur = e
        out.append(cur)
    return sorted(out)


def drums(ev):
    out, dropped = [], 0
    ev = sorted(ev)
    snares = sorted(s for s, e, n, v in ev if n == 38)
    for s, e, n, v in ev:
        if n not in DRUM_MAP:
            dropped += 1
            continue
        n2, ln, f = DRUM_MAP[n]
        if n == 38 and any(abs(s - t) == 96 for t in snares):     # 16e-roffel/fill: echte snare
            n2, ln, f = SNARE, 192, 0.8
        out.append([s, s + ln, n2, int(v * f)])
    out = dedupe(out)
    by = {}
    for e in out:
        by.setdefault(e[2], []).append(e)
    for lst in by.values():                         # een nieuwe slag op dezelfde drumnoot kapt de vorige af
        for a, b in zip(lst, lst[1:]):
            a[1] = min(a[1], b[0])
    for e in out:                                   # hihat open wordt gesloten door de volgende hihat
        if e[2] == OHAT:
            nx = [h[0] for h in by.get(HAT, []) if h[0] > e[0]]
            if nx: e[1] = min(e[1], nx[0])
    return sorted(out), dropped


def build():
    m = mido.MidiFile(SRC)
    assert m.ticks_per_beat == TPB
    T = {i: [[a, b, n, 127] for a, b, n, v in notes_of(m.tracks[i])] for i in range(10)}
    clip = lambda ev: [[s, min(e, END), n, v] for s, e, n, v in ev if s < END]
    dr, drum_drop = drums(T[0] + T[1] + T[2])
    for e in dr:
        e[3] = min(127, e[3])

    # bas: onderstem, een octaaf lager (zoals in het origineel), niet onder E1
    bass = []
    for g in groups(T[3]):
        e = list(g[0])
        if e[2] - 12 >= 28:
            e[2] -= 12
        bass.append(e)
    # sawtooth: bovenste noot = melodie (legato); octaaf eronder = PSG-verdubbeling; rest = tweede lijn (1 stem)
    lead, lead_psg, saw_lo = [], [], []
    for g in groups(T[4]):
        top = g[-1]
        lead.append(list(top))
        rest = [e for e in g[:-1] if e[2] != top[2] - 12]
        for e in g[:-1]:
            if e[2] == top[2] - 12:
                lead_psg.append(list(e))
        if rest:
            saw_lo.append(list(rest[-1]))
    for e in saw_lo + lead:
        while e[2] < 36:
            e[2] += 12
    # glissando's (32e/64e-loopjes in de intro): niet meer dan één noot per 48 ticks, anders stapelen de staarten op
    gl, last = [], -999
    for e in sorted(lead):
        if e[1] - e[0] < 48 and e[0] - last < 48:
            continue
        gl.append(e); last = e[0]
    lead = gl
    lead = legato(lead, 2 * BEAT)
    saw_lo = legato(saw_lo, BEAT)
    # 'gitaar' = synth brass: vanaf C3 akkoorden (3 bovenste stemmen) die doorklinken tot het volgende akkoord;
    # daaronder de lage partij (powerchord-grondtoon / C2-chug) op een eigen, laag gerenderde sample
    hi = [e for e in T[5] if e[2] >= 48]
    lo = [e for e in T[5] if e[2] < 48]
    brass = legato(merge_repeats(thin(hi, 3, 'top')), BAR)
    brass = thin(brass, 3, 'top')
    brass_lo = [g[0] for g in groups(lo)]
    organ = thin(T[6], 3, 'top')
    parts = {'lead': lead, 'drums': dr, 'bass': bass, 'brass': brass, 'organ': organ, 'steel': T[8],
             'brass_lo': brass_lo, 'saw_lo': saw_lo}
    parts = {k: dedupe(clip(v)) for k, v in parts.items()}
    psg = {'lead_psg': dedupe(clip(lead_psg)), 'sine': dedupe(clip(T[7])), 'tri': dedupe(clip(T[9]))}

    voicegroup()
    rel = releases('grounded_neo_plasma')
    progs = {'lead': SAW, 'bass': SLAP, 'brass': BRASS, 'organ': ORGAN, 'steel': STEEL, 'brass_lo': BRASS_LO,
             'saw_lo': SAW_LO}
    tail = {k: release_ticks(rel[p], TPB, BPM) for k, p in progs.items()}
    tail.update(drums=0)
    for k in progs:
        parts[k] = detach(parts[k], tail[k])
    order = ['lead', 'drums', 'bass', 'brass', 'organ', 'steel', 'brass_lo', 'saw_lo']
    res = allocate(parts, order, tail)
    print('drumnoten buiten de kit (weg): %d' % drum_drop)
    for k in order:
        n, kept = len(parts[k]), len(res[k])
        print('  %-9s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - kept, 100 * (n - kept) / max(n, 1)))
    p = res
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (LOOP0, END)
    tracks = [
        (p['lead'], SAW, VOL['lead'], 0, 64),
        (psg['lead_psg'], LEAD_PSG, VOL['lead_psg'], 1, 64),
        (p['brass'], BRASS, VOL['brass'], 2, 56),
        (p['brass_lo'], BRASS_LO, VOL['brass_lo'], 3, 64),
        (p['organ'], ORGAN, VOL['organ'], 4, 72),
        (p['bass'], SLAP, VOL['bass'], 5, 64),
        (p['saw_lo'], SAW_LO, VOL['saw_lo'], 7, 76),
        (p['steel'], STEEL, VOL['steel'], 8, 52),
        (psg['sine'], SINE, VOL['sine'], 10, 64),
        (psg['tri'], TRI, VOL['tri'], 11, 64),
        (p['drums'], DRUMS, VOL['drums'], 9, None),
    ]
    written = 0
    for notes, prog, vol, ch, pan in tracks:
        if notes:
            song.add(notes, prog, vol, ch, pan)
            written += len(notes)
    assert written == sum(len(p[k]) for k in order) + sum(len(v) for v in psg.values()), 'niet elke partij staat in de MIDI'
    song.save(OUT, END)
    print(OUT, '(%d sporen, intro %.1f s, loop %.1f s)' % (len(song.tracks), LOOP0 / TPB * 60 / BPM,
                                                           (END - LOOP0) / TPB * 60 / BPM))


if __name__ == '__main__':
    build()
