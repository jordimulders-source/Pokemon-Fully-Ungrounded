# Gedeelde hulpjes Kricketune-evolutie: klassen per natieve modelpixel, palet, opslaan, labels.
# Natief raster 99x99 (pitch 10,24, fase 9,25/9,20; natief.py), figuur x10-84, y6-90 (75x85).
import numpy as np; from PIL import Image
MODEL='model/v3_r1_vinger_ogen.png'; NATIEF='gereedschap/natief.png'
U0,V0,U1,V1=10,6,85,91            # uitsnede natief (75x85)
X0,Y0=4,0                          # plek in de sprite (56x64 -> x4-59, y0-63)
# Modelklassen (natief): 0 bg | 1 K zwart | 2 d pak donker | 3 m pak midden | 4 g hemd grijsroze | 5 w hemd wit
#                        | 6 r1 donkerrood (lijn) | 7 r2 rood schaduw | 8 r3 rood | 9 r4 rood licht | 10 r5 rood hooglicht
#                        | 11 e oog grijsbruin (Kricketune-oog in het model)
KL='.Kdmgw12345e'
def klassen(path=NATIEF):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)[V0:V1,U0:U1]
    L=a.mean(2); R,G,B=a[...,0],a[...,1],a[...,2]
    bg=a.min(2)>=215; red=(R>G+50)&~bg
    c=np.zeros(L.shape,int)
    c[~bg&~red&(L<25)]=1; c[~bg&~red&(L>=25)&(L<60)]=2; c[~bg&~red&(L>=60)&(L<110)]=3; c[~bg&~red&(L>=110)]=4
    oog=~bg&~red&(R>=B+8)&(L>=60)&(L<110)
    c[oog]=11
    for i,(lo,hi) in enumerate(((0,120),(120,160),(160,190),(190,215),(215,999))): c[red&(R>=lo)&(R<hi)]=6+i
    # wit dat niet met de buitenkant verbonden is en in het hemd/de knoopjes of de oogglans ligt = wit, geen gat
    lab,n=label(bg,acht=False); buiten=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1])
    for i in range(1,n+1):
        m=lab==i
        if i in buiten: continue
        yy,xx=np.where(m)
        if (28<=yy.min() and yy.max()<=60 and 30<=xx.min() and xx.max()<=44) or (m.sum()<=3 and 16<=yy.min() and yy.max()<=24 and 26<=xx.min() and xx.max()<=46):
            c[m]=5
    return a,c,L
# Sprite-palet (index: kleur). Tinten uit het model; kleur mag afwijken (Jordi).
PAL=[(152,208,160),(16,16,16),
     (52,48,62),(74,70,86),(104,98,118),           # 2-4 pak/hand/snor: donker, midden, licht (4 = alleen volume, niet uit het model)
     (184,160,168),(248,248,248),                   # 5 hemd grijsroze, 6 wit
     (106,31,31),(140,40,40),(176,54,50),(204,68,60),(228,98,84),  # 7-11 rood: lijn, schaduw, midden, licht, hooglicht
     (82,74,65)]                                    # 12 oog grijsbruin (Kricketune)
PAK={2,3,4}; ROOD={7,8,9,10,11}
CH='.Kdmlgw12345e'
def rgb(o,bg=None):
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
def laden(path):
    return np.asarray(Image.open(path)).astype(int)
def label(mask,acht=True):
    lab=np.zeros(mask.shape,int); n=0
    nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if acht else [(-1,0),(1,0),(0,-1),(0,1)]
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in nb:
                yy,xx=cy+dy,cx+dx
                if 0<=yy<mask.shape[0] and 0<=xx<mask.shape[1] and mask[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
    return lab,n
def toon(o,ch=CH,y0=0,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(ch[v] for v in o[y,x0:x1]))
