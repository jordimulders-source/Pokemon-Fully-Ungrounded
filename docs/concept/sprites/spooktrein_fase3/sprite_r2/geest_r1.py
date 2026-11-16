# Kleine geest (rijen 0-13, x >= 12) uit de r1-onderlaag (oppervlak-middeling per kleurgroep uit het natieve raster):
# die houdt de krul/arm rechts en de lichtere kop links beter dan de LANCZOS-verkleining. Daarna netjes.py opnieuw.
import numpy as np; from PIL import Image
a=Image.open('onderlaag_r2.png'); o=np.array(a); g=np.array(Image.open('../sprite_r1/onderlaag.png'))
for y in range(0,14):
    for x in range(12,64):
        if y==13 and x<24: continue
        o[y,x]=g[y,x]
im=Image.fromarray(o,'P'); im.putpalette(a.getpalette()); im.save('onderlaag_r2g.png',transparency=0)
