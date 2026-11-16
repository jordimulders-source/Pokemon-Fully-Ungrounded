# Bewijs r10: diff t.o.v. ../r9/sprite_a.png per opdrachtzone; buiten de zones moet alles 0 zijn. Plus restmetingen.
import json, numpy as np; from PIL import Image
from scipy import ndimage
r9=np.asarray(Image.open('../r9/sprite_a.png')).astype(int); W=json.load(open('wijzigingen.json')); SP=np.load('spikkels_r9.npy')
Y,X=np.mgrid[:64,:64]
def mask(lst):
    m=np.zeros((64,64),bool)
    for x,y in lst: m[y,x]=1
    return m
z1=mask([eval(k) for k in W['1 links van het oog']]); z2=mask(W['2 roze rand']); z4=mask(W['4 zwart']); z3=mask([eval(k) for k in W['3 kopruis']])
Y,X=np.mgrid[:64,:64]; KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24))
TW=np.zeros((64,64),bool)                       # twinkels uit het model (plusjes), niet aanraken
for cx,cy in ((6,4),(3,8),(20,26),(15,31),(29,18)):
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): TW[cy+dy,cx+dx]=1
OOG=(X>=11)&(X<=14)&(Y>=20)&(Y<=23)
for f in ('sprite_B.png','sprite_rond.png'):
    s=np.asarray(Image.open(f)).astype(int); d=s!=r9
    zones={'1 links oog':z1,'2 roze rand':z2,'3 kopruis':z3,'4 zwart':z4}
    print(f,'| kleuren incl. transparant',len(np.unique(s)))
    for k,m in zones.items(): print('  ',k,int((d&m).sum()))
    LO=SP&(X<=26)&(Y>=28); nieuw=d&(r9==0)
    print('   6 barst linksonder weg',int((d&LO&(s==0)).sum()),'| nieuwe spikkels (op lege pixels)',int(nieuw.sum()))
    rest=d&~z1&~z2&~z3&~z4&~LO&~nieuw
    print('   BUITEN DE ZONES gewijzigd:',int(rest.sum()),'| rechteroog gewijzigd:',int((d&OOG&~z1).sum()),
          '| silhouet hoofdmassa gewijzigd:',int(((s>0)!=(r9>0))[~LO&~nieuw].sum()))
    # restmeting kop: creme-vlakjes < 3 px (4-buren) in de kopzone
    k=0
    for i in (3,4,5):
        l,n=ndimage.label((s==i)&KZ&~SP&~TW&~OOG); k+=sum(1 for j in range(1,n+1) if (l==j).sum()<3)
    op=s>0; lab,n=ndimage.label(op,np.ones((3,3))); big=lab==(np.argmax(np.bincount(lab.ravel())[1:])+1)
    rb=big&~ndimage.binary_erosion(big,np.ones((3,3)),border_value=0)
    print('   rest: creme-vlakjes<3 in de kop (zonder oog/twinkels)',k,'| roze(7) op de rand',sorted((int(x),int(y)) for y,x in zip(*np.where(rb&(s==7)))))
    # wat in zone 1 niet uit het model komt
