# Palet en opslaan (geen neveneffecten). Index: 0 transparant, 1 zwart, 2..8 water toon 0..6, 9 stip, 10 stip licht.
import numpy as np; from PIL import Image
# watertonen: modelmedianen (9,55,84) (16,93,117) (28,123,145) (52,151,169) (89,177,191) (136,203,212) (224,241,245), richting Gen 3
# (Kyogre/Sharpedo-gba: donkerste vulling L~60, stappen ~30) een stap lichter, donker iets blauwer, licht iets cyaner.
PAL=[(152,208,160),(16,16,24),(16,64,100),(22,98,128),(34,128,150),(60,156,174),(98,186,198),(150,214,220),(228,246,246),(0,206,188),(176,255,236)]
def k2idx(k):   # kaalklassen -> paletindex
    m={-1:0,0:2,1:3,2:4,3:5,4:6,5:7,6:8,7:1,8:9}
    return np.vectorize(m.get)(k).astype('uint8')
def opslaan(idx,pad,pal=PAL):
    im=Image.fromarray(idx.astype('uint8'),'P'); p=[c for rgb in pal for c in rgb]; im.putpalette(p+[0]*(768-len(p)))
    im.save(pad,transparency=0); return im
def rgba(idx,pal=PAL,bg=None):
    P=np.array(pal,'uint8'); o=P[idx]
    if bg is None:
        al=np.where(idx==0,0,255).astype('uint8'); return Image.fromarray(np.dstack([o,al]),'RGBA')
    o=o.copy(); o[idx==0]=bg; return Image.fromarray(o,'RGB')
