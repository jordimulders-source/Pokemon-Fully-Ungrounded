# Trainer-effect zoals in referenties/corruptie_trainer_red.png: vorm blijft heel, maar de pixels krijgen
# verkeerde paletindexen (bitvlakken door elkaar), waardoor schaduw verandert in een hard, contrastrijk
# mozaïek van de eigen paletkleuren. Eerst naar 15 kleuren + doorzichtig (Gen 3), dan in zones de
# indexbits verwisselen. Gebruik: IN OUT zones(links|half|heel)
import sys; from PIL import Image; import numpy as np
IN, OUT, Z = sys.argv[1], sys.argv[2], sys.argv[3]
rgb = Image.open(IN).convert('RGB'); a = np.asarray(rgb).astype(int); H, W, _ = a.shape
fg = a.mean(2) < 235
q = rgb.quantize(colors=15, method=Image.Quantize.MAXCOVERAGE, dither=Image.Dither.NONE)
pal = np.array(q.getpalette()[:45]).reshape(15, 3); idx = np.asarray(q).astype(int)
# palet op helderheid sorteren: index 1 = donkerst ... 15 = lichtst; 0 = doorzichtig
volg = np.argsort(pal.mean(1)); rang = np.empty(15, int); rang[volg] = np.arange(15)
I = rang[idx] + 1; I[~fg] = 0; P = np.vstack([[255, 255, 255], pal[volg]])
yy, xx = np.mgrid[0:H, 0:W]
zone = {'arm': (xx < 24) & (yy > 32), 'links': (xx < 30) & (yy > 30), 'half': xx < 32, 'heel': np.ones_like(fg)}[Z] & fg
def schud(i):  # bits 0..3 verwisselen: (b0 b1 b2 b3) -> (b2 b0 b3 b1), en nooit 0
    b = [(i >> k) & 1 for k in range(4)]; n = b[2] | (b[0] << 1) | (b[3] << 2) | (b[1] << 3)
    return n if n else 1
J = I.copy(); J[zone] = np.vectorize(schud)(I[zone])
out = a.copy(); out[zone] = P[J][zone]; out = out.astype('uint8'); out[~fg] = 255   # buiten de zone: origineel
Image.fromarray(out).save(OUT)
