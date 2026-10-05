#!/usr/bin/env python3
"""Project Grounded: de Keccles-samples (kc_*: trombone, cuatro, salsapercussie). Afgesplitst van gm_samples.py bij
het samenvoegen (v0.9.66); genereert alleen de kc_*-samples.

Oorspronkelijk: eigen DirectSound-samples uit de GM-soundfont FluidR3 (voor instrumenten die de game niet heeft,
zoals een schone e-gitaar of steel drums). Rendert één noot met fluidsynth, knipt, resamplet en schrijft een 8-bit
WAV met smpl-chunk (grondtoon + eventuele loop); make zet die via wav2agb om in een .bin.
Vereist: apt-get install fluidsynth fluid-soundfont-gm (zie MUZIEK.md).
Gebruik: python3 tools/grounded/keccles_samples.py"""
import os, struct, subprocess, tempfile, wave
import numpy as np
import mido

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'

# naam: (GM-programma, noot, lengte in s, samplerate, loop) ; loop=None -> eenmalig (uitklinkend instrument),
# loop='auto' -> aanhoudend instrument (koper): een loop van hele perioden met crossfade (zie auto_loop).
# GM-programma 'drum' = GM-drumkit (kanaal 10), noot = drumnoot; de sample krijgt grondtoon 60 (speel op 60 = echt).
SAMPLES = {
    'gm_clean_guitar': (27, 60, 1.6, 16000, None),
    'gm_steel_drums':  (114, 72, 0.9, 22050, None),
    # Battle! Keccles v2 (keccles_theme.py): trombones, cuatro (= steel-string, hoog), salsa-percussie
    'kc_trombone_55':  (57, 55, 1.0, 22050, 'auto'),
    'kc_trombone_67':  (57, 67, 1.0, 22050, 'auto'),
    'kc_cuatro':       (25, 74, 0.7, 22050, None),
    'kc_bongo_hi':     ('drum', 60, 0.25, 22050, None),
    'kc_bongo_lo':     ('drum', 61, 0.3, 22050, None),
    'kc_claves':       ('drum', 75, 0.2, 22050, None),
    'kc_cowbell':      ('drum', 56, 0.35, 22050, None),
    'kc_timbale_hi':   ('drum', 65, 0.45, 22050, None),
    'kc_timbale_lo':   ('drum', 66, 0.5, 22050, None),
    'kc_guiro_long':   ('drum', 74, 0.45, 22050, None),
    # Keccles v3: riffende elektrische gitaar à la 'Vigilante' (Colón/Blades 1983): FluidR3 GM 27 (clean) door een
    # lichte overdrive (CRUNCH; GM 29 van FluidR3 is al zo fuzzy als een distortion), met loop (aanhoudende bends);
    # tabel keysplit_french_horn (t/m 66 = A3, daarboven = A4)
    'kc_guitar_57':    (27, 57, 1.2, 22050, 'auto'),
    'kc_guitar_69':    (27, 69, 1.2, 22050, 'auto'),
}
CRUNCH = {'kc_guitar_57': (4.0, 3500), 'kc_guitar_69': (4.0, 3500)}   # (tanh-versterking, lowpass Hz)
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


def render(prog, note, dur, vel=110):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 9 if prog == 'drum' else 0
    if ch == 0:
        t.append(mido.Message('program_change', program=prog, time=0))
    t.append(mido.Message('note_on', channel=ch, note=note, velocity=vel, time=0))
    t.append(mido.Message('note_off', channel=ch, note=note, velocity=0, time=int(dur * 960)))   # 120 bpm: 960 ticks/s
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


def auto_loop(a, rate, note, at=0.45, length=0.12, xfade=0.03):
    """Aanhoudende noot: loop [s, e) van een geheel aantal perioden (zo dicht mogelijk bij een gehele lengte), het
    einde gecrossfade met het stuk vóór s, zodat de sprong e -> s geen klik geeft. Geeft (a[:e], (s, e))."""
    per = rate / (440.0 * 2 ** ((note - 69) / 12))
    best = min(range(max(1, int(length * rate / per)), int(2 * length * rate / per) + 1),
               key=lambda m: abs(m * per - round(m * per)))
    L = int(round(best * per))
    e = int(at * rate) + L
    s = e - L
    x = int(xfade * rate)
    w = np.linspace(0, 1, x)
    a = a.copy()
    a[e - x:e] = a[e - x:e] * (1 - w) + a[s - x:s] * w
    return a[:e], (s, e)


def drive(a, rate, gain, lp):
    """Lichte overdrive: tanh-verzadiging en een eenpolige lowpass (de scherpe kant eraf)."""
    a = np.tanh(a / max(1e-6, np.abs(a).max()) * gain)
    k = np.exp(-2 * np.pi * lp / rate)
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



SAMPLES = {k: v for k, v in SAMPLES.items() if k.startswith('kc_')}
WAVES = {}

def main(only=()):
    """only: alleen deze samples (opnieuw) maken, bv. `keccles_samples.py kc_guitar_57 kc_guitar_69`."""
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for name, (prog, note, dur, rate, loop) in SAMPLES.items():
        if only and name not in only:
            continue
        a = render(prog, note, dur, 127 if prog in range(56, 64) else 110)
        if name in CRUNCH:
            a = drive(a, 44100, *CRUNCH[name])   # koper: vol = brallend (FluidR3-filter)
        start = np.argmax(np.abs(a) > 0.002)                       # stilte vooraan weg
        a = resample(a[start:start + int(dur * 44100)], 44100, rate)
        a = a / max(1e-6, np.abs(a).max()) * 0.97                  # 8 bit: volle schaal
        if loop == 'auto':
            a, loop = auto_loop(a, rate, note)
        elif loop is None:
            fade = int(rate * (0.02 if prog == 'drum' else 0.05))
            a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, rate, 60 if prog == 'drum' else note, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s GM %4s noot %d, %d samples @ %d Hz' % (name, prog, note, len(a), rate))
    for name, (kind, harm) in WAVES.items():
        a, rate = synth(kind, harm)
        write_wav(OUT + name + '.wav', a, rate, 60, (0, len(a)))
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s %s, loop %d samples @ %d Hz' % (name, kind, len(a), rate))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
