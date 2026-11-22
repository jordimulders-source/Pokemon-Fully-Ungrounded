# Gedeelde hulpjes Mightyena-evolutie: klassen per natieve modelpixel, schrappen 74x70 -> 64x61, palet, opslaan, labels.
# Natief raster 99x99 (pitch 10,24, fase 9,20; natief.py), figuur x15-88, y14-83 (74x70).
import numpy as np; from PIL import Image
MODEL='referenties/gemini_gekozen_r4.png'; NATIEF='gereedschap/natief.png'
U0,V0,U1,V1=15,14,89,84          # uitsnede natief (74x70)
X0,Y0=0,2                         # plek in de sprite (64x61 -> x0-63, y2-62)
# Modelklassen (natief): 0 bg | 1 K zwart | 2 N bijna-zwart | 3 D donkergrijs | 4 M middengrijs | 5 G lichtgrijs
#                        | 6 geel (oog) | 7 rood (oog) | 8 bek donker | 9 bek midden | 10 tand wit
KL='.KNDMGyrbmt'
def klassen(path=NATIEF):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)[V0:V1,U0:U1]
    L=a.mean(2); sat=a.max(2)-a.min(2); R,G,B=a[...,0],a[...,1],a[...,2]
    c=np.zeros(L.shape,int)
    bg=a.min(2)>=215
    c[~bg&(L<20)]=1; c[~bg&(L>=20)&(L<46)]=2; c[~bg&(L>=46)&(L<96)]=3; c[~bg&(L>=96)&(L<135)]=4; c[~bg&(L>=135)]=5
    col=~bg&(sat>=20)
    geel=col&(G>R*0.75)&(B<G-25)&(R>150)
    rood=col&(R>G+40)&(R>140)&~geel
    bek=col&~geel&~rood
    c[geel]=6; c[rood]=7; c[bek&(L<75)]=8; c[bek&(L>=75)]=9
    c[~bg&(sat<20)&(L>=175)&(np.arange(L.shape[0])[:,None]<35)]=10   # tanden (wit, alleen in de kop)
    # wit dat niet met de buitenkant verbonden is en in de bek ligt = tand (model: witte tandjes), geen gat
    lab,n=label(bg,acht=False); buiten=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1])
    for i in range(1,n+1):
        m=lab==i
        if i not in buiten:
            yy,xx=np.where(m)
            if yy.max()<35 and xx.max()<20: c[m]=10
    return a,c,L
# Sprite-palet (index: kleur). Kleur mag van het model afwijken (Jordi); tinten van de Gen 3-Mightyena voor familie.
PAL=[(57,164,164),(16,16,24),
     (40,40,54),(66,70,92),(100,106,132),         # 2-4 zwarte vacht: donker, midden, licht (Mightyena 32/49/74 iets lichter)
     (128,124,146),(164,162,178),(200,200,212),(232,232,240),  # 5-8 grijs: schaduw, midden, licht; 8 = klauwtip
     (248,208,64),(216,48,40),                   # 9 geel, 10 rood (oog)
     (88,36,40),(160,92,96),(248,248,248)]       # 11 bek donker, 12 bek/tong, 13 tand wit
VACHT={2,3,4}; GRIJS={5,6,7,8}
CH='.Knmlsgwhyrbtx'
def rgb(o,bg=None):
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
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
