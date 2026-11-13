# glad.py in out: 3x3-meerderheidsfilter op vulpixels (niet op 1/0), houdt features (geel/grijs/roze) 
import cfg,numpy as np,sys
a=cfg.read(sys.argv[1]); b=a.copy()
for y in range(1,63):
  for x in range(1,63):
    if a[y,x] in (0,1): continue
    w=a[y-1:y+2,x-1:x+2].ravel(); w=w[(w!=0)&(w!=1)]
    cnt=np.bincount(w,minlength=16)
    if cnt[a[y,x]]<=2 and cnt.max()>=4: b[y,x]=cnt.argmax()
cfg.write(b,sys.argv[2])
