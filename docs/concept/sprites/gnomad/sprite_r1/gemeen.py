# Gedeelde hulpjes Gnomad r1: schaal, palet, zones, opslaan. Palet volgt Gnomini (af/gnomini.png) waar het kan.
import numpy as np; from PIL import Image
S=50/68                # natief figuur 68 hoog (y16-83) -> 50 px
BOTN,BOTS=84,60        # natieve onderrand 84 -> sprite-onderrand 60 (voeten op rij 59)
CXN,CXS=52.5,31.5      # natief midden x 52,5 -> spritekolom 31,5
ZNAAM={1:'muts',2:'neus',3:'snor L',4:'snor R',5:'lijf',6:'arm L',7:'arm R',8:'broek',9:'voet L',10:'voet R'}
PRIO=[1,2,3,4,6,7,9,10,8,5]   # voor -> achter
# 0 transp | 1 zwart | 2-5 muts (donker, schaduw, midden, licht) = Gnomini | 6-8 roze (donker, schaduw, midden) = Gnomini
# 9-11 blauw (donker, schaduw, midden) = Gnomini | 12-13 creme (schaduw, licht) | 14-15 riem (licht, donker); 14 is ook de selout van de snor
PAL_A=[(152,208,160),(24,20,32),
     (112,95,138),(137,119,170),(184,163,211),(205,183,230),
     (172,72,102),(213,102,136),(244,153,181),
     (56,109,142),(82,148,197),(122,188,232),
     (218,198,158),(248,242,222),
     (164,110,72),(112,70,46)]
PAL=PAL_A
MUTS=[2,3,4,5]; ROZE=[6,7,8]; BLAUW=[9,10,11]; CREME=[14,12,13]
FAMZ={1:MUTS,2:ROZE+[13],3:CREME,4:CREME,5:ROZE,6:ROZE+[13],7:ROZE+[13],8:BLAUW,9:BLAUW,10:BLAUW}
def opslaan(o,path,pal=None):
    pal=pal or PAL
    p=Image.fromarray(o.astype('uint8'),'P'); f=[v for c in pal for v in c]; p.putpalette(f+[0]*(768-len(f))); p.save(path,transparency=0)
def lees(p): return np.asarray(Image.open(p)).astype(int).copy()
def rgb(o,bg=(255,255,255),pal=None):
    pal=pal or PAL
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
