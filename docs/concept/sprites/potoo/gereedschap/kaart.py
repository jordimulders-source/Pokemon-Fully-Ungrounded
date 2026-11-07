# kaart.py: meetkaarten van het model per spritepixel (alleen meting, geen sprite).
# Rooster 1: helderheid gemiddeld (0-9, *26). Rooster 2: donker-aandeel (fractie modelpx met L<70: . <10%, 1 <25%, 2 <50%, 3 >=50%).
# Rooster 3: kleurklasse b=blauw/paars (B-R>25), o=olijf/groen-geel, w=wit/grijs.
import json,numpy as np; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
k=json.load(open(P+'gereedschap/kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(P+'model/model_lijf_30.png')).astype(float)
sil=np.asarray(Image.open(P+'silhouet/silhouet.png'))[...,3]>0
G1=[];G2=[];G3=[]
for y in range(64):
  a=b=d=''
  for x in range(64):
    blk=c[int(Y0+y*s):int(Y0+(y+1)*s),int(X0+x*s):int(X0+(x+1)*s)]; f=blk[...,3]>0
    if not sil[y,x] or not f.any(): a+=' ';b+=' ';d+=' ';continue
    rgb=blk[...,:3][f]; L=rgb.mean(1); m=rgb.mean(0)
    a+=str(min(9,int(L.mean()/25.6)))
    fr=(L<70).mean(); b+='.' if fr<.1 else '1' if fr<.25 else '2' if fr<.5 else '3'
    d+='b' if m[2]-m[0]>25 else ('o' if m[1]-m[2]>15 else 'w')
  G1.append(a);G2.append(b);G3.append(d)
hdr='   '+''.join(str(x//10) for x in range(64))+'\n   '+''.join(str(x%10) for x in range(64))
for n,G in (('helderheid',G1),('donker',G2),('klasse',G3)):
  print(n);print(hdr)
  for y,r in enumerate(G): print(f'{y:2d} '+r)
