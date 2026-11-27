# controle.py: wat is er anders dan r13 buiten de nieuwe trossen; ruimte tussen de trossen; kleuren; roodverdeling
import sys; sys.path.insert(0,'sprite_r9'); sys.path.insert(0,'sprite_r16'); import numpy as np; from PIL import Image; from hulp import *
import bouw16 as B
o=np.array(Image.open('sprite_r16/guarana2_r16.png')).astype(int); o13=np.array(Image.open('sprite_r13/guarana2_r13.png')).astype(int)
oud=B.oude_tros(o13); M={}
for n,(sp,sr,dx,dy) in B.INSTEL.items():
    M[n]=set()
    for f in B.tros(n,sp,sr,dx,dy): M[n]|=f['F']
tros=np.zeros((64,64),bool)
for s in M.values():
    for x,y in s: tros[y,x]=True
d=(o!=o13)
print('anders dan r13:',int(d.sum()),'| waarvan nieuwe tros:',int((d&tros).sum()),'| oude tros die achtergrond werd:',int((d&~tros&oud&(o==0)).sum()),
      '| gaatjes gevuld:',int((d&~tros&oud&(o!=0)).sum()),'| groen/liaan anders buiten tros en oude tros:',int((d&~tros&~oud).sum()))
print('groen afgedekt door tros:',int((tros&np.isin(o13,B.GROEN)).sum()),'px; zwart van liaan/blad afgedekt:',int((tros&(o13==1)&~oud).sum()))
def dist(a,b):
    return min(max(abs(x1-x2),abs(y1-y2)) for x1,y1 in a for x2,y2 in b)
print('kleinste afstand (Chebyshev) L-M',dist(M['L'],M['M']),'M-R',dist(M['M'],M['R']),'L-R',dist(M['L'],M['R']))
ys,xs=np.where(o>0); print('kader x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'| kleuren',sorted(set(o.flatten().tolist())))
c=[(o==k).sum() for k in (2,3,4,5)]; t=sum(c); print('rood L/S/M/H %',[round(100*v/t,1) for v in c],'van',t,'px')
