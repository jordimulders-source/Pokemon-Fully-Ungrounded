# Zoekt Gen 3-sprites (_gba) met dunne poten: verticale stroken van >=5 rijen waar de vorm 3 px breed is
# (lijn | 1 px vulling | lijn) en onder het midden van de sprite ligt. Telt per soort de langste zo'n strook.
import glob, numpy as np
from PIL import Image
res = []
for f in glob.glob("graphics/pokemon/**/anim_front_gba.png", recursive=True):
    im = Image.open(f).convert("RGBA").crop((0,0,64,64)); a = np.asarray(im).astype(int)
    bg = a[0,0]; fg = ~np.all(a == bg, axis=2)
    best = 0
    for x in range(1,63):
        run = 0
        for y in range(32,64):
            row = fg[y]
            # kolom x is vulling van een 3-brede strook: x-1,x,x+1 voorgrond, x-2 en x+2 achtergrond
            ok = row[x-1] and row[x] and row[x+1] and (x-2 < 0 or not row[x-2]) and (x+2 > 63 or not row[x+2])
            run = run+1 if ok else 0; best = max(best, run)
    res.append((best, f.split("/")[2] if f.count("/")==3 else "/".join(f.split("/")[2:-1])))
res.sort(reverse=True)
for b,n in res[:40]: print(b, n)
