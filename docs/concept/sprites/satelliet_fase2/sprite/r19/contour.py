# Meet per spriterij (sub-rijen .1-.9) de buitenlijn van het lijf naast een witte opening tussen lijf en paneel in het model.
from PIL import Image; import numpy as np, sys
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(float); k = 12.703
LM = .299 * M[..., 0] + .587 * M[..., 1] + .114 * M[..., 2]
x0, x1, y0, y1, kant = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
for y in range(y0, y1):
    res = []
    for f in (.25, .5, .75):
        my = int(143 + (y + f - 7) * k); xs = np.arange(x0, x1, .05)
        bg = [(LM[my, int(103 + x * k)] > 250 and abs(M[my, int(103 + x * k), 0] - M[my, int(103 + x * k), 2]) < 14) for x in xs]
        dk = [LM[my, int(103 + x * k)] < 70 for x in xs]
        # rechterkant: eerste achtergrond na lijf; de lijn = laatste donkere run ervoor
        idx = [i for i in range(1, len(xs)) if bg[i] and not bg[i - 1]] if kant == 'r' else [i for i in range(len(xs) - 1) if bg[i] and not bg[i + 1]]
        if not idx: res.append('  --  '); continue
        i = idx[0] if kant == 'r' else idx[-1]
        if kant == 'r':
            j = i - 1
            while j > 0 and not dk[j]: j -= 1
            e = j
            while j > 0 and dk[j]: j -= 1
            res.append('%5.2f-%5.2f' % (xs[j + 1], xs[e] + .05))
        else:
            j = i + 1
            while j < len(xs) - 1 and not dk[j]: j += 1
            s = j
            while j < len(xs) - 1 and dk[j]: j += 1
            res.append('%5.2f-%5.2f' % (xs[s], xs[j]))
    print(y, '  '.join(res))
