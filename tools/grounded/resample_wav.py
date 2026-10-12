"""Project Grounded: een 8-bit sample-wav (met smpl-chunk) naar een lagere samplerate (v0.9.231, ROM-ruimte).

FFT-resample (band boven de nieuwe Nyquist valt weg = anti-aliasing), fmt-, smpl-periode en loop-punten mee.
Gebruik: python3 tools/grounded/resample_wav.py <doel-Hz> <wav ...>   (overschrijft de bestanden)
         python3 tools/grounded/resample_wav.py --all
--all (Jordi 10 okt, A/B SickBlik: "de b-versie is prima"): alle eigen samples in sound/direct_sound_samples/grounded/
naar max. 11025 Hz (grondtoon vanaf C6: 16000 Hz), behalve drums (alles uit sound/voicegroups/drumsets/). Idempotent.
Draai dit na elke samplegenerator (*_samples.py, gm_samples.py) en na elke muziekmerge."""
import glob, os, re, struct, sys
import numpy as np


def chunks(d):
    i, out = 12, []
    while i < len(d):
        cid, n = d[i:i + 4], struct.unpack('<I', d[i + 4:i + 8])[0]
        out.append([cid, bytearray(d[i + 8:i + 8 + n])])
        i += 8 + n + (n & 1)
    return out


def _fft_resample(x, m, periodic=False):
    """x naar m samples. periodic: x is één loop (geen spiegeling, de loop blijft naadloos)."""
    n = len(x)
    if periodic:
        X = np.fft.rfft(x)
        Y = np.zeros(m // 2 + 1, complex)
        k = min(len(X), len(Y))
        Y[:k] = X[:k]
        return np.fft.irfft(Y, m) * (m / n)
    X = np.fft.rfft(np.concatenate([x, x[::-1]]))      # spiegelen: geen klik door de periodieke rand
    return np.fft.irfft(X[:m + 1], 2 * m)[:m] * (m / n)


KEEP_16K = ('mitch7',)   # Mitch v7 (DnB: zaag-leads en reese leven van 2-7 kHz; 11 kHz = 'goedkoop'): 16 kHz houden
MIN_LOOP = 128   # kortere loops (chiptune-golfjes van een paar periodes) niet verlagen: afronden maakt ze vals


def resample(path, rate):
    cs = chunks(open(path, 'rb').read())
    fmt = next(c for c in cs if c[0] == b'fmt ')[1]
    ch, old, bits = struct.unpack_from('<H', fmt, 2)[0], struct.unpack_from('<I', fmt, 4)[0], struct.unpack_from('<H', fmt, 14)[0]
    assert ch == 1 and bits == 8, path
    if old <= rate:
        return old, old
    data = next(c for c in cs if c[0] == b'data')
    x = np.frombuffer(bytes(data[1]), np.uint8).astype(np.float64) - 128
    n = len(x)
    smpl = next((c for c in cs if c[0] == b'smpl'), None)
    loop = None
    if smpl and struct.unpack_from('<I', smpl[1], 28)[0]:
        loop = struct.unpack_from('<I', smpl[1], 36 + 8)[0]
    if loop is not None and 0 < loop < n:
        L = n - loop
        if L < MIN_LOOP:
            return old, old
        mL = max(2, int(round(L * rate / old)))
        new = old * mL / L                          # exacte rate: de loop blijft een heel aantal samples, toonhoogte gelijk
        mA = int(round(loop * new / old))
        y = np.concatenate([_fft_resample(x[:loop], mA) if loop >= 2 else x[:loop], _fft_resample(x[loop:], mL, True)])
        newrate, loops = int(round(new)), (mA, mA + mL - 1)
    else:
        m = max(1, int(round(n * rate / old)))
        y = _fft_resample(x, m)
        newrate, loops = rate, None
    data[1] = bytearray(np.clip(np.round(y) + 128, 0, 255).astype(np.uint8).tobytes())
    struct.pack_into('<I', fmt, 4, newrate)
    struct.pack_into('<I', fmt, 8, newrate)
    if smpl:
        s_ = smpl[1]
        struct.pack_into('<I', s_, 8, int(round(1e9 / newrate)))
        if loops:
            struct.pack_into('<II', s_, 36 + 8, *loops)
    body = b''.join(c[0] + struct.pack('<I', len(c[1])) + bytes(c[1]) + (b'\0' if len(c[1]) & 1 else b'') for c in cs)
    open(path, 'wb').write(b'RIFF' + struct.pack('<I', 4 + len(body)) + b'WAVE' + body)
    return old, newrate


def rate_of(path):
    fmt = next(c for c in chunks(open(path, 'rb').read()) if c[0] == b'fmt ')[1]
    return struct.unpack_from('<I', fmt, 4)[0]


def base_note(path):
    for c in chunks(open(path, 'rb').read()):
        if c[0] == b'smpl':
            return struct.unpack_from('<I', c[1], 12)[0]
    return 60


KEEP_RATE = ('az_voice',)   # Area Zero v4: stem uit het origineel op 16 kHz (Jordi: '11 kHz te muffled')


def resample_all(root='.'):
    drum = set()
    for f in glob.glob(os.path.join(root, 'sound/voicegroups/drumsets/*.inc')):
        drum |= set(re.findall(r'DirectSoundWaveData_(\w+)', open(f).read()))
    inc = open(os.path.join(root, 'sound/direct_sound_data.inc')).read()
    n = 0
    for name, p in re.findall(r'^DirectSoundWaveData_(\w+)::?\s*\n\s*\.incbin "([^"]+)"', inc, re.M):
        w = os.path.join(root, p[:-4] + '.wav')
        if '/grounded/' not in p or name in drum or name.startswith(KEEP_RATE) or not os.path.exists(w):
            continue
        fmt = next(c for c in chunks(open(w, 'rb').read()) if c[0] == b'fmt ')[1]
        if struct.unpack_from('<H', fmt, 14)[0] != 8:
            continue
        tgt = 16000 if base_note(w) >= 84 or name.startswith(KEEP_16K) else 11025
        old, new = resample(w, tgt) if rate_of(w) > tgt * 1.05 else (0, 0)
        n += old != new
    return n


if __name__ == '__main__':
    if sys.argv[1] == '--all':
        print(resample_all(), 'samples omgezet')
        sys.exit()
    r = int(sys.argv[1])
    for p in sys.argv[2:]:
        print(p, '%d -> %d Hz' % resample(p, r))
