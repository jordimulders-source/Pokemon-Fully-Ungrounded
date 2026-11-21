# Altaria (onweerswolk) r6: alleen het lijf (X10-53, Y44-57) en de rechtervleugel (X38-60, Y19-31 + punt Y16-18) als ronde bollen
# (eindkeuring r5, MOET 6b). Start = sprite_r5/proef_eindkeuring.png (r5 + MOETEN 1-6). Kop, ogen, snavel, hals, kuif, static,
# linkervleugel, buitenrand en silhouet: diff 0 (assert onderaan).
# Werkwijze: de bollen van het model (model_kop/natief_kop15_dy10.png, 3x3 natief per spritepixel) zijn per bol opgemeten: plek, breedte,
# hoogte, licht/midden/donker en de hooglichtkern (sprite_r6/bollen.txt, achter -> voor; ov.png toont ze over het model). Elke bol wordt
# als bolvorm belicht van linksboven (kern 6 -> licht 5 -> midden 4 -> donker 3), de voorste bol wint; waar een bol eindigt en de
# volgende begint ligt aan de onder-/rechterkant een onderboog in 3 (geen selout, geen zwart). Daarna ontkorrelen en de handreparaties
# (FIX) per pixel. Jordi: "iets minder detail is niet erg tov het model, zolang die niet blurry wordt" / "De belijning moet juist zachter
# en niet zwart". Bouwen vanuit altaria/: python3 sprite_r6/bouw.py && python3 sprite_r6/vel.py
import sys, numpy as np
sys.path.insert(0,'gereedschap')
from gemeen import label
from PIL import Image
im=Image.open('sprite_r5/proef_eindkeuring.png'); P=np.asarray(im).astype(int); o=P.copy()
N4=((-1,0),(1,0),(0,-1),(0,1)); fig=P>0
rand=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)): rand[Y,X]=any(not fig[Y+dy,X+dx] for dy,dx in N4)
ZONE=np.zeros((64,64),bool); ZONE[44:58,10:54]=True; ZONE[19:32,38:61]=True; ZONE[16:19,55:61]=True   # + vleugelpunt (bol A)
MAG=ZONE&np.isin(P,[2,3,4,5,6])&~rand          # alleen wolkvulling binnen de zone
BOL=[l.split() for l in open('sprite_r6/bollen.txt') if l.strip() and not l.startswith('#')]
T6,T5,T4=0.8,0.55,0.15                          # belichtingsdrempels (licht type); midden -0.10, donker -0.45
OFF={'l':0.0,'m':0.10,'d':0.45}
Lv=np.array([-0.55,-0.65,0.75]); Lv/=np.linalg.norm(Lv)
own=np.zeros((64,64),int); I=np.zeros((64,64))
for i,(n,cx,cy,rx,ry,t,*kern) in enumerate(BOL):
    cx,cy,rx,ry=map(float,(cx,cy,rx,ry))
    for Y in range(64):
        for X in range(64):
            dx=(X-cx)/rx; dy=(Y-cy)/ry; d2=dx*dx+dy*dy
            if d2<=1 and fig[Y,X]:
                own[Y,X]=i+1; I[Y,X]=dx*Lv[0]+dy*Lv[1]+max(0,1-d2)**.5*Lv[2]-OFF[t]
val=np.zeros((64,64),int)
for Y,X in zip(*np.where(own>0)):
    i=own[Y,X]; v=I[Y,X]; t6=T6 if BOL[i-1][5]=='l' else 9
    val[Y,X]=6 if v>t6 else 5 if v>T5 else 4 if v>T4 else 3
    if any(own[Y+a,X+b]!=i for a,b in ((1,0),(0,1),(1,1))) and v<T5+0.15: val[Y,X]=3     # onderboog op de bolgrens
for i,(n,cx,cy,rx,ry,t,*kern) in enumerate(BOL):     # kern >= 3x2 (eindkeuring), plek uit het model; ring licht eromheen
    if not kern: continue
    kx,ky,b,h=map(int,kern)
    for Y in range(ky,ky+h):
        for X in range(kx,kx+b):
            if own[Y,X]==i+1: val[Y,X]=6
            for a,c in N4:
                if own[Y+a,X+c]==i+1 and val[Y+a,X+c]<5 and not (kx<=X+c<kx+b and ky<=Y+a<ky+h) and (a<0 or c<0 or val[Y+a,X+c]==4): val[Y+a,X+c]=5
m=MAG&(own>0); o[m]=val[m]
# oude selout-naden van r5 in het lijf die geen bol raakt: onderboog in 3 (model: zwarte lijn = onderboog), geen selout
o[MAG&(own==0)&(P==2)&(np.arange(64)[:,None]>=44)]=3
def ontkorrel():
    for _ in range(3):
        for k in (3,4,5,6):
            lab,n=label(o==k,acht=False)
            for j in range(1,n+1):
                mm=lab==j
                if mm.sum()>=3 or not MAG[mm].all(): continue
                b=[o[Y+a,X+c] for Y,X in zip(*np.where(mm)) for a,c in N4 if o[Y+a,X+c] in (3,4,5,6) and o[Y+a,X+c]!=k]
                if k==5 and 6 in b: continue      # ring rond een kern = tussenstap (functie), blijft
                if b: o[mm]=min(set(b),key=lambda t:(abs(t-k),-b.count(t),-t))   # dichtstbijzijnde toon (tussenstap blijft)
ontkorrel()
kaal=o.copy()
# handreparaties: (X, Y, tint) met 2 selout, 3 donker, 4 midden, 5 licht, 6 hooglicht
FIX=[]
exec(open('sprite_r6/fix.py').read()) if __import__('os').path.exists('sprite_r6/fix.py') else None
for X,Y,k in FIX:
    assert MAG[Y,X], ('bevroren pixel',X,Y); o[Y,X]=k
# --- controles ---
assert ((o>0)==(P>0)).all()                     # silhouet
assert (o[~MAG]==P[~MAG]).all()                 # buiten de zone diff 0
def korrel():
    kl=[]
    for k in (2,3,4,5,6):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()<3 and (m&MAG).any(): kl.append((k,[(int(x),int(y)) for y,x in zip(*np.where(m))]))
    return kl
def naden(minl=5):        # rechte horizontale grens: rij donker (3) onder lichter (4-6), >= minl px aaneen
    out=[]
    for Y in range(1,64):
        run=[]
        for X in range(64):
            ok=MAG[Y,X] and o[Y,X]==3 and o[Y-1,X] in (4,5,6) and o[Y+1,X]==3 if Y<63 else False
            if ok: run.append(X)
            if (not ok or X==63) and run:
                if len(run)>=minl: out.append((Y,run[0],run[-1]))
                run=[]
    return out
if __name__=='__main__':
    uit=Image.fromarray(o.astype('uint8'),'P'); uit.putpalette(im.getpalette()); uit.save('sprite_r6/altaria_r6.png',transparency=0)
    pal=np.array(im.getpalette()[:39]).reshape(-1,3); r=np.full((64,64,3),255,'uint8')
    for k in range(1,13): r[o==k]=pal[k]
    Image.fromarray(r).resize((512,512),Image.NEAREST).save('sprite_r6/altaria_r6_8x.png')
    d=o!=P; Lz=d&(np.arange(64)[:,None]>=44); Rz=d&~Lz
    print('diff met proef: %d px (lijf %d, rechtervleugel %d); handreparaties %d px'%(d.sum(),Lz.sum(),Rz.sum(),int((o!=kaal).sum())))
    kl=korrel(); print('tintvlakjes < 3 px die de zone raken:',len(kl)); [print(' ',k) for k in kl]
    print('rechte naden (>=5 px):',naden())
    print('zwart buiten de pupillen:',int(((o==1)&~(P==1)).sum()))
