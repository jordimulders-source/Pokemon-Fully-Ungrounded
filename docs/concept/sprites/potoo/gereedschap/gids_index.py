# gids_index.py: MEETKAART (geen sprite). Per spritepixel de dichtstbijzijnde paletkleur bij het modelgemiddelde,
# en de paletkleur bij p15 (donkerste 15%: waar lijnen lopen). Gebruik: python3 gids_index.py kleur_rN/palet.py
import sys,json,importlib.util,numpy as np; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
sp=importlib.util.spec_from_file_location('p',sys.argv[1]); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
PAL=np.array(m.PAL[1:16],float); CH='123456789ABCDEF'
k=json.load(open(P+'gereedschap/kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(P+'model/model_lijf_30.png')).astype(float)
sil=np.asarray(Image.open(P+'silhouet/silhouet.png'))[...,3]>0
def near(v): return CH[((PAL-v)**2).sum(1).argmin()]
A=[];B=[]
for y in range(64):
  a=b=''
  for x in range(64):
    blk=c[int(Y0+y*s):int(Y0+(y+1)*s),int(X0+x*s):int(X0+(x+1)*s)]; f=blk[...,3]>0
    if not sil[y,x]: a+='.';b+='.';continue
    if not f.any(): a+='?';b+='?';continue
    rgb=blk[...,:3][f]; L=rgb.mean(1); a+=near(rgb.mean(0))
    d=rgb[L<=np.percentile(L,15)].mean(0); b+=near(d)
  A.append(a);B.append(b)
hdr='   '+''.join(str(x//10) for x in range(64))+'\n   '+''.join(str(x%10) for x in range(64))
for n,G in (('gemiddeld',A),('p15',B)):
  print(n);print(hdr)
  for y,r in enumerate(G): print(f'{y:2d} '+r)
