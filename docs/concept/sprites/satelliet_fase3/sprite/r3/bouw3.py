# r3: kale reductie van het model (kaal.py, ongewijzigd) + alleen benoemde pixelreparaties.
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
    PM[k]=(PCOV[k]>=0.5)&(PCOV[k]>modcov)&~np.isin(K,[6,7,8,9,10,12,13,14,15])   # romp/kraag/oog in kaal blijft romp
    OWNK[PM[k]]=k
PAN=OWNK!=''
# 1. silhouet panelen: drempel 50% modeldekking (rechte modelrand -> regelmatige trap)
oudpan=(sum(PCOV.values())/np.maximum(nonbg,1e-9)>=0.5)&(K>0)&~np.isin(K,[6,7,8,9,10,12,13,14,15])
for y in range(OH):
    for x in range(64):
        if oudpan[y,x] and not PAN[y,x] and modcov[y,x]<0.5*nonbg[y,x]: zet(x,y,0,'paneelrand','silhouet: <50% modeldekking')
# 2. vakken = navy (2, gemeten vakkleur 40,38,70), randen volgens DC
def nb(y,x):
    return OWNK[y,x] if 0<=y<OH and 0<=x<64 else ''
for y in range(OH):
    for x in range(64):
        k=OWNK[y,x]
        if not k: continue
        onder=nb(y+1,x)!=k and (y+1>=OH or K[y+1,x]==0 or nb(y+1,x)!='' or spr[y+1,x]==0)
        rechts=nb(y,x+1)!=k and (x+1>=64 or spr[y,x+1]==0 or nb(y,x+1)!='')
        boven_in=nb(y-1,x)==k
        if onder or (rechts and boven_in): c=1          # schaduwkant: zwart
        else: c=2                        # vak / lichtkant: donkerste eigen tint (navy)
        zet(x,y,c,k,'paneel: vak navy / DC-rand' if c==2 else 'paneel: rand schaduwkant zwart')
# 3. dwarslijnen uit het model: per lijn de pixel met de meeste lijndekking per kolom (vlakke lijn) of rij (steile lijn)
LIJNC=5
for k,Cs in KC.items():
    T,R,L=map(np.array,GEO[k]); d=L-T; vlak=abs(d[0])>abs(d[1])
    for i,C in enumerate(Cs):
        C=np.where((OWNK==k)&(spr!=1),C,0)   # niet op de zwarte schaduwrand
        if vlak:
            for x in range(64):
                col=C[:,x]
                yy=int(col.argmax())
                if col.max()>=0.05: zet(x,yy,LIJNC,k,'dwarslijn %d uit model'%(i+1))
        else:
            for y in range(OH):
                row=C[y]
                xx=int(row.argmax())
                if row.max()>=0.05: zet(xx,y,LIJNC,k,'dwarslijn %d uit model'%(i+1))
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
# 6. palet: index 5 = gemeten lijnkleur van het paneelraster in het model (mediaan 116,99,143; kaal.py had 106,88,130)
PAL=list(kaal.PAL); PAL[5]=(116,99,143)
TOP=(64-OH)//2+3
if __name__=='__main__':
    from collections import Counter
    full=np.zeros((64,64),np.uint8); full[TOP:TOP+OH]=spr
    im=Image.fromarray(full,'P'); flat=[v for c in PAL for v in c]; im.putpalette(flat+[0]*(768-len(flat))); im.save('sprite.png',transparency=0)
    kaal.save(K.astype(np.uint8),'kaal.png')
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
