# r7: kopie van r4/bouw4.py; alleen OGEN/staafje per bolvariant (VAR) en OH variabel. VAR=100 geeft r4 exact terug.
# r4 (vanaf r3): kale reductie van het model (kaal.py, ongewijzigd) + alleen benoemde pixelreparaties.
# Elke afwijking van kaal wordt gelogd met onderdeel en reden (log.txt, diff.png).
import numpy as np, json
from PIL import Image
import kaal
from kruis import KC, REG, PCOV, covpan, nonbg, OH, GEO
K,_=kaal.reduce(); K=K.astype(int); spr=K.copy(); LOG=[]
def zet(x,y,c,deel,reden):
    if spr[y,x]!=c: LOG.append((int(x),int(y),int(K[y,x]),int(c),deel,reden)); spr[y,x]=c
ORDE=['PC','PA','PB','PD','PF','PE']            # achter -> voor (zoals het model)
modcov=nonbg-covpan                             # dekking door romp (wit/paars/oog)
# --- paneelmaskers: modeldekking van paneelkleuren >= 50% en meer paneel dan romp
PM={}; OWNK=np.full((OH,64),'',object)
for k in ORDE:
    PM[k]=(((PCOV[k]>=0.5)&(PCOV[k]>modcov))|((PCOV[k]>=0.3)&np.isin(K,[1,2,3,4,5])))&~np.isin(K,[6,7,8,9,10,12,13,14,15])   # romp/kraag/oog in kaal blijft romp
    OWNK[PM[k]]=k
PAN=OWNK!=''
# 1. silhouet panelen: drempel 50% modeldekking (rechte modelrand -> regelmatige trap)
oudpan=(sum(PCOV.values())/np.maximum(nonbg,1e-9)>=0.5)&(K>0)&~np.isin(K,[6,7,8,9,10,12,13,14,15])
for y in range(OH):
    for x in range(64):
        if oudpan[y,x] and not PAN[y,x] and nonbg[y,x]<0.5: zet(x,y,0,'paneelrand','silhouet: <50% modeldekking')
# 2. vakken = navy (2, gemeten vakkleur 40,38,70), randen volgens DC
def nb(y,x):
    return OWNK[y,x] if 0<=y<OH and 0<=x<64 else ''
LEEG=(spr==0)&~PAN
for y in range(OH):
    for x in range(64):
        k=OWNK[y,x]
        if not k: continue
        # r4: zwart alleen als BUITENrand (tegen transparant), niet tegen romp of een ander paneel
        onder=y+1>=OH or LEEG[y+1,x]
        rechts=x+1>=64 or LEEG[y,x+1]
        boven_in=nb(y-1,x)==k
        tegen_romp=any(0<=yy<OH and 0<=xx<64 and K[yy,xx] not in (0,1,2,3,4,5) for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
        if K[y,x]==1 and (tegen_romp or (y>0 and K[y-1,x]==1 and not OWNK[y-1,x])): continue   # donkere naad paneel/romp uit het model laten staan
        if onder or (rechts and boven_in): c=1          # schaduwkant: zwart
        else: c=2                        # vak / lichtkant: donkerste eigen tint (navy)
        zet(x,y,c,k,'paneel: vak navy / DC-rand' if c==2 else 'paneel: rand schaduwkant zwart')
# 3. dwarslijnen (r4): doorlopend over de hele paneeldikte, gelijk verdeeld zoals in het model.
#    Modelmeting (lijnen.py): binnenlijnen op u=0,24/0,49/0,75 (PD), 0,25/0,47/0,73 (PE), 0,23/0,53/0,77 (PA), 0,20/0,48/0,72 (PC)
#    tussen randen op u~0 en u~0,98 -> gelijk verdeeld = kwarten; mast PB/PF 3 vakken -> derden. Richting = korte paneelzijde
#    (gemeten hoeken; komt overeen met de gefitte modellijnen: PA -0,77/0,64 tegen GEO -0,78/0,62).
from lijnen import uv as _uv
s_=3.515625
LIJNPOS={'PA':[.25,.5,.75],'PC':[.25,.5,.75],'PD':[.25,.5,.75],'PE':[.25,.5,.75],'PB':[1/3,2/3],'PF':[1/3,2/3]}
SY,SX=np.mgrid[0:OH,0:64]; MX=3+(SX+0.5)*s_; MY=3+(SY+0.5)*s_
LIJNC=5
for k,ps in LIJNPOS.items():
    u,v=_uv(k,MX,MY); dux=np.abs(_uv(k,MX+s_,MY)[0]-u); duy=np.abs(_uv(k,MX,MY+s_)[0]-u)
    T,R,L=map(np.array,GEO[k]); d=L-T; vlak=abs(d[0])>=abs(d[1])
    lim=(duy if vlak else dux)/2
    for j,p in enumerate(ps):
        for y,x in zip(*np.where((OWNK==k)&(np.abs(u-p)<=lim)&(spr!=1))):
            zet(x,y,LIJNC,k,'dwarslijn %d (doorlopend, modelpositie)'%(j+1))
# 4. omlijning romp (Gen 3 / DC): randpixel tegen achtergrond -> zwart aan schaduwkant (onder/rechts), navy aan lichtkant.
#    Silhouet blijft gelijk (pixel wordt vervangen, niet toegevoegd).
DONKER={1,2}
rand=[]
for y in range(OH):
    for x in range(64):
        if spr[y,x]==0 or OWNK[y,x] or spr[y,x] in DONKER: continue
        def leeg(yy,xx): return not(0<=yy<OH and 0<=xx<64) or spr[yy,xx]==0
        if leeg(y+1,x) or leeg(y,x+1): rand.append((x,y,1))
        elif leeg(y-1,x) or leeg(y,x-1): rand.append((x,y,2))
for x,y,c in rand: zet(x,y,c,'romp','omlijning: '+('schaduwkant zwart' if c==1 else 'lichtkant navy'))
# 5. pupillen: modelpupil (donker binnen de iris) met >=30% dekking -> navy 2 (gemeten pupil ~40,38,66)
from oog import PUP
for y,x in zip(*np.where(PUP>=0.29)): zet(x,y,2,'oog','pupil uit model (>=29% dekking)')
# 5b. ogen (r4): ring + iris + pupil leesbaar, geen wit; kleuren uit het model (ring paars 6/7/8, iris teal a, pupil navy 2)
from common import VAR
import ogen7
OGEN_R4={ # voorste oog: pupil 2x2 op de modelplek (dekking (14,36) .94, (13,36) .30, (14,37) .21)
 'voor':[(13,37,2),(14,37,2)],
 # linkeroog: ring links terug (omlijning schuift naar buiten), ring boven/onder, pupil op de modelplek (18,18)
 'links':[(18,16,8),(19,16,8),(17,17,7),(17,18,6),(16,17,2),(16,18,2),(18,19,6),(19,19,6),(18,20,1),(19,20,1),(17,19,1)],
 # rechteroog: ring rondom (boven licht 8, links 8/7, rechts en onder 6), pupil (51,25)
 'rechts':[(50,24,8),(51,24,8),(52,24,8),(49,25,8),(49,26,7),(53,25,6),(53,26,6),(50,27,6),(51,27,6),(52,27,6)],
}
OGEN=OGEN_R4 if VAR=='100' else ogen7.OGEN[VAR]
for nm,px in OGEN.items():
    for x,y,c in px: zet(x,y,c,'oog_'+nm,'oog leesbaar: ring/pupil (modelkleuren)')
# 5d (r7). ogen afmaken volgens de r4-regel (ring + iris + pupil, geen wit, ring gesloten), alleen bij VAR!=100
if VAR!='100':
    RING=(6,7,8); IRIS=(9,10)
    for nm,(cx,cy,R) in ogen7.ZONE.items():
        inz=lambda x,y,m=0.0: np.hypot(x+.5-cx,y+.5-cy)<=R+m
        # (a) pupil: voorste oog 2x2 op het blok met de meeste modelpupil (r4: 'pupil 2x2 op de modelplek'); zij-ogen: >=1 px
        P=ogen7.PUPC[nm]
        groot=(nm=='voor') or (VAR.startswith(('s','r9','r10')) and 2*ogen7.INFO[nm]['iris_r']/s_>=3.3)   # r8: zij-oog met iris >=3,3 px -> pupil 2x2
        if groot:
            bx=max(((x,y) for y in range(OH-1) for x in range(63) if inz(x+.5,y+.5)),key=lambda q:P[q[1]:q[1]+2,q[0]:q[0]+2].sum())
            for y in range(bx[1],bx[1]+2):
                for x in range(bx[0],bx[0]+2): zet(x,y,2,'oog_'+nm,'pupil 2x2 op de modelplek')
            if VAR.startswith(('s','r9','r10')):
                for y in range(OH):
                    for x in range(64):
                        if spr[y,x]==2 and np.hypot(x+.5-cx,y+.5-cy)<=0.75*R and not(bx[0]<=x<=bx[0]+1 and bx[1]<=y<=bx[1]+1):
                            zet(x,y,10,'oog_'+nm,'pupil 2x2: losse pupilpixel -> iris')
        else:   # zij-ogen: 1 pupilpixel op de plek met de meeste modelpupil (r4: links/rechts op de modelplek)
            y,x=np.unravel_index(P.argmax(),P.shape); zet(x,y,2,'oog_'+nm,'pupil op de modelplek (max modeldekking)')
        # (b) iris/pupil op de silhouetrand: rand naar buiten als het model daar >=40% bol heeft, anders wordt de irispixel ring
        for _ in range(2):
            for y in range(OH):
                for x in range(64):
                    if not(inz(x,y) and spr[y,x] in IRIS+(2,)): continue
                    for dy,dx in ((0,-1),(-1,0),(0,1),(1,0)):
                        yy,xx=y+dy,x+dx
                        if 0<=yy<OH and 0<=xx<64 and spr[yy,xx]==0:
                            if ogen7.NONBG[yy,xx]>=0.4: zet(xx,yy,2 if dx<0 or dy<0 else 1,'oog_'+nm,'omlijning naar buiten (model >=40% bol)')
                            else: zet(x,y,6,'oog_'+nm,'iris op de rand -> ring')
        # (b2) iris direct tegen de buitenlijn (geen ring ertussen) -> ring (r4/r6: ring tussen omlijning en iris)
        for y in range(OH):
            for x in range(64):
                if not(inz(x,y) and spr[y,x] in IRIS): continue
                for dy,dx in ((0,-1),(-1,0),(0,1),(1,0)):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<OH and 0<=xx<64 and spr[yy,xx] in (1,2) and any(not(0<=yy+ey<OH and 0<=xx+ex<64) or spr[yy+ey,xx+ex]==0 for ey,ex in ((0,-1),(-1,0),(0,1),(1,0))):
                        zet(x,y,6 if dx>0 or dy>0 else 7,'oog_'+nm,'ring tussen buitenlijn en iris'); break
        # (c) ring sluiten: niet-oogpixel binnen de zone (+0,7) die aan iris/pupil grenst -> ring, tint van de meeste ringburen (anders 6)
        for _ in range(2):
            todo=[]
            for y in range(OH):
                for x in range(64):
                    v=spr[y,x]
                    if v==0 or v in RING+IRIS or v==2 or not inz(x,y,0.7): continue
                    nb4=[spr[y+dy,x+dx] for dy,dx in ((0,-1),(-1,0),(0,1),(1,0)) if 0<=y+dy<OH and 0<=x+dx<64]
                    if not any(q in IRIS for q in nb4): continue
                    if v==1 and any(q==0 for q in nb4): continue      # buitenlijn blijft
                    nb8=[spr[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<OH and 0<=x+dx<64 and spr[y+dy,x+dx] in RING]
                    todo.append((x,y,max(set(nb8),key=nb8.count) if nb8 else 6))
            for x,y,c in todo: zet(x,y,c,'oog_'+nm,'ring gesloten (geen wit/bol tussen iris en bol)')
    for nm,x,y,c in ogen7.EXTRA.get(VAR,[]): zet(x,y,c,'oog_'+nm,'handreparatie: '+('ring links/boven (r4-regel ring rondom)' if nm=='rechts' else 'iris 2x2 zoals r6'))
# 5c. staafje romp->PE: gat (24,36) dicht (modeldekking 0,48 tussen (23,36) 0,63 en (25,36) 1,0)
for x,y in (((24,36),) if VAR=='100' else ogen7.STAAF.get(VAR,[])): zet(x,y,1,'staafje_PE','staafje doorlopend (gat in reductie)')
# 6. palet: index 5 = gemeten lijnkleur van het paneelraster in het model (mediaan 116,99,143; kaal.py had 106,88,130)
PAL=list(kaal.PAL); PAL[5]=(116,99,143)
TOP=(64-OH)//2+3
if __name__=='__main__':
    from collections import Counter
    full=np.zeros((64,64),np.uint8); full[TOP:TOP+OH]=spr
    im=Image.fromarray(full,'P'); flat=[v for c in PAL for v in c]; im.putpalette(flat+[0]*(768-len(flat))); im.save('sprite.png',transparency=0)
    kaal.save(K.astype(np.uint8),'kaal.png'); np.save('ownk.npy',OWNK.astype(str)); np.save('kaal.npy',K)
    P=np.array(PAL,np.uint8)
    def rgb(A,bgc):
        r=P[A]; r[A==0]=bgc; return Image.fromarray(r)
    rgb(full,(235,240,235)).resize((512,512),Image.NEAREST).save('sprite_8x.png')
    # diffkaart: kaal 8x, rood = afwijkend
    d=np.array(rgb(np.pad(K,((TOP,64-TOP-OH),(0,0))).astype(int),(235,240,235))).astype(int)
    fk=np.zeros((64,64),bool); fk[TOP:TOP+OH]=spr!=K
    d=(d*0.45+255*0.55).astype(np.uint8); d[fk]=(220,30,30)
    Image.fromarray(d).resize((512,512),Image.NEAREST).save('diff.png')
    with open('log.txt','w') as f:
        f.write('x y kaal->r3 onderdeel reden  (y = rij in de 43-hoge uitsnede; in sprite.png +%d)\n'%TOP)
        for l in LOG: f.write('%d %d %d->%d %s %s\n'%l)
        f.write('\nTELLING (pixels afwijkend van kaal, laatste reden telt)\n')
        last={}
        for l in LOG: last[(l[0],l[1])]=l
        fin=[l for (x,y),l in last.items() if spr[y,x]!=K[y,x]]
        for (dl,r),n in sorted(Counter((l[4],l[5]) for l in fin).items()): f.write('%-10s %-45s %d\n'%(dl,r,n))
        f.write('totaal %d van %d sprite-pixels\n'%(len(fin),int(((spr>0)|(K>0)).sum())))
    print(open('log.txt').read().split('TELLING')[1])
    print('kleuren',len(np.unique(full)))
