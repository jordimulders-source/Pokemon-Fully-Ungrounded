# Gedeelde hulpjes Gnometrotter ICE (kopie van Rock; alleen materiaalindexen 2-5 en 12-14 eigen): palet, ramps, opslaan. Palet volgt Gnomad (af/gnomad.png) voor zwart, roze, blauw (zelfde indexen).
import numpy as np; from PIL import Image
# 0 transp | 1 zwart (=Gnomad) | 2-5 ijs (2 = outline base ijs, 3-5 ijsblauw: muts, rugkam, stok) [muts-plek van Gnomad]
# 6-8 roze (=Gnomad) | 9-11 blauw (=Gnomad) | 12-14 sneeuw/ijspegelwit (baard, haar, riem, zolen) [creme-plek van Gnomad] | 15 roze hooglicht (=Gnomini)
PAL=[(152,208,160),(24,20,32),
     (64,88,122),(124,160,196),(176,206,232),(222,238,250),
     (172,72,102),(213,102,136),(244,153,181),
     (56,109,142),(82,148,197),(122,188,232),
     (170,192,214),(214,228,240),(246,249,252),
     (251,184,202)]
DONKER=[3,4,5]; LICHT=[12,13,14]; ROZE=[7,8,15]; BLAUW=[9,10,11]   # vlaktinten; lijnen in BASIS
ZNAAM={1:'muts+rugkam',2:'haar L',3:'haar R',4:'baard',5:'neus',6:'lijf',7:'arm L+hand',8:'arm R',9:'hand R',10:'riem',11:'stok',12:'broek/benen',13:'zool L',14:'zool R'}
RAMP={1:DONKER,2:LICHT,3:LICHT,4:LICHT,5:ROZE,6:ROZE,7:ROZE,8:ROZE,9:ROZE,10:LICHT,11:DONKER,12:BLAUW,13:LICHT,14:LICHT}
BASIS={1:2,2:2,3:2,4:2,5:6,6:6,7:6,8:6,9:6,10:2,11:2,12:9,13:2,14:2}   # outline base per onderdeel
PRIO=[5,2,3,4,7,11,9,8,1,10,6,12,13,14]   # voor -> achter
def lum(c): return 0.30*c[0]+0.59*c[1]+0.11*c[2]
def opslaan(o,path,pal=None):
    pal=pal or PAL
    p=Image.fromarray(o.astype('uint8'),'P'); f=[v for c in pal for v in c]; p.putpalette(f+[0]*(768-len(f))); p.save(path,transparency=0)
def lees(p): return np.asarray(Image.open(p)).astype(int).copy()
def rgb(o,bg=(255,255,255),pal=None):
    pal=pal or PAL
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
