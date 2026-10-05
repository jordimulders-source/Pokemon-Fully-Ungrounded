# Gebruik: python3 tools/grounded/solo_rms.py <rom> <intro.bin> <debugscript-nr> <midi> '{"groep": [spoornummers]}' [seconden]
# solo-opnames per groep sporen (volX = 0 op de rest, zoals balance.gba), RMS per sectie
import sys, re, json, numpy as np, mido
sys.path.insert(0,'tools/grounded/maptools'); sys.path.insert(0,'tools/grounded')
from emu import Emu, load, KEYS
rom, st, k, midi, groups = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], json.loads(sys.argv[5])
SEC = float(sys.argv[6]) if len(sys.argv) > 6 else 52
base = int(re.search(r'(0x[0-9a-f]+)\s+gMPlayTrack_BGM\n', open('pokeemerald.map').read()).group(1), 16)
m = mido.MidiFile(midi); ntr = len(m.tracks) - 1
# bar -> seconds
t = 0; tempo = 500000; bars = {}; tick = 0; secs = 0.0
ev = []
for msg in m.tracks[0]:
    tick += msg.time
    if msg.type == 'set_tempo': ev.append((tick, msg.tempo))
def sec_at(tk):
    s = 0; last = 0; tp = 500000
    for et, tpo in ev:
        if et >= tk: break
        s += (et - last) / 24 * tp / 1e6; last = et; tp = tpo
    return s + (tk - last) / 24 * tp / 1e6
SECT = [(0, 4), (4, 8), (8, 16), (16, 20), (20, 24), (24, 28), (28, 32), (32, 36), (36, 40)]
print('sectie(maten):', ' '.join('%d-%d' % s for s in SECT))
for name, g in groups.items():
    mute = [i - 1 for i in range(1, ntr + 1) if i not in g]
    e = Emu(rom); load(e, st); mem = e.core.memory
    buf = e.core.get_audio_channels(); buf.set_rate(32768)
    rec = []; on = [False]
    def frame():
        for tt in mute:
            a = base + 0x50 * tt
            mem.u8[a + 19] = 0; mem.u8[a] = mem.u8[a] | 0x03
        e.core.run_frame()
        av = buf.available
        if av:
            s = buf.read(av)
            if on[0]: rec.extend(s)
    e.core.set_keys(KEYS['START']); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(30)]
    e.core.set_keys(KEYS['A']); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(30)]
    for _ in range(5):
        e.core.set_keys(KEYS['DOWN']); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(6)]
    e.core.set_keys(KEYS['A']); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(30)]
    for _ in range(k - 1):
        e.core.set_keys(KEYS['DOWN']); [frame() for _ in range(4)]; e.core.set_keys(); [frame() for _ in range(6)]
    on[0] = True
    e.core.set_keys(KEYS['A']); [frame() for _ in range(4)]; e.core.set_keys()
    for _ in range(int(60 * SEC)): frame()
    x = np.array(rec, dtype=np.int16).reshape(-1, 2).astype(float).mean(1)
    out = []
    for b0, b1 in SECT:
        a, z = int(sec_at(b0 * 96) * 32768), int(sec_at(b1 * 96) * 32768)
        seg = x[a:z]
        out.append('%5.0f' % (np.sqrt((seg ** 2).mean()) if len(seg) else 0))
    print('%-10s' % name, ' '.join(out), flush=True)
    np.save('solo_%s_%s.npy' % (midi.split('/')[-1][:-4], name), x)
