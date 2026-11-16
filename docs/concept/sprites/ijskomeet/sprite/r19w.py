# r19: ontkorrelen. Korrel = 8-verbonden vlekje van <= MAX px in een vulkleur; krijgt de meest voorkomende vulkleur van zijn buren (zelfde groep).
# Diagonale lijntjes/facetten (8-verbonden, >= 3 px) blijven; lijnkleuren (K,S,N), ogen en silhouet blijven.
import sys, numpy as np; from PIL import Image
from collections import deque, Counter
MAXP=int(sys.argv[1]) if len(sys.argv)>1 else 2
im=Image.open('r18.png'); pal=im.getpalette(); o=np.array(im).copy(); vap=np.load('r15w/vap.npy')
ICE={2,3,4,5}; PUR={7,8,9,10}; GAS={2,3,11,15}
def grp(y,x):
  c=o[y,x]
  if vap[y,x]: return GAS if c in GAS else None
  if c in ICE: return ICE
  if c in PUR: return PUR
  return None
tot=0
for it in range(3):
  seen=np.zeros((64,64),bool); n=0
  for y in range(64):
    for x in range(64):
      g=grp(y,x)
      if seen[y,x] or g is None: continue
      c=o[y,x]; q=deque([(y,x)]); seen[y,x]=True; cl=[]
      while q:
        cy,cx=q.popleft(); cl.append((cy,cx))
        for dy in(-1,0,1):
          for dx in(-1,0,1):
            ny,nx=cy+dy,cx+dx
            if 0<=ny<64 and 0<=nx<64 and not seen[ny,nx] and o[ny,nx]==c and vap[ny,nx]==vap[y,x]: seen[ny,nx]=True; q.append((ny,nx))
      ys_=[p[0] for p in cl]; xs_=[p[1] for p in cl]; h=max(ys_)-min(ys_)+1; w=max(xs_)-min(xs_)+1
      lijnig=max(h,w)>=3 and len(cl)<=max(h,w)+1   # dun en langwerpig = facetlijntje: blijft
      lim=5 if g is ICE else MAXP
      if len(cl)>lim or (len(cl)>2 and lijnig): continue
      nb=Counter()
      for cy,cx in cl:
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
          ny,nx=cy+dy,cx+dx
          if 0<=ny<64 and 0<=nx<64 and o[ny,nx]!=c and o[ny,nx] in g and vap[ny,nx]==vap[y,x]: nb[o[ny,nx]]+=1
      if nb:
        t=nb.most_common(1)[0][0]
        for cy,cx in cl: o[cy,cx]=t
        n+=len(cl)
  tot+=n
  if not n: break
a=np.array(im); assert ((np.isin(a,[1,6,13,12,14]))==(np.isin(o,[1,6,13,12,14]))).all()
print('pixels',tot)
out=Image.fromarray(o).convert('P'); out.putpalette(pal); out.save('r19.png',transparency=0)
x8=out.convert('RGB').resize((512,512),Image.NEAREST); x8.save('r19_8x.png')
b=Image.open('r18.png').convert('RGB').resize((512,512),Image.NEAREST); m=Image.open('vel_r9.png').crop((1060,0,1590,520))
v=Image.new('RGB',(1600,700),'white'); v.paste(x8,(0,8)); v.paste(b,(530,8)); v.paste(m,(1060,0))
for k,f in enumerate(['r19.png','r18.png']):
  s=Image.open(f).convert('RGB'); v.paste(s,(20+k*300,560)); v.paste(s.resize((128,128),Image.NEAREST),(100+k*300,560))
v.save('voor_jordi_r19.png')
