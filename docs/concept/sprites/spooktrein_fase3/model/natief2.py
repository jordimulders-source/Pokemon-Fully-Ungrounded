# Raster adaptief: celgrenzen = pieken in randsterkte (afstand 12-18 px), cel = mediaan van het binnenste. Niets getekend.
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int); OUT=sys.argv[2]
def bounds(ax):
    g=np.abs(np.diff(a,axis=ax)).sum(axis=2).sum(axis=1-ax).astype(float)
    g=np.convolve(g,[0.25,0.5,0.25],'same')
    b=[int(np.argmax(g[:10]))]
    while b[-1]+6<len(g):
        lo,hi=b[-1]+6,min(len(g),b[-1]+10)
        seg=g[lo:hi]; k=lo+int(np.argmax(seg))
        if seg.max()<g.mean()*0.6: k=b[-1]+8
        b.append(k)
    return np.array(b)+1
bx,by=bounds(1),bounds(0)
print('cellen',len(bx)-1,len(by)-1,'pitch x',np.diff(bx).min(),np.diff(bx).max())
H,W=len(by)-1,len(bx)-1; out=np.zeros((H,W,3),'uint8')
for j in range(H):
    for i in range(W):
        y0,y1,x0,x1=by[j],by[j+1],bx[i],bx[i+1]
        my,mx=max(1,(y1-y0)//3),max(1,(x1-x0)//3)
        out[j,i]=np.median(a[y0+my:y1-my,x0+mx:x1-mx].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT)
m=out.min(axis=2)<215; yy,xx=np.where(m); print('bbox w',xx.max()-xx.min()+1,'h',yy.max()-yy.min()+1)
Image.fromarray(out).resize((W*6,H*6),Image.NEAREST).save(OUT.replace('.png','_12x.png'))
