# Uku Pacha r1: natief raster van r2 (100x100) -> 64 px, oppervlak-gewogen meerderheidsstem per spritepixel;
# omlijning (bijna zwart) wint als ze >= DREMPEL van de pixel bedekt. Palet = 15 clusters uit het model + wit.
import sys; from PIL import Image; import numpy as np
N=np.asarray(Image.open('model/r2_natief.png').convert('RGB')).astype(float)
wit=(N.sum(2)>735)
# achtergrond = wit dat met de rand verbonden is (tanden/oogwit binnen de kop blijven)
bg=np.zeros_like(wit); st=[(0,0)]
while st:
    y,x=st.pop()
    if 0<=y<wit.shape[0] and 0<=x<wit.shape[1] and wit[y,x] and not bg[y,x]:
        bg[y,x]=True; st+= [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
# ingesloten wit: grote gaten = achtergrond, kleine (<8 cellen: tanden, oogglans) = wit detail
binnen=wit&~bg; lab=np.zeros(wit.shape,int); n=0
for y0_,x0_ in zip(*np.where(binnen)):
    if lab[y0_,x0_]: continue
    n+=1; st=[(y0_,x0_)]; comp=[]
    while st:
        y,x=st.pop()
        if 0<=y<wit.shape[0] and 0<=x<wit.shape[1] and binnen[y,x] and not lab[y,x]:
            lab[y,x]=n; comp.append((y,x)); st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    if len(comp)>=8:
        for y,x in comp: bg[y,x]=True
witdetail=wit&~bg; print('wit detail',witdetail.sum())
ys,xs=np.where(~bg); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
W,H=x1-x0,y1-y0; f=64/max(W,H); w,h=round(W*f),round(H*f); print('bbox',W,H,'factor',round(f,3),'->',w,h)
# palet uit model (alleen voorgrond)
# vaste accenten uit het model: oog (geel) en tong (paars); de rest 13 clusters
r,g,b=N[...,0],N[...,1],N[...,2]
geel=(~bg)&(r>170)&(g>150)&(r>b+60); paars=(~bg)&(r>g+12)&(b>g+25)
print('geel',geel.sum(),'paars',paars.sum())
rest=N[(~bg)&~geel&~paars&~witdetail]; q=Image.fromarray(rest.reshape(1,-1,3).astype('uint8')).quantize(12,method=Image.MEDIANCUT,kmeans=3)
pal=np.array(q.getpalette()[:36]).reshape(12,3).astype(float)
pal=np.vstack([pal,N[geel].mean(0),N[paars].mean(0),[250,252,252]])  # 12,13,14 ; wit detail=15
idx=np.argmin(((N[...,None,:]-pal[None,None,:12])**2).sum(-1),axis=-1); idx[geel]=12; idx[paars]=13; idx[witdetail]=14; idx[bg]=15
pal=np.vstack([pal,[255,255,255]])  # 15 = achtergrond (transparant)
dark=pal.sum(1)<140; DREMPEL=float(sys.argv[1]) if len(sys.argv)>1 else 0.34
out=np.full((64,64),15); ox=(64-w)//2; oy=64-h
for j in range(h):
  for i in range(w):
    sx0,sx1=x0+i/f,x0+(i+1)/f; sy0,sy1=y0+j/f,y0+(j+1)/f
    acc=np.zeros(16)
    for cy in range(int(sy0),int(np.ceil(sy1))):
      for cx in range(int(sx0),int(np.ceil(sx1))):
        a=(min(sx1,cx+1)-max(sx0,cx))*(min(sy1,cy+1)-max(sy0,cy))
        if a>0: acc[idx[cy,cx]]+=a
    acc/=acc.sum()
    if acc[15]>0.5: continue
    d=acc[:12]*dark[:12]
    if acc[12]>=0.2: out[oy+j,ox+i]=12; continue
    if acc[13]>=0.3: out[oy+j,ox+i]=13; continue
    if acc[14]>=0.3: out[oy+j,ox+i]=14; continue
    out[oy+j,ox+i]= int(np.argmax(d)) if d.sum()>=DREMPEL else int(np.argmax(acc[:15]))
im=Image.fromarray(pal[out].astype('uint8')); im.save('sprite/r1/uku_pacha_r1.png')
print('kleuren',len(np.unique(out)))
