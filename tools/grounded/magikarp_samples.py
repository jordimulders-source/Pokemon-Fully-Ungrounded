#!/usr/bin/env python3
"""Project Grounded: eigen samples voor Battle! Magikarp v2 (magikarp_theme.py). De v1-samples (fagot, woodblock,
vibraslap, kazoo, boing) staan nog in gm_samples.py; nieuwe samples komen hier.

- magikarp_cry          de echte Gen 3-cry (sound/direct_sound_samples/cries/magikarp.wav), onbewerkt, grondtoon 60
                        (speel op 60 = zoals de cry klinkt), als gewone (ongecomprimeerde) DirectSound-sample.
- magikarp_cry_scratch  'Ma-': het begin van de cry als DJ-scratch: de plaat wordt vanuit stilstand aangetrokken
                        (versnellen tot iets boven normaal), na ±0,13 s afgekapt en kort teruggetrokken ('wikka').
                        Samen ±0,19 s = net onder een achtste bij 150 bpm.
Gebruik: python3 tools/grounded/magikarp_samples.py"""
import struct, wave
import numpy as np

CRY = 'sound/direct_sound_samples/cries/magikarp.wav'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'


def write_wav(path, x, rate, key):
    q = np.clip(np.round(x * 127), -128, 127).astype(np.int16) + 128
    data = q.astype(np.uint8).tobytes()
    fmt = struct.pack('<HHIIHH', 1, 1, rate, rate, 1, 8)
    smpl = struct.pack('<9I', 0, 0, int(1e9 / rate), key, 0, 0, 0, 0, 0)
    chunks = b'fmt ' + struct.pack('<I', len(fmt)) + fmt + b'smpl' + struct.pack('<I', len(smpl)) + smpl
    chunks += b'data' + struct.pack('<I', len(data)) + data + (b'\0' if len(data) & 1 else b'')
    open(path, 'wb').write(b'RIFF' + struct.pack('<I', 4 + len(chunks)) + b'WAVE' + chunks)


def varispeed(a, speed):
    """Lees a af met een snelheid per uitvoersample (1 = normaal, negatief = achteruit); lineaire interpolatie."""
    pos = np.cumsum(speed) - speed[0]
    pos = np.clip(pos, 0, len(a) - 1)
    return np.interp(pos, np.arange(len(a)), a)


def scratch(a, rate):
    # vooruit: van ±0,35x naar 1,15x in 40 ms (hand laat de plaat los), dan normaal tot 0,13 s
    n1 = int(0.13 * rate)
    t = np.arange(n1) / rate
    sp = np.where(t < 0.04, 0.35 + 0.8 * (t / 0.04), 1.15 - 0.15 * np.clip((t - 0.04) / 0.03, 0, 1))
    fwd_pos_end = sp.sum()
    # terug: snel (tot -2x) en weer tot stilstand, ±0,06 s ('wikka')
    n2 = int(0.06 * rate)
    u = np.arange(n2) / n2
    sp2 = -2.0 * np.sin(np.pi * u)
    sp_all = np.concatenate([sp, sp2])
    pos = np.cumsum(sp_all) - sp_all[0]
    pos = np.clip(pos, 0, min(fwd_pos_end, len(a) - 1))
    x = np.interp(pos, np.arange(len(a)), a)
    env = np.ones(len(x))
    k = int(0.004 * rate)
    env[:k] = np.linspace(0, 1, k)                          # geen klik vooraan
    env[n1:] *= 0.7                                         # het terugtrekken iets zachter
    f = int(0.012 * rate)
    env[-f:] *= np.linspace(1, 0, f)
    return x * env


def main():
    w = wave.open(CRY)
    rate = w.getframerate()
    a = (np.frombuffer(w.readframes(w.getnframes()), np.uint8).astype(float) - 128) / 128.0
    inc = open(DATA).read()
    outs = {'magikarp_cry': a.copy(), 'magikarp_cry_scratch': scratch(a, rate)}
    f = int(0.01 * rate)
    outs['magikarp_cry'][-f:] *= np.linspace(1, 0, f)
    for name, x in outs.items():
        write_wav(OUT + name + '.wav', x, rate, 60)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-22s %d samples @ %d Hz (%.2f s)' % (name, len(x), rate, len(x) / rate))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()
