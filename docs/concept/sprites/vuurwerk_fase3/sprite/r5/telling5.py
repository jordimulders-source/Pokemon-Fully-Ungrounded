# Bewijs r5: diff t.o.v. r4 per zone. Buiten kop (vervormde kopzone), meegeschoven kop-twinkels, losse vlam en spikkels = 0.
import json, pickle, numpy as np; from PIL import Image
r4=np.asarray(Image.open('../r4/sprite.png')).astype(int); r3=np.asarray(Image.open('../r3/sprite.png')).astype(int); kop3=np.load('../r3/r3_kop_V.npy')
SP4=r3!=kop3; Y,X=np.mgrid[:64,:64]; FZ=(X>=38)&(X<=46)&(Y>=3)&(Y<=6)
TWC=[(8,6),(5,9),(20,26),(16,29)]
def plus(c):
    m=np.zeros((64,64),bool)
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): m[c[1]+dy,c[0]+dx]=1
    return m
for maat,tw in ((115,[(6,4),(3,8),(20,26),(15,31)]),(125,[(5,3),(1,7),(20,26),(15,32)])):
    Z=np.load('zone5_%d.npy'%maat); TWo=sum(plus(c) for c in TWC)>0; TWn=sum(plus(c) for c in tw)>0
    for naam in ('geel','goud','magenta','rood'):
        s=np.asarray(Image.open('sprite_%d_%s.png'%(maat,naam))).astype(int); d=s!=r4
        SP5=d&~Z&~TWo&~TWn&~FZ&~SP4&(r4==0)          # nieuw geplaatste spikkels (op pixels die in r4 leeg waren)
        rest=d&~Z&~TWo&~TWn&~FZ&~SP4&~SP5
        oog=int(((s==int({'geel':13,'goud':14,'magenta':7,'rood':11}[naam]))&Z&(Y>=19)&(Y<=24)&(X>=10)&(X<=15)).sum())
        print(maat,naam,'| kop:',int((d&Z).sum()),'| twinkels (mee geschoven):',int((d&(TWo|TWn)).sum()),'| vlam:',int((d&FZ).sum()),
              '| spikkels weg/nieuw:',int((d&SP4).sum()),'/',int(SP5.sum()),'| REST (lijf, lijnen, pijl, lijfspikkels, twinkel rechts):',int(rest.sum()),
              '| oogpixels in variantkleur:',oog,'| kleuren',len(np.unique(s)))
