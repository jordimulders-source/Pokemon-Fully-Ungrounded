# r5: Jordi's vleugellijn (21 px, plek vast) netjes afgewerkt op r1/frame2.png. Basis = variant A (index 11),
# Jordi: "A is een goede basis, maar moeten meer tinten". Licht linksboven: bovenrand lichter (4, taps 12),
# rechterrand tegen de donkere staart donker (3), daaronder 11 en naar het einde 4 -> 12 (taps).
# Binnen de lijn (1 px) waar e tegen de donkere lijn ligt: d als zachte schaduw.
# (a) pixels rechts van de lijn ongewijzigd; (b) die lichte pixels (y17-21) transparant = kier uit het model, staartrand dicht.
import numpy as np; from PIL import Image
pal=[tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[3:19]]
r1=np.array(Image.open('../r1/frame2.png')).astype(int)
LIJN=[(45,9),(46,9),(44,10),(47,10),(48,10),(43,11),(48,11),(49,11),(42,12),(48,12),(48,13),(47,14),(46,15),(46,16),(46,17),(45,18),(46,18),(45,19),(45,20),(44,21),(43,22)]
# Jordi: "het moet heel subtiel kleurgebruik zijn, zodat die in een gif niet gek eruit ziet" -> niet harder dan de
# vleugelrand in frame 1 (die is c=12, met 4 als vleugellijn): lijn in 12/4, alleen tegen de donkere staart 11; geen 3/1.
A={(42,12):(12,'begin, taps: c zoals de vleugelrand van frame 1'),
   (43,11):(12,'bovenkant (lichtkant): c'),
   (44,10):(12,'bovenkant: c'),
   (45,9):(12,'bovenkant, top van de bult: c'),
   (46,9):(12,'bovenkant: c'),
   (47,10):(4,'hoek rechtsboven, overgang naar schaduwkant: 4'),
   (48,10):(4,'hoek: 4'),
   (48,11):(4,'rechterkant: 4'),
   (49,11):(4,'buitenste hoekpixel: 4'),
   (48,12):(11,'tegen de donkere staart: een tint donkerder, 11 (basis A)'),
   (48,13):(11,'tegen de staart: 11'),
   (47,14):(4,'staart wijkt: 4'),
   (46,15):(4,'rechterkant (schaduwkant): 4'),
   (46,16):(4,'rechterkant: 4'),
   (46,17):(4,'rechterkant: 4'),
   (46,18):(4,'buitenste van het dubbele stuk: 4'),
   (45,18):(12,'binnenste van het dubbele stuk: c (lijn dunner)'),
   (45,19):(4,'onderloop: 4'),
   (45,20):(4,'onderloop: 4 (was al 4)'),
   (44,21):(12,'einde taps: c'),
   (43,22):(12,'einde taps: c (was al c)')}
BINNEN={(47,12):(13,'1 px binnen de lijn naast 11: e -> d, zachte schaduw (frame 1 heeft d-banden in deze vleugel)'),
        (47,13):(13,'idem')}
def bouw(variant):
    a=r1.copy(); log=[]
    regels=dict(A)
    if variant=='b':   # rechts van de lijn wordt kier: lijn is daar buitenrand aan de schaduwkant -> donkerder
        regels.update({(44,21):(4,'b: buitenrand naar de kier: 4, taps naar c op (43,22)')})
    for (x,y),(v,r) in list(regels.items())+list(BINNEN.items()):
        if a[y,x]!=v: log.append((x,y,int(a[y,x]),v,r)); a[y,x]=v
    if variant=='b':
        Y,X=np.mgrid[0:64,0:64]
        kier=(Y>=17)&(Y<=21)&(X>=46)&(X<=50)&np.isin(r1,[4,11,12,13,14])
        for x,y in LIJN: kier[y,x]=False
        for y,x in zip(*np.where(kier)): log.append((int(x),int(y),int(a[y,x]),0,'b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)')); a[y,x]=0
        for x,y in [(51,18),(51,19),(51,20),(51,21)]:   # staartrand aan de kier dicht
            if a[y,x]==5: log.append((x,y,5,2,'b: staartrand aan de kier dicht: 5 -> 2 (donkere rand)')); a[y,x]=2
    return a,log
ZONE=np.zeros((64,64),bool); ZONE[8:24,41:53]=True
for v in 'ab':
    a,log=bouw(v); d=a!=r1; assert not (d&~ZONE).any(); assert ((a>0)!=(r1>0)).sum()==sum(1 for l in log if l[3]==0)
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(pal,())); im.save(f'frame2_{v}.png',transparency=0)
    f1=np.array(Image.open('frame1.png')); an=Image.fromarray(np.vstack([f1,a]).astype('uint8'),'P'); an.putpalette(sum(pal,())); an.save(f'anim_front_{v}.png',transparency=0)
    with open(f'log_{v}.txt','w') as f:
        f.write(f'variant {v}: {int(d.sum())} px gewijzigd t.o.v. r1/frame2.png, buiten zone x41-52 y8-23: {int((d&~ZONE).sum())}\n')
        for l in sorted(log,key=lambda t:(t[1],t[0])): f.write('(%d,%d) %d -> %d  %s\n'%l)
    print(open(f'log_{v}.txt').readline().strip())
