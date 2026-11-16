# r21: pieken-/kernzone opnieuw uit het model met gemiddelde per 3x3 (glad, geen aliasing-korrel), gekwantiseerd naar de paarse tinten; ijs, ogen, gas = r18
import numpy as np; from PIL import Image
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); a=np.pad(a,((30,30),(30,30),(0,0)),constant_values=255)
ox,oy=15,-6
im=Image.open('r18.png'); pal=im.getpalette(); P=np.array(pal[:48]).reshape(16,3).astype(float); o=np.array(im).copy()
vap=np.load('r15w/vap.npy')
PUR=[1,7,8,9,10]
zone=np.isin(o,[7,8,9,10]) | ((o==1)&(np.arange(64)[None,:]>=20)&(np.arange(64)[:,None]<=50))
# alleen pixels die nu paars of K in de staart zijn, plus lichte strepen (D/M/S/N) die tussen paars liggen
strip=np.isin(o,[4,5,6,13]) & ~vap
for y in range(64):
  for x in range(64):
    if strip[y,x]:
      nb=o[max(0,y-1):y+2,max(0,x-1):x+2]
      if (np.isin(nb,[7,8,9,10]).sum()>=4): zone[y,x]=True
# behoud buitenrand K van het ijs (x<=34 en grens met ijs) : niet in zone als een 4-buur ijs is
ICE=[2,3,4,5]
for y in range(1,63):
  for x in range(1,63):
    if zone[y,x] and o[y,x]==1 and any(o[y+dy,x+dx] in ICE and not vap[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1))) and x<36: zone[y,x]=False
cand=[1,7,8,9,10,4,5]   # K, paars donker->licht, lichte scherfstrepen M/D
n=0
for y,x in zip(*np.where(zone)):
  b=a[3*y+oy+30:3*y+oy+33,3*x+ox+30:3*x+ox+33].reshape(-1,3).mean(0)
  k=cand[int(np.argmin(((P[cand]-b)**2).sum(1)))]
  if o[y,x]!=k: n+=1
  o[y,x]=k
print('zone',zone.sum(),'gewijzigd',n)
out=Image.fromarray(o).convert('P'); out.putpalette(pal); out.save('r21.png',transparency=0)
x8=out.convert('RGB').resize((512,512),Image.NEAREST); x8.save('r21_8x.png')
