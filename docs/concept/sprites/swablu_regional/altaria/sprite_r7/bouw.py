# Altaria (onweerswolk) r7 (vanaf r6): de donkere scheidingslijnen tussen de bollen 1-op-1 uit het model (natief_kop15_dy10: blok met een
# bijna zwarte modelpixel, L < LIJN) in de wolk-selout (tint 2, L55: gekleurd, niet zwart), als 1 px gebogen lijnen; binnen elke bol 3 tinten
# (kap licht linksboven, midden, schaduw 3 boven de selout-boog). Coördinator r7: zo lezen de bollen zoals in het model, zacht en niet zwart.
# Zones: lijf Y40-57 + rechtervleugel (wolkvulling) + linkervleugelnaad (7-11,25). Bevroren (assert): kop, ogen, snavel, hals, kuif, static,
# silhouet. Bouwen vanuit altaria/: python3 sprite_r7/bouw.py && python3 sprite_r7/vel.py
import sys, os, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r5')
import basis as B
from gemeen import label
from PIL import Image
im=Image.open('sprite_r6/altaria_r6.png'); P=np.asarray(im).astype(int); o=P.copy()
P5=np.asarray(Image.open('sprite_r5/proef_eindkeuring.png')).astype(int)
L=B.L
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b]; fig=P>0
rand=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)): rand[Y,X]=any(not fig[Y+dy,X+dx] for dy,dx in N4)
ZONE=np.zeros((64,64),bool); ZONE[40:58,8:56]=True; ZONE[16:32,38:61]=True; ZONE[22:30,5:14]=True
MAG=ZONE&np.isin(P,[2,3,4,5,6])&~rand
LIJN=float(os.environ.get('LIJN','32'))
mn=np.full((64,64),255.)
for Y,X in zip(*np.where(fig)):
    u,v=B.blok(X,Y); mn[Y,X]=L[v:v+3,u:u+3].min()
lijn=MAG&(mn<LIJN)
# oude selout in de zone die het model niet als lijn heeft -> weg (vultint van de buren); 1 px dik houden
for Y,X in zip(*np.where(MAG&(P==2)&~lijn)):
    nb=[P[Y+a,X+b] for a,b in N4 if P[Y+a,X+b] in (3,4,5,6)]
    o[Y,X]=max(set(nb),key=nb.count) if nb else 3
lab,n=label(lijn,acht=True)                       # lijnstukjes < 3 px die niet aan een andere lijn/rand raken: weg
for i in range(1,n+1):
    m=lab==i
    if m.sum()<3 and not any(((P[Y+a,X+b]==2)&~MAG[Y+a,X+b]) for Y,X in zip(*np.where(m)) for a,b in N8): lijn[m]=False
# dun: een lijnpixel met een lijnpixel eronder en een erboven-links/rechts verdubbelt de lijn -> de bovenste wordt schaduw
for Y,X in sorted(zip(*np.where(lijn))):
    if lijn[Y+1,X] and (lijn[Y,X-1] or lijn[Y,X+1]) and (lijn[Y+1,X-1] or lijn[Y+1,X+1]): lijn[Y,X]=False
# bolgrenzen uit r6 (bollen.txt = bollen opgemeten op het model): de onderboog van elke bol (grens onder/rechts met een andere bol)
# wordt ook selout, zodat de lijnen doorlopen waar het model op 1/3 maar een stukje zwart laat zien
R6={}; exec(open('sprite_r6/bouw.py').read().split('def ontkorrel')[0],R6)
own=R6['own']
for Y,X in zip(*np.where(MAG&(own>0))):
    i=own[Y,X]
    if P[Y,X]==3 and any(own[Y+a,X+b] not in (i,0) and own[Y+a,X+b]>0 for a,b in ((1,0),(0,1),(1,1))): lijn[Y,X]=True
for Y,X in sorted(zip(*np.where(lijn))):          # opnieuw dunnen (1 px)
    if lijn[Y+1,X] and (lijn[Y,X-1] or lijn[Y,X+1]) and (lijn[Y+1,X-1] or lijn[Y+1,X+1]): lijn[Y,X]=False
o[lijn]=2
# lijf van de bol midden (4) i.p.v. donker: de bol leest door kap + midden + schaduw tegen de lijn (rok Y>=54 blijft donker zoals het model)
SCH=np.zeros((64,64),bool)
for Y,X in zip(*np.where(lijn)):
    if MAG[Y-1,X] and not lijn[Y-1,X]: SCH[Y-1,X]=True
    if MAG[Y,X-1] and not lijn[Y,X-1] and lijn[Y+1,X-1]==False and o[Y,X-1] in (3,4): SCH[Y,X-1]=True
for Y,X in zip(*np.where(MAG&~lijn&~SCH&(o==3))):
    if Y<54 and own[Y,X]>0: o[Y,X]=4
# schaduw tegen de boog: vulpixel direct boven een lijnpixel -> 3 (behalve een kern 6, die krijgt eerst 5)
for Y,X in zip(*np.where(lijn)):
    y=Y-1
    if MAG[y,X] and not lijn[y,X] and o[y,X] in (4,5): o[y,X]=3
for Y,X in zip(*np.where(SCH&(o==4))): o[Y,X]=3
exec(open('sprite_r7/fix.py').read()) if os.path.exists('sprite_r7/fix.py') else None
# --- controles ---
assert ((o>0)==(P>0)).all()
assert (o[~MAG]==P[~MAG]).all()
if __name__=='__main__':
    uit=Image.fromarray(o.astype('uint8'),'P'); uit.putpalette(im.getpalette()); uit.save('sprite_r7/altaria_r7.png',transparency=0)
    pal=np.array(im.getpalette()[:39]).reshape(-1,3); r=np.full((64,64,3),255,'uint8')
    for k in range(1,13): r[o==k]=pal[k]
    Image.fromarray(r).resize((512,512),Image.NEAREST).save('sprite_r7/altaria_r7_8x.png')
    d=o!=P; print('diff r6: %d px (lijf %d, rechtervleugel %d, linkervleugel %d); diff proef r5: %d'%(d.sum(),d[40:58,8:56].sum(),d[16:32,38:61].sum(),d[22:30,5:14].sum(),(o!=P5).sum()))
    kl=[]
    for k in (2,3,4,5,6):
        lb,nn=label(o==k,acht=(k==2))
        for i in range(1,nn+1):
            m=lb==i
            if m.sum()<3 and (m&MAG).any(): kl.append((k,[(int(x),int(y)) for y,x in zip(*np.where(m))]))
    print('vlakjes < 3 px:',len(kl),kl)
    print('zwart buiten pupillen:',int(((o==1)&(P!=1)).sum()))
