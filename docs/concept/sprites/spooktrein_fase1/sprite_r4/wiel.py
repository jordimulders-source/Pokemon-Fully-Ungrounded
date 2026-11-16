# Reparatie 4 (wiel weer rond): het wiel opnieuw verkleind uit model.png (1024) met een UNIFORME schaal, zonder
# kolom-/rijschrapping, op dezelfde plek en maat als in r1. Per spritepixel een blok van 12x12 modelpixels:
# lijnaandeel >= TL -> lijn, anders vlakgemiddelde -> dichtstbijzijnde modelkleur in de kleurgroep. Niets getekend.
import sys,numpy as np; from PIL import Image
TL=float(sys.argv[1]) if len(sys.argv)>1 else 0.35; IN=sys.argv[2] if len(sys.argv)>2 else 'basis.npy'; OUT=sys.argv[3] if len(sys.argv)>3 else 'wiel.npy'
m=np.asarray(Image.open('../model/model.png').convert('RGB')).astype(float)
L=m@[0.299,0.587,0.114]; sat=m[...,0]-m[...,2]; bg=m.min(2)>=225
hx=lambda c:[int(c[i:i+2],16) for i in (1,3,5)]
PAL=['#1e170e','#433425','#5f4b3a','#765a43','#9f7e65','#b39b87','#36332b','#4e4a44','#7b7975','#a39b93','#d8c8b0']
P=np.array([hx(c) for c in PAL],float)
S=0.425/5.12; SC=(46.75,48.0); MC=(7.86+5.118*134.5, 7.46+5.122*115)   # spritecentrum <-> modelcentrum van het wiel (natief 134.5,115)
RX,RY=24*0.425+0.6,32*0.425+0.6
o=np.load(IN).copy(); n=0
for sy in range(64):
    for sx in range(64):
        if ((sx+.5-SC[0])/RX)**2+((sy+.5-SC[1])/RY)**2>1: continue
        x0=MC[0]+(sx-SC[0])/S; y0=MC[1]+(sy-SC[1])/S; x1=x0+1/S; y1=y0+1/S
        sl=(slice(int(y0),int(y1)),slice(int(x0),int(x1)))
        b=bg[sl]; 
        if b.mean()>0.5: v=0
        else:
            l=L[sl][~b]; c=m[sl][~b]; s=sat[sl][~b]
            if (l<45).mean()>=TL: v=1
            else:
                k=l>=45; br=(s[k]>22).mean()>=0.5; idx=np.arange(3,6) if br else np.arange(8,11)
                v=int(idx[((P[idx-1]-c[k].mean(0))**2).sum(1).argmin()])
        if o[sy,sx]!=v: n+=1
        o[sy,sx]=v
# buitenrand van het wiel: randpixel -> lijn (zoals het model)
fg=o>0; pad=np.pad(fg,1); edge=fg&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,xx=np.mgrid[0:64,0:64]; inE=((xx+.5-SC[0])/RX)**2+((yy+.5-SC[1])/RY)**2<=1
o[edge&inE]=1
np.save(OUT,o); print('wielpixels veranderd',n)
