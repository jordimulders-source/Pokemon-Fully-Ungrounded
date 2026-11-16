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
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(D+'r13/mate.png',transparency=0)
d=a!=r12; print('buiten de zones anders dan r12:',int((d&~(ZH|ZO)).sum()),'| want anders dan r12:',int((d&ZH).sum()),
 'afwijkend van kaal.png:',int(((a!=k)&ZH).sum()),'| oog anders dan r12:',int((d&ZO).sum()),'afwijkend van kaal.png:',int(((a!=k)&ZO).sum()))
ch='.#abcdGHIstu'
for y in range(38,54): print(y,''.join(ch[v] for v in a[y,8:19]),' ',''.join(ch[v] for v in r12[y,8:19]))
for y in range(39,44): print(y,''.join(ch[v] for v in a[y,27:36]),' ',''.join(ch[v] for v in r12[y,27:36]))
