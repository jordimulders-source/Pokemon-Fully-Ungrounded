# Lijf vereenvoudigen (Krassault-recept): (1) groene kieren helder waar het model helder groen (2/3) heeft;
# (2) ijzer/roest-ontkorrelen: clusters < 3 px (zelfde index, 8-buren) en losse 1-px zwarte stukjes binnen een vlak
#     nemen de meest voorkomende ijzerbuur aan. Alleen binnen x24-46, y16-44; gezicht (x0-23,y29-48), wolken (index 4) en
#     wielen blijven onaangeroerd.
from PIL import Image; import numpy as np
IN='sprite_r6/stap_kv.png'; OUT='sprite_r6/stap_lijf.png'
im=Image.open(IN); pal=im.getpalette(); a=np.array(im).astype(int); r=a.copy()
m=np.array(Image.open('model/model.webp').convert('RGB')).astype(float)
K=13.77; BX,BY,OY=102,71,2
P=np.array(pal[:13*3]).reshape(13,3).astype(float)
def mk(sx,sy):
    c=m[int(BY+(sy-OY)*K)+3:int(BY+(sy-OY+1)*K)-3, int(BX+sx*K)+3:int(BX+(sx+1)*K)-3].reshape(-1,3)
    d=((c[:,None,:]-P[None,:,:])**2).sum(2); d[:,0]=1e9
    return np.bincount(d.argmin(1),minlength=13).argmax()
X0,X1,Y0,Y1=24,46,16,44
IJ={1,7,8,9,10,11,12}
log=[]
# (1) kieren
for y in range(20,39):
    for x in range(X0,40):   # x>=40 = wolkrand (bevroren)
        k=mk(x,y)
        if k in (2,3) and a[y,x] in (5,6):
            a[y,x]=k; log.append(('kier',x,y))
# (2) ontkorrelen ijzer
N8=[(dy,dx) for dy in(-1,0,1) for dx in(-1,0,1) if dy or dx]
for it in range(2):
    b=a.copy()
    lab=np.zeros_like(b); n=0; cl={}
    for y in range(Y0,Y1):
        for x in range(X0,X1):
            if b[y,x] not in IJ or lab[y,x]: continue
            n+=1; st=[(y,x)]; lab[y,x]=n; cl[n]=[]
            while st:
                cy,cx=st.pop(); cl[n].append((cy,cx))
                for dy,dx in N8:
                    ny,nx=cy+dy,cx+dx
                    if Y0<=ny<Y1 and X0<=nx<X1 and b[ny,nx]==b[y,x] and not lab[ny,nx]: lab[ny,nx]=n; st.append((ny,nx))
    for k,pts in cl.items():
        if len(pts)>=3: continue
        y,x=pts[0]; v=b[y,x]
        nb=[b[y+dy,x+dx] for (y,x) in pts for dy,dx in N8 if 0<=y+dy<64 and 0<=x+dx<64 and (y+dy,x+dx) not in pts]
        ij=[q for q in nb if q in IJ and q!=v]
        if not ij: continue
        # zwart dat aan andere lijnen of de rand raakt blijft (lijn), ander zwart wordt vlak
        if v==1 and (sum(q==1 for q in nb)>=1 or any(q==0 or q in(2,3,4,5,6) for q in nb)): continue
        if v!=1 and any(q in (2,3,5,6,4,0) for q in nb) and len(pts)==2: continue  # randje langs kier/lucht laten
        w=max(set(ij),key=ij.count)
        for (y,x) in pts: a[y,x]=w; log.append(('korrel',x,y,'%X>%X'%(v,w)))
o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save(OUT,transparency=0)
print(len(log),'wijzigingen'); print(log)
for y in range(16,46): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in a[y,16:50])+'   '+''.join('.' if v==0 else '%X'%v for v in r[y,16:50]))
