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
SAMPLES = {
    'gm_clean_guitar': (27, 60, 1.6, 16000, None),
    'gm_steel_drums':  (114, 72, 0.9, 22050, None),
    # Shaymin (shaymin_theme.py): harp, celesta en nylon zonder loop; fluit en klarinet met een loop van exacte
    # perioden (loop = (begin in s, perioden); de samplerate wordt dan grondtoon x 32 of 64, zodat een periode precies
    # een geheel aantal samples is, en het loopeinde vloeit over in het loopbegin)
    'shaymin_harp':     (46, 60, 1.6, 16000, None),
    'shaymin_celesta':  (8, 72, 1.2, 22050, None),
    'shaymin_nylon':    (24, 60, 1.4, 16000, None),
    'shaymin_flute':    (73, 72, 0.9, None, (0.35, 16)),
    'shaymin_clarinet': (71, 60, 0.9, None, (0.35, 8)),
    # Battle! Magikarp (magikarp_theme.py); ('drum', n) = GM-drumkanaal 10, noot n
    'magikarp_bassoon':   (70, 48, 1.2, 16000, None),
    'magikarp_woodblock': (115, 72, 0.3, 22050, None),
    'magikarp_vibraslap': (('drum', 58), 60, 1.1, 16000, None),
    'jirachi_celesta':   (8, 72, 1.5, 22050, None),     # Battle! Jirachi (jirachi_theme.py)
    'jirachi_music_box': (10, 72, 1.5, 22050, None),
}
# 'loopjes' van meerdere noten in één sample (bv. een windgong/mark tree): (GM-programma, grondtoon, noten,
# stap in s, lengte in s, samplerate)
RUNS = {
    'jirachi_chimes': (9, 96, [108, 105, 103, 100, 98, 96, 93, 91, 88, 86, 84, 81], 0.045, 1.4, 22050),
}
# gesynthetiseerde golven met een loop van precies 4 perioden op C4 (64 samples per periode): (golf, harmonischen)
WAVES = {
    'gm_saw_lead': ('saw', 24),
    'magikarp_kazoo': ('kazoo', 24),     # zoemende, nasale puls met formanten (kazoo)
}
# gesynthetiseerde eenmalige geluiden: naam -> (functie, samplerate)
ONESHOTS = {
    'magikarp_boing': ('boing', 16000),  # springveer/mondharp: 'bwoiiing'
}


def synth(kind, harm, per=64, cycles=4):
    t = np.arange(per * cycles) / per * 2 * np.pi
    a = np.zeros_like(t)
    if kind == 'kazoo':
        # kazoo: veel boventonen (zoem) met twee formanten rond de 4e en 9e harmonische (nasaal 'oe-ie')
        for k in range(1, harm + 1):
            amp = k ** -0.55 * (0.5 + np.exp(-((k - 4) / 1.6) ** 2) + 0.6 * np.exp(-((k - 9) / 2.5) ** 2))
            a += amp * np.sin(k * t + 0.3 * k * k)
        return a / np.abs(a).max() * 0.97, int(round(261.6256 * per))
    for k in range(1, harm + 1):
        roll = 1.0 if k <= harm // 2 else np.cos((k - harm // 2) / (harm // 2) * np.pi / 2) ** 2   # zachte bovenkant
        a += roll * np.sin(k * t) / k
    return a / np.abs(a).max() * 0.97, int(round(261.6256 * per))


def oneshot(kind, rate):
    if kind == 'boing':
        # springveer: toon die snel omhoog schiet en met een trage, brede vibrato uitzwiept; boventonen = twang
        n = int(rate * 0.75)
        t = np.arange(n) / rate
        f = 150 + 170 * (1 - np.exp(-t / 0.035)) + 55 * np.sin(2 * np.pi * 9 * t) * np.exp(-t / 0.35)
        ph = 2 * np.pi * np.cumsum(f) / rate
        a = np.sin(ph) + 0.55 * np.sin(2 * ph) * np.exp(-t / 0.12) + 0.3 * np.sin(3 * ph) * np.exp(-t / 0.08)
        env = np.minimum(1, t / 0.004) * np.exp(-t / 0.22)
        return a * env
    raise ValueError(kind)


def render(prog, note, dur, run=None, step=0.0):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 0
    if isinstance(prog, tuple):          # ('drum', n): GM-drumkanaal, noot n
        ch, note = 9, prog[1]
    else:
        t.append(mido.Message('program_change', program=prog, time=0))
    if run:                                    # loopje: noten na elkaar, allemaal tot het eind laten klinken
        for i, n in enumerate(run):
            t.append(mido.Message('note_on', channel=ch, note=n, velocity=100 - i * 3, time=0 if i == 0 else int(step * 960)))
        t.append(mido.Message('note_off', channel=ch, note=run[0], velocity=0, time=int(dur * 960)))
        for n in run[1:]:
            t.append(mido.Message('note_off', channel=ch, note=n, velocity=0, time=0))
    else:
        t.append(mido.Message('note_on', channel=ch, note=note, velocity=110, time=0))
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
    jobs = [(name, prog, note, dur, rate, loop, None, 0) for name, (prog, note, dur, rate, loop) in SAMPLES.items()]
    jobs += [(name, prog, key, dur, rate, None, run, step) for name, (prog, key, run, step, dur, rate) in RUNS.items()]
    for name, prog, note, dur, rate, loop, run, step in jobs:
        a = render(prog, note, dur + (1.0 if loop else 0), run, step)
        start = np.argmax(np.abs(a) > 0.002)                       # stilte vooraan weg
        a = a[start:start + int((dur + (1.0 if loop else 0)) * 44100)]
        if loop is None:
            a = resample(a, 44100, rate)
            a = a / max(1e-6, np.abs(a).max()) * 0.97              # 8 bit: volle schaal
            fade = int(rate * 0.05)
            a[-fade:] *= np.linspace(1, 0, fade)
        else:
            per = 64 if note < 66 else 32
            f0 = 440 * 2 ** ((note - 69) / 12)
            rate = int(round(f0 * per))
            a = resample(a, 44100, f0 * per)                       # precies `per` samples per periode
            ls = int(loop[0] * rate) // per * per
            ln = loop[1] * per
            w = np.linspace(0, 1, ln)
            body = a[ls:ls + ln] * (1 - w) + a[ls - ln:ls] * w     # loopeinde gaat vloeiend over in a[ls]
            a = np.concatenate([a[:ls], body])
            a = a / max(1e-6, np.abs(a).max()) * 0.97
            loop = (ls, ls + ln)
        write_wav(OUT + name + '.wav', a, rate, note, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s GM %-10s noot %d, %d samples @ %d Hz' % (name, prog, note, len(a), rate))
    for name, (kind, harm) in WAVES.items():
        a, rate = synth(kind, harm)
        write_wav(OUT + name + '.wav', a, rate, 60, (0, len(a)))
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s %s, loop %d samples @ %d Hz' % (name, kind, len(a), rate))
    for name, (kind, rate) in ONESHOTS.items():
        a = oneshot(kind, rate)
        a = a / np.abs(a).max() * 0.97
        write_wav(OUT + name + '.wav', a, rate, 60, None)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s %s, %d samples @ %d Hz' % (name, kind, len(a), rate))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
