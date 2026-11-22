import sys,numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
BASE=sys.argv[4] if len(sys.argv)>4 else 'a2'
B2=Image.open(R+'icoon/onderdelen/'+BASE+'.png'); b2=np.array(B2); c=b2.copy()
V8=np.array(Image.open(R+'icoon/maker/icon_v8.png'))
E=[]; ZONES={}
cur=['?']
def zone(n): cur[0]=n
def put(y,x0,s):
    for i,ch in enumerate(s):
        if ch==' ': continue
        E.append((x0+i,y,0 if ch=='.' else int(ch,16),cur[0]))
exec(open(sys.argv[1]).read())
for x,y,v,z in E: c[y,x]=v
def mask(spec):
    m=np.zeros((32,32),bool)
    for (a,b),x0 in spec: m[a:b+1,x0:]=True
    return m
T1=mask([((10,16),22),((17,17),24),((18,20),25),((21,22),24),((23,24),25)])&(b2>0)
c[T1]=b2[T1]
mm=c>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)):
    if T1[y,x] or c[y,x] in (8,9,1): continue
    c[y,x]=15 if y<mid else 14
# frame 2: lijf 1 px omlaag boven rij CUT, voeten blijven; staart = v8 frame 2
CUT=int(sys.argv[3]) if len(sys.argv)>3 else 23
nt=c.copy(); nt[T1]=0
f2=np.zeros_like(c); f2[1:CUT+1]=nt[0:CUT]; f2[CUT+1:]=nt[CUT+1:]
T2=mask([((10,16),20),((17,17),24),((18,20),25),((21,22),24)])
v2=V8[32:64]
for y in range(31):
    for x in range(32):
        if T2[y,x] and v2[y,x]: f2[y+1,x]=v2[y,x]
out=np.vstack([c,f2])
im=Image.fromarray(out,'P'); im.putpalette(B2.getpalette()); im.save(sys.argv[2],transparency=0)
im.resize((256,512),Image.NEAREST).save(sys.argv[2].replace('.png','_8x.png'),transparency=0)
d=c!=b2
from collections import Counter
zc=Counter(); 
last={}
for x,y,v,z in E: last[(x,y)]=z
for y,x in zip(*np.nonzero(d)): zc[last.get((x,y),'?')]+=1
print('anders t.o.v. b2 (frame 1):',int(d.sum()),dict(zc),'staart',int((d&T1).sum()))
print('   '+''.join(str(i%10) for i in range(32)))
for y in range(7,30):print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in c[y]),'  ',''.join('.' if v==0 else '%x'%v for v in b2[y]))
