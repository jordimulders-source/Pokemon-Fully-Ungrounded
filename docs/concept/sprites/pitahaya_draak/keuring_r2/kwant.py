from PIL import Image; import numpy as np
im=Image.open('sprite_r2/pitahaya_r2.png'); S=np.array(im); pal=np.array(im.getpalette()[:48]).reshape(16,3); L=(pal*[0.299,0.587,0.114]).sum(1)
d=np.load('keuring_r2/model_per_px.npz'); mlum=d['mlum']; mg=d['mg']; mean=d['mean']
Q=np.zeros_like(S)
grp={2:[2,3,4,5],4:[8,9,10,11]}
for y in range(64):
  for x in range(64):
    s=S[y,x]
    if s in (3,4,5) : opts=[2,3,4,5]
    elif s in (9,10,11): opts=[8,9,10,11]
    else: Q[y,x]=s; continue
    Q[y,x]=min(opts,key=lambda i:abs(L[i]-mlum[y,x]))
diff=(Q!=S)
print('vul-pixels afwijkend van model-blokgemiddelde (gekwantiseerd):',diff.sum(),'van',np.isin(S,[3,4,5,9,10,11]).sum())
# signed: sprite lighter or darker
sl=(L[S]-L[Q]); 
for nm,m in [('kop y<=36',np.arange(64)[:,None]<=36),('lijf y>36',np.arange(64)[:,None]>36)]:
    mm=diff&np.broadcast_to(m,(64,64))
    print(nm,'afwijkend',mm.sum(),'sprite lichter',(mm&(sl>0)).sum(),'donkerder',(mm&(sl<0)).sum(), '>=2 stappen', (mm&(np.abs(sl)>55)).sum())
q=Image.fromarray(Q.astype('uint8'),'P'); q.putpalette(im.getpalette()); q.save('keuring_r2/model_kwant.png',transparency=0)
# gemiddelde helderheid kop links vs rechts
for nm,(x0,x1) in [('kop links x18-29',(18,30)),('kop rechts x30-44',(30,45))]:
    m=np.zeros((64,64),bool); m[8:22,x0:x1]=True; m&=np.isin(S,[3,4,5])
    print(nm,'sprite',L[S][m].mean().round(1),'model',mlum[m].mean().round(1))
