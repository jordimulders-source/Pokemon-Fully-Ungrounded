# Gedeeld: palet, namen, opslaan, rgb. Paletkleuren = modeltinten (k-means-centra van natief.png, kmeans.py 18),
# en waar het model bijna gelijk is de tinten van de gaucho-Lombre (af/) zodat de lijn bij elkaar past.
import numpy as np; from PIL import Image
PAL=[(152,208,160),(20,16,18),                       # 0 transparant, 1 zwart (Lotad/Lombre-zwart; model 2,1,1)
     (108,44,30),(136,60,42),(160,74,50),(186,94,64),(204,114,80),(230,154,112),  # rood: lijn (Lombre; model 111-126), diep (model 138), donker (Lombre; model 149-158), middendonker (model 178-188), midden (Lombre; model 202-214), licht (Lombre; model 206,138,102)
     (66,56,30),(86,76,44),(110,98,58),(156,142,86),  # olijf: lijn (Lombre; model 50), diep (model 72), donker (Lombre; model 88), midden (Lombre; model 137)
     (193,143,41),(240,200,73),                       # 12 13 geel donker/licht (model, snavel)
     (124,52,36),(255,255,255)]                       # 14 ponchoschaduw (alleen varianten), 15 wit (reserve)
NAAM={0:'transp',1:'zwart',2:'rood lijn',3:'rood diep',4:'rood donker',5:'rood mdonker',6:'rood midden',7:'rood licht',
      8:'olijf lijn',9:'olijf diep',10:'olijf donker',11:'olijf midden',12:'geel donker',13:'geel licht',14:'poncho extra',15:'wit'}
ROOD={2,3,4,5,6,7,14}; OLIJF={8,9,10,11}; GEEL={12,13}; LIJN={1,2,8}
def lum(c): return 0.3*c[0]+0.59*c[1]+0.11*c[2]
def opslaan(o,pad,pal=None):
    pal=pal or PAL
    im=Image.fromarray(o.astype('uint8'),'P'); p=[]
    for c in pal[:16]: p+=list(c)
    p+=[0]*(768-len(p)); im.putpalette(p); im.save(pad,transparency=0)
def rgb(o,bg=None,pal=None):
    pal=pal or PAL
    a=np.array([pal[k] for k in o.ravel()]).reshape(o.shape+(3,)).astype('uint8')
    if bg is not None: a[o==0]=bg
    return a
