# Randanalyse per richting: welke omlijningskleur waar (alleen lezen)
import numpy as np, sys
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'
p=sys.argv[1] if len(sys.argv)>1 else R+'docs/concept/sprites/nachtaap_evo/kleur/ronde14/nachtaap.png'
a=np.array(Image.open(p).convert('P') if False else Image.open(p))
if a.ndim==3: a=a[:,:,0]
a=a[:64,:64]; op=a>0; H,W=a.shape
def t(x,y): return not(0<=x<W and 0<=y<H) or not op[y,x]
res={}
for y in range(H):
  for x in range(W):
    if not op[y,x]: continue
    side=[]
    if t(x-1,y) or t(x,y-1): side.append('lichtkant(L/B)')
    if t(x+1,y) or t(x,y+1): side.append('schaduwkant(R/O)')
    for s in side: res.setdefault(s,{}).setdefault(int(a[y,x]),[]).append((x,y))
for s in res:
  print(s,{k:len(v) for k,v in sorted(res[s].items())})
if len(sys.argv)<2:
  sk=res['schaduwkant(R/O)']
  print('schaduwkant, niet zwart:',{k:v for k,v in sk.items() if k!=1})
  print('lichtkant zwart:',res['lichtkant(L/B)'].get(1))
