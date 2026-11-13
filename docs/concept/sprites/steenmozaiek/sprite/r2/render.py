# labelraster (.npy of .txt) -> 64x64 geindexeerde PNG (index 0 transparant), onderaan uitgelijnd, + 8x.
import sys
import numpy as np
from PIL import Image
PAL = [('.', (255, 0, 255)), ('K', (16, 12, 18)), ('DB', (58, 58, 98)), ('DR', (78, 40, 38)), ('X', (40, 36, 40)), ('G', (118, 120, 130)),
       ('B0', (86, 92, 139)), ('B1', (123, 127, 176)), ('B2', (172, 173, 212)),
       ('R0', (110, 60, 50)), ('R1', (158, 94, 78)), ('R2', (196, 132, 114)),
       ('C0', (160, 140, 114)), ('C1', (206, 190, 158)), ('C2', (238, 232, 212)), ('W', (250, 252, 255))]
CH = {'.': '.', 'K': 'k', 'DB': 'd', 'DR': 'q', 'S': 's', 'X': 'x', 'G': 'g', 'B0': 'a', 'B1': 'b', 'B2': 'c', 'R0': 'r', 'R1': 'R',
      'R2': 'p', 'C0': 'e', 'C1': 'f', 'C2': 'h', 'W': 'w'}
INV = {v: k for k, v in CH.items()}
IDX = {k: i for i, (k, _) in enumerate(PAL)}

def load(path):
    if path.endswith('.npy'):
        return np.load(path, allow_pickle=True)
    rows = [r.rstrip('\n') for r in open(path) if r.strip()]
    return np.array([[INV[c] for c in r] for r in rows], object)

def save_txt(lab, path):
    with open(path, 'w') as f:
        for r in lab: f.write(''.join(CH[c] for c in r) + '\n')

def to_img(lab):
    m = lab != '.'
    ys, xs = np.where(m)
    o = lab[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    hh, ww = o.shape
    full = np.zeros((64, 64), np.uint8)
    x0 = (64 - ww) // 2
    for j in range(hh):
        for i in range(ww):
            full[63 - hh + j, x0 + i] = IDX[o[j, i]]
    p = Image.fromarray(full, 'P')
    fl = [v for _, c in PAL for v in c]
    p.putpalette(fl + [0] * (768 - len(fl)))
    p.info['transparency'] = 0
    return p, ww, hh, full

if __name__ == '__main__':
    lab = load(sys.argv[1]); uit = sys.argv[2]
    p, ww, hh, full = to_img(lab)
    p.save(uit, transparency=0)
    p.convert('RGBA').resize((512, 512), Image.NEAREST).save(uit.replace('.png', '_8x.png'))
    tot = (full > 0).sum()
    k = (full == IDX['K']).sum(); s = (full == IDX['DB']).sum() + (full == IDX['DR']).sum(); x = (full == IDX['X']).sum()
    print(uit, ww, 'x', hh, 'kleuren', len(set(full.ravel())) - 1, 'zwart K %.1f%% voeg+selout (DB/DR) %.1f%% zwarte tegels %.1f%% samen donker %.1f%%'
          % (100 * k / tot, 100 * s / tot, 100 * x / tot, 100 * (k + s + x) / tot))
