# afwijking.py ronde [drempel]: spritepixels waar de helderheid > drempel afwijkt van het modelgemiddelde (meting).
import sys,json,numpy as np; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
k=json.load(open(P+'gereedschap/kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(P+'model/model_lijf_30.png')).astype(float)
sp=np.asarray(Image.open(P+sys.argv[1]+'/potoo.png').convert('RGBA')).astype(float)
t=float(sys.argv[2]) if len(sys.argv)>2 else 80
out=[]
for y in range(64):
  for x in range(64):
    if sp[y,x,3]==0: continue
    b=c[int(Y0+y*s):int(Y0+(y+1)*s),int(X0+x*s):int(X0+(x+1)*s)]; f=b[...,3]>0
    if not f.any(): continue
    L=b[...,:3][f].mean(1); d=sp[y,x,:3].mean()-L.mean()
    if abs(d)>t: out.append((x,y,int(sp[y,x,:3].mean()),int(L.mean()),int(np.percentile(L,15))))
print(len(out),'pixels: (x,y,sprite L,model gem,model p15)')
for o in out: print(o)
