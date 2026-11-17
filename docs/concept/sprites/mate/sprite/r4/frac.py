# frac.py x0 y0 x1 y1 : per spritepixel in het model: zwartfractie (0-9) en groenfractie (0-9) en helderheid
import sys; sys.path.insert(0,'r4')
import numpy as np
from meet import crop
from PIL import Image
N=8; A=np.asarray(crop.resize((64*N,64*N),Image.BOX)).astype(int)
R,G,B=A[...,0],A[...,1],A[...,2]; L=0.299*R+0.587*G+0.114*B
TB=float(sys.argv[6]) if len(sys.argv)>6 else 40; blk=L<TB; grn=(G>R+6)&(G>B)&~blk; wit=A.min(-1)>=225; gry=(A.max(-1)-A.min(-1)<22)&(L>=60)&~wit
def f(m): return m.reshape(64,N,64,N).mean((1,3))
fb,fg,fw,fs=f(blk),f(grn),f(wit),f(gry); Lm=L.reshape(64,N,64,N).mean((1,3))
x0,y0,x1,y1=map(int,sys.argv[1:5]); what=sys.argv[5] if len(sys.argv)>5 else 'bg'
hdr='   '+''.join(str(x%10) for x in range(x0,x1+1))
for nm,F in (('zwart',fb),('groen',fg),('zilver',fs),('wit',fw)):
    if nm[0] not in what: continue
    print(nm); print(hdr)
    for y in range(y0,y1+1): print('%2d '%y+''.join(('%d'%min(9,int(F[y,x]*10)) if F[y,x]>=0.05 else '.') for x in range(x0,x1+1)))
if 'l' in what:
    print('helderheid/10'); print(hdr)
    for y in range(y0,y1+1): print('%2d '%y+''.join('%x'%min(15,int(Lm[y,x]/16)) for x in range(x0,x1+1)))
