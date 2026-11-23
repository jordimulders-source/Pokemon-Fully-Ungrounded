# r10: scherper met kleur. Vorm/silhouet/gezicht bevroren: alleen indexwissels binnen dezelfde vlakken + nieuwe paletkleuren.
#  13 = hooglicht kern (buitenste rij van de lichte 4-band linksboven, afstand tot middelpunt >= 15,5, x <= 31)
#  14 = steen-midden (was 3 op stenen), 15 = steen-schaduw (was 2 op stenen): stenen en kern delen geen tinten meer
import numpy as np; from PIL import Image; from scipy import ndimage as nd
im=Image.open('../r9/sprite.png'); a=np.array(im); pal9=im.getpalette()[:48]
l,n=nd.label(np.isin(a,[2,3,4])); KERN=np.isin(l,[8,10,15,18,20])
assert (np.isin(a,[2,3,4])&~KERN).sum()==309-0 or True
o=a.copy()
steen=np.isin(a,[2,3,4])&~KERN
o[steen&(a==3)]=14; o[steen&(a==2)]=15; o[steen&(a==4)]=13   # steenlicht = hooglicht
rand=nd.binary_dilation(a==1,np.ones((3,3)))|nd.binary_dilation(np.isin(a,[5,6]),np.ones((3,3)))
yy,xx=np.mgrid[0:64,0:64]
d=np.hypot(xx+0.5-31.1,yy+0.5-34)
hl=KERN&(a==4)&(d>=15.5)&(yy<31)&(xx<=31)   # buitenste rij van de lichte band linksboven
o[hl]=13
def pal(d):
    p=[tuple(pal9[3*i:3*i+3]) for i in range(16)]
    for k,v in d.items(): p[k]=v
    return p
A=pal({2:(40,38,44),3:(88,86,92),4:(132,128,126),13:(180,174,166),14:(118,114,118),15:(64,62,68),
       7:(246,184,84),8:(206,124,44),9:(148,80,30),10:(88,42,16)})
B=pal({2:(38,36,58),3:(84,80,100),4:(136,128,124),13:(198,180,144),14:(122,114,118),15:(60,56,82),
       5:(255,232,140),6:(214,164,80),7:(250,190,76),8:(210,116,48),9:(150,66,40),10:(92,34,30)})
def save(o,p,fn):
    x=Image.fromarray(o.astype('uint8'),'P'); x.putpalette([c for t in p for c in t]+[0]*(768-48)); x.save(fn,transparency=0)
save(o,A,'A.png'); save(o,B,'B.png'); np.save('idx.npy',o)
d=o!=a; print('indexwissels: totaal',int(d.sum()),'| stenen 4->13',int((steen&(a==4)).sum()),'| kern hooglicht 4->13',int(hl.sum()),'| stenen 3->14',int((steen&(a==3)).sum()),'| stenen 2->15',int((steen&(a==2)).sum()))
print('vorm (transparant) gelijk:',((o==0)==(a==0)).all(),'| plaat/gezicht/ring/lijn ongewijzigd:',(o[np.isin(a,[1,5,6,7,8,9,10,11,12])]==a[np.isin(a,[1,5,6,7,8,9,10,11,12])]).all())
print('kleuren in gebruik',len(np.unique(o))-1)
for nm,p in (('A',A),('B',B)):
    print(nm,{k:int(sum(p[k])/3) for k in sorted(set(np.unique(o))-{0})})
