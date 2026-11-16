import numpy as np
from gio import from_txt, to_txt, CH
from r2_ijs import IJS2, OGEN, GLOED
I={c:k for k,c in enumerate(CH)}
G=from_txt('r2_stapA.txt'); m=np.load('mask_r1.npy')
for y,(x0,s) in IJS2.items():
    for k,c in enumerate(s): G[y,x0+k]=I[c]
# ogen: eerst oude oogpixels terug naar ijs (W), dan nieuwe ogen + gloed (g)
for y in range(31,39):
    for x in range(3,19):
        if CH[G[y,x]] in 'rcC': G[y,x]=I['W']
for e in OGEN.values():
    for y,(x0,s) in e.items():
        for k,c in enumerate(s): G[y,x0+k]=I[c]
for x,y in GLOED: G[y,x]=I['g']
# nevel: één ronde gloed v -> n -> j rond (24.5,35), losse v-kolom weg; ster (26,30) blijft
for y in range(27,40):
    for x in range(21,33):
        if CH[G[y,x]] in 'nvj':
            d=((x-24.5)**2+((y-35)*1.1)**2)**0.5
            G[y,x]=I['v'] if d<=2.3 else (I['n'] if d<=4.6 else I['j'])
G[30,26]=I['v']
# rechte kopkant tegen de nevel: gekleurde selout S i.p.v. zwart
for y in range(26,39):
    for x in (20,21,22):
        if CH[G[y,x]]=='K' and CH[G[y,x+1]] in 'nvj': G[y,x]=I['S']
for x,y,c in [(4,33,'S'),(50,8,'W'),(9,51,'M'),(23,39,'K')]: G[y,x]=I[c]
to_txt(G,'r2.txt')
print('alpha-diff',int(((G>=0)!=m).sum()))
