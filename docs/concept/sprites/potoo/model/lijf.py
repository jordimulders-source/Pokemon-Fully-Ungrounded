# Stap 2: lijf groter in verhouding (Jordi 6 nov: "het lichaam moet net wat groter (wel in verhouding blijven)").
# Jordi 7 nov: "je hebt hem dikker gemaakt, niet langer" -> alleen in de hoogte oprekken, breedte blijft.
# Kop/snavel/muil (boven Y0) onaangeroerd; eronder alleen verticaal x s.
# Daarna gespiegeld (Jordi: "dit beeld spiegelen kan je zelf"). Uitvoer: model_lijf_<pct>.png
import numpy as np, sys; from PIL import Image
a=np.asarray(Image.open('model_los.png')).astype(np.uint8)
H,W,_=a.shape; Y0,Y1,CX=540,660,485
for s in (1.10,1.20,1.30):
    Hn=int(Y0+(H-Y0)*s)+10; Wn=W+200; off=100
    out=np.zeros((Hn,Wn,4),np.uint8)
    for yo in range(Hn):
        if yo<Y0: ys=yo; f=1.0
        else:
            ys=Y0+(yo-Y0)/s
            f=1.0
        yi=int(round(ys))
        if yi>=H: continue
        xo=np.arange(Wn)-off; xs=np.round(CX+(xo-CX)/f).astype(int)
        ok=(xs>=0)&(xs<W); out[yo,ok]=a[yi,xs[ok]]
    out=out[:,::-1]  # spiegelen: kijkt naar links-voor
    Image.fromarray(out).save(f'model_lijf_{int(round((s-1)*100))}.png')
