# Ronde 13: basis r12. Want (x10-16, y40-51) en onderrand rechteroog (x29-34, y41-42) uit de kale reductie van de
# keurder (scratchpad/k11/kaal.png, fit x163-859 -> 11-50, y82-941 -> 15-62), als geheel geplakt; daarna alleen randen.
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/'
K='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f952c4af-e06e-5b56-87d5-86ed60c9233c/scratchpad/k11/kaal.png'
im=Image.open(D+'r12/mate.png'); PAL=im.getpalette(); r12=np.asarray(im).astype(int)
k=np.asarray(Image.open(K)).astype(int)
Y,X=np.mgrid[0:64,0:64]
ZH=(X>=10)&(X<=16)&(Y>=40)&(Y<=51); ZO=(X>=29)&(X<=34)&(Y>=41)&(Y<=42)
a=r12.copy(); a[ZH]=k[ZH]; a[ZO]=k[ZO]; kaal=a.copy()
C={'.':0,'#':1,'a':2}
FIX=[
 (14,40,'#','open rand links/boven; aansluiting op lijfrand (14,39) en model zwart 48-77% (r8-meting)'),
 (14,41,'#','open rand links (enkele rand, geen dubbele meer)'),
 (12,42,'a','open rand linksboven (lichtzijde: selout)'),(13,42,'a','open rand boven'),
 (12,43,'a','open rand links'),(11,44,'a','open rand links'),(11,45,'a','open rand links'),(11,46,'a','open rand links'),
 (11,47,'#','open rand linksonder: zwarte onderboog (schaduwzijde; model zwart, r8-meting)'),
 (12,48,'#','onderboog'),(13,49,'#','onderboog'),(14,49,'#','onderboog'),
]
for x,y,c,_ in FIX: a[y,x]=C[c]
# Besluit rechteroog: groen eindigt op y40, y41 x30-32 lichtbruine rand (d) zoals in het model; y42 blijft kaal.png
OOG=[(30,41,5),(31,41,5),(32,41,5)]
for x,y,c in OOG: a[y,x]=c
# Jordi: "links en rechts onderin kan misschien nog iets smoother rond". Buitenlijn op de omtrek van kaal.png (+-1 px),
# trapjes regelmatig gemaakt; tint die binnen de oude rand lag schuift mee (b = schaduwtint ernaast).
B=3
RAND=[ # linksonder: verticale runs x16:2, x17:1, x18:1, daarna horizontaal y55:2, y56:2, y57:4 (kaal-rand x16,16,17,18,19)
 (16,51,1),(17,51,B),(16,52,1),(17,52,B),(18,54,1),(19,54,B),(19,55,1),(21,55,B),
 # rechtsonder: verticale runs x50:3, x49:3, x48:2, x47:1, x46:1, x45:1, horizontaal y55:2, y56:3 (kaal-rand 49,49,48,47,46,46,45,43,42)
 (48,48,B),(49,48,1),(48,49,B),(49,49,1),(47,50,B),(48,50,1),(47,51,1),(48,51,1),
 (45,52,B),(46,52,B),(47,52,1),(44,53,B),(45,53,B),(46,53,1),(43,54,B),(44,54,B),(45,54,1),
 (42,55,B),(43,55,1),(44,55,1),(42,56,1),
]
for x,y,c in RAND: a[y,x]=c
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(D+'r13/mate.png',transparency=0)
ZR=np.zeros((64,64),bool)
for x,y,_ in RAND: ZR[y,x]=True
ZO2=ZO.copy()
d=a!=r12; print('onderhoeken gewijzigd t.o.v. r12:',int((d&ZR).sum()),'| oog t.o.v. kaal.png:',int(((a!=k)&ZO).sum())); ZH=ZH|ZR
print('buiten de zones anders dan r12:',int((d&~(ZH|ZO)).sum()),'| want anders dan r12:',int((d&ZH).sum()),
 'afwijkend van kaal.png:',int(((a!=k)&ZH).sum()),'| oog anders dan r12:',int((d&ZO).sum()),'afwijkend van kaal.png:',int(((a!=k)&ZO).sum()))
ch='.#abcdGHIstu'
for y in range(46,58): print(y,''.join(ch[v] for v in a[y,11:24]),'  ',''.join(ch[v] for v in a[y,36:52]))
if 0:
 for y in range(38,54): print(y,''.join(ch[v] for v in a[y,8:19]),' ',''.join(ch[v] for v in r12[y,8:19]))
for y in range(39,43): print(y,''.join(ch[v] for v in a[y,27:36]),' ',''.join(ch[v] for v in r12[y,27:36]))
