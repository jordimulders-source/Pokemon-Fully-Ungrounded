#!/usr/bin/env python3
"""Project Grounded: de Heatran-samples (heatran_st_*), v6: Kyuss-fuzz ('Odyssey'/'Green Machine') als Gen 3-sample.

v6 is gemeten aan Jordi's audioreferenties (Spleeter-'other'-stem = de gitaren, per sectie, zie MUZIEK.md):
  aandeel energie  < 250 Hz | 250-500 | 500-1k | 1-2k | > 2 kHz
  Odyssey             49-72 %   21-40 %   2-7 %   1-3 %   1-3 %
  Green Machine       52-62 %   19-21 %   2-3 %   3-4 %  14-21 %
  v5 (in de game)     12-19 %   18-23 %  20-23 % 17-23 % 18-27 %   <- dun, fel en 'krakend': surf/Mario Kart
Een Kyuss-gitaar is een muur van laag (gitaar door een basversterker): v6 maakt elke riffnoot zo, met een eigen sample
per noot (geen transpositie die het spectrum verschuift) en daarna 'bitcrushed' zoals een Gen 3-sample (13.379 Hz,
8 bit, korte loop).

Keten (st = stoner): FluidR3 Distortion Guitar (GM 30) als powerchord (grondtoon + kwint + octaaf = 1 kanaal)
  -> toonknop dicht (lowpass 3 kHz) -> lage shelf +5 dB (<180 Hz) -> fuzz (tanh x9, asymmetrisch)
  -> basversterker: lage shelf +3 dB (<150 Hz), middenscoop -6 dB rond 900 Hz, 8-polige lowpass 2,4 kHz
  -> lichte compressie (tanh x1,4) en weer lowpass 3,4 kHz -> 13.379 Hz, 8 bit.
  Gemeten per sample (C2/Gb2/C3): < 250 Hz ±75/68/48 %, > 2 kHz 1-3 % (Odyssey-gitaarstem: 49-72 % / 1-3 %).
Lead (st_lead): dezelfde keten op één noot met octaaf eronder (C4/G4), kast 1,9 kHz (donker, geen felle lead).

Rendert met fluidsynth, schrijft 8-bit WAV's met smpl-chunk; make maakt er .bin van. Gebruik:
  python3 tools/grounded/heatran_samples.py            (maakt de samples, labels in direct_sound_data.inc)
  python3 tools/grounded/heatran_samples.py --bands    (alleen het spectrum per sample tonen)"""
import os, sys, glob, subprocess, tempfile, wave
import numpy as np
import mido
from scipy.signal import butter, sosfilt, lfilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
FS = 44100                       # bewerken op 44,1 kHz
RATE = 13379                     # = samplerate van de Gen 3-gitaarsamples (sd90_classical_*): 'bitcrushed'

# C-standard, C-klein blues/frygisch: C Db Eb F Gb G Ab Bb C (keysplit_heatran, index 0-8)
RIFF_KEYS = (36, 37, 39, 41, 42, 43, 44, 46, 48)
LEAD_KEYS = (60, 67)             # C4, G4 (keysplit_heatran_lead)

# naam: (GM-programma, noten (akkoord = tuple), lengte in s, keten, label-toets)
SAMPLES = {}
for k in RIFF_KEYS:
    SAMPLES['heatran_st_pw_%d' % k] = (30, (k, k + 7, k + 12), 0.9, 'st', k)        # powerchord, 1 kanaal
for k in LEAD_KEYS:
    SAMPLES['heatran_st_lead_%d' % k] = (30, (k, k - 12), 0.9, 'lead' if k < 64 else 'leadhi', k)   # + octaaf eronder


def old_samples():
    """Alle heatran_*-samples van v1-v5 (heatran_st_* is v6). Geen ander thema gebruikt ze (gecontroleerd v0.9.81:
    SickBlik heeft eigen sb_*-kopieën van de v3-drums)."""
    names = {os.path.basename(p)[:-4] for p in glob.glob(OUT + 'heatran_*.wav') + glob.glob(OUT + 'heatran_*.bin')}
    return sorted(n for n in names if not n.startswith('heatran_st_'))


def render(prog, note, dur, vel=112):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    notes = note if isinstance(note, tuple) else (note,)
    t.append(mido.Message('program_change', channel=0, program=prog, time=0))
    for n in notes:
        t.append(mido.Message('note_on', channel=0, note=n, velocity=vel, time=0))
    for i, n in enumerate(notes):
        t.append(mido.Message('note_off', channel=0, note=n, velocity=0, time=int(dur * 960) if i == 0 else 0))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(FS), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


# ---- filters -----------------------------------------------------------------------------------------------------
def sos(kind, f, order=2):
    return butter(order, f, kind, fs=FS, output='sos')


def biquad(kind, f0, q, gain_db=0.0):
    """RBJ-cookbook: 'peak', 'lowshelf'."""
    A = 10 ** (gain_db / 40)
    w = 2 * np.pi * f0 / FS
    al = np.sin(w) / (2 * q)
    c = np.cos(w)
    if kind == 'peak':
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    else:   # lowshelf, S = 1
        sq = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * c + sq), 2 * A * ((A - 1) - (A + 1) * c), A * ((A + 1) - (A - 1) * c - sq)]
        a = [(A + 1) + (A - 1) * c + sq, -2 * ((A - 1) + (A + 1) * c), (A + 1) + (A - 1) * c - sq]
    return np.array(b) / a[0], np.array(a) / a[0]


def bqf(x, kind, f0, q, gain_db=0.0):
    b, a = biquad(kind, f0, q, gain_db)
    return lfilter(b, a, x)


def norm(a):
    return a / max(1e-9, np.abs(a).max())


# ---- de keten ------------------------------------------------------------------------------------------------------
def stoner(a, mid_hz=900, mid_db=-6.0, cab=2400):
    a = sosfilt(sos('highpass', 45, 2), a)
    a = sosfilt(sos('lowpass', 3000, 2), a)                      # toonknop dicht
    a = bqf(a, 'lowshelf', 180, 0.7, 5.0)
    a = norm(a)
    a = np.tanh(a * 9 + 0.15) - np.tanh(0.15)                    # fuzz, licht asymmetrisch
    a = bqf(a, 'lowshelf', 150, 0.7, 3.0)                        # basversterker
    a = bqf(a, 'peak', mid_hz, 0.8, mid_db)
    a = sosfilt(sos('lowpass', cab, 8), a)                       # kast
    a = np.tanh(norm(a) * 1.4)
    return sosfilt(sos('lowpass', 3400, 4), a)


def chain(kind, a):
    if kind == 'st':
        return stoner(a)
    if kind == 'lead':                                           # donker: geen felle lead
        return stoner(a, mid_hz=700, mid_db=0.0, cab=1900)
    if kind == 'leadhi':                                         # G4: de kast nog verder dicht (zelfde klankkleur)
        return stoner(a, mid_hz=1200, mid_db=-4.0, cab=1300)
    return a


def resample(a, src, dst):
    if dst < src:                                                    # anti-alias
        f = np.fft.rfft(a)
        f[int(len(f) * 0.9 * dst / src):] = 0
        a = np.fft.irfft(f, len(a))
    n = int(len(a) * dst / src)
    return np.interp(np.arange(n) * src / dst, np.arange(len(a)), a)


def auto_loop(a, rate, period):
    """Loop in het sustaindeel van een geheel aantal perioden (± het best passende), laatste 40% gecrossfade met wat
    vóór het loopbegin staat (geen klik bij de terugsprong)."""
    s = int(len(a) * 0.40)
    k = max(1, round(0.30 * rate / period))
    cands = [int(round(j * period)) for j in range(k - 2, k + 3)]
    n = int(rate * 0.04)
    best = max(cands, key=lambda L: np.dot(a[s:s + n], a[s + L:s + L + n]) / (np.linalg.norm(a[s + L:s + L + n]) + 1e-9))
    e = s + best
    f = int(best * 0.4)
    w = np.linspace(0, 1, f)
    a = a[:e].copy()
    a[e - f:e] = a[e - f:e] * (1 - w) + a[s - f:s] * w
    return a, (s, e)


def bands(a, rate):
    f = np.abs(np.fft.rfft(a * np.hanning(len(a)))) ** 2
    fr = np.fft.rfftfreq(len(a), 1 / rate)
    tot = f[fr > 30].sum()
    return [f[(fr >= lo) & (fr < hi)].sum() / tot for lo, hi in ((30, 250), (250, 500), (500, 1000), (1000, 2000), (2000, rate))]


def build(name):
    prog, note, dur, kind, key = SAMPLES[name]
    a = render(prog, note, dur + 0.3, 120)
    start = np.argmax(np.abs(a) > 0.002)                           # stilte vooraan weg
    a = a[start:start + int(dur * FS)]
    a = chain(kind, a)
    a = resample(a, FS, RATE)
    a = norm(a) * 0.97                                             # 8 bit: volle schaal
    low = min(note)
    a, loop = auto_loop(a, RATE, RATE / (440 * 2 ** ((low - 69) / 12)))
    a = np.round(a * 127) / 127                                    # 8 bit (zoals in de ROM)
    return a, loop, key


def main():
    if '--bands' in sys.argv:
        print('%-22s %s' % ('sample', '<250 / 250-500 / 500-1k / 1-2k / >2k (%)'))
        for name in SAMPLES:
            a, loop, key = build(name)
            print('%-22s %s' % (name, ' / '.join('%2.0f' % (100 * x) for x in bands(a, RATE))))
        return
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for old in old_samples():
        inc = inc.replace('\n\t.align 2\nDirectSoundWaveData_%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (old, old), '')
        for ext in ('.wav', '.bin'):
            if os.path.exists(OUT + old + ext):
                os.remove(OUT + old + ext)
    assert 'DirectSoundWaveData_heatran_' not in inc.replace('DirectSoundWaveData_heatran_st_', ''), 'oude labels'
    total = 0
    for name in SAMPLES:
        a, loop, key = build(name)
        write_wav(OUT + name + '.wav', a, RATE, key, loop)
        total += len(a)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-20s %-5s %6d samples  banden %s' % (name, SAMPLES[name][3], len(a),
                                                      ' / '.join('%2.0f' % (100 * x) for x in bands(a, RATE))))
    print('totaal %.0f KB' % (total / 1024))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
