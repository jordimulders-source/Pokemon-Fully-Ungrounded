# Stok dikker op het natieve raster, alleen door bestaande middenrijen/-kolommen van de stok te dupliceren
# (niets getekend). Schacht: per rij N middenkolommen erbij (groeit naar rechts). Handvat: bovenboog per kolom
# 2 middenrijen erbij (groeit omhoog), dalende haak per rij 2 middenkolommen erbij (groeit naar links). natief_been -> natief_stok
import sys; from PIL import Image; import numpy as np
Y0=int(sys.argv[3]) if len(sys.argv)>3 else 58
N=int(sys.argv[1]) if len(sys.argv)>1 else 3; K=int(sys.argv[2]) if len(sys.argv)>2 else 2
a=np.asarray(Image.open('natief_been.png').convert('RGB')).copy(); L=a.astype(int).mean(axis=2)
out=a.copy(); n=0; D=lambda y,x: L[y,x]<170
# bovenboog van het handvat (kolommen 7..24, eerste donkere run vanaf boven in rijen 46..60, max 8 hoog)
for x in ([] if True else range(7,25)):  # handvat ongemoeid (opdracht: crook behouden)
    ys=[y for y in range(46,61) if D(y,x)]
    if not ys: continue
    yt=ys[0]; yb=yt
    while D(yb+1,x): yb+=1
    if yb-yt>8: continue
    ym=(yt+yb+1)//2; col=a[:,x].copy()
    new=np.concatenate([col[yt:ym],col[ym-K:ym],col[ym:yb+1]])
    out[yt-K:yt-K+len(new),x]=new; n+=1
a2=out.copy(); L2=a2.astype(int).mean(axis=2)
# dalende haak links (rijen 54..64, eerste donkere run vanaf links in x 4..16, max 7 breed)
for y in ([] if True else range(54,65)):
    xs=[x for x in range(4,17) if L2[y,x]<170]
    if not xs: continue
    xl=xs[0]; xr=xl
    while L2[y,xr+1]<170: xr+=1
    if xr-xl>7: continue
    xm=(xl+xr+1)//2; row=a2[y].copy()
    new=np.concatenate([row[xl:xm],row[xm-K:xm],row[xm:xr+1]])
    out[y,xl-K:xl-K+len(new)]=new; n+=1
a3=out.copy(); L3=a3.astype(int).mean(axis=2)
# schacht
for y in range(Y0,125):  # r3: ook de handschoenrijen (in het model loopt de stok over de hand)
    c=int(round(15+0.73*(y-56)))+3
    if L3[y,c]>=170:
        cs=[x for x in range(c-4,c+5) if L3[y,x]<170]
        if not cs: continue
        c=cs[len(cs)//2]
    xl=c
    while L3[y,xl-1]<170: xl-=1
    xr=c
    while L3[y,xr+1]<170: xr+=1
    if xr-xl>12: continue
    xm=(xl+xr+1)//2; row=a3[y].copy()
    new=np.concatenate([row[xl:xm],row[xm-N:xm],row[xm:xr+1]])
    out[y,xl:xl+len(new)]=new; n+=1
Image.fromarray(out).save('natief_stok.png'); print('rijen/kolommen verbreed',n)
