# Reparatie 3 (linkerbout): kop + schacht uit de modelpixels. Per spritepixel in de boutzone: de MODUS van de
# modelklassen in zijn blok (lijn <45, staal donker 45-90, midden 90-140, licht >140) i.p.v. het gemiddelde,
# zodat de lichte kopvlakken en de donkere schacht niet tot een klomp middelen. Zelfde afbeelding als r1.
import numpy as np, ast; from PIL import Image
o=np.load('midden.npy').copy()
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); fg=a.min(2)<225; L=a@[0.299,0.587,0.114]
ys,xs=np.where(fg); cy0,cx0=ys.min()-1,xs.min()-1
r=open('schrap.txt').read().split('\n'); rows=set(ast.literal_eval(r[0])); cols=set(ast.literal_eval(r[1]))
kR=[i for i in range(ys.max()+2-cy0) if i not in rows]; kC=[i for i in range(xs.max()+2-cx0) if i not in cols]
X,Y,ww,hh=map(int,open('plaats.txt').read().split())
def blok(x,y):
    hy,hx=y-Y,x-X; rr=[cy0+kR[1+2*hy+k] for k in (0,1)]; cc=[cx0+kC[2*hx+k] for k in (0,1)]
    return [(q,p) for q in rr for p in cc]
def kl(q,p):
    if not fg[q,p]: return 0
    l=L[q,p]; return 1 if l<45 else (8 if l<90 else (9 if l<140 else 10))
BX=(60,74,99,111); n=0
for y in range(38,50):
    for x in range(12,24):
        b=blok(x,y); inb=[(q,p) for q,p in b if BX[0]<=p<=BX[1] and BX[2]<=q<=BX[3]]
        if len(inb)<3 or o[y,x]==0: continue
        c=[kl(q,p) for q,p in b]; u,cn=np.unique(c,return_counts=True)
        best=u[cn==cn.max()]
        v=int(max(best,key=lambda t:(t==1, t)))   # bij gelijkspel: lijn, dan de lichtste (glans van de kop)
        if v==0: continue                           # silhouet blijft
        if o[y,x]!=v: n+=1; o[y,x]=v
np.save('bout.npy',o); print('boutpixels veranderd',n); print(o[39:49,12:23])
