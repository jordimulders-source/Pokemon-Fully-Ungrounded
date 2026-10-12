"""Project Grounded: SPC (SNES-geluid) uitlezen: BRR-samples uit het RAM en een noten-log uit DSP-schrijfacties.

De log komt van spclog (spclog.cpp, blargg's snes_spc met een DSP-schrijfhaak): per regel "ms register waarde".
Gebruikt door spc2gba.py (Yoshi's Island, v0.9.235)."""
import math, struct
import numpy as np

DSP_KON, DSP_KOFF, DSP_DIR, DSP_FLG, DSP_EON = 0x4C, 0x5C, 0x5D, 0x6C, 0x4D


class Spc:
    def __init__(self, path):
        d = open(path, 'rb').read()
        self.ram = d[0x100:0x10100]
        self.dsp = d[0x10100:0x10180]
        self.title = d[0x2E:0x4E].split(b'\0')[0].decode('latin1')

    def brr(self, srcn, dirpage):
        """BRR-sample nummer srcn uitpakken: (pcm float -1..1, loopstart in samples of None)."""
        ent = dirpage * 0x100 + srcn * 4
        start, loop = struct.unpack_from('<HH', self.ram, ent)
        out, p, o1, o2, loop_at = [], start, 0, 0, None
        while p + 9 <= 0x10000 and len(out) < 16 * 4000:
            if p == loop:
                loop_at = len(out)
            hdr = self.ram[p]
            shift, filt, end, lp = hdr >> 4, (hdr >> 2) & 3, hdr & 1, (hdr >> 1) & 1
            for b in self.ram[p + 1:p + 9]:
                for nib in (b >> 4, b & 15):
                    s = nib - 16 if nib >= 8 else nib
                    s = (s << shift) >> 1 if shift <= 12 else (-2048 if s < 0 else 0)
                    if filt == 1:
                        s += o1 + ((-o1) >> 4)
                    elif filt == 2:
                        s += (o1 << 1) + ((-((o1 << 1) + o1)) >> 5) - o2 + (o2 >> 4)
                    elif filt == 3:
                        s += (o1 << 1) + ((-(o1 + (o1 << 2) + (o1 << 3))) >> 6) - o2 + (((o2 << 1) + o2) >> 4)
                    s = max(-32768, min(32767, s))
                    s = (s << 1) & 0xFFFF                       # 15-bit-wrap zoals de echte DSP
                    s = (s - 0x10000 if s & 0x8000 else s) >> 1
                    o2, o1 = o1, s
                    out.append(s)
            p += 9
            if end:
                break
        x = np.array(out, np.float64) / 16384.0
        return x, (loop_at if (end and lp) else None)


def read_log(path):
    ev = []
    for l in open(path):
        t, r, v = l.split()
        ev.append((int(t), int(r), int(v)))
    return ev


def notes(ev, dsp0):
    """Noten per stem: dicts met t0, t1 (ms), srcn, pitch (begin), bends [(ms, pitch)], vol (l, r), adsr."""
    regs = bytearray(dsp0)
    open_ = [None] * 8
    out = []

    def close(v, t):
        n = open_[v]
        if n:
            n['t1'] = t
            out.append(n)
            open_[v] = None
    for t, r, val in ev:
        if r < 0x80:
            regs[r] = val
        if r == DSP_KOFF:
            for v in range(8):
                if val >> v & 1:
                    close(v, t)
        elif r == DSP_KON:
            for v in range(8):
                if val >> v & 1:
                    close(v, t)
                    b = v * 16
                    open_[v] = dict(voice=v, t0=t, srcn=regs[b + 4], pitch=(regs[b + 2] | regs[b + 3] << 8) & 0x3FFF,
                                    vol=(np.int8(regs[b]), np.int8(regs[b + 1])), adsr=(regs[b + 5], regs[b + 6]),
                                    gain=regs[b + 7], bends=[], vols=[], echo=regs[DSP_EON] >> v & 1)
        elif (r & 15) in (2, 3) and open_[r >> 4]:
            b = r & 0xF0
            open_[r >> 4]['bends'].append((t, (regs[b + 2] | regs[b + 3] << 8) & 0x3FFF))
        elif (r & 15) in (0, 1) and open_[r >> 4]:
            b = r & 0xF0
            open_[r >> 4]['vols'].append((t, (int(np.int8(regs[b])), int(np.int8(regs[b + 1])))))
    for v in range(8):
        close(v, ev[-1][0] if ev else 0)
    out.sort(key=lambda n: (n['t0'], n['voice']))
    return out, regs


def fundamental(x, sr=32000, loop=None):
    """Grondtoon (Hz) van een sample via autocorrelatie op het stabiele deel; None bij ruis/drum.
    Met een loop wordt het loopdeel herhaald (korte golfvormen van 1-4 periodes, chiptune-achtig)."""
    if loop is not None and len(x) - loop >= 8:
        cyc = x[loop:]
        x = np.concatenate([x[:loop], np.tile(cyc, max(1, 8192 // len(cyc)))])
    if len(x) < 256:
        return None
    seg = x[len(x) // 4:]
    if len(seg) > 8192:
        seg = seg[:8192]
    seg = seg - seg.mean()
    if np.abs(seg).max() < 1e-3:
        return None
    n = len(seg)
    f = np.fft.rfft(seg, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    ac /= ac[0]
    lo, hi = int(sr / 2000), min(n - 1, int(sr / 30))
    k = lo + int(np.argmax(ac[lo:hi]))
    if ac[k] < 0.5:
        return None
    # parabolische interpolatie
    if 1 <= k < n - 1:
        a, b, c = ac[k - 1], ac[k], ac[k + 1]
        k = k + 0.5 * (a - c) / (a - 2 * b + c)
    return sr / k
