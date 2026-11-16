# Route B, stap 3a: natief (na samenvoegen) -> exacte 2x2-reductie met de Krassault-regels (octillery_evo/sprite3/half2.py),
# aangepast aan roest/staal. Niets getekend: elke pixel komt uit zijn 2x2-blok modelpixels.
import sys; from PIL import Image; import numpy as np
IN=sys.argv[1] if len(sys.argv)>1 else 'natief_samen.png'; OY=int(sys.argv[2]) if len(sys.argv)>2 else 0; OX=int(sys.argv[3]) if len(sys.argv)>3 else 0
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); H,W=a.shape[:2]
lum=a@[0.299,0.587,0.114]; sat=a[...,0]-a[...,2]
bg=a.min(2)>=225; drk=(lum<40)&~bg; wit=(lum>180)&~bg
hx=lambda c:[int(c[i:i+2],16) for i in (1,3,5)]
PAL=['#1e170e','#433425','#5f4b3a','#765a43','#9f7e65','#b39b87','#36332b','#4e4a44','#7b7975','#a39b93','#d8c8b0']
P=np.array([hx(c) for c in PAL],float)
def cls(px):
    br=(px[:,0]-px[:,2]>22).mean()>=0.5; idx=np.arange(2,7) if br else np.arange(7,11)
    return int(idx[((P[idx-1]-px.mean(0))**2).sum(1).argmin()])
h=(H-OY)//2; w=(W-OX)//2; o=np.zeros((h,w),int); nd=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2))
        if bg[sl].sum()>=3: continue
        m=~bg[sl]; d=drk[sl]&m; nd[j,i]=d.sum()
        # pupil (Krassault-regel): donkere modelpixel met oogwit links en rechts ervan
        pup=False
        for yy in range(OY+2*j,OY+2*j+2):
            for xx in range(OX+2*i,OX+2*i+2):
                if drk[yy,xx] and wit[yy,max(xx-3,0):xx].any() and wit[yy,xx+1:xx+4].any(): pup=True
        if pup: o[j,i]=1; continue
        if (wit[sl]&m).sum()>=2: o[j,i]=11; continue
        rest=m&~d&~wit[sl]
        if d.sum()>=3 or rest.sum()==0: o[j,i]=1; continue
        o[j,i]=cls(a[sl][rest]) if d.sum()<2 else -1
for j in range(h):
    for i in range(w):
        if o[j,i]!=-1: continue
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2)); d=drk[sl]
        nb=[(j-1,i),(j+1,i),(j,i-1),(j,i+1)]
        edge=any(not(0<=y<h and 0<=x<w) or (o[y,x]==0) for y,x in nb)
        vert=d[:,0].all() or d[:,1].all(); hor=d[0,:].all() or d[1,:].all()
        thick=False
        if vert: thick=any(0<=x<w and nd[j,x]>=3 for x in (i-1,i+1))
        if hor: thick=thick or any(0<=y<h and nd[y,i]>=3 for y in (j-1,j+1))
        o[j,i]=1 if (edge or not thick) else -2
for j in range(h):
    for i in range(w):
        if o[j,i]==-2:
            sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2)); rest=~bg[sl]&~drk[sl]
            o[j,i]=cls(a[sl][rest]) if rest.any() else 1
ys,xs=np.where(o>0); open('half_crop.txt','w').write(f'{ys.min()} {ys.max()+1} {xs.min()} {xs.max()+1}'); o=o[ys.min():ys.max()+1,xs.min():xs.max()+1]
np.save('half.npy',o); print('2x-reductie',o.shape[1],'x',o.shape[0],'zwart %.0f%%'%(100*(o==1).sum()/(o>0).sum()))
img=np.full(o.shape+(3,),255,np.uint8); img[o>0]=P[o[o>0]-1]
Image.fromarray(img).resize((o.shape[1]*8,o.shape[0]*8),Image.NEAREST).save('half_8x.png')
