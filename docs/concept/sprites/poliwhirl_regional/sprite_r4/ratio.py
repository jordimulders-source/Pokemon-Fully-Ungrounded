# geel/zwart-verhouding (HSV): geel h 0.1-0.2 s>0.4 v>0.5 ; donker v<0.45 s<0.6. python3 ratio.py beeld.png [model]
import sys,numpy as np,colorsys; from PIL import Image
def rat(a):
    a=a/255.0; mx=a.max(2); mn=a.min(2); v=mx; s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
    r,g,b=a[...,0],a[...,1],a[...,2]; d=np.maximum(mx-mn,1e-6)
    h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))/6
    Y=(h>=0.1)&(h<=0.2)&(s>0.4)&(v>0.5); D=(v<0.45)&(s<0.6)
    return Y.sum(),D.sum(),Y.sum()/D.sum()
for p in sys.argv[1:]:
    im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
    print(p,rat(np.asarray(bg.convert('RGB')).astype(float)))
