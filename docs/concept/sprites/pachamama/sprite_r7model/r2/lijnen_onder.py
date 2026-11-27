# r2 punt 3: lange dunne modellijnen in de onderkant (oker/turquoise, rij >= 40) doorlopend maken in de donkerste eigen tint
# i.p.v. losse zwarte stukjes. Lijncel = >= 1 natieve modelpixel met helderheid < 60; alleen ketens (8-samenhang) van >= 4 cellen.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
a=np.asarray(Image.open('../natief_g1.png').convert('RGB')).astype(float); L=lum(a); bg=np.load('basis_bg.npy')
MY,MX=np.load('basis_map.npy'); o=np.load(sys.argv[1]); oud=o.copy()
m=o>0; p=np.pad(m,1); rand=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
zw=(L<60)&~bg; c=np.zeros((64,64),bool)
for y in range(40,63):
  for x in range(64):
    if not m[y,x] or rand[y,x]: continue
    b=(slice(MY+3*y,MY+3*y+3),slice(MX+3*x,MX+3*x+3)); c[y,x]=zw[b].sum()>=1
lab=np.zeros((64,64),int); n=0; sizes={}
for y in range(64):
  for x in range(64):
    if c[y,x] and not lab[y,x]:
      n+=1; st=[(y,x)]; lab[y,x]=n; k=0
      while st:
        q=st.pop(); k+=1
        for dy in (-1,0,1):
          for dx in (-1,0,1):
            r=(q[0]+dy,q[1]+dx)
            if 0<=r[0]<64 and 0<=r[1]<64 and c[r] and not lab[r]: lab[r]=n; st.append(r)
      sizes[n]=k
DONK={11:11,12:11,14:14,15:14,9:7,8:7,7:7,2:2,3:2,4:3,13:4,10:6,6:13,5:13}
log={}
for y in range(64):
  for x in range(64):
    if not lab[y,x]: continue
    keten=sizes[lab[y,x]]>=4
    nb=[o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx]>1 and not lab[y+dy,x+dx]]
    if not nb: continue
    t=min({DONK[v] for v in nb},key=lambda i:lum(P[i]))
    if keten and o[y,x]!=t: log['lijn doorlopend in eigen tint']=log.get('lijn doorlopend in eigen tint',0)+1; o[y,x]=t
    elif not keten and o[y,x]==1: o[y,x]=max(set(nb),key=nb.count); log['los zwart stukje -> vlak']=log.get('los zwart stukje -> vlak',0)+1
np.save(sys.argv[2],o); print(log,(o!=oud).sum())
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save(sys.argv[2].replace('.npy','.png'),transparency=0)
# grijze gezichtstinten (3,4,13) in de romp (rij >= 33): model is daar plantje/oker -> dichtstbijzijnde romptint (mediaan van het blok)
for y in range(33,64):
  for x in range(64):
    if o[y,x] in (3,4,13):
      b=(slice(MY+3*y,MY+3*y+3),slice(MX+3*x,MX+3*x+3)); md=np.median(a[b].reshape(-1,3),0)
      t=nearest(md[None],(2,7,8,9,11,12,14,15) if md[0]-md[1]>=40 else (2,11,12,14,15))[0]; o[y,x]=t; log['grijs in romp -> romptint']=log.get('grijs in romp -> romptint',0)+1
np.save(sys.argv[2],o); print(log,(o!=oud).sum())
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save(sys.argv[2].replace('.npy','.png'),transparency=0)
# plantje linksonder (model: okergele varen op turquoise): cellen per mediaan naar oker/donkerbruin (11,12,2)
for y in range(48,51):
  for x in range(11,16):
    if o[y,x] in (2,11,12):
      b=(slice(MY+3*y,MY+3*y+3),slice(MX+3*x,MX+3*x+3)); md=np.median(a[b].reshape(-1,3),0)
      t=nearest(md[None],(2,11,12))[0]
      if t!=o[y,x]: o[y,x]=t; log['plantje per mediaan']=log.get('plantje per mediaan',0)+1
np.save(sys.argv[2],o); print(log,(o!=oud).sum())
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save(sys.argv[2].replace('.npy','.png'),transparency=0)
# losse plantpixels aansluiten (r2): (48,15) 11 -> 12 (geel blad), (49,15) 2 -> 11 (sluit aan op de donkere plantvoet)
for c,v in {(48,15):12,(49,15):11}.items(): o[c]=v
np.save(sys.argv[2],o)
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save(sys.argv[2].replace('.npy','.png'),transparency=0)
# buitenrand zonder zwarte modellijn (linkerarm boven): geen lichte kleur op de rand -> donkerste eigen tint (12 -> 11)
for (y,x) in ((33,7),(34,6),(35,5)):
  if o[y,x]==12: o[y,x]=11
np.save(sys.argv[2],o)
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save(sys.argv[2].replace('.npy','.png'),transparency=0)
