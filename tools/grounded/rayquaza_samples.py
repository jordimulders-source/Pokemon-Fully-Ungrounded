#!/usr/bin/env python3
"""Project Grounded: de Rayquaza-gamelansamples (rayquaza_*, additief gesynthetiseerd: tabel ADDITIVE). Afgesplitst
van gm_samples.py bij het samenvoegen (v0.9.66); genereert alleen de rayquaza_*-samples.

Oorspronkelijk: eigen DirectSound-samples uit de GM-soundfont FluidR3 (voor instrumenten die de game niet heeft,
zoals een schone e-gitaar of steel drums). Rendert één noot met fluidsynth, knipt, resamplet en schrijft een 8-bit
WAV met smpl-chunk (grondtoon + eventuele loop); make zet die via wav2agb om in een .bin.
Vereist: apt-get install fluidsynth fluid-soundfont-gm (zie MUZIEK.md).
Gebruik: python3 tools/grounded/rayquaza_samples.py"""
import os, struct, subprocess, tempfile, wave
import numpy as np
import mido

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'

# naam: (GM-programma, noot, lengte in s, samplerate, loop) ; loop=None -> eenmalig (uitklinkend instrument)
SAMPLES = {
    'gm_clean_guitar': (27, 60, 1.6, 16000, None),
    'gm_steel_drums':  (114, 72, 0.9, 22050, None),
}
# gesynthetiseerde golven met een loop van precies 4 perioden op C4 (64 samples per periode): (golf, harmonischen)
WAVES = {
    'gm_saw_lead': ('saw', 24),
}
# additief gesynthetiseerde, uitklinkende slaginstrumenten met inharmonische partialen (gamelan voor Battle! Rayquaza,
# rayquaza_theme.py). naam: (grondtoon-noot, lengte s, samplerate, ombak Hz, aanslag (amp, ms, helderheid),
#                              [(verhouding, amplitude, t60 in s), ...])
# ombak = een tweede, licht ontstemd exemplaar erbij (pengumbang/pengisep): de zweving van een gamelanpaar zit in de
# sample, dus één DirectSound-kanaal per paar.
ADDITIVE = {
    # gangsa (pemade/kantilan): bronzen staaf boven een bamboeresonator, harde hoornen hamer -> heldere tik
    'rayquaza_gangsa':  (72, 1.3, 16000, 6.0, (0.35, 6, 0.8),
                         [(1.0, 1.0, 1.4), (2.0, 0.08, 0.5), (2.76, 0.30, 0.45), (5.40, 0.14, 0.16), (8.93, 0.06, 0.07)]),
    # reyong/trompong: gebolde ketelgong, zachtere hamer (met touw omwonden) -> ronde 'tong' met ketelklank
    'rayquaza_reyong':  (72, 1.6, 16000, 5.0, (0.25, 8, 0.4),
                         [(1.0, 1.0, 1.6), (1.51, 0.10, 0.6), (2.02, 0.22, 0.8), (2.93, 0.18, 0.5), (4.13, 0.10, 0.3),
                          (5.65, 0.05, 0.15)]),
    # jegogan/calung: grote, diepe staven met lange bamboeresonator, zachte hamer -> bijna zuivere, lange toon
    'rayquaza_jegogan': (48, 2.6, 11025, 2.5, (0.12, 12, 0.2),
                         [(1.0, 1.0, 3.2), (2.0, 0.10, 1.2), (2.76, 0.16, 0.8), (5.40, 0.05, 0.25)]),
    # gong ageng: grote gebolde gong, gezoem op de grondtoon + octaaf, langzame 'golf' (ombak ±1,5 Hz), lange nagalm
    'rayquaza_gong':    (36, 5.0, 8000, 1.4, (0.30, 25, 0.15),
                         [(1.0, 1.0, 7.0), (2.0, 0.55, 4.5), (2.97, 0.30, 2.5), (4.18, 0.16, 1.4), (5.46, 0.10, 0.9),
                          (7.10, 0.06, 0.5), (9.2, 0.03, 0.3)]),
}


def synth(kind, harm, per=64, cycles=4):
    t = np.arange(per * cycles) / per * 2 * np.pi
    a = np.zeros_like(t)
    for k in range(1, harm + 1):
        roll = 1.0 if k <= harm // 2 else np.cos((k - harm // 2) / (harm // 2) * np.pi / 2) ** 2   # zachte bovenkant
        a += roll * np.sin(k * t) / k
    return a / np.abs(a).max() * 0.97, int(round(261.6256 * per))


def additive(key, dur, rate, ombak, strike, partials, seed=1):
    """Uitklinkende inharmonische klank: som van gedempte sinussen (t60 per partiaal), plus een licht ontstemde kopie
    (ombak) en een korte, gefilterde ruisaanslag van de hamer. Geen loop: de sample klinkt uit en geeft het kanaal vrij."""
    rng = np.random.default_rng(seed)
    f0 = 440.0 * 2 ** ((key - 69) / 12)
    t = np.arange(int(dur * rate)) / rate
    a = np.zeros_like(t)
    for ratio, amp, t60 in partials:
        f = f0 * ratio
        if f > rate * 0.45:
            continue
        env = np.exp(-6.91 * t / t60)
        for det, w in ((0.0, 1.0), (ombak * ratio ** 0.5, 0.85)):   # ombak: hogere partialen zweven iets sneller
            a += w * amp * env * np.sin(2 * np.pi * (f + det) * t + rng.uniform(0, 2 * np.pi))
    s_amp, s_ms, bright = strike
    n = int(rate * s_ms / 1000) * 4
    if n:
        noise = rng.standard_normal(n)
        k = max(1, int(round(1 / max(bright, 0.05))))              # helderheid -> eenvoudig laagdoorlaatfilter
        noise = np.convolve(noise, np.ones(k) / k, mode='same')
        noise *= np.exp(-np.arange(n) / (rate * s_ms / 1000))
        a[:n] += s_amp * noise / np.abs(noise).max() * np.abs(a[:n]).max()
    fade = int(rate * 0.06)
    a[-fade:] *= np.linspace(1, 0, fade)
    a[:int(rate * 0.001)] *= np.linspace(0, 1, int(rate * 0.001))   # geen klik bij de aanzet
    return a / np.abs(a).max() * 0.97


def render(prog, note, dur):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    t.append(mido.Message('program_change', program=prog, time=0))
    t.append(mido.Message('note_on', note=note, velocity=110, time=0))
    t.append(mido.Message('note_off', note=note, velocity=0, time=int(dur * 960)))   # 120 bpm: 960 ticks/s
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', '44100', '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


def resample(a, src, dst):
    n = int(len(a) * dst / src)
    return np.interp(np.arange(n) * src / dst, np.arange(len(a)), a)


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



SAMPLES = {k: v for k, v in SAMPLES.items() if k.startswith('rayquaza_')}
WAVES = {}

def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for name, (prog, note, dur, rate, loop) in SAMPLES.items():
        a = render(prog, note, dur)
        start = np.argmax(np.abs(a) > 0.002)                       # stilte vooraan weg
        a = resample(a[start:start + int(dur * 44100)], 44100, rate)
        a = a / max(1e-6, np.abs(a).max()) * 0.97                  # 8 bit: volle schaal
        if loop is None:
            fade = int(rate * 0.05)
            a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, rate, note, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s GM %3d noot %d, %d samples @ %d Hz' % (name, prog, note, len(a), rate))
    for name, (kind, harm) in WAVES.items():
        a, rate = synth(kind, harm)
        write_wav(OUT + name + '.wav', a, rate, 60, (0, len(a)))
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s %s, loop %d samples @ %d Hz' % (name, kind, len(a), rate))
    for name, (key, dur, rate, ombak, strike, partials) in ADDITIVE.items():
        a = additive(key, dur, rate, ombak, strike, partials)
        write_wav(OUT + name + '.wav', a, rate, key, None)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s additief, noot %d, %d samples @ %d Hz' % (name, key, len(a), rate))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
