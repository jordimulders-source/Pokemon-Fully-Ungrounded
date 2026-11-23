# Sprite-palet (index = modelklasse 1-9 + extra). Kleur mag van het model afwijken (Jordi); Gen 3-stappen, Emolga-familie.
from PIL import Image; import numpy as np
PAL=[(152,208,160),          # 0 transparant
     (16,16,24),             # 1 K zwart
     (36,36,44),             # 2 D vacht donker (model 33; Emolga 32/32/40)
     (60,60,70),             # 3 E vacht midden (model 48; Emolga 56/56/64)
     (90,88,100),            # 4 G vacht licht (model 66; Emolga 88/80/88)
     (184,140,24),           # 5 y geel schaduw (model 166,140,50)
     (224,184,40),           # 6 Y geel midden (model 218,188,62)
     (248,220,80),           # 7 L geel licht (model 241,216,89)
     (180,194,208),          # 8 B wit schaduw (model 194,210,218)
     (240,246,250),          # 9 W wit (model 236,243,248)
     (128,140,160)]          # 10 wit diepe schaduw / selout wit
def rgb(o,bg=None):
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
