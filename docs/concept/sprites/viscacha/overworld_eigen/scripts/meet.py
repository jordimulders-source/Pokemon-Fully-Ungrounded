"""Controle van af/overworld.png tegen de eisen (OW-meetstudie): maat, onderkant, midden, symmetrie, kleuren,
omlijning, losse pixels, loopframes. Gebruik (repo-root): python3 .../scripts/meet.py"""
import sys,os,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H); from ow_pal import PAL
o=np.array(Image.open(H+'/../af/overworld.png')); print('formaat',o.shape[::-1],Image.open(H+'/../af/overworld.png').mode)
F=[o[:,k*32:k*32+32] for k in range(6)]
lum=lambda c:0.299*c[0]+0.587*c[1]+0.114*c[2]
fronth=49
for k,n in [(0,'voor'),(2,'achter'),(4,'opzij')]:
    a=F[k]; ys,xs=np.nonzero(a); h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1
    m=a>0; sym=(m&m[:,::-1]).sum()/max(m.sum(),1)
    # symmetrie om het eigen midden
    c=xs.min()+xs.max(); mm=np.zeros_like(m)
    for y,x in zip(ys,xs):
        x2=c-x
        if 0<=x2<32: mm[y,x2]=True
    sym=(m&mm).sum()/m.sum()
    pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    top=[lum(PAL[a[y,x]]) for y,x in zip(*np.nonzero(edge)) if y==0 or a[y-1,x]==0]
    bot=[lum(PAL[a[y,x]]) for y,x in zip(*np.nonzero(edge)) if y==31 or a[y+1,x]==0]
    # losse pixels: een kleur zonder 4-buur van dezelfde kleur (behalve omlijning 1/2/3 en glans e)
    los=[]
    for y,x in zip(ys,xs):
        v=a[y,x]
        if v in (1,2,3,14,15): continue
        if not any(0<=y+dy<32 and 0<=x+dx<32 and a[y+dy,x+dx]==v for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): los.append((x,y,'%x'%v))
    d=(F[k]!=F[k+1]).sum()
    ys2,xs2=np.nonzero(F[k+1])
    print(f'{n}: h {h} ({h/fronth:.2f}x front) b {w}  y {ys.min()}-{ys.max()}  midden x {(xs.min()+xs.max())/2}  silhouet-symmetrie {sym:.0%}  '
          f'kleuren {len(np.unique(a[a>0]))}  rand boven {np.median(top):.0f} onder {np.median(bot):.0f}  '
          f'loopframe: {d} px anders, bovenkant {ys2.min()} hoogte {ys2.max()-ys2.min()+1}')
    print('   eenlingen (kleur zonder gelijke buur):',los)
print('kleuren totaal',len(np.unique(o[o>0])))
