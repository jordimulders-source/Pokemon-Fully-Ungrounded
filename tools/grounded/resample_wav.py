"""Project Grounded: een 8-bit sample-wav (met smpl-chunk) naar een lagere samplerate (v0.9.231, ROM-ruimte).

FFT-resample (band boven de nieuwe Nyquist valt weg = anti-aliasing), fmt-, smpl-periode en loop-punten mee.
Gebruik: python3 tools/grounded/resample_wav.py <doel-Hz> <wav ...>   (overschrijft de bestanden)"""
import struct, sys
import numpy as np


def chunks(d):
    i, out = 12, []
    while i < len(d):
        cid, n = d[i:i + 4], struct.unpack('<I', d[i + 4:i + 8])[0]
        out.append([cid, bytearray(d[i + 8:i + 8 + n])])
        i += 8 + n + (n & 1)
    return out


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
    m = max(1, int(round(n * rate / old)))
    X = np.fft.rfft(np.concatenate([x, x[::-1]]))          # spiegelen: geen klik door de periodieke rand
    y = np.fft.irfft(X[:m + 1], 2 * m) * (m / n)
    y = y[:m]
    data[1] = bytearray(np.clip(np.round(y) + 128, 0, 255).astype(np.uint8).tobytes())
    struct.pack_into('<I', fmt, 4, rate)
    struct.pack_into('<I', fmt, 8, rate)
    for c in cs:
        if c[0] == b'smpl':
            s = c[1]
            struct.pack_into('<I', s, 8, int(round(1e9 / rate)))
            nl = struct.unpack_from('<I', s, 28)[0]
            for k in range(nl):
                o = 36 + k * 24
                a, b = struct.unpack_from('<II', s, o + 8)
                struct.pack_into('<II', s, o + 8, int(round(a * rate / old)), min(m - 1, int(round(b * rate / old))))
    body = b''.join(c[0] + struct.pack('<I', len(c[1])) + bytes(c[1]) + (b'\0' if len(c[1]) & 1 else b'') for c in cs)
    open(path, 'wb').write(b'RIFF' + struct.pack('<I', 4 + len(body)) + b'WAVE' + body)
    return old, rate


if __name__ == '__main__':
    r = int(sys.argv[1])
    for p in sys.argv[2:]:
        print(p, '%d -> %d Hz' % resample(p, r))
