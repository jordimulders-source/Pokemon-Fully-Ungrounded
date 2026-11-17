# Bewijs r4: diff t.o.v. r3 (../r3/sprite.png) per zone. Buiten de kop (lijf, lijnen, pijl, twinkels, lijfspikkels, spikkels) = 0.
import json, numpy as np; from PIL import Image
r3=np.asarray(Image.open('../r3/sprite.png')).astype(int); r4=np.asarray(Image.open('sprite.png')).astype(int)
kop3=np.load('../r3/r3_kop_V.npy'); kaal=np.asarray(Image.open('sprite_kaal.png')).astype(int)
Y,X=np.mgrid[:64,:64]; KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24)); FACE=(X>=6)&(X<=17)&(Y>=15)&(Y<=26)
SPIK=r3!=kop3; TW=np.zeros_like(KZ)
for cx,cy in [(8,6),(5,9),(29,18),(20,26),(16,29)]:
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): TW[cy+dy,cx+dx]=1
d=r3!=r4
print('kop (zonder gezicht-vak):',int((d&KZ&~FACE).sum()),'px | gezicht-vak (x6-17, y15-26):',int((d&FACE).sum()),'px | buiten de kop:',int((d&~KZ).sum()),'px')
print('spikkels gewijzigd:',int((d&SPIK).sum()),'| twinkels gewijzigd:',int((d&TW).sum()),'| silhouet erbij:',int(((r4>0)&(r3==0)).sum()),'eraf:',int(((r4==0)&(r3>0)).sum()))
print('kleuren:',len(np.unique(r4)),'(incl. transparant) | palet gelijk aan r3:',Image.open('sprite.png').getpalette()[:48]==Image.open('../r3/sprite.png').getpalette()[:48])
e=kaal!=r4; print('niet uit de kale kop-reductie (gezicht4.json + opschoning):',[(int(x),int(y),int(kaal[y,x]),int(r4[y,x])) for y,x in zip(*np.where(e))])
for k in (2,3,4,5,14): print('  index',k,'in de kop: r3',int(((r3==k)&KZ).sum()),'-> r4',int(((r4==k)&KZ).sum()))
