import sys, numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/icoon/onderdelen/'
B=Image.open(R+'icon_a2_af.png'); b=np.array(B)
spec=sys.argv[1]; out=sys.argv[2]
# spec: lines "yy xx|chars" region rows for frame 0, x from 0; '.'=transparent, ' '=keep
f0=b[:32].copy()
F2EXTRA=[]
for line in open(spec):
    line=line.rstrip('\n')
    if not line.strip() or line.startswith('#'): continue
    if line.startswith('F2 '):  # frame2 extra: F2 y x chars
        _,y,x,s=line.split(' ',3); F2EXTRA.append((int(y),int(x),s)); continue
    y=int(line[:2]); s=line[3:]
    for x,ch in enumerate(s):
        if ch==' ': continue
        f0[y,x]=0 if ch=='.' else int(ch,16)
d0=f0!=b[:32]
f2=b[32:].copy()
for y,x in zip(*np.nonzero(d0)):
    if y<=22: f2[y+1,x]=f0[y,x]
    elif y>=24: f2[y,x]=f0[y,x]
for y,x,s in F2EXTRA:
    for i,ch in enumerate(s):
        if ch==' ': continue
        f2[y,x+i]=0 if ch=='.' else int(ch,16)
out_a=np.vstack([f0,f2])
im=Image.fromarray(out_a,'P'); im.putpalette(B.getpalette()); im.save(out,transparency=0)
im.resize((256,512),Image.NEAREST).save(out.replace('.png','_8x.png'),transparency=0)
d=out_a!=b
print('changed f0',int(d0.sum()),'f2',int(d[32:].sum()))
print('   '+''.join(str(i%10) for i in range(32)))
for y in range(6,30): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in f0[y]),'  ','%2d '%y+''.join('.' if v==0 else '%X'%v for v in f2[y]))
