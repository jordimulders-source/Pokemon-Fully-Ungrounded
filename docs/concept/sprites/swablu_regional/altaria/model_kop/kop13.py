# Jordi 21 nov: kop van Altaria te klein (r1 ±10x8 px vs game ±13x11) -> optie A: kop+kuif in het model x1,3,
# ankerpunt = kin/halsaansluiting; overlap over de wolk mag ("extra overlap over de wolk heen is ook niet erg").
# Werkt op het natieve raster (gereedschap/natief.png, 199x199); wolk, hals en static blijven pixelgelijk.
import numpy as np, sys; from PIL import Image
F=float(sys.argv[1]) if len(sys.argv)>1 else 1.3
DY=int(sys.argv[2]) if len(sys.argv)>2 else 0   # kop zakt DY natieve px in de wolk/hals (Jordi: hoofd mag in de wolk verstopt)
a=np.asarray(Image.open('gereedschap/natief.png').convert('RGB')).astype(int)
H,W,_=a.shape; r,g,b=a[...,0],a[...,1],a[...,2]
bg=a.min(2)>=240                                 # wit + anti-aliashalo
teal=(g-r>25)&(np.abs(g-b)<45)&~bg            # wolk + static (cyaan/teal)
violet=(b-g>35)
yy,xx=np.mgrid[:H,:W]
m=np.zeros((H,W),bool)
m|=(yy<=50)&(xx>=66)&(xx<=140)&~bg              # kop + kuif boven de wolk (incl. lichte kuifglans)
m|=(yy>50)&(yy<=61)&(xx>=70)&(xx<=101)&~bg       # onderkant kop (incl. snavel en wangen)
# ankerpunt: kin, midden van de hals
AX,AY=85,61
out=a.copy()
out[(yy<=50)&(xx>=66)&(xx<=140)]=255             # oude kuif/kop boven de wolk weg (lag op wit), halo's mee
ys,xs=np.nonzero(m)
ny0=int(np.floor(AY+DY-(AY-ys.min())*F)); ny1=AY+DY; nx0=int(np.floor(AX-(AX-xs.min())*F)); nx1=int(np.ceil(AX+(xs.max()-AX)*F))
for y in range(max(0,ny0),ny1+1):
    for x in range(max(0,nx0),min(W,nx1+1)):
        sy=int(round(AY-(AY+DY-y)/F)); sx=int(round(AX+(x-AX)/F))
        if 0<=sy<H and 0<=sx<W and m[sy,sx]: out[y,x]=a[sy,sx]
# wat van de oude kop/kuif buiten de nieuwe valt: alleen achtergrond (wit) als het boven de wolk lag
Image.fromarray(out.astype('uint8')).save('model_kop/natief_kop%s%s.png'%(str(F).replace('.',''),'_dy%d'%DY if DY else ''))
big=np.repeat(np.repeat(out,int(1024/199)+0,0),5,1)
Image.fromarray(np.kron(out,np.ones((5,5,1))).astype('uint8')).save('model_kop/model_kop%s%s.png'%(str(F).replace('.',''),'_dy%d'%DY if DY else ''))
print('mask',m.sum(),'nieuw bbox y',ny0,'x',nx0,nx1)
