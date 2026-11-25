# Gedeeld: palet, namen, opslaan, rgb. Paletkleuren = modelkleuren (k-means-centra van natief.png, kmeans.py 18),
# samengevoegd waar het model twee bijna-gelijke tinten voor dezelfde rol heeft; mond = Lotad-snaveltinten (Jordi).
import numpy as np; from PIL import Image
PAL=[(152,208,160),(20,16,18),                     # 0 transparant, 1 zwart (Lotad-zwart)
     (118,48,31),(159,69,46),(201,111,77),(211,125,90),   # rood: lijn (k8+k13), donker (k17), midden (k6), licht (k11)
     (46,36,22),(92,80,48),(118,99,65),(145,130,78),(174,157,100),  # olijf: lijn (k7+k14), donker (k5+k16), k12, midden (k4), licht (k0)
     (222,193,160),                                 # 11 oogwit (model, crème)
     (179,155,90),(228,199,123),(88,68,46),         # 12 13 14: Lotad-snavel midden, licht, lijn (mond, Jordi)
     (255,255,255),                                 # 15 wit (model: wit in het nabije oog en het verre oog)
     (236,198,103)]                                 # 16 modelsnavel-geel (alleen in de kale reductie, niet in de sprite)
NAAM={0:'transp',1:'zwart',2:'rood lijn',3:'rood donker',4:'rood midden',5:'rood licht',6:'olijf lijn',7:'olijf donker',
      8:'olijf 118',9:'olijf midden',10:'olijf licht',11:'oogwit',12:'mond midden',13:'mond licht',14:'mond lijn',15:'wit',16:'snavel(model)'}
ROOD={2,3,4,5}; OLIJF={6,7,8,9,10}; LIJN={1,2,6,14}
def lum(c): return 0.3*c[0]+0.59*c[1]+0.11*c[2]
def opslaan(o,pad):
    im=Image.fromarray(o.astype('uint8'),'P'); p=[]
    for c in (PAL[:16] if o.max()<16 else PAL): p+=list(c)   # sprite: precies 16 paletkleuren (GBA); kale reductie met snavelgeel: 17
    p+=[0]*(768-len(p)); im.putpalette(p); im.save(pad,transparency=0)
def rgb(o,bg=None):
    a=np.array([PAL[k] for k in o.ravel()]).reshape(o.shape+(3,)).astype('uint8')
    if bg is not None: a[o==0]=bg
    return a
