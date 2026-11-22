# Gedeelde hulpjes Gnomini r1: natieve zones, schaal, palet, opslaan.
import numpy as np; from PIL import Image
S=41/53            # natief -> sprite (figuur 53 natief hoog -> 41 px)
CXN,CXS=49.5,32    # natieve kolom 49,5 -> spritekolom 32 (midden)
BOTN,BOTS=75,59    # natieve onderrand 75 -> sprite-onderrand 59 (voeten op rij 58)
# zones: 0 achtergrond, 1 muts, 2 neus, 3 lijf, 4 arm L, 5 arm R, 6 voet L, 7 voet R
ZNAAM={1:'muts',2:'neus',3:'lijf',4:'arm L',5:'arm R',6:'voet L',7:'voet R'}
PRIO=[1,2,4,5,6,7,3]   # voor -> achter
# spritepalet: 0 transp | 1 zwart | 2-5 muts (donker, schaduw, midden, licht) | 6-9 roze (donker, schaduw, midden, licht) | 10-13 blauw (donker, schaduw, midden, licht) | 14 muts hooglicht
PAL=[(152,208,160),(24,20,32),
     (112,95,138),(137,119,170),(184,163,211),(205,183,230),
     (172,72,102),(213,102,136),(244,153,181),(251,184,202),
     (56,109,142),(82,148,197),(122,188,232),(170,216,244),
     (226,212,244)]
FAM={1:[2,3,4,5],2:[6,7,8,9],3:[6,7,8,9,10,11,12],4:[6,7,8,9],5:[6,7,8,9],6:[10,11,12,13],7:[10,11,12,13]}
def natief():
    """natief RGB (float), zonekaart (lijnen toegewezen aan de voorste buurzone), lijnmasker"""
    a=np.asarray(Image.open('natief.png')).astype(float)
    idx=np.load('natief_idx.npy'); lab=np.load('natief_lab.npy')
    m={1:1,3:1,2:2,4:3,5:4,6:5,7:6,8:7}   # labels uit zones.py -> zones (label 3 = 2 px mutsrand)
    z=np.zeros(lab.shape,int)
    for k,v in m.items(): z[lab==k]=v
    lijn=(idx>0)&(z==0)
    for y,x in zip(*np.where(lijn)):
        buren=set(z[y-1:y+2,x-1:x+2].ravel())-{0}
        for p in PRIO:
            if p in buren: z[y,x]=p; break
    # lijnen zonder vlakbuur (dubbel dik): tweede ronde
    for y,x in zip(*np.where(lijn&(z==0))):
        buren=set(z[y-1:y+2,x-1:x+2].ravel())-{0}
        for p in PRIO:
            if p in buren: z[y,x]=p; break
    return a,z,lijn
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
def rgb(o,bg=(255,255,255)):
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
