#!/usr/bin/env python3
"""Project Grounded: de Heatran-samples (heatran_gb_*), v5: Kyuss' 'Odyssey' op een Game Boy Advance.

Jordi over v5: 'het moet klinken alsof Kyuss de originele R/S-Heatran-baasmuziek op de GBA inspeelde': low-bitrate,
zwaar gecomprimeerde, verzadigde 'crunchy' 16-bit-PCM-gitaren in C-standard, geen moderne studioklank.
Daarom maar weinig eigen samples; de rest is de echte Gen 3-soundfont (zie heatran_theme.py):
  - leadgitaar = sd90_classical_distortion_guitar_high, feedback = sd90_classical_overdrive_guitar,
  - bas = sc88pro_synth_bass, drums = rnd_kick / rnd_snare / orchestra crash / hihats / sc55-tom (drumsets/heatran.inc).
Eigen: de slaggitaar in C-standard (laagste noot C2), want de Gen 3-gitaren liggen op C3/C4 en klinken twee octaven
omlaag als een 'puuup'. Gemaakt zoals een Gen 3-sample: FluidR3 Distortion Guitar (GM 30), hard gecomprimeerd
(tanh), presence-bult rond 1,2 kHz, lowpass 5 kHz, naar 13.379 Hz (de samplerate van de Gen 3-gitaren), 8 bit, een
korte loop (±0,25 s) in het sustain. Eén sample per riffnoot (keysplit_heatran): powerchord (grondtoon + kwint +
octaaf = 1 kanaal), riffnoot (grondtoon + octaaf) en palm-mute.

Rendert met fluidsynth, schrijft 8-bit WAV's met smpl-chunk; make maakt er .bin van.
Vereist: apt-get install fluidsynth fluid-soundfont-gm.  Gebruik: python3 tools/grounded/heatran_samples.py"""
import os, glob, struct, subprocess, tempfile, wave
import numpy as np
import mido
from scipy.signal import butter, sosfilt, lfilter

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
DRUMKIT = 16
FS = 44100                       # bewerken op 44,1 kHz
RATE = 13379                     # = samplerate van de Gen 3-gitaarsamples (sd90_classical_*)

RIFF_KEYS = (36, 39, 41, 42, 43, 46, 48)   # C2 Eb2 F2 Gb2 G2 Bb2 C3 (keysplit_heatran, index 0-6)

# naam: (GM-programma, noten (akkoord = tuple), lengte in s, loop, keten, label-toets)
SAMPLES = {}
for k in RIFF_KEYS:
    SAMPLES['heatran_gb_pw_%d' % k] = (30, (k, k + 7, k + 12), 0.75, 'auto', 'gb', k)    # powerchord, 1 kanaal
    SAMPLES['heatran_gb_nt_%d' % k] = (30, (k, k + 12), 0.75, 'auto', 'gb', k)           # riffnoot (+ octaaf)
    SAMPLES['heatran_gb_pm_%d' % k] = (30, (k, k + 7), 0.30, None, 'gbmute', k)          # palm-mute


def old_samples():
    """Alle heatran_*-samples van v1-v4 (heatran_gb_* is v5). Geen ander thema gebruikt ze (gecontroleerd v0.9.80)."""
    names = {os.path.basename(p)[:-4] for p in glob.glob(OUT + 'heatran_*.wav') + glob.glob(OUT + 'heatran_*.bin')}
    return sorted(n for n in names if not n.startswith('heatran_gb_'))


def render(prog, note, dur, vel=112):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 9 if prog >= 128 else 0
    notes = note if isinstance(note, tuple) else (note,)
    t.append(mido.Message('program_change', channel=ch, program=DRUMKIT if ch == 9 else prog, time=0))
    for n in notes:
        t.append(mido.Message('note_on', channel=ch, note=n, velocity=vel, time=0))
    for i, n in enumerate(notes):
        t.append(mido.Message('note_off', channel=ch, note=n, velocity=0, time=int(dur * 960) if i == 0 else 0))
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
    """RBJ-cookbook: 'bp' (bandpass, piek 0 dB), 'peak', 'lowshelf'."""
    A = 10 ** (gain_db / 40)
    w = 2 * np.pi * f0 / FS
    al = np.sin(w) / (2 * q)
    c = np.cos(w)
    if kind == 'bp':
        b = [al, 0, -al]; a = [1 + al, -2 * c, 1 - al]
    elif kind == 'peak':
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
def gba_crunch(a, drive=4.0):
    """Zoals een Gen 3-gitaarsample: hard gecomprimeerd/verzadigd, presence rond 1,2 kHz, geen 'lucht' (lowpass 5 kHz)."""
    a = sosfilt(sos('highpass', 70, 2), a)
    a = np.tanh(norm(a) * drive)
    a = bqf(a, 'peak', 1200, 1.0, 3.0)
    a = bqf(a, 'lowshelf', 160, 0.7, 3.0)
    a = np.tanh(norm(a) * 1.6)                       # tweede compressie: bijna blokvormig, 'crunchy'
    return sosfilt(sos('lowpass', 5000, 4), a)


def chain(kind, a):
    if kind == 'gb':
        return gba_crunch(a)
    if kind == 'gbmute':                             # palm-mute: snaar sterft snel, minder verzadiging
        a = a * np.exp(-np.arange(len(a)) / FS / 0.07)
        a = gba_crunch(a, 2.5)
        return a * np.exp(-np.arange(len(a)) / FS / 0.12)
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


def write_wav(path, x, rate, key, loop):
    q = np.clip(np.round(x * 127), -128, 127).astype(np.int16) + 128
    data = q.astype(np.uint8).tobytes()
    fmt = struct.pack('<HHIIHH', 1, 1, rate, rate, 1, 8)
    nloops = 1 if loop else 0
    smpl = struct.pack('<9I', 0, 0, int(1e9 / rate), key, 0, 0, 0, nloops, 0)
    if loop:
        smpl += struct.pack('<6I', 0, 0, loop[0], loop[1] - 1, 0, 0)
    chunks = b'fmt ' + struct.pack('<I', len(fmt)) + fmt + b'smpl' + struct.pack('<I', len(smpl)) + smpl
    chunks += b'data' + struct.pack('<I', len(data)) + data + (b'\0' if len(data) & 1 else b'')
    open(path, 'wb').write(b'RIFF' + struct.pack('<I', 4 + len(chunks)) + b'WAVE' + chunks)


def make(name, out=OUT):
    prog, note, dur, loop, kind, key = SAMPLES[name]
    a = render(prog, note, dur + 0.3, 120)
    start = np.argmax(np.abs(a) > 0.002)                           # stilte vooraan weg
    a = a[start:start + int(dur * FS)]
    low = min(note) if isinstance(note, tuple) else note
    a = chain(kind, a)
    a = resample(a, FS, RATE)
    a = norm(a) * 0.97                                             # 8 bit: volle schaal
    if loop == 'auto':
        a, loop = auto_loop(a, RATE, RATE / (440 * 2 ** ((low - 69) / 12)))
    else:
        fade = int(RATE * 0.03)
        a[-fade:] *= np.linspace(1, 0, fade)
    write_wav(out + name + '.wav', a, RATE, key, loop)
    return len(a)


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for old in old_samples():
        inc = inc.replace('\n\t.align 2\nDirectSoundWaveData_%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (old, old), '')
        for ext in ('.wav', '.bin'):
            if os.path.exists(OUT + old + ext):
                os.remove(OUT + old + ext)
    assert 'DirectSoundWaveData_heatran_' not in inc.replace('DirectSoundWaveData_heatran_gb_', ''), 'oude labels'
    total = 0
    for name in SAMPLES:
        n = make(name)
        total += n
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-20s %-7s %6d samples' % (name, SAMPLES[name][4], n))
    print('totaal %.0f KB' % (total / 1024))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
