# check.py: kleurtelling, kleine clusters (<3, 4-buren, geen K/n), losse K/n binnenin, afwijking per zone t.o.v. de kale reductie
import numpy as np, sys; from pal import *
f=sys.argv[1] if len(sys.argv)>1 else 'rufflet_r1.txt'
g=lees(f); k=lees('kaal.txt'); H,W=g.shape
print('silhouet t.o.v. kale reductie: px verschil =',int(((g!='.')!=(k!='.')).sum()), [ (y,x) for y,x in zip(*np.where((g!='.')!=(k!='.')))])
print('kleuren:',''.join(sorted(set(g.ravel())-{'.'})),len(set(g.ravel())-{'.'}))
seen=np.zeros((H,W),bool); klein=[]
for y in range(H):
  for x in range(W):
    if seen[y,x] or g[y,x]=='.': continue
    c=g[y,x]; st=[(y,x)]; seen[y,x]=1; cl=[]
    while st:
      p=st.pop(); cl.append(p)
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        q=(p[0]+dy,p[1]+dx)
        if 0<=q[0]<H and 0<=q[1]<W and not seen[q] and g[q]==c: seen[q]=1; st.append(q)
    if len(cl)<3 and c not in 'Kn': klein.append((c,cl))
print('clusters <3 px (geen K/n):',len(klein)); print(' ',klein)
# zones
Z={}
for y in range(H):
  for x in range(W):
    if g[y,x]=='.' and k[y,x]=='.': continue
    if y<=17 and x<=11 and y>=9: z='snavel/masker/oog' 
    elif y<=17: z='kuif/kop'
    elif y>=36 or (y>=35 and 11<=x<=24 and g[y,x] in 'yedKn.'): z='poten/klauwen'
    elif x<=8 or (x<=10 and y>=29 and g[y,x] in 'cbanK'): z='verre vleugel'
    elif x>=17 and g[y,x] not in 'Wwvu' or x>=24: z='nabije vleugel/staart'
    else: z='borst/buik'
    Z.setdefault(z,[0,0]); Z[z][1]+=1
    if g[y,x]!=k[y,x]: Z[z][0]+=1
tot=sum(v[0] for v in Z.values()); n=sum(v[1] for v in Z.values())
for z,(d,m) in Z.items(): print(f'{z:24s} {d:4d} / {m}')
print('totaal afwijkend van kale reductie:',tot,'/',n,'(%.0f%%)'%(100*tot/n))
