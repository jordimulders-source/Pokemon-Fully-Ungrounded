# recaudio.py rom state k seconds out.wav  (state "-" = koude start, k 0 = geen debugscript)
# Neemt de emulator-audio op (incl. PSG). Leest de audiobuffer ELKE frame uit (ook tijdens menu-navigatie), anders
# loopt hij over en neem je ruis op.
# mGBA (python-binding) geeft af en toe een korte burst (~10 samples: 0 / 15136 / 32520 om en om, of exacte nullen
# om en om). Die zit niet in de game; het tijdstip hangt af van de samplerate. Daarom: twee opnames (32768 Hz en
# 44100 Hz, zelfde frames); elk glitchvenster in de eerste wordt vervangen door het echte geluid uit de tweede
# (omgerekend naar 32768 Hz). Alleen als beide op dezelfde plek een glitch hebben, wordt er lineair overbrugd.
from emu import *
import sys, wave, numpy as np
rom, st, k, sec, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
RATE = 32768


def record(rate):
    e = Emu(rom)
    if st != '-':
        load(e, st)
    buf = e.core.get_audio_channels(); buf.set_rate(rate)
    rec = []; on = [False]; orig = e.core.run_frame

    def rf():
        orig(); av = buf.available
        if av:
            s = buf.read(av)
            if on[0]: rec.extend(s)
    e.core.run_frame = rf
    if k:
        e.press('START', after=30); e.press('A', after=30)
        for _ in range(5): e.press('DOWN', after=6)
        e.press('A', after=30)
        for _ in range(k - 1): e.press('DOWN', after=6)
        on[0] = True                        # al vóór de laatste A opnemen: anders mis je het begin van het nummer
        e.press('A', after=0)
    on[0] = True; e.run(int(60 * sec))
    return np.array(rec, dtype=np.int16).reshape(-1, 2).astype(np.float64)


def glitch_mask(x):
    """Bool-masker (per sample, één kanaal) van glitchvensters, ruim (±32 samples)."""
    m = np.zeros(len(x), bool)
    bad = np.where(abs(np.diff(x)) > 12000)[0]
    z = (x == 0).astype(np.int32); cz = np.convolve(z, np.ones(12, dtype=np.int32), 'same')
    loud = np.convolve(np.abs(x), np.ones(256) / 256, 'same') > 300
    bad = np.concatenate([bad, np.where((cz >= 4) & loud)[0]])
    for i in bad:
        m[max(0, i - 32):i + 33] = True
    return m


a = record(RATE)
b = record(44100)
n = len(a)
tb = np.arange(len(b)) / 44100.0
ta = np.arange(n) / RATE
b32 = np.stack([np.interp(ta, tb, b[:, c]) for c in (0, 1)], axis=1)
fixed = repl = 0
for c in (0, 1):
    ma = glitch_mask(a[:, c]); mb = glitch_mask(b32[:, c])
    use_b = ma & ~mb
    a[use_b, c] = b32[use_b, c]
    repl += int(np.count_nonzero(np.diff(use_b.astype(int)) == 1))
    both = np.where(ma & mb)[0]                # zelden: allebei kapot -> lineair overbruggen
    i = 0
    while i < len(both):
        j = i
        while j + 1 < len(both) and both[j + 1] - both[j] < 2: j += 1
        lo = max(0, both[i] - 1); hi = min(n - 1, both[j] + 1)
        a[lo:hi + 1, c] = np.linspace(a[lo, c], a[hi, c], hi + 1 - lo); fixed += 1; i = j + 1
    left = len(np.where(abs(np.diff(a[:, c])) > 12000)[0])
    if left: print('LET OP: nog %d sprongen in kanaal %d' % (left, c))
if repl or fixed:
    print('glitches vervangen door de 2e opname: %d, lineair overbrugd: %d' % (repl, fixed))
pcm = np.clip(a, -32768, 32767).astype(np.int16).reshape(-1)
w = wave.open(out, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(pcm.tobytes()); w.close()
x = pcm.astype(float)
print(out.split('/')[-1], 'rms', int(np.sqrt((x * x).mean())), 'peak', int(abs(x).max()), 'clip%%%.2f' % (100 * (abs(x) >= 32000).mean()))
