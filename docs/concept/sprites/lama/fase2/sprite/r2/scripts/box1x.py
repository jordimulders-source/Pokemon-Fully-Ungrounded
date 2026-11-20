# Model op 1x op het spriteraster (vlakgemiddelde per blok, witte achtergrond) -> model_1x.png (64x64 RGB)
import os, sys; import numpy as np; from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
from reduceer import S, X0, Y0, COLS, MODEL
a = np.asarray(Image.open(MODEL).convert('RGB')).astype(float); ox = (64 - COLS) // 2
out = np.full((64, 64, 3), 255.0)
for y in range(1, 63):
    for x in range(64):
        ya, yb = int(round(Y0 + (y - 1) * S)), int(round(Y0 + y * S)); xa, xb = int(round(X0 + (x - ox) * S)), int(round(X0 + (x - ox + 1) * S))
        if xa < 0 or xb > 1024 or yb > 1024: continue
        out[y, x] = a[ya:yb, xa:xb].reshape(-1, 3).mean(0)
Image.fromarray(out.astype('uint8')).save(os.path.join(os.path.dirname(HIER), 'model_1x.png'))
