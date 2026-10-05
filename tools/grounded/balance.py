#!/usr/bin/env python3
"""Project Grounded: mixbalans van een omgezette MIDI vergelijken met de bron (Neo Plasma v3, Jordi: 'klinkt totaal
niet zoals de bron').

Per instrumentgroep:
- referentie: de bronsporen van die groep solo gerenderd met de GM-soundfont FluidR3 (fluidsynth), RMS;
- GBA: één test-ROM met het nummer; tijdens de opname staan alle andere sporen op volume 0 (volX van
  gMPlayTrack_BGM, net als m4aMPlayVolumeControl), RMS uit de emulator-audio (incl. PSG).
Uitkomst: per groep de verhouding GBA/referentie in dB t.o.v. het gemiddelde, en een voorstel voor het spoorvolume
(CC7) zodat alle groepen even ver van de bron zitten. Pas die toe in het generatiescript en meet opnieuw.

Gebruik (vanuit de hoofdmap, test-ROM met het nummer als debugscript 1 via testrom.py):
  PYTHONPATH=tools/grounded/maptools python3 tools/grounded/balance.py <bron.mid> <omgezet.mid> <test.gba> \
      <intro.bin> <groepen.json> [seconden]
groepen.json: {"lead": {"src": [4], "out": [1, 2, 7]}, ...}  (MIDI-spoornummers; m4a-spoor = MIDI-spoor - 1 als
spoor 0 alleen tempo/meta bevat, zoals bij Song uit musiclib)"""
import json, os, re, subprocess, sys, tempfile, wave
import numpy as np
import mido

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'


def rms(x):
    x = np.asarray(x, float)
    bad = np.where(np.abs(np.diff(x)) > 12000)[0]          # mGBA-bursts niet meetellen
    keep = np.ones(len(x), bool)
    for i in bad:
        keep[max(0, i - 32):i + 33] = False
    return float(np.sqrt((x[keep] ** 2).mean()))


def solo_midi(mid, keep):
    out = mido.MidiFile(type=1, ticks_per_beat=mid.ticks_per_beat)
    for i, t in enumerate(mid.tracks):
        nt = mido.MidiTrack(); acc = 0
        for x in t:
            acc += x.time
            if x.type in ('note_on', 'note_off') and i not in keep:
                continue
            nt.append(x.copy(time=acc)); acc = 0
        out.tracks.append(nt)
    return out


def reference(src, groups, sec):
    mid = mido.MidiFile(src)
    res = {}
    with tempfile.TemporaryDirectory() as d:
        for name, g in groups.items():
            p, w = os.path.join(d, 'g.mid'), os.path.join(d, 'g.wav')
            solo_midi(mid, set(g['src'])).save(p)
            subprocess.run(['fluidsynth', '-ni', '-g', '0.5', '-R', '0', '-C', '0', '-r', '32768', '-F', w, SF2, p],
                           check=True, capture_output=True)
            f = wave.open(w)
            a = np.frombuffer(f.readframes(min(f.getnframes(), int(sec * 32768))), np.int16).astype(float)
            res[name] = rms(a)
    return res


def record(rom, state, mute, sec):
    """Neemt `sec` seconden op (emulator-audio incl. PSG, 32768 Hz, mono) met de m4a-sporen in `mute` op volume 0."""
    from emu import Emu, load
    base = int(re.search(r'(0x[0-9a-f]+)\s+gMPlayTrack_BGM\n', open('pokeemerald.map').read()).group(1), 16)
    e = Emu(rom); load(e, state)
    mem = e.core.memory
    buf = e.core.get_audio_channels(); buf.set_rate(32768)
    rec, on = [], [False]

    def frame():
        for t in mute:                       # volX = 0 + MPT_FLG_VOLCHG, elke frame (de MIDI zet vol opnieuw)
            a = base + 0x50 * t
            mem.u8[a + 19] = 0
            mem.u8[a] = mem.u8[a] | 0x03
        e.core.run_frame()
        av = buf.available
        if av:
            s = buf.read(av)
            if on[0]: rec.extend(s)
    e.core.set_keys(3); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(30)]
    e.core.set_keys(0); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(30)]
    for _ in range(5):
        e.core.set_keys(7); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(6)]
    e.core.set_keys(0); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(30)]
    on[0] = True
    e.core.set_keys(0); [frame() for _ in range(4)]; e.core.set_keys()
    for _ in range(int(60 * sec)):
        frame()
    return np.array(rec, dtype=np.int16).reshape(-1, 2).astype(float).mean(1)


def gba(rom, state, groups, sec, ntracks):
    res = {}
    for name, g in groups.items():
        mute = [i - 1 for i in range(1, ntracks) if i not in g['out']]
        res[name] = rms(record(rom, state, mute, sec))
    return res


def main():
    src, out, rom, state, gfile = sys.argv[1:6]
    sec = float(sys.argv[6]) if len(sys.argv) > 6 else 60
    groups = json.load(open(gfile))
    om = mido.MidiFile(out)
    ref = reference(src, groups, sec)
    got = gba(rom, state, groups, sec, len(om.tracks))
    db = {k: 20 * np.log10(max(got[k], 1) / max(ref[k], 1)) for k in groups}
    mean = float(np.mean(list(db.values())))
    print('%-10s %8s %8s %7s   voorstel (CC7 per spoor)' % ('groep', 'ref rms', 'gba rms', 'dB'))
    for k, g in groups.items():
        corr = mean - db[k]
        vols = []
        for i in g['out']:
            v = next((x.value for x in om.tracks[i] if x.type == 'control_change' and x.control == 7), 127)
            vols.append('%d:%d->%d' % (i, v, max(1, min(127, round(v * 10 ** (corr / 20))))))
        print('%-10s %8d %8d %+7.1f   %s' % (k, ref[k], got[k], db[k] - mean, ', '.join(vols)))


if __name__ == '__main__':
    main()
