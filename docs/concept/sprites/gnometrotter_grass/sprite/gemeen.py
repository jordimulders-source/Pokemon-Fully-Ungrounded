# Gedeelde hulpjes Gnometrotter Grass. Palet: indexen 0, 1, 6-11 en 15 EXACT gelijk aan Rock (= Gnomad/Gnomini, zie GEDEELD.md);
# eigen materiaal: 2-4 schors (bruin, 2 = outline base) op de plek van Rocks donker gesteente, 5 en 12-14 blad (groen, 5 = outline base).
import numpy as np; from PIL import Image
PAL=[(152,208,160),(24,20,32),
     (72,50,36),(112,82,58),(152,118,84),
     (38,70,42),
     (172,72,102),(213,102,136),(244,153,181),
     (56,109,142),(82,148,197),(122,188,232),
     (58,98,56),(104,150,80),(176,210,120),
     (251,184,202)]
SCHORS=[3,4]; BLAD_D=[12,13]; BLAD_L=[13,14]; ROZE=[7,8,15]; BLAUW=[10,11]
ZNAAM={1:'bladmuts',2:'haar L',3:'haar R',4:'baard',5:'neus',6:'lijf',7:'arm L+hand',8:'elleboogschijf R',9:'hand R',10:'riem',11:'stok',12:'broek/benen',13:'zool L',14:'zool R',15:'rugplank+twijg',16:'twijgblaadjes',17:'knoesten',18:'schouderschijf R',19:'vuist L'}
RAMP={1:BLAD_D,2:BLAD_L,3:BLAD_L,4:BLAD_L,5:ROZE,6:ROZE,7:ROZE,8:ROZE,9:ROZE,10:SCHORS,11:SCHORS,12:BLAUW,13:SCHORS,14:SCHORS,15:SCHORS,16:BLAD_L,17:SCHORS,18:ROZE,19:ROZE}
BASIS={1:5,2:5,3:5,4:5,5:6,6:6,7:6,8:6,9:6,10:2,11:2,12:9,13:2,14:2,15:2,16:5,17:2,18:6,19:6}
PRIO=[5,2,3,4,19,7,11,9,8,18,1,16,15,10,6,17,12,13,14]   # voor -> achter
def lum(c): return 0.30*c[0]+0.59*c[1]+0.11*c[2]
def opslaan(o,path,pal=None):
    pal=pal or PAL
    p=Image.fromarray(o.astype('uint8'),'P'); f=[v for c in pal for v in c]; p.putpalette(f+[0]*(768-len(f))); p.save(path,transparency=0)
def lees(p): return np.asarray(Image.open(p)).astype(int).copy()
