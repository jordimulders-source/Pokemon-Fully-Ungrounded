#!/usr/bin/env python3
"""Project Grounded: de Heatran-samples (heatran_*), v3 (desert/stoner rock & heavy psych à la Kyuss/Sleep).

Jordi over v2: 'klinkt als surf rock, ska-punk of upbeat 60s rock'. De v2-fuzz had een middenboost (150-700 Hz,
'honk' = 60s-fuzz zoals een Maestro/Tone Bender) en vertrok van GM 30 (al vervormd). v3 bouwt de keten zoals een echte
stonerrig: een schone gitaar (FluidR3 GM 27/28/33) gaat door
  - 'Big Muff': ingangshighpass, twee clipstadia (het tweede licht asymmetrisch), daarna de Muff-toonregeling met de
    typische middenscoop (lowpass 400 Hz + highpass 1 kHz, knop richting bas);
  - 'SVT/Sunn + 4x12/8x10': lage shelf +5 dB onder 150 Hz, lichte buisoverdrive, kast-resonantie rond 100 Hz en een
    steile kast-lowpass (2 x 2-polig) op 2,0-2,6 kHz: geen treble, geen twang.
Akkoorden worden in één sample gerenderd (C2+G2+C3 = 1 kanaal per powerchord, de intermodulatie zit erin), met een
gecrossfade loop in het fuzz-sustain. Drums uit de FluidR3 'Power'-kit (programma 16 op kanaal 10): dikke kick/snare
met kamer; bekkens licht verzadigd (gruizig).

Rendert met fluidsynth, knipt, resamplet (anti-alias) en schrijft 8-bit WAV's met smpl-chunk; make maakt er .bin van.
Vereist: apt-get install fluidsynth fluid-soundfont-gm (zie MUZIEK.md).  Gebruik: python3 tools/grounded/heatran_samples.py"""
import os, struct, subprocess, tempfile, wave
import numpy as np
import mido
from scipy.signal import butter, sosfilt

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
DRUMKIT = 16                     # FluidR3 'Power'-kit

# naam: (GM-programma, noot, lengte in s, samplerate, loop, keten)
#   noot mag een tuple zijn (akkoord in één sample); programma 128 = drumkit (noot = drumtoets)
#   loop='auto' -> aanhoudend (gecrossfade loop in het sustaindeel), None -> eenmalig
#   keten: 'muff' (stonerfuzz), 'mute' (palm-mute door dezelfde fuzz), 'svt' (fuzzbas), 'lead', 'warm' (schoon,
#   donker), 'drum', 'cymbal' (licht verzadigd), of None
SAMPLES = {
    'heatran_doom_power':  (27, (36, 43, 48), 3.0, 22050, 'auto', 'muff'),
    'heatran_doom_mute':   (27, (36, 43, 48), 0.6, 22050, None, 'mute'),
    'heatran_svt_bass':    (33, 36, 2.4, 16000, 'auto', 'svt'),
    'heatran_doom_lead':   (27, 60, 2.4, 22050, 'auto', 'lead'),
    'heatran_warm_clean':  (26, 60, 2.0, 16000, None, 'warm'),
    'heatran_kick':        (128, 36, 0.6, 16000, None, 'drum'),
    'heatran_snare':       (128, 38, 0.9, 22050, None, 'snare'),
    'heatran_floor_tom':   (128, 41, 1.0, 16000, None, 'drum'),
    'heatran_open_hat':    (128, 46, 1.0, 22050, None, 'cymbal'),
    'heatran_ride':        (128, 51, 1.8, 22050, None, 'cymbal'),
    'heatran_crash':       (128, 49, 2.4, 22050, None, 'cymbal'),
    'heatran_china':       (128, 52, 2.0, 22050, None, 'cymbal'),
    'heatran_side_stick':  (128, 37, 0.3, 22050, None, 'drum'),
}
# v1/v2-samples die v3 niet meer gebruikt (worden verwijderd, ook uit direct_sound_data.inc)
OLD = ('heatran_fuzz_power', 'heatran_fuzz_low', 'heatran_fuzz_bass', 'heatran_fuzz_lead', 'heatran_muff_power',
       'heatran_muff_low', 'heatran_doom_low', 'heatran_mute_power', 'heatran_octfuzz_bass', 'heatran_closed_hat')


def render(prog, note, dur, vel=110):
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
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', '44100', '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


def resample(a, src, dst, antialias=True):
    if antialias and dst < src:                                     # alles boven 0,45 x de nieuwe samplerate eruit (anti-alias)
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


def bq(kind, f, fs, order=2):
    return butter(order, f, kind, fs=fs, output='sos')


def peak(a, f, gain_db, q, fs):
    """Resonantie/scoop: bandpass rond f erbij optellen (gain > 0) of aftrekken (gain < 0)."""
    bw = f / q
    band = sosfilt(bq('bandpass', [max(20, f - bw / 2), f + bw / 2], fs), a)
    return a + (10 ** (gain_db / 20) - 1) * band


def big_muff(a, fs, gain=60.0, tone=0.75):
    """Twee clipstadia met een lowpass ertussen (de Muff-transistoren), dan de passieve toonregeling: mengsel van
    lowpass 400 Hz (tone) en highpass 1 kHz (1 - tone) = de typische middenscoop rond 700-1000 Hz."""
    a = sosfilt(bq('highpass', 70, fs, 1), a / max(1e-6, np.abs(a).max()))
    a = np.tanh(a * gain)
    a = sosfilt(bq('lowpass', 5000, fs, 1), a)
    a = np.tanh(a * 6.0 + 0.15) - np.tanh(0.15)                     # tweede stadium, licht asymmetrisch
    return tone * sosfilt(bq('lowpass', 400, fs, 1), a) + (1 - tone) * sosfilt(bq('highpass', 1000, fs, 1), a)


def amp_cab(a, fs, cab=2200, drive=1.6, low_db=5.0):
    """SVT/Sunn-achtige buisversterker + 4x12-kast: lage shelf, lichte buisoverdrive, kastresonantie rond 100 Hz,
    steile kast-lowpass (4-polig), highpass tegen subrommel/DC."""
    a = a / max(1e-6, np.abs(a).max())
    a = a + (10 ** (low_db / 20) - 1) * sosfilt(bq('lowpass', 150, fs), a)
    a = np.tanh(a * drive)
    a = peak(a, 105, 4.0, 1.4, fs)
    a = sosfilt(bq('lowpass', cab, fs), sosfilt(bq('lowpass', cab * 1.15, fs), a))
    return sosfilt(bq('highpass', 45, fs), a)


def chain(name, kind, a, fs):
    if kind == 'muff':
        return amp_cab(big_muff(a, fs, 80.0, 0.5), fs, 3200, 1.6, 3.0)
    if kind == 'mute':                       # palm-mute: de handpalm dempt de boventonen van de snaar (lowpass vóór
        env = np.exp(-np.arange(len(a)) / fs / 0.12)                    # de fuzz) en de snaar sterft snel; na de
        a = sosfilt(bq('lowpass', 800, fs), a) * env                    # fuzz nog een keer dempen, anders blaast
        a = amp_cab(big_muff(a, fs, 50.0, 0.6), fs, 2800, 1.8, 4.0)     # de fuzz de staart weer op
        return a * np.exp(-np.arange(len(a)) / fs / 0.22)
    if kind == 'svt':                        # fuzzbas: SVT-overdrive + schoon laag (bas-blend), growl rond 700 Hz
        clean = sosfilt(bq('lowpass', 180, fs), a / max(1e-6, np.abs(a).max()))
        d = np.tanh(a / max(1e-6, np.abs(a).max()) * 14.0)
        d = peak(d, 700, 3.0, 1.2, fs)
        d = sosfilt(bq('lowpass', 2000, fs), sosfilt(bq('lowpass', 2400, fs), d))
        return sosfilt(bq('highpass', 38, fs), d / np.abs(d).max() + 0.5 * clean / np.abs(clean).max())
    if kind == 'lead':                       # lead: dezelfde Muff, toon iets meer naar de middens, kast 2,8 kHz
        return amp_cab(big_muff(a, fs, 80.0, 0.6), fs, 2300, 1.4, 2.0)
    if kind == 'warm':                       # schone halfakoestische gitaar, toonknop dicht (geen twang)
        a = sosfilt(bq('lowpass', 1700, fs), sosfilt(bq('lowpass', 2200, fs), a))
        return np.tanh(a / np.abs(a).max() * 1.5)
    if kind == 'snare':                      # dikke snare: body laten, de kamer-sis eraf, licht verzadigd
        a = np.tanh(a / np.abs(a).max() * 1.8)
        return sosfilt(bq('lowpass', 4000, fs, 1), a)
    if kind == 'cymbal':                     # gruizig: licht verzadigd, bovenkant iets eraf
        a = np.tanh(a / np.abs(a).max() * 2.0)
        return sosfilt(bq('lowpass', 4500, fs, 1), a)
    return a


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
    prog, note, dur, rate, loop, kind = SAMPLES[name]
    a = render(prog, note, dur)
    start = np.argmax(np.abs(a) > 0.002)                           # stilte vooraan weg
    a = a[start:start + int(dur * 44100)]
    a = chain(name, kind, a, 44100)                                # vervormen op 44,1 kHz, dan pas omlaag
    a = resample(a, 44100, rate)
    a = a / max(1e-6, np.abs(a).max()) * 0.97                      # 8 bit: volle schaal
    if loop == 'auto':
        a, loop = auto_loop(a, rate)
    else:
        fade = int(rate * 0.05)
        a[-fade:] *= np.linspace(1, 0, fade)
    key = 60 if prog >= 128 else (note[0] if isinstance(note, tuple) else note)
    write_wav(out + name + '.wav', a, rate, key, loop)
    return len(a), rate


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for old in OLD:       # samples die v3 niet meer gebruikt
        inc = inc.replace('\n\t.align 2\nDirectSoundWaveData_%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (old, old), '')
        for ext in ('.wav', '.bin'):
            if os.path.exists(OUT + old + ext):
                os.remove(OUT + old + ext)
    for name in SAMPLES:
        n, rate = make(name)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-20s %s, %d samples @ %d Hz' % (name, SAMPLES[name][5], n, rate))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
