# Afwijking van de onderlaag per zone: stapA = onderlaag op het oude palet (zone + toon per pixel);
# telt per zone hoeveel pixels de sprite anders heeft, uitgesplitst naar stap (buitenlijn/binnenlijn, ruis, reparatie).
import numpy as np; from PIL import Image
A=np.load('stapA.npy'); B=np.load('stapB.npy'); R=np.load('stapR.npy'); zone=np.load('zone_t.npy'); H,W=A.shape
ond=np.asarray(Image.open('../onderlaag.png'))[...,3]>0
print('silhouet: pixels anders dan onderlaag =',int(((R>0)!=ond).sum()))
def regio(y,x):
    z=zone[y,x]
    if z in 'TP': return 'oren+kwastjes'
    if z=='G' or (z=='C' and y>=30): return 'handschoenen+manchetten'
    if z=='C': return 'kraag'
    if z=='E' or (y<=19 and x<=17): return 'kop+gezicht'
    if z=='D': return 'verre achterpoot'
    if y>=36 or (y>=33 and x>=24): return 'poten'
    if x>=22 and y<=27: return 'staart'
    return 'hals+lijf'
from collections import defaultdict
t=defaultdict(lambda:[0,0,0,0])
for y in range(H):
  for x in range(W):
    if not ond[y,x]: continue
    r=regio(y,x); t[r][0]+=1
    if B[y,x]!=A[y,x]: t[r][1]+=1
    if R[y,x]!=B[y,x]: t[r][2]+=1
    if R[y,x]!=A[y,x]: t[r][3]+=1
print('%-26s %5s %8s %10s %8s'%('zone','px','opschoon','reparatie','totaal'))
for r,v in sorted(t.items()): print('%-26s %5d %8d %10d %8d'%(r,*v))
tot=np.array(list(t.values())).sum(0); print('%-26s %5d %8d %10d %8d'%('TOTAAL',*tot))
im=Image.open('../palpaca.png'); a=np.array(im); print('kleuren gebruikt (excl. 0):',len(set(a[a>0].ravel())),'| formaat',im.size,im.mode)
ys,xs=np.nonzero(a); print('wezen: %d breed x %d hoog, x %d-%d, y %d-%d'%(xs.max()-xs.min()+1,ys.max()-ys.min()+1,xs.min(),xs.max(),ys.min(),ys.max()))
