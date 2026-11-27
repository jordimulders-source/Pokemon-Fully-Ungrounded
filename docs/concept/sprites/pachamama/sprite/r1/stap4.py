# Tintvlakjes < 3 px (niet-lijn) naar de tweede keuze uit hetzelfde modelblok, mits die een buurkleur is.
# Daarna reparaties per pixel (sneeuwtopje linkerschouder) - elk benoemd.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image; from clusters import vlakjes
a=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float); Lm=lum(a)
near=nearest(a); gr=a[...,1]-a[...,0]; g=gr<8; near[g&(near>=13)]=nearest(a[g&(near>=13)],range(2,13))
o=np.load('gezicht.npy'); lijn=np.load('lijn.npy'); oud=o.copy(); log={}
m=o>0; pd=np.pad(m,1); rand=m&~(pd[:-2,1:-1]&pd[2:,1:-1]&pd[1:-1,:-2]&pd[1:-1,2:])
gezm=np.zeros((64,64),bool); gezm[13:29,22:35]=True   # gezicht staat apart gemeten in gezicht.py
def tel(k,n=1): log[k]=log.get(k,0)+n
OOG={(18,24),(18,25),(19,24),(19,25),(18,29),(18,30),(18,31),(19,29),(19,30),(19,31)}
for it in range(3):
  for v,comp in vlakjes(o):
    if v in (5,6): continue          # sneeuw/glans laten staan
    for (y,x) in comp:
      if (y,x) in OOG or lijn[y,x] or rand[y,x] or gezm[y,x]: continue
      if any(lijn[y+dy,x+dx] and o[y+dy,x+dx]==v for dy in (-1,0,1) for dx in (-1,0,1)): continue  # lijnstuk
      b=near[3*y-9:3*y-6,3*x+3:3*x+6].ravel(); bc=np.bincount(b,minlength=16)
      buur={o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))}-{0,1,v}
      kand=sorted(buur,key=lambda k:-bc[k])
      if kand and bc[kand[0]]>0: o[y,x]=kand[0]; tel('vlakje -> 2e modelkeuze')
      elif kand:
        cnt={k:sum(o[y+dy,x+dx]==k for dy in (-1,0,1) for dx in (-1,0,1)) for k in kand}
        o[y,x]=max(cnt,key=cnt.get); tel('vlakje -> buurkleur (model had die tint niet in het blok)')
# reparaties (niet uit de kale reductie; modelplek gemeten: 4 resp. 2 witte modelpixels in het blok)
for p in ((31,16),(31,17)):
  if o[p]!=6: o[p]=6; tel('sneeuwtopje linkerschouder teruggezet')
np.save('stap4.npy',o); print(log,'totaal gewijzigd',int((o!=oud).sum()))
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('stap4.png',transparency=0)
