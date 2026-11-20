# per spritepixel: gem. helderheid van de wolpixels zonder lijn (>=100) en van het kleedrood -> toon_model.npy (2 x 64 x 64)
import numpy as np
from meet import cel
T = np.full((2, 64, 64), np.nan)
for y in range(64):
    for x in range(64):
        c = cel(x, y)
        if c is None: continue
        f = c['rgb']['fur'].mean(1) if len(c['rgb']['fur']) else np.array([])
        f = f[f >= 100]
        if len(f) >= 20: T[0, y, x] = f.mean()
        r = c['rgb']['red'].mean(1) if len(c['rgb']['red']) else np.array([])
        if len(r) >= 20: T[1, y, x] = r.mean()
np.save('toon_model.npy', T); print('ok')
