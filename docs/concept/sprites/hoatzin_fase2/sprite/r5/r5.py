# Hoatzin r5: alleen benoemde pixels op r4 (canvascoördinaten x,y), elke wijziging gemeten/gelogd; rest pixeldiff 0
import numpy as np; from PIL import Image
im=Image.open('r4.png'); pal=im.getpalette()[:48]; A=np.asarray(im).copy(); S=A.copy()
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); L=N.mean(2); Z=np.load('zones_nat.npy')
ys,xs=np.where(Z!='.'); x0,y0=xs.min(),ys.min(); s=(ys.max()+1-y0)/63
def gem(x,y):
    a=y0+(y-1)*s; b=x0+(x-6)*s; blk=L[int(a):int(np.ceil(a+s)),int(b):int(np.ceil(b+s))]; zb=Z[int(a):int(np.ceil(a+s)),int(b):int(np.ceil(b+s))]
    return blk[zb!='.'].mean()
def med(x,y):
    a=y0+(y-1)*s; b=x0+(x-6)*s; blk=L[int(a):int(np.ceil(a+s)),int(b):int(np.ceil(b+s))]; zb=Z[int(a):int(np.ceil(a+s)),int(b):int(np.ceil(b+s))]
    return np.median(blk[zb!='.'])
log=[]
def zet(x,y,v,why):
    if S[y,x]!=v: log.append((why,x,y,int(S[y,x]),v)); S[y,x]=v
# 1. donkere streep borst/vleugel: x22-23, y28-36, model < 30 -> toon 2
for y in range(28,37):
    for x in (22,23):
        if med(x,y)<30 and S[y,x] not in (1,2): zet(x,y,2,'1 streep model mediaan<30 (px.py)')
# 2. oog volgens de meting (R-B per cel): pupil x12 y21-22, iris rood (11,22),(13,21),(13,22); (11,21) en (12,23) blauw 9
zet(11,21,9,'2 oog: blauw (model R-B -42)')
zet(12,21,1,'2 oog: pupil'); zet(12,22,1,'2 oog: pupil')
for x,y in ((11,22),(13,21),(13,22)): zet(x,y,10,'2 oog: iris (model roze)')
zet(12,23,9,'2 oog: blauw (model R-B -68)')
# 3. selout linkerrand buik x16-17, y38-46: één toon 3 (alleen randpixels)
for y in range(38,47):
    for x in (16,17):
        if S[y,x]>0 and (S[y,x-1]==0) and S[y,x] in (1,2,3,11): zet(x,y,3,'3 selout buik één toon')
# 4. bovenrand buik y37: zijpixels toon 4 (modelcurve: 100/102 links, 108 rechts lager dan het midden 111-112)
zet(18,37,4,'4 bovenrand buik rond'); zet(22,37,4,'4 bovenrand buik rond')
# 5a. tenen: paarse pixels -> 1 (model < 50) of 14
for x,y in ((22,55),(18,56),(20,57),(17,58)): zet(x,y,1 if gem(x,y)<50 else 14,'5 tenen (model %d)'%gem(x,y))
# 5b. staartlijn 1 px: per rij in het dubbele stuk de rechterpixel houden
for y,(xa,xb) in {49:(42,43),50:(43,44),51:(44,45),53:(45,46),54:(46,47),55:(47,48)}.items():
    if S[y,xa]==1 and S[y,xb]==1: zet(xa,y,2,'5 staartlijn 1 px')
# 5c. blauw gezicht achter/onderrand x15-16 y19-22: toon 8 waar het model donker is (< 70)
for y in range(19,23):
    for x in (15,16):
        if S[y,x]==9 and gem(x,y)<70: zet(x,y,8,'5 gezicht achterrand donker (model %d)'%gem(x,y))
p=Image.fromarray(S,'P'); p.putpalette(pal); p.save('hoatzin.png',transparency=0)
open('normal.pal','w').write(open('../r4/normal.pal').read())
for r in log: print(r)
print('pixeldiff t.o.v. r4:',int((S!=A).sum()),' silhouetdiff:',int(((S>0)!=(A>0)).sum()))
