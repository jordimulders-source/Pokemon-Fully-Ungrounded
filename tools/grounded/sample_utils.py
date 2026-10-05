"""Project Grounded: gedeelde samplehulpjes (resample, auto_loop, write_wav) uit heatran_samples v3.
Thema-generatoren importeren hieruit, niet uit elkaars scripts (Heatran v4 veranderde ze en brak Mitch)."""
import struct, wave
import numpy as np

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
