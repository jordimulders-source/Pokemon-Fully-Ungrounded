from lib import *
import numpy as np, sys
s=Sprite('alpaca/ronde16')          # ronde 16 (vuist + rug) als basis
f1=s.old[:64].copy()
n=f1.copy()
# kop (y4-21) en kaakrij (y22) 2 px naar links
n[4:23,:]=0; n[4:23,0:62]=f1[4:23,2:64]
def row(y,x0,txt):
    n[y,10:32]=np.where(np.arange(10,32)>=0,0,0) if y!=22 else n[y,10:32]
    for i,ch in enumerate(txt): n[y,x0+i]=0 if ch=='.' else int(ch,16)
# hals schuin naar voren en taps (boven 6 breed, onder 9 breed)
n[22,21:32]=0
for i,ch in enumerate('2333441'): n[22,21+i]=int(ch)
for y,x0,t in [(23,20,'62333441'),(24,20,'622333441'),(25,21,'622333441'.replace('622333441','623333441'))]:
    n[y,10:32]=0; row(y,x0,t)
# y26 blijft; y27 aan de rugkant 1 px breder
assert n[27,30]==1 and n[27,31]==0
n[27,30]=4; n[27,31]=1
s.a[:64]=n
f2=n.copy(); f2[5:24]=n[4:23]; f2[4]=0
s.a[64:]=f2
d=s.save(sys.argv[1]); print(report(d))
