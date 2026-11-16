# Ronde 8: hoorns en linkerarm UIT HET MODEL GEKNIPT en mechanisch verkleind (geen omtrek met de hand).
# Reductie (zelfde mapping als vergelijk.py/overlay.py), per spritecel op het natieve raster (natief.png), vlakgewogen:
#   dekking < 0,5 -> transparant; zwart (L<45) >= 0,2 van de dekking -> '#';
#   donkerbruine lijnpixels (45<=L<66) >= 0,5 -> 'a'; anders vlakgemiddelde van de lichte pixels -> dichtstbijzijnde b/c/d.
# Het resultaat wordt per zone als geheel geplakt (ring/yerba-pixels van r7 blijven). Daarna alleen benoemde
# reparaties waar de reductie aantoonbaar iets kapotmaakt (FIX, met reden). Buiten de zones: pixeldiff 0 met r7.
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/'
im=Image.open(D+'r7/mate.png'); PAL=im.getpalette(); r7=np.asarray(im).astype(int)
N=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(float)
P=np.array(PAL[:36]).reshape(-1,3).astype(float)
o=np.load(D+'r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
L=(N*[.299,.587,.114]).sum(2); FG=N.min(2)<200; BL=FG&(L<45); LN=FG&~BL&(L<66); VL=FG&(L>=66)
def w(lo,hi,n):
    v=np.zeros(n)
    for k in range(int(np.floor(lo)),int(np.ceil(hi))):
        if 0<=k<n: v[k]=min(hi,k+1)-max(lo,k)
    return v
def red(sx,sy):
    ny=NY0+(sy-top+oy0)*s; nx=NX0+(sx-fx+ox0)*s
    W=w(ny,ny+s,100)[:,None]*w(nx,nx+s,100)[None,:]; t=W.sum(); fg=(W*FG).sum()
    if fg/t<0.5: return 0
    if (W*BL).sum()/fg>=0.2: return 1
    if (W*LN).sum()/fg>=0.5 or (W*VL).sum()==0: return 2
    v=W*VL; m=(N*v[...,None]).sum((0,1))/v.sum(); k=[3,4,5]
    return k[int(((P[k]-m)**2).sum(1).argmin())]
H=W_=64; Y,X=np.mgrid[0:64,0:64]
RING=(r7>=6)
ZL=(X>=16)&(X<=24)&(Y>=21)&(Y<=30)&~RING
ZR=(X>=40)&(X<=46)&(Y>=22)&(Y<=32)&~RING&~((X<=41)&(Y<=27))
ZA=(X>=11)&(X<=16)&(Y>=40)&(Y<=51)
Z=ZL|ZR|ZA
kaal=r7.copy()
for y,x in zip(*np.where(Z)): kaal[y,x]=red(x,y)
a=kaal.copy()
L_={'.':0,'#':1,'a':2,'b':3,'c':4,'d':5}
FIX=[ # (x,y,kleur,reden)
 (18,23,'a','linkerhoorn: modelrand (donkerbruin 47%) valt in de cel, reductie liet de rand open'),
 (20,23,'a','linkerhoorn: rechter modelrand valt in deze cel (dekking 15%, allemaal lijn), anders open rand'),
 (22,26,'a','linkerhoorn: rechter modelrand (donker 57%), reductie liet hem open naar de lucht'),
 (44,24,'a','rechterhoorn: linker modelrand, dekking 49% (net onder 50%), anders open rand'),
 (44,25,'a','rechterhoorn: linker modelrand (donker 44%), anders open rand'),
 (42,27,'a','rechterhoorn: bovenrand voet (donker 34% bovenin de cel), anders open rand'),
 (46,24,'#','rechterhoorn: rechter modellijn valt in de cel (donker 48%), anders open rand; zwart zoals eronder'),
 (46,25,'#','idem'),
 (46,30,'#','rechterhoorn: modellijn (dekking 39%, 100% zwart) net onder de dekkingsgrens, anders open rand'),
 (40,29,'d','rechterhoorn: modellijn ligt op de grens x39/40 en staat al in r7 op x39 (ringrand); zwart ook op x40 gaf een dubbele lijn; vlakkleur gemeten (d)'),
 (40,30,'c','idem, vlakkleur gemeten (c)'),
 (11,44,'a','linkerarm: buitenrand van de want valt in kolom 11 (dekking 34%, allemaal lijn), weggevallen door de dekkingsgrens'),
 (11,45,'a','idem'),(11,46,'a','idem'),
 (12,43,'a','linkerarm: modelrand linksboven in de cel, anders open rand'),
 (12,48,'#','linkerarm: zwarte onderboog (dekking 47%, zwart 38%) net onder de dekkingsgrens'),
 (13,49,'#','linkerarm: zwarte onderboog (dekking 43%, zwart 37%) idem'),
 (14,40,'#','linkerarm/lijfrand: modellijn (dekking 48%, zwart 48%) net onder de dekkingsgrens, anders open rand'),
]
for x,y,k,_ in FIX: a[y,x]=L_[k]
np.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f952c4af-e06e-5b56-87d5-86ed60c9233c/scratchpad/kaal8.npy',kaal)
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(D+'r8/mate.png',transparency=0)
d=a!=r7
print('buiten de zones anders dan r7:',int((d&~Z).sum()))
for nm,z in (('linkerhoorn',ZL),('rechterhoorn',ZR),('linkerarm',ZA)):
    print(nm,'anders dan r7:',int((d&z).sum()),' afwijkend van kale reductie:',int(((a!=kaal)&z).sum()))
ch='.#abcdGHIstu'
for nm,(x0,y0,x1,y1) in (('L',(15,21,25,31)),('R',(38,21,48,34)),('A',(10,38,20,53))):
    print(nm,'   r8 | kaal | r7')
    for y in range(y0,y1+1): print('%2d '%y+''.join(ch[v] for v in a[y,x0:x1+1]),' '+''.join(ch[v] for v in kaal[y,x0:x1+1]),' '+''.join(ch[v] for v in r7[y,x0:x1+1]))
