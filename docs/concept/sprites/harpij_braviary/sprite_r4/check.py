# check.py: silhouet, bevroren delen, kleurtelling, kleine clusters, afwijking per zone t.o.v. de kale reductie
import numpy as np; from pal import *
g=lees('harpij_r4.txt'); k=lees('stap_tonen.txt'); z=lees('zones.txt'); l=np.load('lijn.npy')
r3=lees('../sprite_r3/harpij_r3b.txt'); r3c=lees('../sprite_r3/harpij_r3c.txt')
V=[tuple(p) for p in np.load('veer_mask.npy')]; O=[tuple(p) for p in np.load('oog_mask.npy')]
print('silhouet t.o.v. reductie: px verschil =',int(((g!='.')!=(l>0)).sum()))
print('2 rechtse kuifveren gelijk aan r3:',all(g[p]==r3[p] for p in V),len(V),'px; oog gelijk aan r3c:',all(g[p]==r3c[p] for p in O),len(O),'px')
print('kleuren:',sorted(set(g.ravel())-{'.'}),len(set(g.ravel())-{'.'}))
# kleine clusters (4-buren) < 3 px, behalve K-lijnen
H,W=g.shape; seen=np.zeros((H,W),bool); klein=[]
for y in range(H):
  for x in range(W):
    if seen[y,x] or g[y,x] in '.': continue
    c=g[y,x]; st=[(y,x)]; seen[y,x]=1; cl=[]
    while st:
      p=st.pop(); cl.append(p)
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        q=(p[0]+dy,p[1]+dx)
        if 0<=q[0]<H and 0<=q[1]<W and not seen[q] and g[q]==c: seen[q]=1; st.append(q)
    if len(cl)<3 and c!='K': klein.append((c,cl))
print('clusters <3 px (geen K):',len(klein)); print(' ',[(c,cl) for c,cl in klein])
# afwijking per zone
ZN={'k':'kuif','h':'kop','s':'snavel','n':'kraag','w':'vleugel/staart','b':'borst/dijen','p':'poten/voeten'}
tot=0
for zz,nm in ZN.items():
  m=(z==zz); d=int(((g!=k)&m).sum()); tot+=d; print(f'{nm:16s} {d:4d} / {int(m.sum())}')
d=(g!=k)&(g!='.'); print('totaal afwijkend van kale reductie (in r4-palet):',int(d.sum()),'/',int((g!='.').sum()))
np.save('afwijking.npy',d)
