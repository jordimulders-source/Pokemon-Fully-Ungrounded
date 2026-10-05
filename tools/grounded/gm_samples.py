#!/usr/bin/env python3
"""Project Grounded: eigen DirectSound-samples uit de GM-soundfont FluidR3 (voor instrumenten die de game niet heeft,
zoals een schone e-gitaar of steel drums). Rendert één noot met fluidsynth, knipt, resamplet en schrijft een 8-bit
WAV met smpl-chunk (grondtoon + eventuele loop); make zet die via wav2agb om in een .bin.
Vereist: apt-get install fluidsynth fluid-soundfont-gm (zie MUZIEK.md).
Gebruik: python3 tools/grounded/gm_samples.py"""
import os, struct, subprocess, tempfile, wave
import numpy as np
import mido

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'

# naam: (GM-programma, noot, lengte in s, samplerate, loop) ; loop=None -> eenmalig (uitklinkend instrument)
# noot mag een tuple zijn (akkoord in één sample, bv. een powerchord = 1 kanaal); programma 128 = GM-drumkit
# (kanaal 10, noot = drumtoets); loop='auto' -> aanhoudend instrument met een gecrossfade loop in het sustaindeel.
SAMPLES = {
    'gm_clean_guitar': (27, 60, 1.6, 16000, None),
    'gm_steel_drums':  (114, 72, 0.9, 22050, None),
    # Battle! Heatran (heatran_theme.py, stoner metal à la Kyuss): fuzzgitaar als powerchord (G2+D3+G3) en als
    # losse noot, fuzzbas (picked bass + eigen overdrive), en een rockkit uit FluidR3 (ride, open hihat, toms)
    'heatran_fuzz_power':  (30, (43, 50, 55), 2.4, 22050, 'auto'),
    'heatran_fuzz_low':    (30, 43, 2.4, 22050, 'auto'),
    'heatran_fuzz_lead':   (30, 69, 2.0, 22050, 'auto'),
    'heatran_fuzz_bass':   (34, 38, 2.0, 16000, 'auto'),
    'heatran_kick':        (128, 36, 0.5, 16000, None),
    'heatran_snare':       (128, 38, 0.6, 22050, None),
    'heatran_open_hat':    (128, 46, 0.9, 22050, None),
    'heatran_ride':        (128, 51, 1.6, 22050, None),
    'heatran_floor_tom':   (128, 41, 0.9, 16000, None),
    'heatran_crash':       (128, 49, 2.2, 22050, None),
}
# extra vervorming na het renderen (naam: (versterking, lowpass in Hz)): tanh-overdrive, daarna de hoogte eraf
DRIVE = {
    'heatran_fuzz_bass': (6.0, 3500),
}
# gesynthetiseerde golven met een loop van precies 4 perioden op C4 (64 samples per periode): (golf, harmonischen)
WAVES = {
    'gm_saw_lead': ('saw', 24),
}


def synth(kind, harm, per=64, cycles=4):
    t = np.arange(per * cycles) / per * 2 * np.pi
    a = np.zeros_like(t)
    for k in range(1, harm + 1):
        roll = 1.0 if k <= harm // 2 else np.cos((k - harm // 2) / (harm // 2) * np.pi / 2) ** 2   # zachte bovenkant
        a += roll * np.sin(k * t) / k
    return a / np.abs(a).max() * 0.97, int(round(261.6256 * per))


def render(prog, note, dur):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 9 if prog >= 128 else 0
    notes = note if isinstance(note, tuple) else (note,)
    if ch == 0:
        t.append(mido.Message('program_change', program=prog, time=0))
    for n in notes:
        t.append(mido.Message('note_on', channel=ch, note=n, velocity=110, time=0))
    for i, n in enumerate(notes):
        t.append(mido.Message('note_off', channel=ch, note=n, velocity=0, time=int(dur * 960) if i == 0 else 0))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', '44100', '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


LEGACY = {'gm_clean_guitar', 'gm_steel_drums'}     # goedgekeurd zonder anti-aliasfilter: niet meer veranderen


def resample(a, src, dst, antialias=False):
    if antialias and dst < src:                       # alles boven 0,45 x de nieuwe samplerate eruit (anders aliasing)
        f = np.fft.rfft(a)
        f[int(len(f) * 0.9 * dst / src):] = 0
        a = np.fft.irfft(f, len(a))
    n = int(len(a) * dst / src)
    return np.interp(np.arange(n) * src / dst, np.arange(len(a)), a)


def auto_loop(a, rate):
    """Loop in het sustaindeel: lengte ±0,3 s waar het signaal het best op zichzelf lijkt (autocorrelatie), en de
    laatste 40% van de loop gecrossfade met wat vóór het loopbegin staat (geen klik bij de terugsprong)."""
    s = int(len(a) * 0.45)
    want, n = int(rate * 0.3), int(rate * 0.05)
    best = max(range(int(want * 0.9), int(want * 1.1)),
               key=lambda L: np.dot(a[s:s + n], a[s + L:s + L + n]) / (np.linalg.norm(a[s + L:s + L + n]) + 1e-9))
    e = s + best
    f = int(best * 0.4)
    w = np.linspace(0, 1, f)
    a = a[:e].copy()
    a[e - f:e] = a[e - f:e] * (1 - w) + a[s - f:s] * w
    return a, (s, e)


def drive(a, rate, gain, lp):
    a = np.tanh(a / max(1e-6, np.abs(a).max()) * gain)
    k = np.exp(-2 * np.pi * lp / rate)                 # eenpolige lowpass (de fuzz-sis eraf)
    out, y = np.empty_like(a), 0.0
    for i, x in enumerate(a):
        y = (1 - k) * x + k * y
        out[i] = y
    return out


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


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for name, (prog, note, dur, rate, loop) in SAMPLES.items():
        a = render(prog, note, dur)
        start = np.argmax(np.abs(a) > 0.002)                       # stilte vooraan weg
        a = resample(a[start:start + int(dur * 44100)], 44100, rate, antialias=name not in LEGACY)
        if name in DRIVE:
            a = drive(a, rate, *DRIVE[name])
        a = a / max(1e-6, np.abs(a).max()) * 0.97                  # 8 bit: volle schaal
        if loop == 'auto':
            a, loop = auto_loop(a, rate)
        elif loop is None:
            fade = int(rate * 0.05)
            a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, rate, 60 if prog >= 128 else (note[0] if isinstance(note, tuple) else note), loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s GM %3d noot %s, %d samples @ %d Hz' % (name, prog, note, len(a), rate))
    for name, (kind, harm) in WAVES.items():
        a, rate = synth(kind, harm)
        write_wav(OUT + name + '.wav', a, rate, 60, (0, len(a)))
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s %s, loop %d samples @ %d Hz' % (name, kind, len(a), rate))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
