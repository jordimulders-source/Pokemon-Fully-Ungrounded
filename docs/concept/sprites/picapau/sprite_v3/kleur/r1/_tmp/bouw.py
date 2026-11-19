from PIL import Image
import numpy as np
src=Image.open('../../r17/picapau.png'); a=np.array(src); PAL=src.getpalette()
b=a.copy()
Lc,M,Dk,D,Z=2,3,4,13,1
# --- linker lijfrand: 1 px selout (D) i.p.v. zwart + D-binnenrand
for (x,y) in [(17,39),(16,40)]+[(16,y) for y in range(41,47)]+[(17,47),(17,48)]:
    assert a[y,x] in (Z,D); b[y,x]=D
for (x,y) in [(18,39),(17,40),(18,40)]+[(17,y) for y in range(41,47)]:
    assert a[y,x]==D; b[y,x]=M
# --- kop: per rij (x0,x1,kleur) op gele pixels
kop={
 18:[(26,26,Lc),(27,27,M)],
 19:[(26,26,Lc)],
 20:[(25,25,Lc),(26,26,M)],
 21:[(25,27,M)],
 22:[(24,28,Lc),(29,30,M)],
 23:[(20,27,Lc),(28,29,M),(30,30,Dk)],
 24:[(19,27,Lc),(28,29,M),(30,31,Dk)],
 25:[(18,26,Lc),(27,28,M),(29,31,Dk)],
 26:[(18,25,Lc),(26,28,M),(29,32,Dk)],
 27:[(17,24,Lc),(28,29,M),(30,32,Dk)],
 28:[(18,23,Lc),(29,29,M),(30,32,Dk)],
 29:[(19,23,Lc),(29,30,M),(31,33,Dk)],
 30:[(20,22,Lc),(23,23,M),(29,30,M),(31,32,Dk)],
 31:[(21,22,Lc),(23,24,M),(28,29,M),(30,32,Dk)],
 32:[(22,29,M),(30,32,Dk)],
 33:[(22,24,M),(28,29,M),(30,32,Dk)],
 34:[(17,17,M),(21,23,M),(29,29,M),(30,32,Dk)],
 35:[(17,23,M),(29,33,Dk)],
 36:[(17,23,M),(29,31,Dk)],
 37:[(18,18,Dk),(19,24,M),(28,31,Dk)],
 38:[(19,30,Dk)],
}
for y,segs in kop.items():
    for x0,x1,c in segs:
        for x in range(x0,x1+1):
            assert a[y,x] in (2,3,4),(x,y,a[y,x]); b[y,x]=c
# --- lijf: ellipsoide
L=np.array([-0.55,-0.75,0.45]); L/=np.linalg.norm(L)
cx,cy,rx,ry=27.0,46.5,11.5,9.0
for y in range(39,56):
    for x in range(64):
        if b[y,x] not in (2,3,4): continue
        u=(x-cx)/rx; v=(y-cy)/ry; nz=np.sqrt(max(0.,1-u*u-v*v)); n=np.array([u,v,nz]); n/=np.linalg.norm(n)
        i=n@L
        b[y,x]=Lc if i>0.80 else (M if i>0.30 else Dk)
        if y==39 and b[y,x]==Lc: b[y,x]=M
np.save('_tmp/b.npy',b)
p=Image.fromarray(b,'P'); p.putpalette(PAL); p.save('_tmp/b.png',transparency=0)
for y in range(12,63): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in b[y,14:49]))
