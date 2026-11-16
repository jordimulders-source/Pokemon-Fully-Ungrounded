# Ronde 11: basis r10. Rechteroog uit het model verkleind (r9/red9.py, met groen) en als geheel geplakt (alleen de cellen
# die in de reductie of in r10 rand of groen zijn), daarna de rand gesloten langs de modellijn (r10/lijn.py-metingen).
import sys; sys.argv=sys.argv[:1]
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/r9')
import numpy as np; from PIL import Image; import red9 as R
D=R.D; im=Image.open(D+'r10/mate.png'); PAL=im.getpalette(); r10=np.asarray(im).astype(int)
Y,X=np.mgrid[0:64,0:64]
kg=np.zeros((64,64),int)
for y in range(34,43):
    for x in range(27,36): kg[y,x]=R.red(x,y,True)
GRN=lambda a:(a>=6)&(a<=8)
RO=(X>=27)&(X<=35)&(Y>=34)&(Y<=42); ZO=RO&((kg==1)|GRN(kg)|(r10==1)|GRN(r10))
def groen(x,y):   # groen vlakgemiddelde van de cel -> G/H/I
    W=R.cel(x,y); v=W*R.GR; m=(R.N*v[...,None]).sum((0,1))/v.sum(); k=[6,7,8]
    return k[int(((R.P[k]-m)**2).sum(1).argmin())]
kaal=r10.copy(); kaal[ZO]=kg[ZO]; a=kaal.copy()
FIX=[ # (x,y,kleur,modelmeting zwart/a/groen in %)
 (29,38,groen(29,38),'groen 65 (zwart 39): groen in het model, binnenkant gat'),
 (29,39,groen(29,39),'groen 61 (zwart 40)'),
 (33,38,groen(33,38),'groen 81 (zwart 24)'),
 (28,37,2,'linkerrand 18/32: a'),(28,38,2,'linkerrand 21/23 (a >= zwart; a voorkomt a/#/a om en om)'),(28,39,2,'linkerrand 21/46: a'),
 (31,41,2,'onderrand 8/26 (groen 58): de modellijn van de onderrand loopt door deze cel'),
 (32,41,2,'onderrand 2/31 (groen 49)'),(33,41,2,'onderrand 2/27'),
 (28,36,2,'buitenring linksboven 0/32: a, zoals linkeroog'),(29,35,2,'buitenring boven 1/33: a'),
]
for x,y,k,_ in FIX: a[y,x]=k
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(D+'r11/mate.png',transparency=0)
Z=ZO.copy()
for x,y,_,_ in FIX: Z[y,x]=True
d=a!=r10; print('buiten rechteroog anders dan r10:',int((d&~Z).sum()),'| rechteroog anders dan r10:',int((d&Z).sum()),'| afwijkend van kale reductie:',int(((a!=kaal)&Z).sum()))
print('groen r11:',int(GRN(a)[34:43,27:36].sum()),'r10:',int(GRN(r10)[34:43,27:36].sum()))
ch='.#abcdGHI'
for y in range(34,43): print(y,''.join(ch[v] for v in a[y,26:37]),''.join(ch[v] for v in kaal[y,26:37]),''.join(ch[v] for v in r10[y,26:37]))
